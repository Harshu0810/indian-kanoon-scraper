import os
import time
import sys
import signal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


HEADLESS = False
START_YEAR = 2025
END_YEAR = 2000

WAIT = 20

BASE_DIR = os.getcwd()
BASE_PDF_DIR = os.path.join(BASE_DIR, "pdfs")
os.makedirs(BASE_PDF_DIR, exist_ok=True)

driver = None

def handle_exit(sig, frame):
    print("\n🛑 Stopped by user")
    if driver:
        driver.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)


def get_driver(download_dir):
    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,

        "profile.managed_default_content_settings.images": 2,

        "profile.managed_default_content_settings.stylesheets": 2,
    }
    options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(options=options)

def crawl():
    global driver

    for year in range(START_YEAR, END_YEAR - 1, -1):
        print(f"\n🗓️ YEAR {year}")

        year_dir = os.path.join(BASE_PDF_DIR, str(year))
        os.makedirs(year_dir, exist_ok=True)

        driver = get_driver(year_dir)
        wait = WebDriverWait(driver, WAIT)

        search_url = (
            f"https://indiankanoon.org/search/"
            f"?formInput=doctypes:supremecourt year:{year}"
        )
        driver.get(search_url)

        while True:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.result")))
            articles = driver.find_elements(By.CSS_SELECTOR, "article.result")

            print(f"📄 Page with {len(articles)} cases")

            for i in range(len(articles)):
                articles = driver.find_elements(By.CSS_SELECTOR, "article.result")
                link = articles[i].find_element(By.CSS_SELECTOR, "h4.result_title a")

                driver.execute_script("arguments[0].click();", link)
                wait.until(lambda d: "search" not in d.current_url)

                try:
                    pdf_btn = wait.until(
                        EC.element_to_be_clickable((By.ID, "pdfdoc"))
                    )
                    pdf_btn.click()
                    time.sleep(2)
                except:
                    pass

                driver.back()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.result")))

            try:
                next_btn = driver.find_element(By.LINK_TEXT, "Next")
                driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(1)
            except:
                print(f"✅ Year {year} completed")
                break

        driver.quit()

    print("\n🎯 ALL YEARS COMPLETED")

if __name__ == "__main__":
    crawl()
