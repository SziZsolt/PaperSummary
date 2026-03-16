import pandas as pd
from pathlib import Path
import requests
import fitz
from io import BytesIO
from tqdm import tqdm
import re


current_dir = Path(__file__).resolve().parent
from remove_abstract import remove_abstract

file_path = current_dir / '../data/raw/scientific_papers.csv'

df = pd.read_csv(file_path)

target_categories = [
    'Robotics',
    'Computation and Language (Natural Language Processing)'
]

filtered_df = df[df['category'].isin(target_categories)]

limited_df = (
    filtered_df
    .groupby('category', group_keys=False)
    .apply(lambda x: x.sample(n=min(len(x), 2500), random_state=42))
    .reset_index(drop=True)
)

print(limited_df['category'].value_counts())

limited_df['pdf_id'] = (
    limited_df['id']
    .str.replace('^abs-', '', regex=True)
    .replace('^cs-', 'cs/', regex=True)
)

limited_df['pdf_url'] = 'https://arxiv.org/pdf/' + limited_df['pdf_id']

print(limited_df[['id', 'pdf_id', 'pdf_url']].head())


session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
})


def unversioned_arxiv_url(url: str) -> str:
    # 2002.03350v2 -> 2002.03350
    # cs/0012017v1 -> cs/0012017
    return re.sub(r'v\d+$', '', url)


def download_pdf_bytes(url: str, timeout: int = 30):
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.content


def try_download_with_withdrawn_fallback(url: str):
    try:
        return download_pdf_bytes(url), url
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else None

        if status == 404:
            fallback_url = unversioned_arxiv_url(url)
            if fallback_url != url:
                try:
                    print(f"404 on versioned URL, retrying unversioned: {fallback_url}")
                    return download_pdf_bytes(fallback_url), fallback_url
                except Exception as fallback_e:
                    print(f"Skipping unreachable/withdrawn paper: {url} | fallback failed: {fallback_e}")
                    return None, None

        print(f"Skipping unreachable paper: {url} | {e}")
        return None, None

    except Exception as e:
        print(f"Skipping unreachable paper: {url} | {e}")
        return None, None


def extract_pdf_text(pdf_bytes: bytes, source_url: str):
    try:
        pdf_file = BytesIO(pdf_bytes)
        doc = fitz.open(stream=pdf_file, filetype="pdf")

        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())

        text = "".join(text_parts).strip()

        if not text:
            print(f"Skipping malformed/empty PDF: {source_url}")
            return None

        return remove_abstract(text)

    except Exception as e:
        print(f"Skipping malformed/unreadable PDF: {source_url} | {e}")
        return None


def fetch_pdf_text(url: str):
    pdf_bytes, final_url = try_download_with_withdrawn_fallback(url)
    if pdf_bytes is None:
        return None

    return extract_pdf_text(pdf_bytes, final_url)


tqdm.pandas(desc="Fetching PDFs")

limited_df['x'] = limited_df['pdf_url'].progress_apply(fetch_pdf_text)

limited_df = limited_df[limited_df['x'].notna()].copy()

for category in target_categories:
    safe_category = category.replace('/', '_').replace(' ', '_')
    output_path = current_dir / f'../data/processed/{safe_category}_papers.csv'

    limited_df.loc[limited_df['category'] == category, ['x', 'summary']].to_csv(
        output_path,
        index=False
    )
    print(f"Saved {output_path}")