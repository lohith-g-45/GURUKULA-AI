import sys, os
sys.path.append(os.path.dirname(__file__))

from utils.pdf_downloader import validate_pdf_url, download_real_pdf

url = "https://kpsc.kar.nic.in/611.pdf"
save_path = os.path.join("datasets", "KAS", "pyqs", "kas_prelims_paper_1_2024.pdf")

print("Testing URL validity...")
is_valid = validate_pdf_url(url)
print(f"URL Valid? {is_valid}")

if is_valid:
    print("\nAttempting download...")
    success = download_real_pdf(url, save_path)
    if success:
        print(f"\nSUCCESS: PDF saved to {save_path}")
    else:
        print("\nFailed to download PDF")
