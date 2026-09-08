#!/usr/bin/env python3
"""
JobVani - Production Local Server Launcher
Starts FastAPI with Uvicorn and automatically launches default browser.
"""

import sys
import os
import webbrowser
import time
import socket

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add backend directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
sys.path.insert(0, BACKEND_DIR)

import database
import seed_data

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def find_available_port(start_port=8000):
    for p in range(start_port, start_port + 20):
        if not is_port_in_use(p):
            return p
    return 8000

def main():
    print("=" * 65)
    print("🇮🇳 JOBVANI — SARKARI NAUKRI, SEEDHI BAAT")
    print("India's Trusted Government Job Portal")
    print("=" * 65)

    # Check and initialize database
    db_path = os.path.join(BASE_DIR, "jobvani.db")
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        print("Initializing database and seeding 2026 authentic recruitments...")
        seed_data.seed_all()
    else:
        print("Database detected: jobvani.db is ready.")

    port = find_available_port(8000)
    url = f"http://127.0.0.1:{port}"

    print(f"\n🚀 Server running at: {url}")
    print(f"📖 API Documentation: {url}/docs")
    print("⚡ Press Ctrl+C in this terminal to stop the server.\n")

    # Automatically open browser after 1 second
    import threading
    def open_browser():
        time.sleep(1.2)
        webbrowser.open(url)
    threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=port, app_dir=BACKEND_DIR, log_level="info")

if __name__ == "__main__":
    main()
