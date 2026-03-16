import re
from difflib import SequenceMatcher

def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def remove_abstract(text: str, abstract: str, threshold: float = 0.75) -> str:
    """
    Remove the abstract from `text` using fuzzy matching against `abstract`.
    Only removes the first occurrence with similarity >= threshold.
    Preserves all newlines and original spacing.
    """
    if not text or not abstract:
        return text

    best_start = None
    best_end = None
    best_ratio = 0

    len_text = len(text)
    len_abs = len(abstract)

    # Sliding window over text
    # Slightly larger window to allow partial matches
    for start in range(len_text - len_abs + 1):
        end = start + len_abs
        snippet = text[start:end]
        ratio = SequenceMatcher(None, snippet, abstract).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_start = start
            best_end = end

    # If best match is above threshold, remove it
    if best_ratio >= threshold and best_start is not None and best_end is not None:
        # Remove abstract exactly, keep all other chars intact
        result = text[:best_start] + text[best_end:]
        return result

    return text