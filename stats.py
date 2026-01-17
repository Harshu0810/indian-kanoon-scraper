import pandas as pd
from pathlib import Path

PARQUET_DIR = Path("parquet")
STATS_DIR = Path("stats")
STATS_DIR.mkdir(exist_ok=True)


def load_all_parquet():
    dfs = []
    for p in PARQUET_DIR.glob("sci_*.parquet"):
        print(f"Loading {p.name}")
        dfs.append(pd.read_parquet(p))
    return pd.concat(dfs, ignore_index=True)


def save_domain_distribution(df):
    dist = df["Primary_Domain"].value_counts().to_frame("Count")
    dist["Percent"] = (dist["Count"] / len(df) * 100).round(2)
    dist.to_csv(STATS_DIR / "domain_distribution.csv")
    return dist


def save_confidence_summary(df):
    summary = df["Domain_Confidence"].describe()
    summary.to_csv(STATS_DIR / "confidence_summary.csv")
    return summary


def save_unclassified_stats(df):
    total = len(df)
    unclassified = (df["Primary_Domain"] == "Unclassified").sum()
    percent = round(unclassified / total * 100, 2)

    text = (
        f"Total paragraphs: {total}\n"
        f"Unclassified paragraphs: {unclassified}\n"
        f"Unclassified percent: {percent}%\n"
    )

    (STATS_DIR / "unclassified_summary.txt").write_text(text)
    return text


def save_paragraphs_per_case(df):
    stats = df.groupby("Case_ID")["Para_No"].max().describe()
    stats.to_csv(STATS_DIR / "paragraphs_per_case.csv")
    return stats


def save_overall_summary(df):
    text = (
        f"Total paragraphs: {len(df)}\n"
        f"Total cases: {df['Case_ID'].nunique()}\n"
        f"Domains found: {df['Primary_Domain'].nunique()}\n"
        f"Average confidence: {round(df['Domain_Confidence'].mean(), 2)}\n"
    )
    (STATS_DIR / "overall_summary.txt").write_text(text)
    return text


def main():
    df = load_all_parquet()

    print("\n📊 Saving statistics to /stats folder\n")

    save_domain_distribution(df)
    save_confidence_summary(df)
    save_unclassified_stats(df)
    save_paragraphs_per_case(df)
    save_overall_summary(df)

    print("✅ Stats saved successfully")


if __name__ == "__main__":
    main()
