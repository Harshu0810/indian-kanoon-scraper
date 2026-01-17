from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from smartCrawl import get_case_urls_for_year
from inputCrawl import extract_english_paragraphs
from domainClassifier import infer_domain_for_paragraph


# ================= CONFIG =================

START_YEAR = 2022
END_YEAR = 2023              
MAX_CASES_TEST = None        # previously set to 5 for quick test

BASE_DIR = Path(__file__).resolve().parent
PARQUET_DIR = BASE_DIR / "parquet"
PARQUET_DIR.mkdir(exist_ok=True)


# ================= DRIVER =================

def build_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    return driver


# ================= PARQUET =================

def write_parquet(year, rows):
    if not rows:
        print("⚠ No rows to write")
        return

    table = pa.Table.from_pylist(rows)
    out = PARQUET_DIR / f"sci_{year}.parquet"
    pq.write_table(table, out, compression="snappy")
    print(f"✅ Parquet written: {out}")


# ================= MAIN =================

def main():
    driver = build_driver()

    try:
        for year in range(START_YEAR, END_YEAR + 1):
            print(f"\n===== YEAR {year} =====")

            case_urls = get_case_urls_for_year(driver, year)

            if MAX_CASES_TEST:
                case_urls = case_urls[:MAX_CASES_TEST]

            rows = []

            for idx, case_url in enumerate(case_urls, start=1):
                print(f"[{idx}/{len(case_urls)}] {case_url}")

                driver.get(case_url)

                english_paras, case_id, _, _ = extract_english_paragraphs(driver)

                for para_no, para in enumerate(english_paras, start=1):
                    domain, confidence = infer_domain_for_paragraph(para)

                    rows.append({
                        "Case_ID": case_id,
                        "Case_URL": case_url,
                        "Year": year,
                        "Para_No": para_no,
                        "English_Text": para,
                        "Primary_Domain": domain,
                        "Domain_Confidence": confidence,
                        "Hindi_Status": "Unavailable"
                    })

            write_parquet(year, rows)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
