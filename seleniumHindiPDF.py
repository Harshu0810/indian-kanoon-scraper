import time
from pathlib import Path
from selenium.webdriver.common.by import By

from hindiOCR import extract_hindi_paragraphs_from_pdf


# ======================================================
# CONFIG
# ======================================================

DOWNLOAD_DIR = Path("D:/temp_hindi_pdfs")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

PDF_WAIT_TIMEOUT = 20  # seconds


def extract_hindi_from_case_page(driver) -> list[str] | None:
    """
    Assumes driver is ALREADY on case page.
    Fast Hindi detection + Selenium PDF download.
    """
    hindi_links = driver.find_elements(
        By.XPATH, "//a[contains(text(),'हिंदी')]"
    )

    if not hindi_links:
        return None

    hindi_link = hindi_links[0]
    existing_files = set(DOWNLOAD_DIR.glob("*.pdf"))
    hindi_link.click()

    pdf_path = _wait_for_pdf(existing_files)

    if not pdf_path:
        return None

    try:
        return extract_hindi_paragraphs_from_pdf(str(pdf_path))
    finally:
        try:
            pdf_path.unlink(missing_ok=True)
        except:
            pass


# ======================================================
# HELPERS
# ======================================================

def _wait_for_pdf(existing_files: set[Path]) -> Path | None:
    start = time.time()

    while time.time() - start < PDF_WAIT_TIMEOUT:
        current = set(DOWNLOAD_DIR.glob("*.pdf"))
        new = current - existing_files

        if new:
            pdf = new.pop()
            if not pdf.name.endswith(".crdownload"):
                return pdf

        time.sleep(0.3)

    return None
