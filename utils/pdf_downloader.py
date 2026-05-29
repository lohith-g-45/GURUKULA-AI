import os
import requests
import logging
import re
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


def download_real_pdf(url, save_path, timeout=120):
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


def clean_extracted_text(text):
    """Clean extracted text by removing spam, URLs, watermarks, non-ASCII, etc."""
    if not text:
        return text
    
    # Keep only ASCII characters (English, numbers, punctuation)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Remove repeated "Page X" patterns
    text = re.sub(r'^\s*Page\s*\d+\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove testbook-related spam
    testbook_patterns = [
        r'testbook',
        r'www\.testbook',
        r'testbook\.com',
        r'testbook\.in',
    ]
    for pattern in testbook_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove VU-PHP-... patterns (watermarks)
    text = re.sub(r'VU-PHP-\S+', '', text)
    
    # Remove extra newlines and normalize spaces
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()
    
    return text


def extract_text_with_ocr(pdf_path):
    """Extract text from PDF using OCR (PyMuPDF + pytesseract)"""
    try:
        import fitz  # PyMuPDF
        from PIL import Image
        import pytesseract
        
        text = ""
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Render page as high-res image
            zoom = 2  # 2x zoom for better OCR
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Extract text with pytesseract
            page_text = pytesseract.image_to_string(img)
            text += page_text + "\n"
        
        doc.close()
        return text
    except ImportError as e:
        logger.warning(f"[OCR DEPENDENCY MISSING] {str(e)}")
        return None
    except Exception as e:
        logger.error(f"[OCR EXTRACTION ERROR] {str(e)} for {pdf_path}")
        return None


def extract_pdf_text(pdf_path):
    """Extract raw text from a PDF file (first PyMuPDF, then pdfplumber, then OCR fallback)"""
    extracted_text = None
    used_ocr = False
    
    # First try PyMuPDF (fitz) - often better than pdfplumber
    try:
        import fitz
        text = ""
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
        extracted_text = text
    except ImportError:
        logger.warning("PyMuPDF not installed, trying pdfplumber...")
    except Exception as e:
        logger.warning(f"[PyMuPDF ERROR] {str(e)}, trying pdfplumber...")
    
    # If PyMuPDF failed or text is too short, try pdfplumber
    if not extracted_text or len(extracted_text.strip()) < 200:
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            extracted_text = text
        except ImportError:
            logger.warning("pdfplumber not installed, trying OCR...")
        except Exception as e:
            logger.warning(f"[pdfplumber ERROR] {str(e)}, trying OCR...")
    
    # Check if extracted text is still too short (likely image-based PDF)
    if not extracted_text or len(extracted_text.strip()) < 200:
        logger.info(f"Text still too short, trying OCR for {pdf_path}")
        ocr_text = extract_text_with_ocr(pdf_path)
        if ocr_text and len(ocr_text.strip()) > 200:
            extracted_text = ocr_text
            used_ocr = True
    
    # Clean the extracted text
    if extracted_text:
        extracted_text = clean_extracted_text(extracted_text)
    
    return extracted_text, used_ocr


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
