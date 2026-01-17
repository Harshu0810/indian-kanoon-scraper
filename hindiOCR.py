import shutil
import tempfile
from pathlib import Path

import requests
import pytesseract
from pdf2image import convert_from_path


# === CONFIG ===
POPPLER_PATH = r"D:\poppler\Library\bin"
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


# ======================================================
# OCR CORE
# ======================================================

def extract_hindi_paragraphs_from_pdf(pdf_path: str) -> list[str]:
    temp_dir = Path(tempfile.mkdtemp(prefix="hin_ocr_"))
    paragraphs: list[str] = []

    try:
        images = convert_from_path(
            pdf_path,
            dpi=200,
            poppler_path=POPPLER_PATH,
            grayscale=True,
            fmt="png",
            output_folder=str(temp_dir)
        )

        for img in images:
            text = pytesseract.image_to_string(
                img,
                lang="hin",
                config="--oem 1 --psm 6"
            )

            for para in text.split("\n\n"):
                para = para.strip()
                if len(para) > 20:
                    paragraphs.append(para)

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return paragraphs


# ======================================================
# INDIAN KANOON HINDI PDF HANDLING
# ======================================================

def extract_hindi_from_case_page(driver, case_url: str) -> list[str]:
    """
    Indian Kanoon Hindi PDF logic:
    Hindi PDF = same doc URL + ?type=pdf&language=hi
    """

    print(f"[HINDI] Trying Hindi for: {case_url}")

    case_url = case_url.rstrip("/")

    hindi_pdf_urls = [
        f"{case_url}/?type=pdf&language=hi",
        f"{case_url}/?type=pdf&lang=hi",
    ]

    for pdf_url in hindi_pdf_urls:
        try:
            print(f"[HINDI] Trying PDF: {pdf_url}")

            r = requests.get(pdf_url, timeout=30)
            if r.status_code != 200:
                continue

            if not r.headers.get("Content-Type", "").lower().startswith("application/pdf"):
                continue

            temp_dir = Path(tempfile.mkdtemp(prefix="hin_pdf_"))
            pdf_path = temp_dir / "hindi.pdf"
            pdf_path.write_bytes(r.content)

            paras = extract_hindi_paragraphs_from_pdf(str(pdf_path))

            print(f"[HINDI] Extracted {len(paras)} Hindi paragraphs")

            shutil.rmtree(temp_dir, ignore_errors=True)
            return paras

        except Exception as e:
            print(f"[HINDI] Failed attempt: {e}")

    print("[HINDI] No Hindi PDF available")
    return []
