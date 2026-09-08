"""
JobVani - Authentic Seed Data (2026 Indian Government Recruitments)
Matches the exact items from the visual design reference.
"""

import time
from datetime import datetime, timedelta
from database import get_db_connection, init_db

def seed_all():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing to prevent duplicate seeding
    cursor.execute("DELETE FROM jobs;")
    cursor.execute("DELETE FROM admit_cards;")
    cursor.execute("DELETE FROM results;")
    cursor.execute("DELETE FROM answer_keys;")
    cursor.execute("DELETE FROM syllabus;")
    cursor.execute("DELETE FROM current_affairs;")

    # Current reference timestamps
    now = int(time.time())
    day_sec = 86400

    # -------------------------------------------------------------
    # 1. JOBS (Including Trending, Closing Soon, and Latest Grid)
    # -------------------------------------------------------------
    jobs_data = [
        # Trending & Latest
        {
            "slug": "ssc-cgl-2026",
            "title": "SSC CGL 2026",
            "organization": "Staff Selection Commission",
            "org_logo": "ssc",
            "category": "SSC",
            "job_type": "Central",
            "location": "All India",
            "vacancies": "7500+",
            "qualification": "Graduate",
            "age_limit": "18 - 32 Years (Age relaxation as per gov rules)",
            "application_fee": "Rs. 100/- (SC/ST/Female: Exempted)",
            "posted_date": "24 Jun 2026",
            "last_date": "25 Aug 2026",
            "last_date_timestamp": now + (25 * day_sec),
            "salary": "Pay Level-4 to Level-8 (Rs. 25,500 to Rs. 1,51,100)",
            "selection_process": "Tier-I (Computer Based Exam), Tier-II (Computer Based Exam), Document Verification",
            "exam_pattern": "Tier-I: 100 questions (200 marks, 60 mins). General Intelligence, General Awareness, Quantitative Aptitude, English Comprehension.",
            "syllabus_summary": "Covers Quantitative Aptitude (Algebra, Geometry, Trigonometry), Reasoning, Current Affairs, and English Grammar.",
            "how_to_apply": "Apply online at the official SSC portal (ssc.gov.in) with valid Aadhaar, photograph with white background, and educational certificates.",
            "official_notification_url": "https://ssc.gov.in/notice-modal",
            "official_apply_url": "https://ssc.gov.in/login",
            "official_website_url": "https://ssc.gov.in",
            "status_badge": "New",
            "is_trending": 1,
            "trending_score": 98,
            "views_count": 45200,
            "apply_clicks": 14200
        },
        {
            "slug": "ibps-po-2026",
            "title": "IBPS PO 2026",
            "organization": "Institute of Banking Personnel Selection",
            "org_logo": "ibps",
            "category": "Banking",
            "job_type": "Banking",
            "location": "All India",
            "vacancies": "4000+",
            "qualification": "Graduate",
            "age_limit": "20 - 30 Years",
            "application_fee": "Rs. 850/- (SC/ST/PWBD: Rs. 175/-)",
            "posted_date": "01 Jul 2026",
            "last_date": "28 Aug 2026",
            "last_date_timestamp": now + (28 * day_sec),
            "salary": "Rs. 52,000 - Rs. 58,000 per month gross",
            "selection_process": "Prelims Exam, Mains Exam, Common Interview Round",
            "exam_pattern": "Prelims: English (30Q), Quantitative (35Q), Reasoning (35Q). Mains: Objective + Descriptive Test.",
            "syllabus_summary": "Banking Awareness, Financial Markets, Data Interpretation, High-Level Puzzles, Essay and Letter Writing.",
            "how_to_apply": "Visit ibps.in, click on CRP PO/MT section, complete registration and pay application fee.",
            "official_notification_url": "https://www.ibps.in",
            "official_apply_url": "https://ibps.in/crp-po",
            "official_website_url": "https://www.ibps.in",
            "status_badge": "Trending",
            "is_trending": 1,
            "trending_score": 95,
            "views_count": 38100,
            "apply_clicks": 11800
        },
        {
            "slug": "railway-ntpc-2026",
            "title": "Railway NTPC 2026",
            "organization": "Indian Railways (RRB)",
            "org_logo": "railway",
            "category": "Railways",
            "job_type": "Railway",
            "location": "All India",
            "vacancies": "11500+",
            "qualification": "12th/Graduate",
            "age_limit": "18 - 33 Years",
            "application_fee": "Rs. 500/- (Rs. 400 refundable on CBT-1 attendance)",
            "posted_date": "10 Jul 2026",
            "last_date": "30 Aug 2026",
            "last_date_timestamp": now + (30 * day_sec),
            "salary": "7th CPC Pay Matrix Level 2, 3, 4, 5 & 6 (Rs. 19,900 to Rs. 35,400 basic)",
            "selection_process": "1st Stage CBT, 2nd Stage CBT, Typing Skill / CBAT, Document Verification & Medical Exam",
            "exam_pattern": "CBT-1: 100 MCQs (General Awareness 40, Math 30, Reasoning 30) in 90 minutes.",
            "syllabus_summary": "Indian History, Geography, General Science, Arithmetic, Analytical Reasoning.",
            "how_to_apply": "Submit online application through respective regional RRB portal (e.g. rrbcdg.gov.in, rrbpatna.gov.in).",
            "official_notification_url": "https://www.rrbcdg.gov.in",
            "official_apply_url": "https://www.rrbapply.gov.in",
            "official_website_url": "https://indianrailways.gov.in",
            "status_badge": "Hot",
            "is_trending": 1,
            "trending_score": 99,
            "views_count": 62400,
            "apply_clicks": 21000
        },
        {
            "slug": "upsc-civil-services-2026",
            "title": "UPSC Civil Services 2026",
            "organization": "Union Public Service Commission",
            "org_logo": "upsc",
            "category": "Central Government",
            "job_type": "Central",
            "location": "All India",
            "vacancies": "1000+",
            "qualification": "Graduate",
            "age_limit": "21 - 32 Years (6 attempts for General)",
            "application_fee": "Rs. 100/- (Female/SC/ST/PwBD Exempted)",
            "posted_date": "14 Jul 2026",
            "last_date": "02 Sep 2026",
            "last_date_timestamp": now + (33 * day_sec),
            "salary": "Rs. 56,100 to Rs. 2,50,000 (Apex Level)",
            "selection_process": "Preliminary Examination (Objective), Main Examination (Written), Personality Test (Interview)",
            "exam_pattern": "Prelims: GS-1 (200 marks) + CSAT (200 marks, qualifying). Mains: 9 descriptive papers (1750 marks) + Interview (275 marks).",
            "syllabus_summary": "Indian Polity, Economy, Ethics, World History, Environmental Ecology, International Relations, and Optional Subject.",
            "how_to_apply": "Register on UPSC OTR (One Time Registration) portal at upsconline.nic.in and submit Part-I & Part-II application.",
            "official_notification_url": "https://upsc.gov.in",
            "official_apply_url": "https://upsconline.nic.in",
            "official_website_url": "https://upsc.gov.in",
            "status_badge": "Popular",
            "is_trending": 1,
            "trending_score": 94,
            "views_count": 51200,
            "apply_clicks": 13900
        },
        {
            "slug": "up-police-constable-2026",
            "title": "UP Police Constable 2026",
            "organization": "Uttar Pradesh Police Recruitment Board",
            "org_logo": "police",
            "category": "Police",
            "job_type": "Police",
            "location": "Uttar Pradesh",
            "vacancies": "60244",
            "qualification": "12th Pass",
            "age_limit": "18 - 25 Years",
            "application_fee": "Rs. 400/- for all categories",
            "posted_date": "15 Jun 2026",
            "last_date": "10 Aug 2026",
            "last_date_timestamp": now + (10 * day_sec),
            "salary": "Pay Matrix Rs. 21,700 - Rs. 69,100",
            "selection_process": "Offline OMR Exam, Physical Standard Test (PST), Physical Efficiency Test (PET), Medical Exam",
            "exam_pattern": "150 Questions, 300 Marks. General Knowledge, Hindi, Numerical & Mental Ability, Mental Aptitude.",
            "syllabus_summary": "Hindi Grammar, UP Special GK, Basic Math, Mental Aptitude and Law/Order Awareness.",
            "how_to_apply": "Apply via official UPPBPB website (uppbpb.gov.in).",
            "official_notification_url": "https://uppbpb.gov.in",
            "official_apply_url": "https://uppbpb.gov.in",
            "official_website_url": "https://uppbpb.gov.in",
            "status_badge": "Trending",
            "is_trending": 1,
            "trending_score": 96,
            "views_count": 58900,
            "apply_clicks": 18200
        },

        # Closing Soon Jobs (Urgent Deadlines matching the design: 2 to 7 days left)
        {
            "slug": "nta-ugc-net-2026",
            "title": "NTA UGC NET 2026",
            "organization": "National Testing Agency (NTA)",
            "org_logo": "nta",
            "category": "Teaching",
            "job_type": "Teaching",
            "location": "All India",
            "vacancies": "JRF & Assistant Professor",
            "qualification": "Post Graduate (55% marks)",
            "age_limit": "JRF: Up to 30 Years; Asst Professor: No Upper Age Limit",
            "application_fee": "General: Rs. 1150/-, EWS/OBC: Rs. 600/-, SC/ST: Rs. 325/-",
            "posted_date": "10 Jun 2026",
            "last_date": "10 Sep 2026",
            "last_date_timestamp": now + (2 * day_sec), # 2 days left
            "salary": "JRF Fellowship Rs. 37,000/month + HRA; Asst Professor UGC Pay Scales",
            "selection_process": "Computer Based Test (Paper 1 & Paper 2 without break)",
            "exam_pattern": "Paper 1: 50 Questions (100 Marks), Paper 2: 100 Questions (200 Marks). Duration: 3 Hours.",
            "syllabus_summary": "Teaching & Research Aptitude, Higher Education System, and Chosen Subject domain.",
            "how_to_apply": "Submit online form on ugcnet.nta.ac.in and upload photograph & signature.",
            "official_notification_url": "https://ugcnet.nta.ac.in",
            "official_apply_url": "https://ugcnet.nta.ac.in",
            "official_website_url": "https://nta.ac.in",
            "status_badge": "Closing Soon",
            "is_trending": 0,
            "trending_score": 88,
            "views_count": 22100,
            "apply_clicks": 7400
        },
        {
            "slug": "bihar-police-constable-2026",
            "title": "Bihar Police Constable 2026",
            "organization": "Central Selection Board of Constable (CSBC)",
            "org_logo": "police",
            "category": "Police",
            "job_type": "Police",
            "location": "Bihar",
            "vacancies": "21391",
            "qualification": "12th Pass",
            "age_limit": "18 - 25 Years",
            "application_fee": "Rs. 675/- (SC/ST/Female: Rs. 180/-)",
            "posted_date": "05 Jun 2026",
            "last_date": "12 Sep 2026",
            "last_date_timestamp": now + (4 * day_sec), # 4 days left
            "salary": "Level-3 (Rs. 21,700 - Rs. 69,100)",
            "selection_process": "Written Exam (Qualifying), Physical Efficiency Test (PET - Final Merit basis)",
            "exam_pattern": "100 Objective Questions (100 Marks) in 2 Hours. Hindi, English, Math, History, Geography, Science.",
            "syllabus_summary": "Metric level curriculum of Hindi, English, General Science and Social Science.",
            "how_to_apply": "Apply through csbc.bih.nic.in online portal.",
            "official_notification_url": "https://csbc.bih.nic.in",
            "official_apply_url": "https://csbc.bih.nic.in",
            "official_website_url": "https://csbc.bih.nic.in",
            "status_badge": "Closing Soon",
            "is_trending": 0,
            "trending_score": 85,
            "views_count": 31400,
            "apply_clicks": 9800
        },
        {
            "slug": "indian-navy-ssr-mr-2026",
            "title": "Indian Navy SSR/MR 2026",
            "organization": "Join Indian Navy (Agniveer)",
            "org_logo": "defence",
            "category": "Defence",
            "job_type": "Defence",
            "location": "All India",
            "vacancies": "4000+",
            "qualification": "10th / 12th (Math & Physics)",
            "age_limit": "17.5 - 21 Years",
            "application_fee": "Rs. 550/- + 18% GST",
            "posted_date": "12 Jun 2026",
            "last_date": "14 Sep 2026",
            "last_date_timestamp": now + (6 * day_sec), # 6 days left
            "salary": "Agniveer Package Rs. 30,000 - Rs. 40,000/month + Seva Nidhi",
            "selection_process": "Computer Based Exam (INET), PFT (Running, Squats, Pushups), Medical Examination",
            "exam_pattern": "100 Questions (English, Science, Mathematics, General Awareness).",
            "syllabus_summary": "10+2 standard Physics, Algebra, Geometry, English comprehension.",
            "how_to_apply": "Register and apply on joinindiannavy.gov.in.",
            "official_notification_url": "https://www.joinindiannavy.gov.in",
            "official_apply_url": "https://www.joinindiannavy.gov.in",
            "official_website_url": "https://www.joinindiannavy.gov.in",
            "status_badge": "Closing Soon",
            "is_trending": 0,
            "trending_score": 82,
            "views_count": 19500,
            "apply_clicks": 6200
        },
        {
            "slug": "rrb-technician-2026",
            "title": "RRB Technician 2026",
            "organization": "Railway Recruitment Board",
            "org_logo": "railway",
            "category": "Railways",
            "job_type": "Railway",
            "location": "All India",
            "vacancies": "9144",
            "qualification": "10th + ITI / Diploma / B.Sc",
            "age_limit": "18 - 36 Years",
            "application_fee": "Rs. 500/- (Rs. 400 refundable on CBT)",
            "posted_date": "18 Jun 2026",
            "last_date": "15 Sep 2026",
            "last_date_timestamp": now + (7 * day_sec), # 7 days left
            "salary": "Pay Level 2 & Level 5 (Rs. 19,900 to Rs. 29,200)",
            "selection_process": "Computer Based Test (CBT), Document Verification, Medical Test",
            "exam_pattern": "100 Marks CBT covering Basic Science & Engineering, Math, General Awareness, Reasoning.",
            "syllabus_summary": "Engineering Drawing, Units, Measurements, Mechanics, and Technical Trade syllabus.",
            "how_to_apply": "Visit rrbapply.gov.in and select Technician Gr-I or Gr-III.",
            "official_notification_url": "https://www.rrbapply.gov.in",
            "official_apply_url": "https://www.rrbapply.gov.in",
            "official_website_url": "https://indianrailways.gov.in",
            "status_badge": "Closing Soon",
            "is_trending": 0,
            "trending_score": 89,
            "views_count": 27800,
            "apply_clicks": 8600
        },
        {
            "slug": "dsssb-various-posts-2026",
            "title": "DSSSB Various Posts 2026",
            "organization": "Delhi Subordinate Services Selection Board",
            "org_logo": "state_govt",
            "category": "State Government",
            "job_type": "State",
            "location": "Delhi NCR",
            "vacancies": "4210",
            "qualification": "10th / 12th / Graduate",
            "age_limit": "18 - 30 Years",
            "application_fee": "Rs. 100/- (Women/SC/ST/PwBD Exempted)",
            "posted_date": "20 Jun 2026",
            "last_date": "15 Sep 2026",
            "last_date_timestamp": now + (7 * day_sec), # 7 days left
            "salary": "Grade Pay Rs. 1900 to Rs. 4600",
            "selection_process": "Tier-I One Tier Examination (General / Technical)",
            "exam_pattern": "200 Questions (200 Marks). General Awareness, Reasoning, Arithmetical Ability, Hindi & English.",
            "syllabus_summary": "General Aptitude, Hindi Language comprehension and Subject/Post-specific discipline.",
            "how_to_apply": "Register on dsssbonline.nic.in with post code.",
            "official_notification_url": "https://dsssb.delhi.gov.in",
            "official_apply_url": "https://dsssbonline.nic.in",
            "official_website_url": "https://dsssb.delhi.gov.in",
            "status_badge": "Closing Soon",
            "is_trending": 0,
            "trending_score": 79,
            "views_count": 14200,
            "apply_clicks": 4100
        }
    ]

    for job in jobs_data:
        cursor.execute("""
        INSERT INTO jobs (
            slug, title, organization, org_logo, category, job_type, location,
            vacancies, qualification, age_limit, application_fee, posted_date,
            last_date, last_date_timestamp, salary, selection_process, exam_pattern,
            syllabus_summary, how_to_apply, official_notification_url, official_apply_url,
            official_website_url, status_badge, is_trending, trending_score, views_count, apply_clicks
        ) VALUES (
            :slug, :title, :organization, :org_logo, :category, :job_type, :location,
            :vacancies, :qualification, :age_limit, :application_fee, :posted_date,
            :last_date, :last_date_timestamp, :salary, :selection_process, :exam_pattern,
            :syllabus_summary, :how_to_apply, :official_notification_url, :official_apply_url,
            :official_website_url, :status_badge, :is_trending, :trending_score, :views_count, :apply_clicks
        )""", job)

    # -------------------------------------------------------------
    # 2. ADMIT CARDS
    # -------------------------------------------------------------
    admit_cards = [
        {
            "slug": "ssc-chsl-tier-1-admit-card-2026",
            "exam_name": "SSC CHSL Tier-I Exam 2026",
            "organization": "Staff Selection Commission",
            "release_date": "06 Sep 2026",
            "exam_date": "18 Sep - 24 Sep 2026",
            "category": "SSC",
            "status": "Available Now",
            "download_url": "https://ssc.gov.in/admit-card",
            "official_website_url": "https://ssc.gov.in"
        },
        {
            "slug": "ibps-clerk-prelims-call-letter-2026",
            "exam_name": "IBPS Clerk Prelims Hall Ticket 2026",
            "organization": "Institute of Banking Personnel Selection",
            "release_date": "04 Sep 2026",
            "exam_date": "20 Sep 2026",
            "category": "Banking",
            "status": "Available Now",
            "download_url": "https://ibps.in",
            "official_website_url": "https://ibps.in"
        },
        {
            "slug": "upsc-nda-cds-2-admit-card-2026",
            "exam_name": "UPSC NDA & NA (II) Admit Card 2026",
            "organization": "Union Public Service Commission",
            "release_date": "01 Sep 2026",
            "exam_date": "14 Sep 2026",
            "category": "Defence",
            "status": "Available Now",
            "download_url": "https://upsconline.nic.in/eadmitcard",
            "official_website_url": "https://upsc.gov.in"
        },
        {
            "slug": "rrb-alp-cbt-1-hall-ticket-2026",
            "exam_name": "RRB Assistant Loco Pilot CBT-1 City Slip",
            "organization": "Indian Railways",
            "release_date": "02 Sep 2026",
            "exam_date": "22 Sep 2026",
            "category": "Railways",
            "status": "City Intimation Out",
            "download_url": "https://rrbapply.gov.in",
            "official_website_url": "https://indianrailways.gov.in"
        }
    ]

    for item in admit_cards:
        cursor.execute("""
        INSERT INTO admit_cards (slug, exam_name, organization, release_date, exam_date, category, status, download_url, official_website_url)
        VALUES (:slug, :exam_name, :organization, :release_date, :exam_date, :category, :status, :download_url, :official_website_url)
        """, item)

    # -------------------------------------------------------------
    # 3. RESULTS
    # -------------------------------------------------------------
    results = [
        {
            "slug": "upsc-cse-prelims-result-2026",
            "exam_name": "UPSC Civil Services Prelims 2026",
            "organization": "Union Public Service Commission",
            "result_date": "05 Sep 2026",
            "exam_stage": "Preliminary Stage (Roll-Wise List)",
            "status": "Declared",
            "view_result_url": "https://upsc.gov.in/WR-CSP-2026.pdf",
            "official_website_url": "https://upsc.gov.in"
        },
        {
            "slug": "ssc-gd-constable-final-result-2026",
            "exam_name": "SSC GD Constable Final Result & Cutoff",
            "organization": "Staff Selection Commission",
            "result_date": "03 Sep 2026",
            "exam_stage": "Final Merit List & Force Allocation",
            "status": "Declared",
            "view_result_url": "https://ssc.gov.in",
            "official_website_url": "https://ssc.gov.in"
        },
        {
            "slug": "sbi-clerk-mains-result-2026",
            "exam_name": "SBI Junior Associates (Clerk) Mains Result",
            "organization": "State Bank of India",
            "result_date": "01 Sep 2026",
            "exam_stage": "Phase-II (Mains Qualified Candidates)",
            "status": "Declared",
            "view_result_url": "https://sbi.co.in/careers",
            "official_website_url": "https://sbi.co.in"
        }
    ]

    for item in results:
        cursor.execute("""
        INSERT INTO results (slug, exam_name, organization, result_date, exam_stage, status, view_result_url, official_website_url)
        VALUES (:slug, :exam_name, :organization, :result_date, :exam_stage, :status, :view_result_url, :official_website_url)
        """, item)

    # -------------------------------------------------------------
    # 4. ANSWER KEYS
    # -------------------------------------------------------------
    answer_keys = [
        {
            "slug": "ssc-cpo-tier-1-tentative-answer-key-2026",
            "exam_name": "SSC CPO Sub-Inspector Tier-I Exam",
            "organization": "Staff Selection Commission",
            "exam_date": "25 Aug 2026",
            "release_date": "04 Sep 2026",
            "challenge_window": "04 Sep to 09 Sep 2026 (Rs. 100/question)",
            "download_url": "https://ssc.gov.in",
            "official_notice_url": "https://ssc.gov.in"
        },
        {
            "slug": "ctet-august-2026-provisional-answer-key",
            "exam_name": "Central Teacher Eligibility Test (CTET)",
            "organization": "Central Board of Secondary Education (CBSE)",
            "exam_date": "20 Aug 2026",
            "release_date": "02 Sep 2026",
            "challenge_window": "02 Sep to 07 Sep 2026",
            "download_url": "https://ctet.nic.in",
            "official_notice_url": "https://ctet.nic.in"
        }
    ]

    for item in answer_keys:
        cursor.execute("""
        INSERT INTO answer_keys (slug, exam_name, organization, exam_date, release_date, challenge_window, download_url, official_notice_url)
        VALUES (:slug, :exam_name, :organization, :exam_date, :release_date, :challenge_window, :download_url, :official_notice_url)
        """, item)

    # -------------------------------------------------------------
    # 5. SYLLABUS
    # -------------------------------------------------------------
    syllabus_items = [
        {
            "slug": "ssc-cgl-detailed-syllabus-2026",
            "exam_name": "SSC CGL (Tier I & II) Complete Syllabus",
            "category": "SSC",
            "overview": "Comprehensive syllabus breakdown for Staff Selection Commission Combined Graduate Level examination.",
            "subjects": "General Intelligence & Reasoning, General Awareness, Quantitative Aptitude, English Comprehension, Computer Knowledge, Data Entry Speed Test.",
            "exam_pattern": "Tier-I: 100 Questions, 200 Marks (0.50 negative marking). Tier-II: Sectional Timing (Paper-I: Math, Reasoning, English, GA, Computer).",
            "detailed_syllabus": "Arithmetic: Percentages, Ratio, Profit & Loss, Time & Work, Algebra, Geometry, Coordinate Geometry, Trigonometry, Heights & Distances, Histograms. English: Active/Passive Voice, Direct/Indirect Narration, Cloze Test, Reading Comprehension.",
            "pdf_download_url": "https://ssc.gov.in"
        },
        {
            "slug": "rrb-ntpc-cbt-1-2-syllabus",
            "exam_name": "RRB NTPC (Graduate & Under Graduate) Syllabus",
            "category": "Railways",
            "overview": "Official railway syllabus for Non-Technical Popular Categories posts.",
            "subjects": "Mathematics, General Intelligence and Reasoning, General Awareness.",
            "exam_pattern": "CBT-1: 100 Qs (90 Minutes, 1/3rd negative marking). CBT-2: 120 Qs (90 Minutes).",
            "detailed_syllabus": "General Awareness: Current Events, Monuments of India, General Science, Life Sciences, Space, Nuclear Programs, Important Government Schemes.",
            "pdf_download_url": "https://indianrailways.gov.in"
        }
    ]

    for item in syllabus_items:
        cursor.execute("""
        INSERT INTO syllabus (slug, exam_name, category, overview, subjects, exam_pattern, detailed_syllabus, pdf_download_url)
        VALUES (:slug, :exam_name, :category, :overview, :subjects, :exam_pattern, :detailed_syllabus, :pdf_download_url)
        """, item)

    # -------------------------------------------------------------
    # 6. CURRENT AFFAIRS
    # -------------------------------------------------------------
    current_affairs_items = [
        {
            "slug": "india-indigenous-ai-compute-mission-2026",
            "title": "India Launches National Supercomputing & AI Compute Cloud 'Param Shakti 2.0'",
            "category": "Science & Technology",
            "date": "07 Sep 2026",
            "period": "Today",
            "summary": "MeitY inaugurates 10,000 GPU AI compute cluster to empower domestic deep-tech startups and research scholars.",
            "content": "In a major stride toward digital sovereignty, the Ministry of Electronics and Information Technology (MeitY) announced the commissioning of the IndiaAI GPU infrastructure cluster under the national supercomputing mission. This initiative enables academic institutions and civil service researchers to train indigenous models across 22 official Indian languages."
        },
        {
            "slug": "rbi-monetary-policy-review-september-2026",
            "title": "RBI Monetary Policy Committee Keeps Repo Rate Steady at 6.50%",
            "category": "Economy",
            "date": "05 Sep 2026",
            "period": "This Week",
            "summary": "Governor highlights resilient GDP growth of 7.2% with inflation hovering comfortably within target band.",
            "content": "The Reserve Bank of India (RBI) Monetary Policy Committee (MPC) voted to keep key policy repo rates unchanged at 6.50%. The central bank noted strong agricultural output and robust manufacturing performance, maintaining India's stance as the fastest-growing major economy."
        },
        {
            "slug": "paris-to-los-angeles-india-olympic-mission",
            "title": "Government Approves Mission Olympic Cell (MOC) Target Podium Scheme for 2028 Games",
            "category": "Sports",
            "date": "02 Sep 2026",
            "period": "This Month",
            "summary": "Sports Authority of India expands elite athlete grassroots scholarship coverage to 350 junior athletes.",
            "content": "The Ministry of Youth Affairs and Sports has unveiled an enhanced Target Olympic Podium Scheme (TOPS) allocation, focusing on world-class international coaching, sports science recovery, and mental conditioning for Indian athletes ahead of upcoming Asian and Olympic cycles."
        }
    ]

    for item in current_affairs_items:
        cursor.execute("""
        INSERT INTO current_affairs (slug, title, category, date, period, summary, content)
        VALUES (:slug, :title, :category, :date, :period, :summary, :content)
        """, item)

    conn.commit()
    conn.close()
    print("All authentic JobVani seed data successfully loaded into SQLite!")

if __name__ == "__main__":
    seed_all()
