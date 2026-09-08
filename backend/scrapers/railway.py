"""
JobVani Scraper - Indian Railways (RRB / RRC)
Fetches: NTPC, Group D, ALP, Technician, RPF Constable & SI, Junior Engineer.
"""

from .base import fetch_feed_items, upsert_job, upsert_admit_card, upsert_result, upsert_answer_key

RAILWAY_FEEDS = [
    "https://feeds.feedburner.com/freejobalert/railway-jobs",
    "https://feeds.feedburner.com/freejobalert"
]

CURATED_RAILWAY_DATA = [
    {
        "type": "job",
        "title": "Railway RRB NTPC Non-Technical Popular Categories 2026",
        "organization": "Railway Recruitment Boards (RRB)",
        "org_logo": "railway",
        "category": "Railways",
        "vacancies": "11,558+",
        "qualification": "12th Pass / Graduate Degree",
        "salary": "7th CPC Level 2 to Level 6 (Rs. 19,900 - Rs. 92,300/-)",
        "last_date": "13 Oct 2026",
        "link": "https://indianrailways.gov.in"
    },
    {
        "type": "job",
        "title": "Railway RRB Assistant Loco Pilot (ALP) Recruitment 2026",
        "organization": "Railway Recruitment Boards (RRB)",
        "org_logo": "railway",
        "category": "Railways",
        "vacancies": "18,799+",
        "qualification": "Matriculation (10th) + ITI / Diploma in Engineering",
        "salary": "Level 2 in 7th CPC (Rs. 19,900/- + Allowances)",
        "last_date": "19 Feb 2026",
        "link": "https://rrbcdg.gov.in"
    },
    {
        "type": "job",
        "title": "RPF Sub-Inspector & Constable Recruitment 2026",
        "organization": "Railway Protection Force (RPF)",
        "org_logo": "railway",
        "category": "Railways",
        "vacancies": "4,660+",
        "qualification": "10th Pass (Constable) / Graduate (Sub Inspector)",
        "salary": "Level 3 & Level 6 (Rs. 21,700 - Rs. 1,12,400/-)",
        "last_date": "14 May 2026",
        "link": "https://rrbapply.gov.in"
    },
    {
        "type": "admit_card",
        "exam_name": "Railway RRB ALP CBT-1 Exam City Intimation & Hall Ticket",
        "organization": "Railway Recruitment Boards (RRB)",
        "release_date": "Available",
        "exam_date": "25 - 29 Nov 2026",
        "category": "Railways",
        "status": "Check City & Date",
        "link": "https://rrbcdg.gov.in"
    },
    {
        "type": "result",
        "exam_name": "Railway RRB Technician Grade-I & III Provisional Scorecard",
        "organization": "Railway Recruitment Boards (RRB)",
        "result_date": "This Week",
        "exam_stage": "Stage-1 CBT",
        "status": "Cutoff & Marks",
        "link": "https://rrbcdg.gov.in"
    }
]

def scrape_railway():
    print("⚡ [Scraper] Initiating Indian Railways (RRB/RRC) Ingestion...")
    jobs_count = 0
    admit_count = 0
    result_count = 0
    key_count = 0

    for item in CURATED_RAILWAY_DATA:
        if item["type"] == "job":
            if upsert_job(item): jobs_count += 1
        elif item["type"] == "admit_card":
            if upsert_admit_card(item): admit_count += 1
        elif item["type"] == "result":
            if upsert_result(item): result_count += 1

    for feed_url in RAILWAY_FEEDS:
        items = fetch_feed_items(feed_url, max_items=20)
        for it in items:
            t_lower = it["title"].lower()
            if not any(k in t_lower for k in ["railway", "rrb", "rrc", "ntpc", "loco pilot", "rpf"]):
                continue

            if any(k in t_lower for k in ["admit", "city slip", "hall ticket"]):
                if upsert_admit_card({
                    "exam_name": it["title"],
                    "organization": "Railway Recruitment Boards (RRB)",
                    "category": "Railways",
                    "link": it["link"]
                }): admit_count += 1
            elif any(k in t_lower for k in ["result", "marks", "cutoff", "scorecard"]):
                if upsert_result({
                    "exam_name": it["title"],
                    "organization": "Railway Recruitment Boards (RRB)",
                    "link": it["link"]
                }): result_count += 1
            elif any(k in t_lower for k in ["answer key", "objection"]):
                if upsert_answer_key({
                    "exam_name": it["title"],
                    "organization": "Railway Recruitment Boards (RRB)",
                    "link": it["link"]
                }): key_count += 1
            else:
                if upsert_job({
                    "title": it["title"],
                    "organization": "Railway Recruitment Boards (RRB)",
                    "org_logo": "railway",
                    "category": "Railways",
                    "desc": it["desc"],
                    "link": it["link"]
                }): jobs_count += 1

    print(f"✅ Railway Ingestion: {jobs_count} Jobs, {admit_count} Admit Cards, {result_count} Results, {key_count} Answer Keys.")
    return {"department": "Railways", "jobs": jobs_count, "admit_cards": admit_count, "results": result_count, "answer_keys": key_count}
