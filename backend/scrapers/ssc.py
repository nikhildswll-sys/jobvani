"""
JobVani Scraper - Staff Selection Commission (SSC)
Fetches: CGL, CHSL, MTS, CPO, GD, JE, Stenographer notifications, admit cards, results, and answer keys.
"""

from .base import fetch_feed_items, upsert_job, upsert_admit_card, upsert_result, upsert_answer_key, clean_html, extract_vacancies

SSC_FEEDS = [
    "https://feeds.feedburner.com/freejobalert/ssc-jobs",
    "https://feeds.feedburner.com/freejobalert"
]

CURATED_SSC_DATA = [
    {
        "type": "job",
        "title": "SSC CGL 2026 Combined Graduate Level Examination",
        "organization": "Staff Selection Commission (SSC)",
        "org_logo": "ssc",
        "category": "SSC",
        "vacancies": "17,727+",
        "qualification": "Bachelor's Degree in any discipline",
        "salary": "Pay Level 4 to Level 8 (Rs. 25,500 - 1,51,100/-)",
        "last_date": "24 Sep 2026",
        "link": "https://ssc.gov.in"
    },
    {
        "type": "job",
        "title": "SSC CHSL (10+2) Combined Higher Secondary Level 2026",
        "organization": "Staff Selection Commission (SSC)",
        "org_logo": "ssc",
        "category": "SSC",
        "vacancies": "3,712+",
        "qualification": "12th Pass (10+2) from recognized Board",
        "salary": "Pay Level 2 & 4 (Rs. 19,900 - 81,100/-)",
        "last_date": "18 Oct 2026",
        "link": "https://ssc.gov.in"
    },
    {
        "type": "job",
        "title": "SSC GD Constable 2026 in BSF, CISF, CRPF, SSB, ITBP, AR",
        "organization": "Staff Selection Commission (SSC)",
        "org_logo": "ssc",
        "category": "SSC",
        "vacancies": "39,481+",
        "qualification": "10th Pass (Matriculation)",
        "salary": "Pay Level 3 (Rs. 21,700 - 69,100/-)",
        "last_date": "14 Nov 2026",
        "link": "https://ssc.gov.in"
    },
    {
        "type": "admit_card",
        "exam_name": "SSC CGL 2026 Tier-1 Computer Based Exam Hall Ticket",
        "organization": "Staff Selection Commission (SSC)",
        "release_date": "Available Now",
        "exam_date": "09 - 26 Sep 2026",
        "category": "SSC",
        "status": "Available Now",
        "link": "https://ssc.gov.in"
    },
    {
        "type": "result",
        "exam_name": "SSC CHSL (10+2) 2025 Final Recommendation List",
        "organization": "Staff Selection Commission (SSC)",
        "result_date": "Declared",
        "exam_stage": "Final Merit List",
        "status": "Declared (PDF)",
        "link": "https://ssc.gov.in"
    },
    {
        "type": "answer_key",
        "exam_name": "SSC GD Constable 2026 Final Answer Key with Response Sheet",
        "organization": "Staff Selection Commission (SSC)",
        "exam_date": "March 2026",
        "release_date": "Live",
        "challenge_window": "Window Active",
        "link": "https://ssc.gov.in"
    }
]

def scrape_ssc():
    print("⚡ [Scraper] Initiating SSC (Staff Selection Commission) Ingestion...")
    jobs_count = 0
    admit_count = 0
    result_count = 0
    key_count = 0

    # Ingest Curated SSC Records
    for item in CURATED_SSC_DATA:
        if item["type"] == "job":
            if upsert_job(item): jobs_count += 1
        elif item["type"] == "admit_card":
            if upsert_admit_card(item): admit_count += 1
        elif item["type"] == "result":
            if upsert_result(item): result_count += 1
        elif item["type"] == "answer_key":
            if upsert_answer_key(item): key_count += 1

    # Ingest Live Public SSC RSS
    for feed_url in SSC_FEEDS:
        items = fetch_feed_items(feed_url, max_items=20)
        for it in items:
            t_lower = it["title"].lower()
            if not any(k in t_lower for k in ["ssc", "staff selection", "cgl", "chsl", "cpo", "mts", "stenographer"]):
                continue

            if any(k in t_lower for k in ["admit", "hall ticket", "call letter", "city slip"]):
                if upsert_admit_card({
                    "exam_name": it["title"],
                    "organization": "Staff Selection Commission (SSC)",
                    "category": "SSC",
                    "link": it["link"]
                }): admit_count += 1
            elif any(k in t_lower for k in ["result", "marks", "cutoff", "merit"]):
                if upsert_result({
                    "exam_name": it["title"],
                    "organization": "Staff Selection Commission (SSC)",
                    "link": it["link"]
                }): result_count += 1
            elif any(k in t_lower for k in ["answer key", "response sheet"]):
                if upsert_answer_key({
                    "exam_name": it["title"],
                    "organization": "Staff Selection Commission (SSC)",
                    "link": it["link"]
                }): key_count += 1
            else:
                if upsert_job({
                    "title": it["title"],
                    "organization": "Staff Selection Commission (SSC)",
                    "org_logo": "ssc",
                    "category": "SSC",
                    "desc": it["desc"],
                    "link": it["link"]
                }): jobs_count += 1

    print(f"✅ SSC Ingestion: {jobs_count} Jobs, {admit_count} Admit Cards, {result_count} Results, {key_count} Answer Keys.")
    return {"department": "SSC", "jobs": jobs_count, "admit_cards": admit_count, "results": result_count, "answer_keys": key_count}
