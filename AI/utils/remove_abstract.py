import re
from difflib import SequenceMatcher

def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def find_header(text, header, threshold=0.8):
    """Return start index of header if fuzzy match exceeds threshold"""
    header_len = len(header)
    for i in range(len(text) - header_len + 1):
        snippet = text[i:i+header_len]
        if SequenceMatcher(None, snippet.lower(), header.lower()).ratio() >= threshold:
            return i
    return -1

def remove_abstract(text):
    start = find_header(text, "abstract")
    end = find_header(text, "introduction")
    if start != -1 and end != -1 and end > start:
        return text[:start] + text[end:]
    return text