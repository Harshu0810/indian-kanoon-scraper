import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_case_urls_for_year(driver, year: int, max_pages: int | None = None):
    """
    Correct & verified crawl flow for Indian Kanoon SCI:
    1. Open /browse/supremecourt/<year>/
    2. Click 'Entire Year'
    3. Wait until case links appear
    4. Paginate using 'Next'
    """

    url = f"https://indiankanoon.org/browse/supremecourt/{year}/"
    print(f"🔍 Collecting Supreme Court cases for year {year}")

    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # ---------- Clicking "Entire Year" ----------
    try:
        entire_year = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Entire Year"))
        )
        driver.execute_script("arguments[0].click();", entire_year)
        print("✓ Clicked 'Entire Year'")
    except Exception as e:
        print("❌ Failed to click 'Entire Year'")
        raise RuntimeError("Cannot proceed without Entire Year view") from e

    # ---------- Waiting for cases to load ----------
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href^='/doc/']")
            )
        )
        print("✓ Case list loaded")
    except:
        print("❌ No cases loaded after clicking 'Entire Year'")
        return []

    # ---------- Collecting cases with pagination ----------
    case_urls = []
    page = 0

    while True:
        links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/doc/']")

        for link in links:
            href = link.get_attribute("href")
            if href and href not in case_urls:
                case_urls.append(href)

        page += 1
        print(f"✓ Page {page} collected ({len(case_urls)} cases so far)")

        if max_pages and page >= max_pages:
            break

        try:
            next_btn = driver.find_element(By.LINK_TEXT, "Next")
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(2)
        except:
            break

    print(f"✔ Total cases collected for {year}: {len(case_urls)}")
    return case_urls
