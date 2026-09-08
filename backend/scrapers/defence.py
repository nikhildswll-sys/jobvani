"""
JobVani Scraper - Indian Armed Forces (Army, Navy, Air Force)
Fetches: Join Indian Army (Agniveer, TGC, TES), Join Indian Navy (SSR, MR, INET), Indian Air Force (AFCAT, Agniveer Vayu).
"""

from .base import fetch_feed_items, upsert_job, upsert_admit_card, upsert_result, upsert_answer_key

DEFENCE_FEEDS = [
    "https://feeds.feedburner.com/freejobalert/defence-jobs",
    "https://feeds.feedburner.com/freejobalert"
]

CURATED_DEFENCE_DATA = [
    # ARMY
    {
        "type": "job",
        "title": "Indian Army Agniveer General Duty (GD), Technical & Tradesmen Rally 2026",
        "organization": "Indian Army (Join Indian Army)",
        "org_logo": "defence",
        "category": "Defence",
        "vacancies": "25,000+",
        "qualification": "10th Pass (45% Aggregate) / 8th Pass for Tradesmen",
        "salary": "Seva Nidhi Package (Rs. 30,000 - 40,000/- pm + Rs. 11.71 Lakh)",
        "last_date": "22 Mar 2026",
        "link": "https://joinindianarmy.nic.in"
    },
    {
        "type": "job",
        "title": "Indian Army Technical Graduate Course (TGC-141) Jan 2026",
        "organization": "Indian Army (Join Indian Army)",
        "org_logo": "defence",
        "category": "Defence",
        "vacancies": "30+",
        "qualification": "B.E / B.Tech in relevant Engineering Stream",
        "salary": "Lieutenant Rank (Level 10: Rs. 56,100 - 1,77,500/-)",
        "last_date": "09 May 2026",
        "link": "https://joinindianarmy.nic.in"
    },
    # NAVY
    {
        "type": "job",
        "title": "Indian Navy Agniveer (SSR & MR) 02/2026 Batch Recruitment",
        "organization": "Indian Navy (Join Indian Navy)",
        "org_logo": "defence",
        "category": "Defence",
        "vacancies": "4,200+",
        "qualification": "10+2 with Math & Physics (SSR) / 10th Pass (MR)",
        "salary": "Seva Nidhi Package (Rs. 30,000 - 40,000/- pm + Benefits)",
        "last_date": "05 Jun 2026",
        "link": "https://joinindiannavy.gov.in"
    },
    {
        "type": "job",
        "title": "Indian Navy Officers (Short Service Commission SSC) Entry 2026",
        "organization": "Indian Navy (Join Indian Navy)",
        "org_logo": "defence",
        "category": "Defence",
        "vacancies": "250+",
        "qualification": "B.E / B.Tech / M.Sc / MCA with minimum 60% marks",
        "salary": "Sub Lieutenant (Level 10: Rs. 56,100/- + MSP)",
        "last_date": "29 Oct 2026",
        "link": "https://joinindiannavy.gov.in"
    },
    # AIR FORCE
    {
        "type": "job",
        "title": "Air Force AFCAT 02/2026 Flying & Ground Duty (Technical & Non-Tech) Branches",
        "organization": "Indian Air Force (IAF)",
        "org_logo": "defence",
        "category": "Defence",
        "vacancies": "317+",
        "qualification": "Graduate Degree (Min 60%) / B.E/B.Tech for Technical Branch",
        "salary": "Flying Officer Rank (Rs. 56,100 - 1,77,500/- + Flying Allowance)",
        "last_date": "30 Sep 2026",
        "link": "https://afcat.cdac.in"
    },
    {
        "type": "job",
        "title": "Indian Air Force Agniveervayu (Musician / Intake 01/2026)",
        "organization": "Indian Air Force (IAF)",
        "org_logo": "defence",
        "category": "Defence",
        "vacancies": "3,500+",
        "qualification": "10+2 Intermediate (Science or Other Streams) / 10th for Musician",
        "salary": "Agniveer Seva Nidhi Package (Rs. 30,000 - 40,000/- pm)",
        "last_date": "11 Feb 2026",
        "link": "https://agnipathvayu.cdac.in"
    },
    {
        "type": "admit_card",
        "exam_name": "Indian Air Force AFCAT 02/2026 Online Exam Admit Card",
        "organization": "Indian Air Force (IAF)",
        "release_date": "Live Now",
        "exam_date": "20 - 22 Sep 2026",
        "category": "Defence",
        "status": "Available Now",
        "link": "https://afcat.cdac.in"
    },
    {
        "type": "admit_card",
        "exam_name": "Indian Army Agniveer CEE Rally Admit Card & Call Letter",
        "organization": "Indian Army",
        "release_date": "Available",
        "exam_date": "Rally Schedule 2026",
        "category": "Defence",
        "status": "Download Hall Ticket",
        "link": "https://joinindianarmy.nic.in"
    },
    {
        "type": "result",
        "exam_name": "Indian Navy Agniveer (SSR/MR) Stage-1 Computer Examination Result",
        "organization": "Indian Navy",
        "result_date": "Declared",
        "exam_stage": "Stage-1 INET",
        "status": "Merit List Live",
        "link": "https://joinindiannavy.gov.in"
    }
]

def scrape_defence():
    print("⚡ [Scraper] Initiating Indian Armed Forces (Army, Navy, Air Force) Ingestion...")
    jobs_count = 0
    admit_count = 0
    result_count = 0
    key_count = 0

    for item in CURATED_DEFENCE_DATA:
        if item["type"] == "job":
            if upsert_job(item): jobs_count += 1
        elif item["type"] == "admit_card":
            if upsert_admit_card(item): admit_count += 1
        elif item["type"] == "result":
            if upsert_result(item): result_count += 1

    for feed_url in DEFENCE_FEEDS:
        items = fetch_feed_items(feed_url, max_items=25)
        for it in items:
            t_lower = it["title"].lower()
            if not any(k in t_lower for k in ["army", "navy", "air force", "airforce", "afcat", "agniveer", "defence", "drdo"]):
                continue

            # Determine Specific Branch
            org = "Indian Armed Forces"
            if "army" in t_lower: org = "Indian Army (Join Indian Army)"
            elif "navy" in t_lower: org = "Indian Navy (Join Indian Navy)"
            elif "air force" in t_lower or "airforce" in t_lower or "afcat" in t_lower: org = "Indian Air Force (IAF)"

            if any(k in t_lower for k in ["admit", "call letter", "hall ticket"]):
                if upsert_admit_card({
                    "exam_name": it["title"],
                    "organization": org,
                    "category": "Defence",
                    "link": it["link"]
                }): admit_count += 1
            elif any(k in t_lower for k in ["result", "merit", "selection list"]):
                if upsert_result({
                    "exam_name": it["title"],
                    "organization": org,
                    "link": it["link"]
                }): result_count += 1
            else:
                if upsert_job({
                    "title": it["title"],
                    "organization": org,
                    "org_logo": "defence",
                    "category": "Defence",
                    "desc": it["desc"],
                    "link": it["link"]
                }): jobs_count += 1

    print(f"✅ Defence Ingestion: {jobs_count} Jobs, {admit_count} Admit Cards, {result_count} Results.")
    return {"department": "Defence (Army/Navy/Air Force)", "jobs": jobs_count, "admit_cards": admit_count, "results": result_count, "answer_keys": key_count}
