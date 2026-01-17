from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from seleniumHindiPDF import extract_hindi_from_case_page


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

case_url = "https://indiankanoon.org/doc/1027556/"

paras = extract_hindi_from_case_page(driver, case_url)

driver.quit()

if paras is None:
    print("Hindi PDF not available")
else:
    print("Hindi paragraphs:", len(paras))
    print(paras[:2])
