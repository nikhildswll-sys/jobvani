"""
JobVani Scraper Framework - Base Engine
Provides shared extraction, regex normalization, and SQLite upserting tools.
"""

import httpx
import re
import time
import os
import sys
import xml.etree.ElementTree as ET
from database import get_db_connection

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 JobVaniBot/2.0"
}

def clean_html(raw_html):
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]+>', '', raw_html)
    clean = clean.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    return re.sub(r'\s+', ' ', clean).strip()

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '-', text)[:80]

def parse_deadline(text):
    now = int(time.time())
    day_sec = 86400
    date_match = re.search(r'(\d{1,2})[-/\s]([A-Za-z]{3}|\d{1,2})[-/\s](\d{4})', text)
    if date_match:
        try:
            return text[date_match.start():date_match.end()], now + (25 * day_sec)
        except Exception:
            pass
    return "30 Days from Notice", now + (30 * day_sec)

def extract_vacancies(text):
    m = re.search(r'(\d[\d,]*)\s*(?:posts|vacancies|seats|positions|various)', text, re.I)
    if m:
        return m.group(1).replace(',', '') + '+'
    return "Various Posts"

def extract_qualification(text):
    t = text.lower()
    if "b.e" in t or "b.tech" in t or "engineering" in t:
        return "B.E / B.Tech"
    elif "post graduate" in t or "pg" in t or "m.sc" in t or "m.tech" in t:
        return "Post Graduate"
    elif "graduate" in t or "degree" in t or "b.a" in t or "b.sc" in t or "b.com" in t:
        return "Bachelor's Degree"
    elif "12th" in t or "intermediate" in t or "10+2" in t:
        return "12th Pass (10+2)"
    elif "10th" in t or "matric" in t or "high school" in t:
        return "10th Pass (Matric)"
    elif "iti" in t or "diploma" in t:
        return "Diploma / ITI"
    return "10th / 12th / Graduate"

def fetch_feed_items(feed_url, max_items=25):
    items_data = []
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True, headers=HEADERS) as client:
            res = client.get(feed_url)
            if res.status_code == 200:
                root = ET.fromstring(res.text)
                elements = root.findall(".//item")
                for el in elements[:max_items]:
                    t = el.find("title")
                    l = el.find("link")
                    d = el.find("description")
                    title = clean_html(t.text if t is not None else "")
                    link = l.text.strip() if l is not None and l.text else "https://jobvani.in"
                    desc = clean_html(d.text if d is not None else "")
                    if title and len(title) > 5:
                        items_data.append({"title": title, "link": link, "desc": desc})
    except Exception as e:
        print(f"Notice: Feed fetch from {feed_url} encountered: {e}")
    return items_data

def sanitize_url(url, fallback="https://india.gov.in"):
    if not url or not isinstance(url, str):
        return fallback
    u = url.strip()
    if not u or u == "#":
        return fallback
    # If it's a raw PDF on FreeJobAlert CDN, route through our internal proxy so user stays on JobVani
    if "freejobalert.com" in u.lower() and u.lower().endswith(".pdf"):
        return f"/api/pdf-stream?url={u}"
    # Strictly reject any freejobalert webpage, portal or social media links
    if any(k in u.lower() for k in ["freejobalert.com", "t.me", "telegram", "whatsapp", "arattai", "instagram", "facebook", "twitter", "play.google", "slate."]):
        return fallback
    if not (u.startswith("http://") or u.startswith("https://") or u.startswith("/")):
        return fallback
    return u

def upsert_job(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    slug = slugify(data["title"])
    cursor.execute("SELECT id FROM jobs WHERE slug = ?", (slug,))
    if cursor.fetchone():
        conn.close()
        return False # Already exists

    last_date_str, last_date_ts = parse_deadline(data.get("last_date", data.get("desc", "")))
    
    official_website = sanitize_url(data.get("official_website_url"), fallback="https://india.gov.in")
    official_notification = sanitize_url(data.get("official_notification_url"), fallback=official_website)
    official_apply = sanitize_url(data.get("official_apply_url"), fallback=official_website)

    cursor.execute("""
    INSERT INTO jobs (
        slug, title, organization, org_logo, category, job_type, location,
        vacancies, qualification, age_limit, application_fee, posted_date,
        last_date, last_date_timestamp, salary, selection_process, exam_pattern,
        syllabus_summary, how_to_apply, official_notification_url, official_apply_url,
        official_website_url, status_badge, is_trending, trending_score, views_count, apply_clicks
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?
    );
    """, (
        slug, data["title"], data.get("organization", "Government of India"), data.get("org_logo", "central_govt"),
        data.get("category", "Central Government"), data.get("job_type", "Central"), data.get("location", "All India"),
        data.get("vacancies", extract_vacancies(data["title"] + " " + data.get("desc", ""))),
        data.get("qualification", extract_qualification(data["title"] + " " + data.get("desc", ""))),
        data.get("age_limit", data.get("age", "18-27/30 Years (Relaxation Applicable)")),
        data.get("application_fee", "Gen/OBC: Rs. 100/- | SC/ST/Female: Rs. 0/- Exempted"),
        data.get("posted_date", "Today"),
        last_date_str, last_date_ts,
        data.get("salary", data.get("pay_scale", "7th CPC Pay Matrix (Level 4 to 8)")),
        data.get("selection_process", "CBT Tier-I, Tier-II, Skill Test, DV & Medical"),
        data.get("exam_pattern", "General Awareness, Reasoning, Quantitative Aptitude & English"),
        data.get("syllabus_summary", "Detailed syllabus as prescribed in official gazette notification."),
        data.get("how_to_apply", "Apply online through the official department web portal before the closing date."),
        official_notification,
        official_apply,
        official_website,
        data.get("status_badge", "New"),
        data.get("is_trending", 1),
        data.get("trending_score", 85),
        data.get("views_count", 240),
        data.get("apply_clicks", 42)
    ))
    conn.commit()
    conn.close()
    return True

def upsert_admit_card(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    slug = slugify(data["exam_name"])
    cursor.execute("SELECT id FROM admit_cards WHERE slug = ?", (slug,))
    if cursor.fetchone():
        conn.close()
        return False
        
    official_website = sanitize_url(data.get("official_website_url"), fallback="https://india.gov.in")
    download_url = sanitize_url(data.get("download_url"), fallback=official_website)

    cursor.execute("""
    INSERT INTO admit_cards (slug, exam_name, organization, release_date, exam_date, category, status, download_url, official_website_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        slug, data["exam_name"], data.get("organization", "Government Authority"),
        data.get("release_date", "Live Now"), data.get("exam_date", "Check Notice"),
        data.get("category", "General"), data.get("status", "Available Now"),
        download_url,
        official_website
    ))
    conn.commit()
    conn.close()
    return True

def upsert_result(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    slug = slugify(data["exam_name"])
    cursor.execute("SELECT id FROM results WHERE slug = ?", (slug,))
    if cursor.fetchone():
        conn.close()
        return False

    official_website = sanitize_url(data.get("official_website_url"), fallback="https://india.gov.in")
    view_result = sanitize_url(data.get("view_result_url"), fallback=official_website)

    cursor.execute("""
    INSERT INTO results (slug, exam_name, organization, result_date, exam_stage, status, view_result_url, official_website_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        slug, data["exam_name"], data.get("organization", "Government Authority"),
        data.get("result_date", "Declared Today"), data.get("exam_stage", "Final Selection"),
        data.get("status", "Declared (PDF)"),
        view_result,
        official_website
    ))
    conn.commit()
    conn.close()
    return True

def upsert_answer_key(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    slug = slugify(data["exam_name"])
    cursor.execute("SELECT id FROM answer_keys WHERE slug = ?", (slug,))
    if cursor.fetchone():
        conn.close()
        return False

    official_notice = sanitize_url(data.get("official_notice_url"), fallback="https://india.gov.in")
    download_url = sanitize_url(data.get("download_url"), fallback=official_notice)

    cursor.execute("""
    INSERT INTO answer_keys (slug, exam_name, organization, exam_date, release_date, challenge_window, download_url, official_notice_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        slug, data["exam_name"], data.get("organization", "Government Authority"),
        data.get("exam_date", "Recent"), data.get("release_date", "Available Now"),
        data.get("challenge_window", "Objection Window Active"),
        download_url,
        official_notice
    ))
    conn.commit()
    conn.close()
    return True
