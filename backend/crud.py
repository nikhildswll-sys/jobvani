"""
JobVani - Database CRUD Operations & Queries
"""

import time
from database import get_db_connection

def dict_from_row(row):
    return dict(row) if row else None

def list_from_rows(rows):
    return [dict(r) for r in rows]

def get_site_settings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM site_settings;")
    rows = cursor.fetchall()
    conn.close()
    return {r["key"]: r["value"] for r in rows}

def update_site_setting(key, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO site_settings (key, value) VALUES (?, ?);", (key, value))
    conn.commit()
    conn.close()

def get_jobs(category=None, qualification=None, job_type=None, sort_by="latest", limit=20, offset=0):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM jobs WHERE is_published = 1"
    params = []

    if category and category.lower() != "all" and category.lower() != "all jobs":
        query += " AND (LOWER(category) = LOWER(?) OR LOWER(job_type) = LOWER(?))"
        params.extend([category, category])

    if qualification and qualification.lower() != "all":
        query += " AND LOWER(qualification) LIKE ?"
        params.append(f"%{qualification.lower()}%")

    if job_type and job_type.lower() != "all":
        query += " AND LOWER(job_type) = LOWER(?)"
        params.append(job_type)

    if sort_by == "closing_soon":
        now = int(time.time())
        query += f" AND last_date_timestamp >= {now} ORDER BY last_date_timestamp ASC"
    elif sort_by == "trending":
        query += " ORDER BY is_trending DESC, trending_score DESC, views_count DESC"
    elif sort_by == "views":
        query += " ORDER BY views_count DESC"
    else: # latest
        query += " ORDER BY is_pinned DESC, id DESC"

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    jobs = list_from_rows(cursor.fetchall())
    conn.close()
    return jobs

def get_job_by_slug(slug):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE slug = ?;", (slug,))
    job = dict_from_row(cursor.fetchone())
    if job:
        cursor.execute("UPDATE jobs SET views_count = views_count + 1 WHERE id = ?;", (job["id"],))
        conn.commit()
    conn.close()
    return job

def get_trending_jobs(limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Dynamic trending score calculation: admin boost + views + apply clicks
    cursor.execute("""
    SELECT * FROM jobs 
    WHERE is_published = 1 
    ORDER BY is_pinned DESC, (is_trending * 50 + trending_score + (views_count / 500) + (apply_clicks / 100)) DESC 
    LIMIT ?;
    """, (limit,))
    rows = list_from_rows(cursor.fetchall())
    conn.close()
    return rows

def get_closing_soon_jobs(limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = int(time.time())
    # Jobs with deadlines in the future, sorted by nearest deadline
    cursor.execute("""
    SELECT *, ROUND((last_date_timestamp - ?) / 86400.0, 1) as days_remaining
    FROM jobs 
    WHERE is_published = 1 AND last_date_timestamp >= ?
    ORDER BY last_date_timestamp ASC 
    LIMIT ?;
    """, (now, now, limit))
    rows = list_from_rows(cursor.fetchall())
    conn.close()

    # Format days left human readable label
    for r in rows:
        days = r.get("days_remaining", 7)
        if days <= 1:
            r["urgency_badge"] = "Last Day!"
        else:
            r["urgency_badge"] = f"{int(round(days))} Days Left"
    return rows

def get_admit_cards(category=None, limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    if category and category.lower() != "all":
        cursor.execute("SELECT * FROM admit_cards WHERE LOWER(category) = LOWER(?) ORDER BY id DESC LIMIT ?;", (category, limit))
    else:
        cursor.execute("SELECT * FROM admit_cards ORDER BY id DESC LIMIT ?;", (limit,))
    rows = list_from_rows(cursor.fetchall())
    conn.close()
    return rows

def get_results(limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results ORDER BY id DESC LIMIT ?;", (limit,))
    rows = list_from_rows(cursor.fetchall())
    conn.close()
    return rows

def get_answer_keys(limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM answer_keys ORDER BY id DESC LIMIT ?;", (limit,))
    rows = list_from_rows(cursor.fetchall())
    conn.close()
    return rows

def get_syllabus(category=None, limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    if category and category.lower() != "all":
        cursor.execute("SELECT * FROM syllabus WHERE LOWER(category) = LOWER(?) ORDER BY id DESC LIMIT ?;", (category, limit))
    else:
        cursor.execute("SELECT * FROM syllabus ORDER BY id DESC LIMIT ?;", (limit,))
    rows = list_from_rows(cursor.fetchall())
    conn.close()
    return rows

def get_current_affairs(period=None, category=None, limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM current_affairs WHERE 1=1"
    params = []
    if period and period.lower() != "all":
        query += " AND LOWER(period) = LOWER(?)"
        params.append(period)
    if category and category.lower() != "all":
        query += " AND LOWER(category) = LOWER(?)"
        params.append(category)
    query += " ORDER BY id DESC LIMIT ?;"
    params.append(limit)
    cursor.execute(query, params)
    rows = list_from_rows(cursor.fetchall())
    conn.close()
    return rows

def global_search(query_str):
    conn = get_db_connection()
    cursor = conn.cursor()
    term = f"%{query_str.lower().strip()}%"

    cursor.execute("""
    SELECT 'job' as type, slug, title, organization as subtitle, last_date as meta, category 
    FROM jobs 
    WHERE LOWER(title) LIKE ? OR LOWER(organization) LIKE ? OR LOWER(category) LIKE ? OR LOWER(qualification) LIKE ?
    LIMIT 10;
    """, (term, term, term, term))
    jobs = list_from_rows(cursor.fetchall())

    cursor.execute("""
    SELECT 'admit_card' as type, slug, exam_name as title, organization as subtitle, exam_date as meta, category 
    FROM admit_cards 
    WHERE LOWER(exam_name) LIKE ? OR LOWER(organization) LIKE ?
    LIMIT 5;
    """, (term, term))
    admit_cards = list_from_rows(cursor.fetchall())

    cursor.execute("""
    SELECT 'result' as type, slug, exam_name as title, organization as subtitle, result_date as meta, exam_stage as category 
    FROM results 
    WHERE LOWER(exam_name) LIKE ? OR LOWER(organization) LIKE ?
    LIMIT 5;
    """, (term, term))
    results = list_from_rows(cursor.fetchall())

    conn.close()
    return {
        "jobs": jobs,
        "admit_cards": admit_cards,
        "results": results,
        "total_matches": len(jobs) + len(admit_cards) + len(results)
    }

def register_apply_click(job_id_or_slug):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET apply_clicks = apply_clicks + 1 WHERE id = ? OR slug = ?;", (job_id_or_slug, job_id_or_slug))
    conn.commit()
    conn.close()

def add_newsletter_subscriber(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("INSERT INTO subscribers (email, subscribed_at) VALUES (?, ?);", (email, now_str))
        conn.commit()
        success = True
    except Exception:
        success = False # already exists
    conn.close()
    return success

def toggle_user_bookmark(job_id, user_id="guest"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM bookmarks WHERE job_id = ? AND user_id = ?;", (job_id, user_id))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM bookmarks WHERE id = ?;", (existing["id"],))
        is_bookmarked = False
    else:
        cursor.execute("INSERT INTO bookmarks (job_id, user_id, created_at) VALUES (?, ?, ?);", (job_id, user_id, time.strftime("%Y-%m-%d %H:%M:%S")))
        is_bookmarked = True
    conn.commit()
    conn.close()
    return is_bookmarked

def get_user_bookmarks(user_id="guest"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT j.* FROM jobs j 
    JOIN bookmarks b ON j.id = b.job_id 
    WHERE b.user_id = ?
    ORDER BY b.id DESC;
    """, (user_id,))
    rows = list_from_rows(cursor.fetchall())
    conn.close()
    return rows
