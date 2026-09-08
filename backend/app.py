"""
JobVani - FastAPI Production Application
Serves REST APIs, Auto-Pilot Web Scraper runner, and responsive frontend templates.
"""

from fastapi import FastAPI, HTTPException, Request, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import time

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import database
import crud
import models
import scraper

# Initialize database on startup
database.init_db()

app = FastAPI(
    title="JobVani API",
    description="Production Indian Government Jobs Information & Automated Scraper Platform",
    version="2.0.0"
)

import asyncio

async def auto_scraper_loop():
    while True:
        try:
            await asyncio.sleep(4 * 3600) # Every 4 hours
            from scrapers.runner import run_all_scrapers
            run_all_scrapers()
        except Exception as e:
            print("Auto-scraper background cycle error:", e)

@app.on_event("startup")
def on_startup():
    asyncio.create_task(auto_scraper_loop())

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Helper to read index.html
def get_index_html():
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

# -------------------------------------------------------------
# REST API ENDPOINTS
# -------------------------------------------------------------

@app.get("/api/settings")
def get_settings():
    return crud.get_site_settings()

@app.post("/api/settings")
def update_settings(data: models.SettingsUpdate):
    for k, v in data.model_dump(exclude_unset=True).items():
        if v is not None:
            crud.update_site_setting(k, str(v))
    return {"status": "success", "settings": crud.get_site_settings()}

@app.get("/api/jobs")
def list_jobs(
    category: str = Query(None),
    qualification: str = Query(None),
    job_type: str = Query(None),
    sort: str = Query("latest"),
    limit: int = Query(24),
    offset: int = Query(0)
):
    return crud.get_jobs(category=category, qualification=qualification, job_type=job_type, sort_by=sort, limit=limit, offset=offset)

@app.get("/api/jobs/{slug}")
def get_job_detail(slug: str):
    job = crud.get_job_by_slug(slug)
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return job

@app.post("/api/jobs")
def create_job(data: models.JobCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    slug = scraper.slugify(data.title)
    cursor.execute("""
    INSERT INTO jobs (
        slug, title, organization, org_logo, category, job_type, location,
        vacancies, qualification, age_limit, application_fee, posted_date,
        last_date, last_date_timestamp, salary, selection_process, exam_pattern,
        syllabus_summary, how_to_apply, official_notification_url, official_apply_url,
        official_website_url, status_badge, is_trending, trending_score
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?,
        ?, ?, ?, ?
    );
    """, (
        slug, data.title, data.organization, data.org_logo or "central_govt", data.category, data.job_type, data.location,
        data.vacancies, data.qualification, data.age_limit, data.application_fee, data.posted_date,
        data.last_date, int(time.time()) + (30 * 86400), data.salary, data.selection_process, data.exam_pattern,
        data.syllabus_summary, data.how_to_apply, data.official_notification_url, data.official_apply_url,
        data.official_website_url, data.status_badge, data.is_trending, data.trending_score
    ))
    conn.commit()
    conn.close()
    return {"status": "created", "slug": slug}

@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = ?;", (job_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted", "job_id": job_id}

@app.get("/api/trending")
def get_trending():
    return crud.get_trending_jobs(limit=5)

@app.get("/api/closing-soon")
def get_closing_soon():
    return crud.get_closing_soon_jobs(limit=5)


@app.post("/api/admit-cards")
def create_admit_card(data: dict):
    conn = database.get_db_connection()
    c = conn.cursor()
    slug = scraper.slugify(data.get("exam_name", ""))
    c.execute("""
    INSERT INTO admit_cards (slug, exam_name, organization, release_date, exam_date, category, status, download_url, official_website_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (slug, data.get("exam_name"), data.get("organization"), data.get("release_date", "Today"), data.get("exam_date", "Announced Soon"), data.get("category", "General"), data.get("status", "Available Now"), data.get("download_url"), data.get("official_website_url")))
    conn.commit()
    conn.close()
    return {"status": "created"}

@app.delete("/api/admit-cards/{item_id}")
def delete_admit_card(item_id: int):
    conn = database.get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM admit_cards WHERE id = ?;", (item_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

@app.post("/api/results")
def create_result(data: dict):
    conn = database.get_db_connection()
    c = conn.cursor()
    slug = scraper.slugify(data.get("exam_name", ""))
    c.execute("""
    INSERT INTO results (slug, exam_name, organization, result_date, exam_stage, status, view_result_url, official_website_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (slug, data.get("exam_name"), data.get("organization"), data.get("result_date", "Today"), data.get("exam_stage", "Final"), data.get("status", "Declared"), data.get("view_result_url"), data.get("official_website_url")))
    conn.commit()
    conn.close()
    return {"status": "created"}

@app.delete("/api/results/{item_id}")
def delete_result(item_id: int):
    conn = database.get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM results WHERE id = ?;", (item_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

@app.get("/api/admit-cards")
def get_admit_cards(category: str = Query(None)):
    return crud.get_admit_cards(category=category, limit=20)

@app.get("/api/results")
def get_results():
    return crud.get_results(limit=20)

@app.get("/api/answer-keys")
def get_answer_keys():
    return crud.get_answer_keys(limit=20)

@app.get("/api/syllabus")
def get_syllabus(category: str = Query(None)):
    return crud.get_syllabus(category=category, limit=20)

@app.get("/api/current-affairs")
def get_current_affairs(period: str = Query(None), category: str = Query(None)):
    return crud.get_current_affairs(period=period, category=category, limit=20)

@app.get("/api/search")
def search(q: str = Query("..")):
    return crud.global_search(q)

@app.post("/api/jobs/{slug}/apply-click")
def track_apply_click(slug: str):
    crud.register_apply_click(slug)
    return {"status": "recorded"}

@app.post("/api/bookmarks/toggle")
def toggle_bookmark(data: models.BookmarkToggle):
    is_saved = crud.toggle_user_bookmark(data.job_id, data.user_id)
    return {"status": "success", "is_bookmarked": is_saved}

@app.get("/api/bookmarks")
def get_bookmarks(user_id: str = "guest"):
    return crud.get_user_bookmarks(user_id)

@app.post("/api/subscribe")
def subscribe_newsletter(data: models.SubscriberCreate):
    success = crud.add_newsletter_subscriber(data.email)
    return {"status": "success" if success else "already_subscribed"}

# -------------------------------------------------------------
# AUTO-PILOT SCRAPER TRIGGER
# -------------------------------------------------------------
@app.post("/api/scraper/run")
def trigger_scraper(department: str = Query(None)):
    if department:
        from scrapers.runner import run_department_scraper
        return run_department_scraper(department)
    from scrapers.runner import run_all_scrapers
    return run_all_scrapers()

# -------------------------------------------------------------
# ADMIN OVERVIEW & STATS
# -------------------------------------------------------------
@app.get("/api/admin/overview")
def admin_overview():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM jobs;")
    total_jobs = cursor.fetchone()["count"]
    cursor.execute("SELECT SUM(views_count) as total_views, SUM(apply_clicks) as total_clicks FROM jobs;")
    stats_row = cursor.fetchone()
    total_views = stats_row["total_views"] or 0
    total_clicks = stats_row["total_clicks"] or 0
    cursor.execute("SELECT COUNT(*) as count FROM subscribers;")
    total_subscribers = cursor.fetchone()["count"]
    conn.close()

    return {
        "total_jobs": total_jobs,
        "total_views": total_views,
        "total_clicks": total_clicks,
        "total_subscribers": total_subscribers,
        "active_jobs_stat": crud.get_site_settings().get("active_jobs_stat", "1K+")
    }

# -------------------------------------------------------------
# SEO & SITEMAP ROUTES
# -------------------------------------------------------------
@app.get("/robots.txt", response_class=Response)
def robots():
    content = "User-agent: *\nAllow: /\nSitemap: https://jobvani.in/sitemap.xml\n"
    return Response(content=content, media_type="text/plain")

@app.get("/sitemap.xml", response_class=Response)
def sitemap():
    jobs = crud.get_jobs(limit=100)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    xml.append('  <url><loc>https://jobvani.in/</loc><priority>1.0</priority><changefreq>hourly</changefreq></url>')
    xml.append('  <url><loc>https://jobvani.in/admit-card</loc><priority>0.9</priority></url>')
    xml.append('  <url><loc>https://jobvani.in/results</loc><priority>0.9</priority></url>')
    xml.append('  <url><loc>https://jobvani.in/answer-key</loc><priority>0.8</priority></url>')
    xml.append('  <url><loc>https://jobvani.in/syllabus</loc><priority>0.8</priority></url>')
    xml.append('  <url><loc>https://jobvani.in/current-affairs</loc><priority>0.8</priority></url>')
    for j in jobs:
        xml.append(f'  <url><loc>https://jobvani.in/jobs/{j["slug"]}</loc><priority>0.85</priority><changefreq>daily</changefreq></url>')
    xml.append('</urlset>')
    return Response(content="\n".join(xml), media_type="application/xml")

# -------------------------------------------------------------
# FRONTEND HTML ENTRYPOINTS (SPA ROUTING)
# -------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
@app.get("/jobs/{slug}", response_class=HTMLResponse)
@app.get("/admit-card", response_class=HTMLResponse)
@app.get("/results", response_class=HTMLResponse)
@app.get("/answer-key", response_class=HTMLResponse)
@app.get("/syllabus", response_class=HTMLResponse)
@app.get("/current-affairs", response_class=HTMLResponse)
@app.get("/admin", response_class=HTMLResponse)
def serve_spa(request: Request):
    return HTMLResponse(content=get_index_html())
