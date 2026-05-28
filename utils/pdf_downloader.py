import os
import requests
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

MIN_PDF_SIZE_BYTES = 5120  # 5 KB minimum


def validate_pdf_url(url, timeout=10):
    """Validate if a URL is a valid PDF source"""
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            logger.warning(f"[INVALID URL] Invalid URL structure: {url}")
            return False
        
        # Check if URL ends with .pdf
        if not url.lower().endswith('.pdf'):
            logger.warning(f"[URL NOT PDF] Does not end with .pdf: {url}")
            return False

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.head(url, headers=headers, allow_redirects=True, timeout=timeout)
        
        if response.status_code != 200:
            logger.warning(f"[STATUS CODE {response.status_code}] Invalid response from {url}")
            return False

        content_type = response.headers.get("content-type", "").lower()
        if "pdf" not in content_type:
            logger.warning(f"[INVALID CONTENT TYPE] {content_type} for {url}")
            return False

        return True

    except requests.exceptions.RequestException as e:
        logger.warning(f"[URL VALIDATION FAILED] {str(e)} for {url}")
        return False


def is_valid_pdf(content):
    """Check if raw content is a valid PDF by checking the header"""
    return content.startswith(b"%PDF")


def download_real_pdf(url, save_path, timeout=30):
    """Download a real PDF file with full validation"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=timeout, stream=True)
        
        if response.status_code != 200:
            logger.error(f"[DOWNLOAD FAILED] Status {response.status_code} for {url}")
            return False
        
        # Read content and validate
        content = response.content
        if not is_valid_pdf(content):
            logger.error(f"[INVALID PDF] Not a valid PDF file: {url}")
            return False
        
        if len(content) < MIN_PDF_SIZE_BYTES:
            logger.warning(f"[PDF TOO SMALL] Size {len(content)} bytes (min {MIN_PDF_SIZE_BYTES} / 5KB)")
            return False
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save file
        with open(save_path, "wb") as f:
            f.write(content)
        
        logger.info(f"[VALID PDF] Downloaded successfully: {save_path}")
        return True
    
    except Exception as e:
        logger.error(f"[DOWNLOAD ERROR] {str(e)} for {url}")
        return False


def extract_pdf_text(pdf_path):
    """Extract raw text from a PDF file using pdfplumber"""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except ImportError:
        print("Warning: pdfplumber not installed! Install with: pip install pdfplumber")
        return None
    except Exception as e:
        logger.error(f"[PDF TEXT EXTRACTION ERROR] {str(e)} for {pdf_path}")
        return None


def get_pdf_metadata(pdf_path):
    """Get basic metadata about a PDF file"""
    try:
        if not os.path.exists(pdf_path):
            return None
        size = os.path.getsize(pdf_path)
        return {"file_path": pdf_path, "size_bytes": size, "size_kb": size / 1024}
    except Exception as e:
        logger.error(f"[METADATA ERROR] {str(e)} for {pdf_path}")
        return None
