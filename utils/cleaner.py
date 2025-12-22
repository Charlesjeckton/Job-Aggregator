import re


def clean_text(text):
    """
    Cleans raw scraped text by removing newlines, extra whitespace, 
    and non-standard characters.
    """
    if not text or not isinstance(text, str):
        return "N/A"

    # 1. Remove newlines and tabs
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # 2. Remove multiple consecutive spaces
    text = re.sub(r'\s+', ' ', text)

    # 3. Strip leading/trailing whitespace
    return text.strip()


def clean_job_data(df):
    """
    Specific helper for your pandas DataFrame.
    """
    # Apply text cleaning to title
    if 'title' in df.columns:
        df['title'] = df['title'].apply(clean_text)

    # Remove duplicates based on the job link
    if 'link' in df.columns:
        df = df.drop_duplicates(subset=['link'], keep='first')

    return df