"""
JobVani Scraper - Police & Paramilitary Forces
Fetches: Delhi Police, UP Police, Bihar Police (CSBC/BPSSC), Rajasthan Police, MP Police, State Police.
"""

from .base import fetch_feed_items, upsert_job, upsert_admit_card, upsert_result, upsert_answer_key

POLICE_FEEDS = [
    "https://feeds.feedburner.com/freejobalert/police-jobs",
    "https://feeds.feedburner.com/freejobalert"
]

CURATED_POLICE_DATA = [
    {
        "type": "job",
        "title": "UP Police Constable Direct Recruitment 2026 (Civil Police)",
        "organization": "Uttar Pradesh Police Recruitment & Promotion Board (UPPRPB)",
        "org_logo": "police",
        "category": "Police",
        "job_type": "State",
        "location": "Uttar Pradesh",
        "vacancies": "60,244+",
        "qualification": "12th Pass (Intermediate) from recognized Board",
        "salary": "Pay Matrix Level 3 (Rs. 21,700 - 69,100/-)",
        "last_date": "16 Jan 2026",
        "link": "https://uppbpb.gov.in"
    },
    {
        "type": "job",
        "title": "Delhi Police Constable (Executive) Male & Female 2026",
        "organization": "Delhi Police / Staff Selection Commission",
        "org_logo": "police",
        "category": "Police",
        "job_type": "Central",
        "location": "Delhi",
        "vacancies": "7,547+",
        "qualification": "10+2 (Senior Secondary) with valid Driving License for males",
        "salary": "Pay Level 3 (Rs. 21,700 - 69,100/-)",
        "last_date": "30 Sep 2026",
        "link": "https://delhipolice.gov.in"
    },
    {
        "type": "job",
        "title": "Bihar Police Constable (CSBC Advertisement 01/2026)",
        "organization": "Central Selection Board of Constable (CSBC Bihar)",
        "org_logo": "police",
        "category": "Police",
        "job_type": "State",
        "location": "Bihar",
        "vacancies": "21,391+",
        "qualification": "10+2 Intermediate Pass",
        "salary": "Level 3 (Rs. 21,700 - 69,100/-)",
        "last_date": "20 Jul 2026",
        "link": "https://csbc.bih.nic.in"
    },
    {
        "type": "admit_card",
        "exam_name": "UP Police Constable Re-Exam City Intimation Slip & Admit Card",
        "organization": "UPPBPB Police Board",
        "release_date": "Live Now",
        "exam_date": "23, 24, 25, 30, 31 Aug 2026",
        "category": "Police",
        "status": "Available Now",
        "link": "https://uppbpb.gov.in"
    },
    {
        "type": "result",
        "exam_name": "Bihar Police Sub-Inspector (BPSSC SI) Final Selection List",
        "organization": "Bihar Police Subordinate Services Commission",
        "result_date": "Declared",
        "exam_stage": "Final Merit & Roll Numbers",
        "status": "PDF Out",
        "link": "https://bpssc.bih.nic.in"
    }
]

def scrape_police():
    print("⚡ [Scraper] Initiating State & Central Police Recruitments Ingestion...")
    jobs_count = 0
    admit_count = 0
    result_count = 0
    key_count = 0

    for item in CURATED_POLICE_DATA:
        if item["type"] == "job":
            if upsert_job(item): jobs_count += 1
        elif item["type"] == "admit_card":
            if upsert_admit_card(item): admit_count += 1
        elif item["type"] == "result":
            if upsert_result(item): result_count += 1

    for feed_url in POLICE_FEEDS:
        items = fetch_feed_items(feed_url, max_items=25)
        for it in items:
            t_lower = it["title"].lower()
            if not any(k in t_lower for k in ["police", "constable", "sub inspector", "daroga", "csbc", "uppbpb", "si"]):
                continue

            if any(k in t_lower for k in ["admit", "hall ticket", "city slip", "physical"]):
                if upsert_admit_card({
                    "exam_name": it["title"],
                    "organization": "Police Recruitment Board",
                    "category": "Police",
                    "link": it["link"]
                }): admit_count += 1
            elif any(k in t_lower for k in ["result", "marks", "cut off", "merit"]):
                if upsert_result({
                    "exam_name": it["title"],
                    "organization": "Police Recruitment Board",
                    "link": it["link"]
                }): result_count += 1
            else:
                if upsert_job({
                    "title": it["title"],
                    "organization": "Police Recruitment Board",
                    "org_logo": "police",
                    "category": "Police",
                    "desc": it["desc"],
                    "link": it["link"]
                }): jobs_count += 1

    print(f"✅ Police Ingestion: {jobs_count} Jobs, {admit_count} Admit Cards, {result_count} Results.")
    return {"department": "Police", "jobs": jobs_count, "admit_cards": admit_count, "results": result_count, "answer_keys": key_count}
