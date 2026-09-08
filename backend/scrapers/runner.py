"""
JobVani Scraper - Master Orchestration Runner
Runs department-specific scrapers (SSC, UPSC, Railway, Defence/Army/Navy/AirForce, Police, All India)
or executes all in parallel with aggregate status reports.
"""

from .ssc import scrape_ssc
from .upsc import scrape_upsc
from .railway import scrape_railway
from .defence import scrape_defence
from .police import scrape_police
from .all_india import scrape_all_india

SCRAPER_REGISTRY = {
    "ssc": scrape_ssc,
    "upsc": scrape_upsc,
    "railway": scrape_railway,
    "defence": scrape_defence,
    "army": scrape_defence,
    "navy": scrape_defence,
    "airforce": scrape_defence,
    "police": scrape_police,
    "all_india": scrape_all_india
}

def run_department_scraper(dept_name):
    key = dept_name.lower().strip()
    handler = SCRAPER_REGISTRY.get(key)
    if not handler:
        return {"status": "error", "message": f"Unknown department: {dept_name}. Supported: {list(SCRAPER_REGISTRY.keys())}"}
    return handler()

def run_all_scrapers():
    print("====================================================================")
    print("🚀 JOBVANI MASTER SCRAPER: Running all India Government Sectors...")
    print("   [1] SSC (CGL, CHSL, MTS, GD, CPO)")
    print("   [2] UPSC (Civil Services, NDA, CDS)")
    print("   [3] Railways (RRB NTPC, ALP, Group D, RPF)")
    print("   [4] Defence (Indian Army, Indian Navy, Indian Air Force)")
    print("   [5] Police (Delhi, UP, Bihar, State Police)")
    print("   [6] All India (Banking IBPS/SBI, ISRO, DRDO, Postal GDS)")
    print("====================================================================")

    reports = []
    total_jobs = 0
    total_admits = 0
    total_results = 0
    total_keys = 0

    functions = [
        scrape_ssc,
        scrape_upsc,
        scrape_railway,
        scrape_defence,
        scrape_police,
        scrape_all_india
    ]

    for fn in functions:
        try:
            res = fn()
            reports.append(res)
            total_jobs += res.get("jobs", 0)
            total_admits += res.get("admit_cards", 0)
            total_results += res.get("results", 0)
            total_keys += res.get("answer_keys", 0)
        except Exception as e:
            print(f"Error executing scraper {fn.__name__}: {e}")

    summary = {
        "status": "success",
        "total_new_jobs": total_jobs,
        "total_new_admit_cards": total_admits,
        "total_new_results": total_results,
        "total_new_answer_keys": total_keys,
        "department_reports": reports
    }

    print("====================================================================")
    print(f"🎉 MASTER INGESTION FINISHED!")
    print(f"   Total Added -> Jobs: {total_jobs}, Admit Cards: {total_admits}, Results: {total_results}, Answer Keys: {total_keys}")
    print("====================================================================")
    return summary

if __name__ == "__main__":
    run_all_scrapers()
