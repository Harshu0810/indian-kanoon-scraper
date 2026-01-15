import os
import time
import uuid

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

SEARCH_URL = "https://indiankanoon.org/search/?formInput=doctypes:supremecourt%20year:2025"
DOWNLOAD_DIR = os.path.join(os.getcwd(), "pdfs")

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def collect_case_links(driver):
    print("🔍 Collecting case links...")
    driver.get(SEARCH_URL)

    wait = WebDriverWait(driver, 40)

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span.results-count")
        )
    )

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    articles = driver.find_elements(By.CSS_SELECTOR, "article.result")
    print(f"📄 Articles detected in DOM: {len(articles)}")

    links = []
    for article in articles:
        try:
            doc_links = article.find_elements(By.CSS_SELECTOR, "a.cite_tag")
            for a in doc_links:
                href = a.get_attribute("href")
                if href and "/doc/" in href:
                    links.append(href)
        except:
            continue

    print(f"✅ Found {len(links)} case links")
    return list(set(links))

def save_html(driver, title):
    safe = title.replace("/", "_").replace("\\", "_")[:80]
    filename = f"{safe}_{uuid.uuid4().hex[:6]}.html"
    path = os.path.join(DOWNLOAD_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print(f"💾 Saved: {filename}")


def crawl_case_pdfs():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    driver = get_driver()

    try:
        links = collect_case_links(driver)

        for i, link in enumerate(links, start=1):
            print(f"\n[{i}/{len(links)}] Visiting {link}")
            driver.get(link)
            time.sleep(4)

            try:
                title = driver.find_element(By.TAG_NAME, "h1").text
            except:
                title = f"case_{i}"

            save_html(driver, title)
            time.sleep(1)

    finally:
        driver.quit()
        print("\n✅ DONE. Files saved in:", DOWNLOAD_DIR)


if __name__ == "__main__":
    crawl_case_pdfs()