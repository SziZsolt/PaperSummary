import pandas as pd
from pathlib import Path
import requests
import fitz
from io import BytesIO
from tqdm import tqdm


current_dir = Path(__file__).resolve().parent
from remove_abstract import remove_abstract

file_path = current_dir / '../data/raw/scientific_papers.csv'

df = pd.read_csv(file_path)

category_counts = df['category'].value_counts().to_dict()

target_categories = [
    'Robotics',
    'Computation and Language (Natural Language Processing)'
]

filtered_df = df[df['category'].isin(target_categories)]

limited_df = (
    filtered_df
    .groupby('category', group_keys=False)
    .apply(lambda x: x.sample(n=min(len(x), 2500), random_state=42))
)

limited_df = limited_df.reset_index(drop=True)

print(limited_df['category'].value_counts())

limited_df['pdf_id'] = limited_df['id'].str.replace('^abs-', '', regex=True).replace('^cs-', 'cs/', regex=True)

limited_df['pdf_url'] = 'https://arxiv.org/pdf/' + limited_df['pdf_id']
 
print(limited_df[['id', 'pdf_id', 'pdf_url']].head())

limited_df = limited_df.iloc[-100:]

def fetch_pdf_text(url):
    """
    Returns the PDF text with abstract removed.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        pdf_file = BytesIO(response.content)
        
        doc = fitz.open(stream=pdf_file, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        text_no_abstract = remove_abstract(text)
        
        return pd.Series(text_no_abstract)
    
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return pd.Series([None, None])

tqdm.pandas(desc="Fetching PDFs")

limited_df['x'] = limited_df.progress_apply(
    lambda row: fetch_pdf_text(row['pdf_url']), axis=1
)


for category in target_categories:
    safe_category = category.replace('/', '_').replace(' ', '_')
    output_path = current_dir / f'../data/processed/{safe_category}_papers.csv'
    limited_df[['x', 'summary']][limited_df['category'] == category].to_csv(output_path, index=False)
    print(f"Saved {output_path}")