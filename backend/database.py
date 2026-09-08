"""
JobVani - Database Connection & Schema Setup
Uses SQLite (Free, zero configuration, production-grade local database)
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jobvani.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Jobs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        organization TEXT NOT NULL,
        org_logo TEXT,
        category TEXT NOT NULL,
        job_type TEXT NOT NULL,
        location TEXT DEFAULT 'All India',
        vacancies TEXT NOT NULL,
        qualification TEXT NOT NULL,
        age_limit TEXT,
        application_fee TEXT,
        posted_date TEXT NOT NULL,
        last_date TEXT NOT NULL,
        last_date_timestamp INTEGER NOT NULL,
        salary TEXT,
        selection_process TEXT,
        exam_pattern TEXT,
        syllabus_summary TEXT,
        how_to_apply TEXT,
        official_notification_url TEXT,
        official_apply_url TEXT,
        official_website_url TEXT,
        status_badge TEXT DEFAULT 'New',
        is_trending INTEGER DEFAULT 0,
        trending_score INTEGER DEFAULT 0,
        views_count INTEGER DEFAULT 0,
        apply_clicks INTEGER DEFAULT 0,
        is_pinned INTEGER DEFAULT 0,
        is_published INTEGER DEFAULT 1
    );
    """)

    # 2. Admit Cards Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admit_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        exam_name TEXT NOT NULL,
        organization TEXT NOT NULL,
        release_date TEXT NOT NULL,
        exam_date TEXT NOT NULL,
        category TEXT NOT NULL,
        status TEXT DEFAULT 'Available Now',
        download_url TEXT NOT NULL,
        official_website_url TEXT
    );
    """)

    # 3. Results Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        exam_name TEXT NOT NULL,
        organization TEXT NOT NULL,
        result_date TEXT NOT NULL,
        exam_stage TEXT NOT NULL,
        status TEXT DEFAULT 'Declared',
        view_result_url TEXT NOT NULL,
        official_website_url TEXT
    );
    """)

    # 4. Answer Keys Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answer_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        exam_name TEXT NOT NULL,
        organization TEXT NOT NULL,
        exam_date TEXT NOT NULL,
        release_date TEXT NOT NULL,
        challenge_window TEXT,
        download_url TEXT NOT NULL,
        official_notice_url TEXT
    );
    """)

    # 5. Syllabus Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS syllabus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        exam_name TEXT NOT NULL,
        category TEXT NOT NULL,
        overview TEXT NOT NULL,
        subjects TEXT NOT NULL,
        exam_pattern TEXT NOT NULL,
        detailed_syllabus TEXT NOT NULL,
        pdf_download_url TEXT
    );
    """)

    # 6. Current Affairs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS current_affairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        period TEXT DEFAULT 'Today',
        summary TEXT NOT NULL,
        content TEXT NOT NULL
    );
    """)

    # 7. Subscribers / Alerts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        subscribed_at TEXT NOT NULL
    );
    """)

    # 8. Bookmarks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        user_id TEXT DEFAULT 'guest',
        created_at TEXT NOT NULL,
        UNIQUE(job_id, user_id)
    );
    """)

    # 9. Trust Stats & Settings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)

    # Default settings
    cursor.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES ('active_jobs_stat', '1K+')")
    cursor.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES ('exam_categories_stat', '50+')")
    cursor.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES ('happy_users_stat', '10M+')")
    cursor.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES ('updated_info_stat', '100%')")
    cursor.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES ('closing_soon_days', '7')")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database schema successfully initialized at:", DB_PATH)
