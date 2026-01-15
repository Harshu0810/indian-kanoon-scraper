import time
from selenium.webdriver.common.by import By

def collect_case_links(driver, max_pages=5):
    all_links = set()

    for page in range(max_pages):
        print(f"🔍 Scraping page {page}")
        time.sleep(3)

        cases = driver.find_elements(By.CSS_SELECTOR, "h4.result_title a")
        print(f"Cases found on page: {len(cases)}")

        for c in cases:
            href = c.get_attribute("href")
            if href:
                all_links.add(href)

        try:
            next_btn = driver.find_element(By.LINK_TEXT, "Next")
            next_btn.click()
        except:
            print("No next page.")
            break

    return list(all_links)