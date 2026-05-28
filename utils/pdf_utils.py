import os
import requests

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    print("Warning: pdfplumber not installed. PDF text extraction will not be available.")


def download_pdf(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"PDF downloaded to {save_path}")


def extract_text_from_pdf(pdf_path):
    if not PDFPLUMBER_AVAILABLE:
        print("Error: pdfplumber not installed. Cannot extract text from PDF.")
        return ""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text
