import os
import sys
import requests
from urllib.parse import urlparse
from config import EXAM_CONFIG


def get_exam_dir(exam_name):
    return os.path.join("datasets", exam_name)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def get_data_path(exam_name, data_type):
    exam_dir = get_exam_dir(exam_name)
    data_dir = os.path.join(exam_dir, data_type)
    return ensure_dir(data_dir)


def get_metadata_path(exam_name):
    return os.path.join(get_data_path(exam_name, "exams"), f"{exam_name}_metadata.json")


def get_syllabus_path(exam_name):
    return os.path.join(get_data_path(exam_name, "syllabus"), f"{exam_name}_syllabus.json")


def get_weightage_path(exam_name):
    return os.path.join(get_data_path(exam_name, "weightage"), f"{exam_name}_weightage.json")


def get_pattern_path(exam_name):
    return os.path.join(get_data_path(exam_name, "patterns"), f"{exam_name}_pattern.json")


def get_pyqs_path(exam_name):
    return os.path.join(get_data_path(exam_name, "pyqs"), f"{exam_name}_pyqs.json")


def get_raw_syllabus_path(exam_name):
    return os.path.join(get_data_path(exam_name, "raw"), f"{exam_name}_syllabus_raw.txt")


def validate_url(url, timeout=5):
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.head(url, headers=headers, allow_redirects=True, timeout=timeout)
        return response.status_code == 200
    except Exception:
        return False


def validate_pdf_url(url, timeout=5):
    if not validate_url(url, timeout):
        return False
    lower_url = url.lower()
    return lower_url.endswith(".pdf") or "pdf" in lower_url


def cleanup_old_structure():
    old_dirs = [
        "datasets/exams",
        "datasets/analytics",
        "datasets/patterns",
        "datasets/pyqs",
        "datasets/raw",
        "datasets/syllabus",
        "datasets/weightage",
        "datasets/agent_contexts"
    ]
    
    for old_dir in old_dirs:
        if os.path.exists(old_dir) and os.path.isdir(old_dir):
            import shutil
            shutil.rmtree(old_dir)
            print(f"Removed old directory: {old_dir}")
    
    print("Old dataset structure cleaned up!")
    return True
