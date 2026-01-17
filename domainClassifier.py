import re
from collections import defaultdict

# ================= DOMAIN KEYWORDS =================

DOMAIN_KEYWORDS = {
    "Criminal Law": [
        r"\bipc\b", r"\bcrpc\b", r"\bfir\b",
        r"section\s+\d+", r"penal code",
        r"offence", r"accused", r"conviction",
        r"bail", r"sentence", r"trial court",
        r"charge sheet", r"criminal appeal",
        r"prosecution", r"culpable homicide"
    ],

    "Constitutional Law": [
        r"article\s+\d+", r"constitution of india",
        r"fundamental rights", r"writ petition",
        r"constitutional bench", r"judicial review",
        r"basic structure", r"public interest litigation",
        r"preamble", r"directive principles"
    ],

    "Service Law": [
        r"service", r"service rules", r"promotion",
        r"pension", r"disciplinary proceedings",
        r"suspension", r"employment",
        r"reinstatement", r"termination",
        r"government servant", r"seniority"
    ],

    "Tax Law": [
        r"income tax", r"gst", r"assessment",
        r"tax act", r"tax liability",
        r"duty", r"excise", r"customs",
        r"taxation", r"revenue department"
    ],

    "Property Law": [
        r"land acquisition", r"compensation",
        r"property", r"possession",
        r"lease", r"ownership", r"title dispute",
        r"immovable property", r"sale deed"
    ],

    "Arbitration / Commercial": [
        r"arbitration", r"arbitral award",
        r"commercial", r"contract",
        r"agreement", r"liability",
        r"damages", r"breach of contract",
        r"specific performance"
    ],

    "Family Law": [
        r"divorce", r"marriage",
        r"maintenance", r"custody",
        r"matrimonial", r"alimony",
        r"family court", r"hindu marriage act"
    ],
}

# ================= PARAGRAPH DOMAIN =================

def infer_domain_for_paragraph(text: str):
    """
    Paragraph-level domain inference.
    Returns (domain, confidence)
    """

    text = text.lower()
    scores = defaultdict(float)
    total_hits = 0.0

    for domain, patterns in DOMAIN_KEYWORDS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                scores[domain] += 1.0
                total_hits += 1.0

    if not scores:
        return "Unclassified", 0.0

    best_domain = max(scores, key=scores.get)
    confidence = round(scores[best_domain] / total_hits, 2)

    return best_domain, confidence


# ================= CASE-LEVEL DOMAIN =================

def infer_case_domain(paragraphs: list[str]):
    """
    Case-level domain inference using all paragraphs.
    Used for fallback / analysis only.
    """

    aggregate = defaultdict(float)

    for para in paragraphs:
        domain, conf = infer_domain_for_paragraph(para)
        if domain != "Unclassified":
            aggregate[domain] += conf

    if not aggregate:
        return "Unclassified"

    return max(aggregate, key=aggregate.get)
