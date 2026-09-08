# JobVani — "Sarkari Naukri, Seedhi Baat." 🇮🇳

An Apple-inspired, production-ready Indian government jobs information portal built with **FastAPI + SQLite + Automated Web Scraper**.

---

## ✨ Key Features

1. **Apple-Inspired Minimal Design**:
   - Matches the uploaded reference design (`media_1788844682460.jpg`) down to spacing, subtle shadows, and rounded cards.
   - Clean color scheme: White, off-white, soft blue gradient tints, and dark navy typography.
   - Responsive across mobile phones, tablets, laptops, and desktops.

2. **100% Automated Scraping (Zero Manual Posting)**:
   - `backend/scraper.py` connects to public government recruitment feeds and auto-ingests new vacancies, admit cards, and results directly into SQLite.
   - You don't have to manually post anything!
   - Can also be triggered anytime with 1-click inside the Admin Dashboard (`#admin`).

3. **₹0 Budget / 100% Free**:
   - Zero paid subscriptions or third-party APIs required.
   - Runs locally using Python and SQLite.
   - Can be deployed online for free on platforms like Render, Vercel, or PythonAnywhere.

4. **Comprehensive Exam Support**:
   - **Trending Jobs**: Real-time trending score calculation based on views, clicks, and recency.
   - **Closing Soon**: Live countdown badges (`2 Days Left`, `4 Days Left`, etc.) with automatic expiry tracking.
   - **Detailed Job Pages**: Important dates, eligibility, age limit, application fees, selection process, syllabus summary, and official notification PDF links.
   - **Admit Cards, Results, Answer Keys & Syllabus**: Dedicated views for every stage of government recruitments.
   - **Admin Command Center**: View analytics (views, apply clicks, subscriber counts) and manage listings.

---

## 🚀 How to Run Locally

In your terminal or PowerShell, run:
```powershell
python C:\Users\NIKIL\.gemini\antigravity\scratch\jobvani\start_server.py
```
This automatically starts the server and opens `http://127.0.0.1:8000` in your default browser.

---

## 🛠️ Auto-Pilot Scraper Usage

To run the scraper from the command line:
```powershell
python C:\Users\NIKIL\.gemini\antigravity\scratch\jobvani\backend\scraper.py
```
Or simply click the **"Run Auto-Pilot Scraper"** button inside the Admin Dashboard at `http://127.0.0.1:8000/#admin`.
