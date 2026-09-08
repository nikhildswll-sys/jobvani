"""
JobVani Scraper - All India Central Recruitments & Public Sector (Banking, ISRO, DRDO, Postal, Teaching)
"""

from .base import fetch_feed_items, upsert_job, upsert_admit_card, upsert_result, upsert_answer_key

ALL_INDIA_FEEDS = [
    "https://feeds.feedburner.com/freejobalert/bank-jobs",
    "https://feeds.feedburner.com/freejobalert/teaching-faculty-jobs",
    "https://feeds.feedburner.com/freejobalert"
]

CURATED_ALL_INDIA_DATA = [
    {
        "type": "job",
        "title": "IBPS Probationary Officers (PO/MT XIV) Recruitment 2026",
        "organization": "Institute of Banking Personnel Selection (IBPS)",
        "org_logo": "ibps",
        "category": "Banking",
        "vacancies": "4,455+",
        "qualification": "Graduate Degree in any discipline",
        "salary": "Starting Basic Pay Rs. 36,000/- + DA, HRA, CCA (Approx Rs. 57,000/- gross)",
        "last_date": "28 Aug 2026",
        "link": "https://ibps.in"
    },
    {
        "type": "job",
        "title": "ISRO Scientist/Engineer 'SC' (Civil, Electrical, Mech, Computer) 2026",
        "organization": "Indian Space Research Organisation (ISRO)",
        "org_logo": "central_govt",
        "category": "Central Government",
        "vacancies": "320+",
        "qualification": "B.E / B.Tech (First Class with min 65% marks)",
        "salary": "Level 10 (Rs. 56,100 - 1,77,500/-)",
        "last_date": "15 Oct 2026",
        "link": "https://isro.gov.in"
    },
    {
        "type": "job",
        "title": "India Post Gramin Dak Sevak (GDS) All India Schedule-II 2026",
        "organization": "Department of Posts (India Post)",
        "org_logo": "central_govt",
        "category": "Central Government",
        "vacancies": "44,228+",
        "qualification": "10th Standard (Matric) with passing marks in Math & English",
        "salary": "TRCA Slab: Rs. 10,000 - Rs. 29,380/- pm",
        "last_date": "05 Aug 2026",
        "link": "https://indiapostgdsonline.gov.in"
    },
    {
        "type": "job",
        "title": "State Bank of India Probationary Officers (SBI PO) 2026",
        "organization": "State Bank of India (SBI)",
        "org_logo": "ibps",
        "category": "Banking",
        "vacancies": "2,000+",
        "qualification": "Graduation in any discipline",
        "salary": "Basic Pay Rs. 41,960/- with 4 advance increments",
        "last_date": "27 Nov 2026",
        "link": "https://sbi.co.in"
    },
    {
        "type": "admit_card",
        "exam_name": "IBPS PO 2026 Prelims Online Call Letter",
        "organization": "Institute of Banking Personnel Selection (IBPS)",
        "release_date": "Available Now",
        "exam_date": "19 - 20 Oct 2026",
        "category": "Banking",
        "status": "Download Call Letter",
        "link": "https://ibps.in"
    },
    {
        "type": "admit_card",
        "exam_name": "NTA UGC NET June 2026 Phase-II Hall Ticket",
        "organization": "National Testing Agency (NTA)",
        "release_date": "Live Now",
        "exam_date": "24 - 30 Sep 2026",
        "category": "Teaching",
        "status": "Available Now",
        "link": "https://ugcnet.nta.ac.in"
    },
    {
        "type": "result",
        "exam_name": "SBI Junior Associates (Clerk) Mains Final Result 2026",
        "organization": "State Bank of India (SBI)",
        "result_date": "Declared Today",
        "exam_stage": "Final Selection",
        "status": "Marks & Roll Numbers",
        "link": "https://sbi.co.in/careers"
    }
]

def scrape_all_india():
    print("⚡ [Scraper] Initiating All India & Central Govt (Banking, ISRO, Postal, Teaching) Ingestion...")
    jobs_count = 0
    admit_count = 0
    result_count = 0
    key_count = 0

    for item in CURATED_ALL_INDIA_DATA:
        if item["type"] == "job":
            if upsert_job(item): jobs_count += 1
        elif item["type"] == "admit_card":
            if upsert_admit_card(item): admit_count += 1
        elif item["type"] == "result":
            if upsert_result(item): result_count += 1

    for feed_url in ALL_INDIA_FEEDS:
        items = fetch_feed_items(feed_url, max_items=25)
        for it in items:
            t_lower = it["title"].lower()
            # Category determination
            cat = "Central Government"
            org = "Government of India"
            org_logo = "central_govt"

            if any(k in t_lower for k in ["bank", "ibps", "sbi", "rbi", "nabard"]):
                cat = "Banking"
                org = "Public Sector Bank / IBPS"
                org_logo = "ibps"
            elif any(k in t_lower for k in ["teacher", "ugc", "net", "ctet", "kvs", "nvs", "school"]):
                cat = "Teaching"
                org = "Education Board / NTA"
                org_logo = "teaching"
            elif any(k in t_lower for k in ["isro", "drdo", "post", "gds", "bis", "intelligence bureau"]):
                cat = "Central Government"
                org = "Central Department / Ministry"
                org_logo = "central_govt"

            if any(k in t_lower for k in ["admit", "hall ticket", "call letter"]):
                if upsert_admit_card({
                    "exam_name": it["title"],
                    "organization": org,
                    "category": cat,
                    "link": it["link"]
                }): admit_count += 1
            elif any(k in t_lower for k in ["result", "marks", "cutoff", "scorecard"]):
                if upsert_result({
                    "exam_name": it["title"],
                    "organization": org,
                    "link": it["link"]
                }): result_count += 1
            else:
                if upsert_job({
                    "title": it["title"],
                    "organization": org,
                    "org_logo": org_logo,
                    "category": cat,
                    "desc": it["desc"],
                    "link": it["link"]
                }): jobs_count += 1

    print(f"✅ All India Ingestion: {jobs_count} Jobs, {admit_count} Admit Cards, {result_count} Results.")
    return {"department": "All India", "jobs": jobs_count, "admit_cards": admit_count, "results": result_count, "answer_keys": key_count}
