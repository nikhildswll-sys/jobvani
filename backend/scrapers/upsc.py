"""
JobVani Scraper - Union Public Service Commission (UPSC)
Fetches: Civil Services (IAS/IPS/IFS), NDA, CDS, CMS, IES, CAPF AC.
"""

from .base import fetch_feed_items, upsert_job, upsert_admit_card, upsert_result, upsert_answer_key

UPSC_FEEDS = [
    "https://feeds.feedburner.com/freejobalert/upsc-jobs",
    "https://feeds.feedburner.com/freejobalert"
]

CURATED_UPSC_DATA = [
    {
        "type": "job",
        "title": "UPSC Civil Services Examination (IAS/IPS/IFS) 2026",
        "organization": "Union Public Service Commission (UPSC)",
        "org_logo": "upsc",
        "category": "Central Government",
        "vacancies": "1,056+",
        "qualification": "Bachelor's Degree in any discipline from recognized University",
        "salary": "Level 10 in Pay Matrix (Rs. 56,100 - 1,77,500/-)",
        "last_date": "05 Mar 2026",
        "link": "https://upsc.gov.in"
    },
    {
        "type": "job",
        "title": "UPSC Combined Defence Services CDS (II) 2026 Examination",
        "organization": "Union Public Service Commission (UPSC)",
        "org_logo": "upsc",
        "category": "Defence",
        "vacancies": "459+",
        "qualification": "Degree / Engineering for IMA, INA & AFA",
        "salary": "Level 10 (Rs. 56,100/-) + Military Service Pay MSP",
        "last_date": "04 Jun 2026",
        "link": "https://upsc.gov.in"
    },
    {
        "type": "job",
        "title": "UPSC National Defence Academy & Naval Academy NDA (II) 2026",
        "organization": "Union Public Service Commission (UPSC)",
        "org_logo": "upsc",
        "category": "Defence",
        "vacancies": "404+",
        "qualification": "12th Pass / Appearing (Physics & Math for Air Force/Navy)",
        "salary": "Cadet Training Stipend Rs. 56,100/- pm",
        "last_date": "04 Jun 2026",
        "link": "https://upsc.gov.in"
    },
    {
        "type": "admit_card",
        "exam_name": "UPSC NDA & CDS (II) 2026 E-Admit Card Direct Download",
        "organization": "Union Public Service Commission (UPSC)",
        "release_date": "Live Now",
        "exam_date": "01 Sep 2026",
        "category": "Defence",
        "status": "Available Now",
        "link": "https://upsc.gov.in"
    },
    {
        "type": "result",
        "exam_name": "UPSC Civil Services Prelims 2026 Written Result with Roll Numbers",
        "organization": "Union Public Service Commission (UPSC)",
        "result_date": "Declared Today",
        "exam_stage": "Stage-1 Prelims",
        "status": "PDF Released",
        "link": "https://upsc.gov.in"
    }
]

def scrape_upsc():
    print("⚡ [Scraper] Initiating UPSC (Union Public Service Commission) Ingestion...")
    jobs_count = 0
    admit_count = 0
    result_count = 0
    key_count = 0

    for item in CURATED_UPSC_DATA:
        if item["type"] == "job":
            if upsert_job(item): jobs_count += 1
        elif item["type"] == "admit_card":
            if upsert_admit_card(item): admit_count += 1
        elif item["type"] == "result":
            if upsert_result(item): result_count += 1

    for feed_url in UPSC_FEEDS:
        items = fetch_feed_items(feed_url, max_items=20)
        for it in items:
            t_lower = it["title"].lower()
            if not any(k in t_lower for k in ["upsc", "civil services", "nda", "cds", "ies", "cms", "ias"]):
                continue

            if any(k in t_lower for k in ["admit", "hall ticket", "e-admit"]):
                if upsert_admit_card({
                    "exam_name": it["title"],
                    "organization": "Union Public Service Commission (UPSC)",
                    "category": "Central Government",
                    "link": it["link"]
                }): admit_count += 1
            elif any(k in t_lower for k in ["result", "marks", "cutoff", "recommendation"]):
                if upsert_result({
                    "exam_name": it["title"],
                    "organization": "Union Public Service Commission (UPSC)",
                    "link": it["link"]
                }): result_count += 1
            else:
                if upsert_job({
                    "title": it["title"],
                    "organization": "Union Public Service Commission (UPSC)",
                    "org_logo": "upsc",
                    "category": "Central Government",
                    "desc": it["desc"],
                    "link": it["link"]
                }): jobs_count += 1

    print(f"✅ UPSC Ingestion: {jobs_count} Jobs, {admit_count} Admit Cards, {result_count} Results.")
    return {"department": "UPSC", "jobs": jobs_count, "admit_cards": admit_count, "results": result_count, "answer_keys": key_count}
