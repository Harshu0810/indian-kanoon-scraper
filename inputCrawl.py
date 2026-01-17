from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_english_paragraphs(driver, timeout=15):
    """
    Robust English extractor for Indian Kanoon SCI cases.
    Works across inconsistent page layouts.
    """

    wait = WebDriverWait(driver, timeout)

    # ✅ Wait for ANY paragraph to appear (not strict container)
    try:
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "p"))
        )
    except:
        # Page loaded but no paragraphs (rare, but possible)
        return [], _get_case_id(driver), "Unknown", "Unknown"

    paras = driver.find_elements(By.TAG_NAME, "p")

    english_paras = [
        p.text.strip()
        for p in paras
        if p.text and len(p.text.strip()) > 30
    ]

    return english_paras, _get_case_id(driver), "Unknown", "Unknown"


def _get_case_id(driver):
    """
    Extract case ID from URL safely
    """
    url = driver.current_url.rstrip("/")
    return url.split("/")[-1]
