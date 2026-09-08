/**
 * JobVani - Primary Application Controller & SPA Router
 */

const JobVaniApp = {
  currentCategory: 'All Jobs',
  currentQual: 'all',
  currentState: 'all',
  currentSort: 'latest',
  currentViewMode: 'grid', // 'grid' or 'list'
  savedJobIds: new Set(),

  init() {
    this.setupTheme();
    this.bindGlobalEvents();
    this.loadSavedBookmarks();
    this.setupScrollListeners();
    this.route();
    window.addEventListener('hashchange', () => this.route());
  },

  // Helper for official organization logo SVGs
  getOrgLogo(org = '', category = '') {
    const text = (org + ' ' + category).toLowerCase();
    if (text.includes('ssc')) return '/static/images/logo_ssc.svg';
    if (text.includes('ibps') || text.includes('bank') || text.includes('sbi') || text.includes('rbi')) return '/static/images/logo_ibps.svg';
    if (text.includes('railway') || text.includes('rrb') || text.includes('rrc')) return '/static/images/logo_railway.svg';
    if (text.includes('upsc') || text.includes('ias')) return '/static/images/logo_upsc.svg';
    if (text.includes('police') || text.includes('csbc') || text.includes('uppbpb')) return '/static/images/logo_police.svg';
    if (text.includes('navy') || text.includes('defence') || text.includes('air force') || text.includes('army') || text.includes('agniveer')) return '/static/images/logo_defence.svg';
    if (text.includes('nta') || text.includes('ugc') || text.includes('teach') || text.includes('ctet') || text.includes('dsssb')) return '/static/images/logo_nta.svg';
    return '/static/images/logo_state.svg';
  },

  // Dynamic Sector Badge Generator (Gradients + Icons + Initial Monograms)
  getOrgBadge(org = '', category = '') {
    const text = (org + ' ' + category).toLowerCase();

    if (text.includes('ssc') || text.includes('staff selection')) {
      return { bg: 'linear-gradient(135deg, #1e3a8a, #3b82f6)', color: '#ffffff', icon: '<i class="fa-solid fa-landmark"></i>' };
    }
    if (text.includes('upsc') || text.includes('union public') || text.includes('ias') || text.includes('ips')) {
      return { bg: 'linear-gradient(135deg, #831843, #be185d)', color: '#ffffff', icon: '<i class="fa-solid fa-scale-balanced"></i>' };
    }
    if (text.includes('railway') || text.includes('rrb') || text.includes('rrc') || text.includes('irctc')) {
      return { bg: 'linear-gradient(135deg, #b91c1c, #ea580c)', color: '#ffffff', icon: '<i class="fa-solid fa-train"></i>' };
    }
    if (text.includes('bank') || text.includes('ibps') || text.includes('sbi') || text.includes('rbi') || text.includes('bob') || text.includes('pnb') || text.includes('exim')) {
      return { bg: 'linear-gradient(135deg, #0f172a, #1e40af)', color: '#fbbf24', icon: '<i class="fa-solid fa-building-columns"></i>' };
    }
    if (text.includes('army') || text.includes('navy') || text.includes('air force') || text.includes('defence') || text.includes('nda') || text.includes('cds') || text.includes('afcat')) {
      return { bg: 'linear-gradient(135deg, #14532d, #15803d)', color: '#ffffff', icon: '<i class="fa-solid fa-shield-halved"></i>' };
    }
    if (text.includes('police') || text.includes('constable') || text.includes('si') || text.includes('itbp') || text.includes('crpf') || text.includes('cisf') || text.includes('bsf')) {
      return { bg: 'linear-gradient(135deg, #1e1b4b, #4338ca)', color: '#facc15', icon: '<i class="fa-solid fa-star"></i>' };
    }
    if (text.includes('teaching') || text.includes('tet') || text.includes('ctet') || text.includes('kvs') || text.includes('nvs') || text.includes('d.el.ed') || text.includes('bed') || text.includes('univ')) {
      return { bg: 'linear-gradient(135deg, #4c1d95, #7c3aed)', color: '#ffffff', icon: '<i class="fa-solid fa-graduation-cap"></i>' };
    }
    if (text.includes('medical') || text.includes('nurse') || text.includes('aiims') || text.includes('tmc') || text.includes('health') || text.includes('doctor')) {
      return { bg: 'linear-gradient(135deg, #0e7490, #06b6d4)', color: '#ffffff', icon: '<i class="fa-solid fa-kit-medical"></i>' };
    }
    if (text.includes('oil') || text.includes('tngecl') || text.includes('mecdm') || text.includes('iocl') || text.includes('ongc') || text.includes('ntpc') || text.includes('power') || text.includes('energy')) {
      return { bg: 'linear-gradient(135deg, #c2410c, #f59e0b)', color: '#ffffff', icon: '<i class="fa-solid fa-bolt"></i>' };
    }

    // Dynamic Monogram from Org Name (e.g. "PSSSB" -> "PS", "High Court" -> "HC")
    const cleanOrg = org.replace(/[^a-zA-Z0-9\s]/g, '').trim();
    const parts = cleanOrg.split(/\s+/).filter(p => p.length > 0);
    let mono = 'GOV';
    if (parts.length >= 2) {
      mono = (parts[0][0] + parts[1][0]).toUpperCase();
    } else if (parts.length === 1) {
      mono = parts[0].slice(0, Math.min(3, parts[0].length)).toUpperCase();
    }

    return {
      bg: 'linear-gradient(135deg, #1e293b, #334155)',
      color: '#38bdf8',
      icon: `<span style="font-size: 0.85rem; font-weight: 800; letter-spacing: -0.02em;">${mono}</span>`
    };
  },

  // Setup Dark / Light mode
  setupTheme() {
    const savedTheme = localStorage.getItem('jobvani_theme') || 'light';
    if (savedTheme === 'dark') {
      document.body.classList.add('dark-mode');
      const themeIcon = document.getElementById('theme-toggle-icon');
      if (themeIcon) themeIcon.className = 'fa-regular fa-sun';
    }
  },

  toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('jobvani_theme', isDark ? 'dark' : 'light');
    const themeIcon = document.getElementById('theme-toggle-icon');
    if (themeIcon) {
      themeIcon.className = isDark ? 'fa-regular fa-sun' : 'fa-regular fa-moon';
    }
    this.showToast(isDark ? 'Dark mode enabled 🌙' : 'Light mode enabled ☀️');
  },

  // View Mode: Cards Grid vs Compact List
  setViewMode(mode) {
    this.currentViewMode = mode;
    const gridBtn = document.getElementById('view-mode-grid-btn');
    const listBtn = document.getElementById('view-mode-list-btn');
    if (gridBtn) gridBtn.classList.toggle('active', mode === 'grid');
    if (listBtn) listBtn.classList.toggle('active', mode === 'list');
    this.loadLatestJobsGrid();
  },

  // Qualification Filter
  filterByQual(qual, btnEl) {
    this.currentQual = qual;
    document.querySelectorAll('.qual-pill').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
    const smartSelect = document.getElementById('smart-qual-select');
    if (smartSelect) smartSelect.value = qual;
    this.loadLatestJobsGrid();
  },

  // State Filter
  filterByState(state, pillEl) {
    this.currentState = state;
    document.querySelectorAll('.state-pill').forEach(p => p.classList.remove('active'));
    if (pillEl) pillEl.classList.add('active');
    this.loadLatestJobsGrid();
    const target = document.getElementById('latest-jobs');
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    this.showToast(state === 'all' ? 'Showing All India Recruitments' : `Filtered for ${state} jobs`);
  },

  // Sort Filter
  changeSort(sortVal) {
    this.currentSort = sortVal;
    this.loadLatestJobsGrid();
  },

  // Smart Sarkari Eligibility Matcher Button
  applySmartFilter() {
    const qual = document.getElementById('smart-qual-select')?.value || 'all';
    const sector = document.getElementById('smart-sector-select')?.value || 'All Jobs';
    const sort = document.getElementById('smart-sort-select')?.value || 'latest';

    this.currentQual = qual;
    this.currentCategory = sector;
    this.currentSort = sort;

    // Update qual pills row
    document.querySelectorAll('.qual-pill').forEach(btn => {
      btn.classList.toggle('active', btn.textContent.toLowerCase().includes(qual.toLowerCase()) || (qual === 'all' && btn.textContent.includes('All')));
    });

    // Update category cards
    document.querySelectorAll('.category-nav-card').forEach(card => {
      card.classList.toggle('active', card.dataset.category === sector);
    });

    this.loadLatestJobsGrid();

    const jobsSection = document.getElementById('latest-jobs');
    if (jobsSection) {
      jobsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    this.showToast('✨ Smart filters applied successfully!');
  },

  // Share on WhatsApp
  shareWhatsApp(title, slug) {
    const url = window.location.origin + '/#jobs/' + slug;
    const text = encodeURIComponent(`🇮🇳 *${title}*\nCheck official notification, eligibility & direct apply on JobVani:\n👉 ${url}\n\n_JobVani — Sarkari Naukri, Seedhi Baat._`);
    window.open(`https://api.whatsapp.com/send?text=${text}`, '_blank');
  },

  // Copy Direct Link
  copyJobLink(slug, btnEl) {
    const url = window.location.origin + '/#jobs/' + slug;
    navigator.clipboard.writeText(url).then(() => {
      this.showToast('Direct job link copied to clipboard! 📋');
      if (btnEl) {
        const orig = btnEl.innerHTML;
        btnEl.innerHTML = '<i class="fa-solid fa-check" style="color: #16a34a;"></i>';
        setTimeout(() => { btnEl.innerHTML = orig; }, 2000);
      }
    });
  },

  // Back-to-Top Scroll Listener
  setupScrollListeners() {
    const btnTop = document.getElementById('btn-back-to-top');
    window.addEventListener('scroll', () => {
      if (btnTop) {
        if (window.scrollY > 350) {
          btnTop.classList.add('visible');
        } else {
          btnTop.classList.remove('visible');
        }
      }
    });
  },

  // Routing
  async route() {
    const hash = window.location.hash || '#home';
    const mainHome = document.getElementById('home-view-container');
    const detailView = document.getElementById('job-detail-container');
    const generalSectionView = document.getElementById('general-section-container');
    const adminView = document.getElementById('admin-dashboard-container');

    // Hide all
    if (mainHome) mainHome.style.display = 'none';
    if (detailView) detailView.classList.remove('active');
    if (generalSectionView) generalSectionView.classList.remove('active');
    if (adminView) adminView.classList.remove('active');

    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
      const target = link.getAttribute('href');
      link.classList.toggle('active', target === hash);
    });

    if (hash.startsWith('#jobs/')) {
      const slug = hash.replace('#jobs/', '');
      this.renderJobDetailPage(slug);
    } else if (hash === '#admin') {
      this.renderAdminDashboard();
    } else if (hash === '#admit-card') {
      this.renderAdmitCardsView();
    } else if (hash === '#results') {
      this.renderResultsView();
    } else if (hash === '#answer-key') {
      this.renderAnswerKeysView();
    } else if (hash === '#syllabus') {
      this.renderSyllabusView();
    } else if (hash === '#current-affairs') {
      this.renderCurrentAffairsView();
    } else if (hash === '#saved') {
      this.renderSavedJobsView();
    } else {
      // Default: Home
      if (mainHome) mainHome.style.display = 'block';
      this.loadHomePageData();
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  // Load Homepage Data
  async loadHomePageData() {
    this.loadTrustStats();
    this.loadTrendingJobs();
    this.loadClosingSoonJobs();
    this.loadLatestJobsGrid();
  },

  async loadTrustStats() {
    const settings = await JobVaniAPI.getSettings();
    if (settings) {
      const el1 = document.getElementById('stat-active-jobs');
      const el2 = document.getElementById('stat-exam-categories');
      const el3 = document.getElementById('stat-happy-users');
      const el4 = document.getElementById('stat-updated-info');

      if (el1) el1.textContent = settings.active_jobs_stat || '1.2K+';
      if (el2) el2.textContent = settings.exam_categories_stat || '50+';
      if (el3) el3.textContent = settings.happy_users_stat || '10M+';
      if (el4) el4.textContent = settings.updated_info_stat || '100%';
    }
  },

  async loadTrendingJobs() {
    const listEl = document.getElementById('trending-jobs-list');
    if (!listEl) return;

    const trending = await JobVaniAPI.getTrending();
    if (!trending || trending.length === 0) return;

    listEl.innerHTML = trending.map((item, idx) => {
      let badgeClass = 'badge-trending';
      if (item.status_badge === 'New') badgeClass = 'badge-new';
      else if (item.status_badge === 'Hot') badgeClass = 'badge-hot';
      else if (item.status_badge === 'Popular') badgeClass = 'badge-popular';

      let rankMedalClass = '';
      if (idx === 0) rankMedalClass = 'rank-1';
      else if (idx === 1) rankMedalClass = 'rank-2';
      else if (idx === 2) rankMedalClass = 'rank-3';

      return `
        <div class="ranked-job-item" onclick="window.location.hash = '#jobs/${item.slug}'">
          <div class="ranked-left">
            <span class="rank-number ${rankMedalClass}">${idx + 1}</span>
            <div class="ranked-details">
              <span class="ranked-title">${item.title}</span>
              <span class="ranked-sub">${item.organization}</span>
            </div>
          </div>
          <span class="status-pill-badge ${badgeClass}">${item.status_badge || 'Trending'}</span>
        </div>
      `;
    }).join('');
  },

  async loadClosingSoonJobs() {
    const listEl = document.getElementById('closing-soon-list');
    if (!listEl) return;

    const closing = await JobVaniAPI.getClosingSoon();
    if (!closing || closing.length === 0) return;

    listEl.innerHTML = closing.map((item, idx) => {
      return `
        <div class="ranked-job-item" onclick="window.location.hash = '#jobs/${item.slug}'">
          <div class="ranked-left">
            <span class="rank-number closing-rank">${idx + 1}</span>
            <div class="ranked-details">
              <span class="ranked-title">${item.title}</span>
              <span class="ranked-sub">Last Date: ${item.last_date}</span>
            </div>
          </div>
          <span class="status-pill-badge badge-urgent"><i class="fa-regular fa-clock" style="margin-right:3px;"></i>${item.urgency_badge || 'Urgent'}</span>
        </div>
      `;
    }).join('');
  },

  async loadLatestJobsGrid() {
    const gridEl = document.getElementById('latest-jobs-grid');
    if (!gridEl) return;

    // Show smooth shimmer skeleton while fetching
    gridEl.className = this.currentViewMode === 'grid' ? 'jobs-four-col-grid' : 'jobs-compact-list';
    gridEl.innerHTML = `
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
    `;

    let jobs = await JobVaniAPI.getJobs({
      category: this.currentCategory,
      qualification: this.currentQual === 'all' ? null : this.currentQual,
      sort: this.currentSort,
      limit: 16
    });

    // Client-side state filter if selected
    if (this.currentState && this.currentState !== 'all' && jobs) {
      jobs = jobs.filter(j => {
        const text = (j.title + ' ' + j.organization + ' ' + (j.location || '')).toLowerCase();
        return text.includes(this.currentState.toLowerCase());
      });
    }

    const badgeCount = document.getElementById('active-jobs-count-badge');
    if (badgeCount) badgeCount.textContent = `${jobs ? jobs.length : 0} Active`;

    if (!jobs || jobs.length === 0) {
      gridEl.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 50px 20px; background: var(--bg-card); border-radius: var(--radius-lg); border: 1px dashed var(--border-card);">
          <div style="font-size: 2.2rem; margin-bottom: 12px;">⚡</div>
          <h3 style="font-size: 1.15rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">Database is Ready for Auto-Pilot Ingestion</h3>
          <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 20px; max-width: 480px; margin-left: auto; margin-right: auto;">
            Saari purani jobs hata di gayi hain! Ab Admin Panel me jaakar <strong>"Run Auto-Pilot Scraper"</strong> par click karke live official recruitments fetch karein!
          </p>
          <a href="#admin" class="btn-login" style="display: inline-flex; align-items: center; gap: 8px; text-decoration: none; padding: 10px 24px;">
            <i class="fa-solid fa-arrows-rotate"></i> Go to Admin & Run Scraper
          </a>
        </div>
      `;
      return;
    }

    // Render in Modern Apple/Stripe Grade Card Grid Mode
    if (this.currentViewMode === 'grid') {
      gridEl.innerHTML = jobs.map(job => {
        const badge = this.getOrgBadge(job.organization, job.category);
        const isSaved = this.savedJobIds.has(job.id);
        const salaryText = job.salary ? job.salary.split('(')[0].trim() : '7th CPC Pay Matrix';
        const cleanQual = job.qualification || 'Graduate / 10th / 12th';
        const isUrgent = job.last_date && (job.last_date.toLowerCase().includes('today') || job.last_date.toLowerCase().includes('tomorrow') || job.last_date.toLowerCase().includes('2025'));

        return `
          <article class="job-card" onclick="window.location.hash = '#jobs/${job.slug}'">
            <!-- Header: Dynamic Sector Avatar, Tags, and Save/Share Tools -->
            <div class="job-card-top">
              <div class="job-org-badge" style="background: ${badge.bg}; color: ${badge.color};">
                ${badge.icon}
              </div>
              <div class="job-header-info">
                <div class="job-pill-row">
                  <span class="pill-govt-verified"><i class="fa-solid fa-check" style="font-size:0.6rem;"></i> Verified</span>
                  <span class="pill-sector-tag">${job.category || 'Central Govt'}</span>
                </div>
                <p class="job-card-org" title="${job.organization}">${job.organization}</p>
              </div>
              <div class="job-card-tools" onclick="event.stopPropagation();">
                <button class="card-tool-btn btn-wa" onclick="JobVaniApp.shareWhatsApp('${job.title.replace(/'/g, "\\'")}', '${job.slug}')" title="Share on WhatsApp">
                  <i class="fa-brands fa-whatsapp"></i>
                </button>
                <button class="card-tool-btn ${isSaved ? 'saved' : ''}" 
                        onclick="JobVaniApp.toggleBookmarkAction(${job.id}, this)" 
                        title="${isSaved ? 'Saved' : 'Save Job'}">
                  <i class="${isSaved ? 'fa-solid' : 'fa-regular'} fa-bookmark"></i>
                </button>
              </div>
            </div>

            <!-- Full Job Title (2-Line Responsive Clamp - No weird dots) -->
            <h3 class="job-card-title" title="${job.title}">${job.title}</h3>

            <!-- Micro Chips Bar: Vacancies, Eligibility, Location -->
            <div class="job-chips-grid">
              <div class="chip-item chip-vacancies">
                <i class="fa-solid fa-users"></i>
                <span>${job.vacancies || 'Various Posts'}</span>
              </div>
              <div class="chip-item chip-qual">
                <i class="fa-solid fa-graduation-cap"></i>
                <span title="${job.qualification}">${cleanQual}</span>
              </div>
              <div class="chip-item">
                <i class="fa-solid fa-location-dot"></i>
                <span>${job.location || 'All India'}</span>
              </div>
            </div>

            <!-- Salary & Deadline Row -->
            <div class="job-meta-bar">
              <div class="meta-salary">
                <i class="fa-solid fa-indian-rupee-sign" style="font-size:0.7rem;"></i>
                <span>${salaryText}</span>
              </div>
              <div class="meta-deadline ${isUrgent ? 'urgent' : ''}">
                <i class="fa-regular fa-calendar-check"></i>
                <span>${job.last_date ? job.last_date : 'Check Notice'}</span>
              </div>
            </div>

            <!-- Card Actions Footer (Details + Apply + 1-Tap PDF) -->
            <div class="job-card-actions" onclick="event.stopPropagation();">
              <button class="btn-card-secondary" onclick="window.location.hash = '#jobs/${job.slug}'">
                <span>View Details</span>
                <i class="fa-solid fa-arrow-right" style="font-size:0.7rem;"></i>
              </button>
              <a href="${job.official_apply_url || job.official_website_url}" target="_blank" class="btn-card-apply" onclick="JobVaniAPI.trackApplyClick('${job.slug}')">
                <span>Apply</span>
                <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:0.7rem;"></i>
              </a>
              ${job.official_notification_url ? `
              <a href="${job.official_notification_url}" target="_blank" class="btn-card-pdf" title="Download Official Notification PDF">
                <i class="fa-regular fa-file-pdf"></i>
              </a>
              ` : ''}
            </div>
          </article>
        `;
      }).join('');
    } else {
      // Render in Compact List Mode
      gridEl.innerHTML = jobs.map(job => {
        const logoUrl = this.getOrgLogo(job.organization, job.category);
        const isSaved = this.savedJobIds.has(job.id);
        const salaryText = job.salary ? job.salary.split('(')[0].trim().slice(0, 22) : 'Govt Pay Scale';

        return `
          <div class="job-list-row">
            <div class="list-row-main">
              <div class="org-logo-circle" style="width: 38px; height: 38px;">
                <img src="${logoUrl}" class="org-logo-img" alt="${job.organization}">
              </div>
              <div style="min-width: 0;">
                <div class="list-row-title" onclick="window.location.hash = '#jobs/${job.slug}'">${job.title}</div>
                <div class="list-row-sub">${job.organization} &bull; <span style="color: var(--primary-blue); font-weight: 600;">${job.category}</span></div>
              </div>
            </div>
            <div>
              <span style="font-size: 0.74rem; color: var(--text-muted);">Vacancies:</span>
              <strong style="color: var(--primary-blue); display: block; font-size: 0.88rem;">${job.vacancies}</strong>
            </div>
            <div>
              <span style="font-size: 0.74rem; color: var(--text-muted);">Salary:</span>
              <strong style="color: #059669; display: block; font-size: 0.82rem;">${salaryText}</strong>
            </div>
            <div>
              <span style="font-size: 0.74rem; color: var(--text-muted);">Last Date:</span>
              <strong style="color: #dc2626; display: block; font-size: 0.82rem;">${job.last_date}</strong>
            </div>
            <div class="list-row-actions">
              <button class="card-action-icon-btn btn-wa" onclick="JobVaniApp.shareWhatsApp('${job.title.replace(/'/g, "\\'")}', '${job.slug}')" title="Share WhatsApp">
                <i class="fa-brands fa-whatsapp"></i>
              </button>
              <button class="card-quick-save-btn ${isSaved ? 'saved' : ''}" onclick="JobVaniApp.toggleBookmarkAction(${job.id}, this)" title="Bookmark">
                <i class="${isSaved ? 'fa-solid' : 'fa-regular'} fa-bookmark"></i>
              </button>
              <a href="${job.official_apply_url || job.official_website_url}" target="_blank" class="btn-apply-now" style="height: 32px; padding: 0 14px;" onclick="JobVaniAPI.trackApplyClick('${job.slug}')">Apply</a>
            </div>
          </div>
        `;
      }).join('');
    }
  },

  // Dedicated Job Detail View (#jobs/[slug])
  async renderJobDetailPage(slug) {
    const detailView = document.getElementById('job-detail-container');
    if (!detailView) return;

    detailView.classList.add('active');
    detailView.innerHTML = '<div style="text-align: center; padding: 100px 0;"><i class="fa-solid fa-spinner fa-spin fa-2x" style="color: var(--primary-blue)"></i><p style="margin-top:12px; color:var(--text-muted); font-weight:600;">Loading verified recruitment notice...</p></div>';

    const job = await JobVaniAPI.getJobBySlug(slug);
    if (!job) {
      detailView.innerHTML = '<div class="container" style="text-align:center; padding: 80px 0;"><h2>Recruitment Notice Not Found</h2><p style="color:var(--text-muted); margin: 10px 0 20px;">The job posting you are looking for may have expired or been archived.</p><a href="#home" class="btn-login">Back to Homepage</a></div>';
      return;
    }

    const logoUrl = this.getOrgLogo(job.organization, job.category);
    const isBookmarked = this.savedJobIds.has(job.id);
    const minAge = 18;
    const maxAge = job.age_limit && job.age_limit.includes('32') ? 32 : (job.age_limit && job.age_limit.includes('30') ? 30 : (job.age_limit && job.age_limit.includes('33') ? 33 : 27));

    detailView.innerHTML = `
      <div class="container">
        <!-- Breadcrumbs -->
        <div class="breadcrumbs-bar">
          <a href="#home"><i class="fa-solid fa-house"></i> Home</a>
          <span class="breadcrumb-separator">/</span>
          <a href="#home" onclick="JobVaniApp.filterByQual('all', null); return false;">Latest Jobs</a>
          <span class="breadcrumb-separator">/</span>
          <a href="#home" onclick="JobVaniApp.currentCategory='${job.category}'; JobVaniApp.loadLatestJobsGrid(); return false;">${job.category}</a>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-current">${job.title}</span>
        </div>

        <div class="detail-layout-grid">
          <!-- Main Large Column -->
          <div class="detail-main-card">
            
            <!-- Hero Header Section -->
            <div class="detail-hero-header">
              <div class="detail-trust-seal-bar">
                <span class="detail-verified-seal"><i class="fa-solid fa-circle-check"></i> Government Verified Notice</span>
                <span class="detail-category-badge"><i class="fa-solid fa-tag"></i> ${job.category} Recruitment</span>
                <span class="detail-category-badge" style="background:#fef3c7; color:#d97706;"><i class="fa-solid fa-bolt"></i> Advt No. 2026/01</span>
                <span class="detail-category-badge" style="background:#f0fdf4; color:#16a34a;"><span class="live-pulse-dot" style="width:6px; height:6px;"></span> Active Application Window</span>
              </div>

              <div class="detail-header-main-row">
                <div class="detail-org-brand-box">
                  <div class="detail-org-circle-large">
                    <img src="${logoUrl}" alt="${job.organization}">
                  </div>
                  <div class="detail-title-block">
                    <h1>${job.title}</h1>
                    <div class="detail-org-name-text">
                      <span><i class="fa-solid fa-landmark"></i> ${job.organization}</span>
                      <span>&bull;</span>
                      <span><i class="fa-solid fa-location-dot"></i> ${job.location || 'All India'}</span>
                      <span>&bull;</span>
                      <span><i class="fa-solid fa-layer-group"></i> ${job.job_type} Sector</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action Buttons Row in Header -->
              <div class="detail-actions-top-row">
                <a href="${job.official_apply_url || job.official_website_url}" target="_blank" class="btn-detail-cta-primary" onclick="JobVaniAPI.trackApplyClick('${job.slug}')">
                  <span>Apply Online (Official Portal)</span>
                  <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:0.78rem;"></i>
                </a>
                <a href="${job.official_notification_url || job.official_website_url}" target="_blank" class="btn-detail-cta-pdf">
                  <i class="fa-regular fa-file-pdf"></i>
                  <span>Download PDF Notice</span>
                </a>
                <button class="btn-detail-tool btn-wa-detail" onclick="JobVaniApp.shareWhatsApp('${job.title.replace(/'/g, "\\'")}', '${job.slug}')" title="Share on WhatsApp">
                  <i class="fa-brands fa-whatsapp" style="color: #16a34a; font-size: 1rem;"></i>
                  <span>Share</span>
                </button>
                <button class="btn-detail-tool ${isBookmarked ? 'bookmarked' : ''}" onclick="JobVaniApp.toggleBookmarkAction(${job.id}, this)">
                  <i class="${isBookmarked ? 'fa-solid' : 'fa-regular'} fa-bookmark"></i>
                  <span>${isBookmarked ? 'Saved' : 'Save'}</span>
                </button>
                <button class="btn-detail-tool" onclick="JobVaniApp.copyJobLink('${job.slug}', this)" title="Copy Shareable Link">
                  <i class="fa-regular fa-copy"></i>
                  <span>Copy Link</span>
                </button>
                <button class="btn-detail-tool" onclick="window.print()" title="Print Job Summary">
                  <i class="fa-solid fa-print"></i>
                  <span>Print</span>
                </button>
              </div>
            </div>

            <!-- 4 KPI Highlight Metric Cards -->
            <div class="detail-kpi-grid">
              <div class="kpi-metric-box">
                <div class="kpi-header-row">
                  <span class="kpi-title-text">Total Vacancies</span>
                  <div class="kpi-icon-pill kpi-blue"><i class="fa-solid fa-users"></i></div>
                </div>
                <span class="kpi-main-val" style="color: var(--primary-blue);">${job.vacancies}</span>
                <span class="kpi-sub-text">All India Category Posts</span>
              </div>

              <div class="kpi-metric-box">
                <div class="kpi-header-row">
                  <span class="kpi-title-text">Last Date</span>
                  <div class="kpi-icon-pill kpi-red"><i class="fa-regular fa-calendar-xmark"></i></div>
                </div>
                <span class="kpi-main-val" style="color: #dc2626;">${job.last_date}</span>
                <span class="kpi-sub-text">Apply before 11:59 PM</span>
              </div>

              <div class="kpi-metric-box">
                <div class="kpi-header-row">
                  <span class="kpi-title-text">Pay Scale / Salary</span>
                  <div class="kpi-icon-pill kpi-green"><i class="fa-solid fa-indian-rupee-sign"></i></div>
                </div>
                <span class="kpi-main-val" style="color: #059669;">${job.salary ? job.salary.split('(')[0].trim() : '7th CPC Pay Matrix'}</span>
                <span class="kpi-sub-text">7th Central Pay Commission</span>
              </div>

              <div class="kpi-metric-box">
                <div class="kpi-header-row">
                  <span class="kpi-title-text">Qualification</span>
                  <div class="kpi-icon-pill kpi-purple"><i class="fa-solid fa-graduation-cap"></i></div>
                </div>
                <span class="kpi-main-val" style="color: #7c3aed;">${job.qualification || 'Graduate / 10th / 12th'}</span>
                <span class="kpi-sub-text">Recognized University/Board</span>
              </div>
            </div>

            <!-- In-Page Sticky Navigation Tabs -->
            <div class="detail-nav-tabs-bar">
              <a class="detail-tab-pill active" onclick="document.getElementById('sec-dates').scrollIntoView({behavior: 'smooth'}); return false;">📅 Dates</a>
              <a class="detail-tab-pill" onclick="document.getElementById('sec-fees').scrollIntoView({behavior: 'smooth'}); return false;">💳 Fee Details</a>
              <a class="detail-tab-pill" onclick="document.getElementById('sec-age').scrollIntoView({behavior: 'smooth'}); return false;">🎂 Age Limit</a>
              <a class="detail-tab-pill" onclick="document.getElementById('sec-eligibility').scrollIntoView({behavior: 'smooth'}); return false;">🎓 Eligibility</a>
              <a class="detail-tab-pill" onclick="document.getElementById('sec-selection').scrollIntoView({behavior: 'smooth'}); return false;">🎯 Selection Steps</a>
              <a class="detail-tab-pill" onclick="document.getElementById('sec-syllabus').scrollIntoView({behavior: 'smooth'}); return false;">📚 Syllabus & Pattern</a>
              <a class="detail-tab-pill" onclick="document.getElementById('sec-how-to-apply').scrollIntoView({behavior: 'smooth'}); return false;">📝 How to Apply</a>
              <a class="detail-tab-pill" onclick="document.getElementById('sec-official-links').scrollIntoView({behavior: 'smooth'}); return false;">🔗 Official Links</a>
              <a class="detail-tab-pill" onclick="document.getElementById('sec-faqs').scrollIntoView({behavior: 'smooth'}); return false;">❓ FAQs</a>
            </div>

            <!-- Section 1: Important Dates -->
            <div id="sec-dates" class="detail-section-block">
              <h3 class="detail-section-title"><i class="fa-regular fa-calendar-check"></i> 1. Important Dates & Recruitment Timeline</h3>
              <table class="info-data-table">
                <tr><td>Notification Release Date</td><td>${job.posted_date}</td></tr>
                <tr><td>Online Application Starts</td><td>${job.posted_date} (09:00 AM)</td></tr>
                <tr><td>Last Date for Online Registration</td><td style="color: #dc2626; font-weight: 800;"><i class="fa-regular fa-clock" style="margin-right:4px;"></i>${job.last_date} (11:59 PM)</td></tr>
                <tr><td>Last Date for Online Fee Payment</td><td>${job.last_date}</td></tr>
                <tr><td>Online Form Correction Window</td><td>3 Days after application closure</td></tr>
                <tr><td>CBT / Stage-1 Exam Schedule</td><td>Announced Soon on JobVani</td></tr>
                <tr><td>Admit Card Release Date</td><td>4 - 7 Days before the exam date</td></tr>
              </table>
            </div>

            <!-- Section 2: Application Fee -->
            <div id="sec-fees" class="detail-section-block">
              <h3 class="detail-section-title"><i class="fa-solid fa-credit-card"></i> 2. Application Fee & Payment Modes</h3>
              <div class="fee-cards-row">
                <div class="fee-card-item">
                  <span class="fee-category-label">General / OBC / EWS (Male)</span>
                  <span class="fee-amount-badge">${job.application_fee ? job.application_fee.split('(')[0] : 'Rs. 100/-'}</span>
                </div>
                <div class="fee-card-item">
                  <span class="fee-category-label">SC / ST / PwBD / ESM</span>
                  <span class="fee-amount-badge" style="color: #16a34a;">Rs. 0/- (Exempted)</span>
                </div>
                <div class="fee-card-item">
                  <span class="fee-category-label">All Female Candidates</span>
                  <span class="fee-amount-badge" style="color: #16a34a;">Rs. 0/- (Exempted)</span>
                </div>
              </div>
              <div class="fee-payment-mode-note">
                <i class="fa-solid fa-shield-halved" style="color: var(--primary-blue); font-size: 1rem;"></i>
                <span><strong>Payment Modes:</strong> Pay the examination fee online via Net Banking, Debit / Credit Cards, UPI (BHIM, Google Pay, PhonePe, Paytm), or offline via State Bank of India (SBI) e-Challan.</span>
              </div>
            </div>

            <!-- Section 3: Age Limit & Calculator -->
            <div id="sec-age" class="detail-section-block">
              <h3 class="detail-section-title"><i class="fa-solid fa-cake-candles"></i> 3. Age Limit & Category-wise Relaxation (As on 01.08.2026)</h3>
              <table class="info-data-table">
                <tr><td>Minimum Age Requirement</td><td><strong>18 Years</strong></td></tr>
                <tr><td>Maximum Age Limit</td><td><strong>${job.age_limit || '27 - 32 Years (Post-wise)'}</strong></td></tr>
                <tr><td>Age Calculation Crucial Date</td><td>01 August 2026</td></tr>
                <tr><td>SC / ST Category Relaxation</td><td><span style="color: #16a34a; font-weight: 700;">+5 Years</span> (Upper age limit up to 37 years)</td></tr>
                <tr><td>OBC (Non-Creamy Layer) Relaxation</td><td><span style="color: #16a34a; font-weight: 700;">+3 Years</span> (Upper age limit up to 35 years)</td></tr>
                <tr><td>PwBD (Unreserved / General)</td><td><span style="color: #16a34a; font-weight: 700;">+10 Years</span></td></tr>
                <tr><td>Ex-Servicemen (ESM)</td><td>3 Years after deduction of military service rendered from actual age</td></tr>
              </table>

              <!-- Interactive Age Calculator -->
              <div class="age-calc-widget">
                <div class="age-calc-title">
                  <i class="fa-solid fa-calculator" style="color: var(--primary-blue);"></i>
                  <span>Check Your Age Eligibility for this Recruitment</span>
                </div>
                <div class="age-calc-inputs-row">
                  <input type="number" id="calc-birth-year" class="age-calc-input" placeholder="Enter Birth Year (e.g. 1998)" min="1975" max="2010" value="1999">
                  <select id="calc-category-select" class="age-calc-input">
                    <option value="gen">General / EWS</option>
                    <option value="obc">OBC (3 Yrs Relaxation)</option>
                    <option value="scst">SC / ST (5 Yrs Relaxation)</option>
                    <option value="pwd">PwBD (10 Yrs Relaxation)</option>
                  </select>
                  <button type="button" class="btn-calc-age" onclick="JobVaniApp.checkAgeEligibility(${minAge}, ${maxAge})">Verify Eligibility</button>
                </div>
                <div id="age-calc-result-box" class="age-calc-result-box"></div>
              </div>
            </div>

            <!-- Section 4: Educational Qualification -->
            <div id="sec-eligibility" class="detail-section-block">
              <h3 class="detail-section-title"><i class="fa-solid fa-graduation-cap"></i> 4. Educational Qualification & Post-wise Eligibility</h3>
              <table class="info-data-table">
                <tr><td>Essential Qualification</td><td><strong style="color: var(--primary-blue);">${job.qualification}</strong> from a recognized University, Board or Institute incorporated by an Act of Central or State Legislature.</td></tr>
                <tr><td>Final Year Candidates</td><td>Candidates who have appeared in their final examination may also apply provisionally, provided they possess the required qualification certificate on or before the cut-off date.</td></tr>
                <tr><td>Required Verification Documents</td><td>10th Marksheet (for Date of Birth), 12th Certificate, Graduation Degree Marksheet, Valid Category/Caste Certificate (if claiming reservation), Photo Identity Proof (Aadhaar / Voter ID / PAN).</td></tr>
              </table>
            </div>

            <!-- Section 5: Selection Process Timeline -->
            <div id="sec-selection" class="detail-section-block">
              <h3 class="detail-section-title"><i class="fa-solid fa-list-check"></i> 5. Selection Process & Stages</h3>
              <div class="selection-timeline-list">
                <div class="timeline-step-item">
                  <div class="timeline-step-number">1</div>
                  <div class="timeline-step-content">
                    <div class="timeline-step-name">Tier-I / Preliminary Exam (Computer Based Test - CBT)</div>
                    <div class="timeline-step-desc">Multiple-choice objective test to screen and shortlist candidates for the Mains examination. Qualifying in nature.</div>
                  </div>
                </div>
                <div class="timeline-step-item">
                  <div class="timeline-step-number">2</div>
                  <div class="timeline-step-content">
                    <div class="timeline-step-name">Tier-II / Mains Examination</div>
                    <div class="timeline-step-desc">Advanced objective examination covering specialized subjects, mathematical abilities, English comprehension, and general awareness. Marks determine merit.</div>
                  </div>
                </div>
                <div class="timeline-step-item">
                  <div class="timeline-step-number">3</div>
                  <div class="timeline-step-content">
                    <div class="timeline-step-name">Skill Test / Typing Test / PET / PST</div>
                    <div class="timeline-step-desc">Post-specific Computer Proficiency Test (CPT), Data Entry Speed Test (DEST), or Physical Standard & Endurance Test for uniform posts.</div>
                  </div>
                </div>
                <div class="timeline-step-item">
                  <div class="timeline-step-number">4</div>
                  <div class="timeline-step-content">
                    <div class="timeline-step-name">Document Verification (DV) & Biometric Matching</div>
                    <div class="timeline-step-desc">Cross-verification of authentic educational certificates, category credentials, Aadhaar biometric verification, and eligibility claims.</div>
                  </div>
                </div>
                <div class="timeline-step-item">
                  <div class="timeline-step-number">5</div>
                  <div class="timeline-step-content">
                    <div class="timeline-step-name">Medical Examination & Final Merit List</div>
                    <div class="timeline-step-desc">Comprehensive medical fitness test by official government medical boards followed by final department cadre allocation.</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Section 6: Exam Pattern & Syllabus -->
            <div id="sec-syllabus" class="detail-section-block">
              <h3 class="detail-section-title"><i class="fa-solid fa-book-open"></i> 6. Detailed Exam Pattern & Syllabus Overview</h3>
              <table class="pattern-table">
                <thead>
                  <tr>
                    <th>Section / Subject</th>
                    <th>Questions</th>
                    <th>Maximum Marks</th>
                    <th>Duration</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>General Intelligence & Reasoning</strong></td>
                    <td>25 Qs</td>
                    <td>50 Marks</td>
                    <td rowspan="4" style="vertical-align: middle; text-align: center; font-weight: 700; background: var(--bg-card);">60 Minutes<br><span style="font-size:0.72rem; color:var(--text-muted); font-weight:500;">(80 Mins for Scribe candidates)</span></td>
                  </tr>
                  <tr>
                    <td><strong>General Awareness & Current Affairs</strong></td>
                    <td>25 Qs</td>
                    <td>50 Marks</td>
                  </tr>
                  <tr>
                    <td><strong>Quantitative Aptitude (Mathematics)</strong></td>
                    <td>25 Qs</td>
                    <td>50 Marks</td>
                  </tr>
                  <tr>
                    <td><strong>English Comprehension & Grammar</strong></td>
                    <td>25 Qs</td>
                    <td>50 Marks</td>
                  </tr>
                  <tr style="background: var(--bg-soft-blue); font-weight: 800;">
                    <td>Total Summary</td>
                    <td>100 Questions</td>
                    <td>200 Marks</td>
                    <td style="text-align: center;">1 Hour</td>
                  </tr>
                </tbody>
              </table>
              <div class="pattern-notes-row">
                <span class="pattern-note-pill"><i class="fa-solid fa-circle-exclamation" style="color: #dc2626;"></i> Negative Marking: 0.50 Marks for each incorrect answer</span>
                <span class="pattern-note-pill"><i class="fa-solid fa-language" style="color: var(--primary-blue);"></i> Question Paper: Bilingual (Hindi and English)</span>
                <span class="pattern-note-pill"><i class="fa-solid fa-calculator"></i> Normalization: Multi-shift normalized score applies</span>
              </div>
            </div>

            <!-- Section 7: How to Apply Guide -->
            <div id="sec-how-to-apply" class="detail-section-block">
              <h3 class="detail-section-title"><i class="fa-solid fa-arrow-pointer"></i> 7. How to Apply Online Step-by-Step (आवेदन प्रक्रिया)</h3>
              <div class="how-to-apply-box">
                <div class="apply-step-row">
                  <span class="apply-step-badge">Step 1</span>
                  <div class="apply-step-text">Visit the official recruitment portal via the direct <strong>Apply Online</strong> link provided in the table below.</div>
                </div>
                <div class="apply-step-row">
                  <span class="apply-step-badge">Step 2</span>
                  <div class="apply-step-text">Complete One Time Registration (OTR) with your basic personal details, valid mobile number, and active email address.</div>
                </div>
                <div class="apply-step-row">
                  <span class="apply-step-badge">Step 3</span>
                  <div class="apply-step-text">Fill out the detailed application form selecting your preferred examination cities and post preferences.</div>
                </div>
                <div class="apply-step-row">
                  <span class="apply-step-badge">Step 4</span>
                  <div class="apply-step-text">Upload your recent passport-sized photograph (taken with white background) and scanned signature in standard JPG format (20KB - 50KB).</div>
                </div>
                <div class="apply-step-row">
                  <span class="apply-step-badge">Step 5</span>
                  <div class="apply-step-text">Review the application preview carefully, pay the online application fee (if applicable), and download a printed copy of the final submitted application for future records.</div>
                </div>
              </div>
            </div>

            <!-- Section 8: Official Links Matrix -->
            <div id="sec-official-links" class="detail-section-block">
              <h3 class="detail-section-title"><i class="fa-solid fa-link"></i> 8. Official Government Recruitment Links</h3>
              <table class="official-links-matrix">
                <tr>
                  <td class="link-title-col">
                    <i class="fa-solid fa-file-pen"></i>
                    <span>Apply Online (Official Registration / Login)</span>
                  </td>
                  <td class="link-action-col">
                    <a href="${job.official_apply_url || job.official_website_url}" target="_blank" class="btn-matrix-action btn-matrix-primary" onclick="JobVaniAPI.trackApplyClick('${job.slug}')">
                      <span>Click Here to Apply</span>
                      <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                  </td>
                </tr>
                <tr>
                  <td class="link-title-col">
                    <i class="fa-regular fa-file-pdf" style="color: #dc2626;"></i>
                    <span>Download Official Detailed Notification (PDF)</span>
                  </td>
                  <td class="link-action-col">
                    <a href="${job.official_notification_url || job.official_website_url}" target="_blank" class="btn-matrix-action btn-matrix-secondary">
                      <span>Download PDF</span>
                      <i class="fa-solid fa-download"></i>
                    </a>
                  </td>
                </tr>
                <tr>
                  <td class="link-title-col">
                    <i class="fa-solid fa-globe" style="color: var(--primary-blue);"></i>
                    <span>Official Department Website</span>
                  </td>
                  <td class="link-action-col">
                    <a href="${job.official_website_url}" target="_blank" class="btn-matrix-action btn-matrix-secondary">
                      <span>Visit Website</span>
                      <i class="fa-solid fa-arrow-right"></i>
                    </a>
                  </td>
                </tr>
                <tr>
                  <td class="link-title-col">
                    <i class="fa-brands fa-whatsapp" style="color: #16a34a;"></i>
                    <span>JobVani WhatsApp Alerts Channel (Instant Notices)</span>
                  </td>
                  <td class="link-action-col">
                    <a href="https://whatsapp.com" target="_blank" class="btn-matrix-action btn-matrix-secondary" style="color: #16a34a; border-color: #86efac;">
                      <span>Join WhatsApp</span>
                      <i class="fa-brands fa-whatsapp"></i>
                    </a>
                  </td>
                </tr>
                <tr>
                  <td class="link-title-col">
                    <i class="fa-brands fa-telegram" style="color: #0284c7;"></i>
                    <span>JobVani Telegram Community (Daily Free PDFs)</span>
                  </td>
                  <td class="link-action-col">
                    <a href="https://t.me" target="_blank" class="btn-matrix-action btn-matrix-secondary" style="color: #0284c7; border-color: #7dd3fc;">
                      <span>Join Telegram</span>
                      <i class="fa-brands fa-telegram"></i>
                    </a>
                  </td>
                </tr>
              </table>
            </div>

            <!-- Section 9: Frequently Asked Questions (FAQs) -->
            <div id="sec-faqs" class="detail-section-block">
              <h3 class="detail-section-title"><i class="fa-regular fa-circle-question"></i> 9. Frequently Asked Questions (FAQs)</h3>
              <div class="faq-accordion-group">
                <div class="faq-item open">
                  <button class="faq-question-btn" onclick="JobVaniApp.toggleFaq(this)">
                    <span>What is the last date to apply online for ${job.title}?</span>
                    <i class="fa-solid fa-chevron-down faq-chevron"></i>
                  </button>
                  <div class="faq-answer-content">
                    The online application portal for ${job.title} will accept submissions until <strong>${job.last_date} (11:59 PM)</strong>. Candidates are advised to apply well before the deadline to avoid last-minute server congestion.
                  </div>
                </div>

                <div class="faq-item">
                  <button class="faq-question-btn" onclick="JobVaniApp.toggleFaq(this)">
                    <span>Is there any application fee for Female and SC/ST candidates?</span>
                    <i class="fa-solid fa-chevron-down faq-chevron"></i>
                  </button>
                  <div class="faq-answer-content">
                    No. As per Government of India recruitment norms, all female candidates, SC, ST, PwBD, and Ex-Servicemen are 100% exempted from paying the examination fee. Only General, OBC, and EWS male candidates pay ${job.application_fee || 'Rs. 100/-'}.
                  </div>
                </div>

                <div class="faq-item">
                  <button class="faq-question-btn" onclick="JobVaniApp.toggleFaq(this)">
                    <span>Can final year appearing candidates apply for this post?</span>
                    <i class="fa-solid fa-chevron-down faq-chevron"></i>
                  </button>
                  <div class="faq-answer-content">
                    Yes. Candidates who have appeared in their final year degree examination are eligible to apply provisionally, provided they acquire the essential qualification certificates before the cut-off date mentioned in the official gazette.
                  </div>
                </div>

                <div class="faq-item">
                  <button class="faq-question-btn" onclick="JobVaniApp.toggleFaq(this)">
                    <span>What is the expected salary and pay scale for this recruitment?</span>
                    <i class="fa-solid fa-chevron-down faq-chevron"></i>
                  </button>
                  <div class="faq-answer-content">
                    Selected candidates are appointed under 7th Central Pay Commission (CPC) Pay Scale: <strong>${job.salary || 'Level-4 to Level-8'}</strong>, including Dearness Allowance (DA), House Rent Allowance (HRA), Transport Allowance (TA), and Government Health Insurance.
                  </div>
                </div>

                <div class="faq-item">
                  <button class="faq-question-btn" onclick="JobVaniApp.toggleFaq(this)">
                    <span>How can I get regular updates on exam dates and admit cards?</span>
                    <i class="fa-solid fa-chevron-down faq-chevron"></i>
                  </button>
                  <div class="faq-answer-content">
                    You can bookmark this page on JobVani, or join our official WhatsApp Alerts Channel and Telegram Community to receive real-time notifications the moment hall tickets and exam schedules are released.
                  </div>
                </div>
              </div>
            </div>

          </div>

          <!-- Right Column: Sticky Sidebar -->
          <aside class="detail-sidebar">
            
            <!-- Sticky Quick Apply Card -->
            <div class="sidebar-sticky-apply-card">
              <span class="sidebar-card-badge"><i class="fa-solid fa-circle-dot"></i> Open Recruitment</span>
              
              <div class="sidebar-vacancies-stat">
                <div>
                  <span style="font-size:0.75rem; color:var(--text-muted); display:block;">Total Posts</span>
                  <span class="sidebar-stat-number">${job.vacancies}</span>
                </div>
                <div style="text-align:right;">
                  <span style="font-size:0.75rem; color:var(--text-muted); display:block;">Deadline</span>
                  <span style="font-size:0.92rem; font-weight:800; color:#dc2626;">${job.last_date}</span>
                </div>
              </div>

              <a href="${job.official_apply_url || job.official_website_url}" target="_blank" class="btn-sidebar-apply-full" onclick="JobVaniAPI.trackApplyClick('${job.slug}')">
                <span>Apply Online Now</span>
                <i class="fa-solid fa-arrow-up-right-from-square"></i>
              </a>

              <a href="${job.official_notification_url || job.official_website_url}" target="_blank" class="btn-detail-cta-pdf" style="height:42px; justify-content:center;">
                <i class="fa-regular fa-file-pdf"></i>
                <span>Download Official PDF</span>
              </a>

              <div style="display:flex; align-items:center; gap:8px;">
                <button class="btn-detail-tool btn-wa-detail" style="flex:1; justify-content:center;" onclick="JobVaniApp.shareWhatsApp('${job.title.replace(/'/g, "\\'")}', '${job.slug}')">
                  <i class="fa-brands fa-whatsapp" style="color:#16a34a;"></i>
                  <span>WhatsApp</span>
                </button>
                <button class="btn-detail-tool" style="flex:1; justify-content:center;" onclick="JobVaniApp.copyJobLink('${job.slug}', this)">
                  <i class="fa-regular fa-copy"></i>
                  <span>Copy</span>
                </button>
              </div>
            </div>

            <!-- Aspirants Community Card -->
            <div class="sidebar-community-card">
              <div class="sidebar-comm-title"><i class="fa-solid fa-bell"></i> Never Miss An Update</div>
              <p class="sidebar-comm-sub">Join 85,000+ students on Telegram & WhatsApp for free PDF notifications and exam alerts.</p>
              <div class="sidebar-comm-btns">
                <a href="https://t.me" target="_blank" class="btn-sidebar-tg"><i class="fa-brands fa-telegram"></i> Telegram</a>
                <a href="https://whatsapp.com" target="_blank" class="btn-sidebar-wa"><i class="fa-brands fa-whatsapp"></i> WhatsApp</a>
              </div>
            </div>

            <!-- Trending Jobs Widget -->
            <div class="sidebar-card">
              <h4 class="sidebar-title"><i class="fa-solid fa-fire" style="color:#ef4444; margin-right:6px;"></i> Trending Recruitments</h4>
              <div id="detail-sidebar-trending" class="ranked-job-list"></div>
            </div>

            <!-- Closing Soon Widget -->
            <div class="sidebar-card">
              <h4 class="sidebar-title"><i class="fa-solid fa-hourglass-half" style="color:#f59e0b; margin-right:6px;"></i> Closing Soon</h4>
              <div id="detail-sidebar-closing" class="ranked-job-list"></div>
            </div>

          </aside>
        </div>
      </div>
    `;

    // Immediately reset scroll to top of page
    window.scrollTo(0, 0);
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;

    // Populate sidebar trending and closing soon
    const trending = await JobVaniAPI.getTrending();
    const trendingBox = document.getElementById('detail-sidebar-trending');
    if (trendingBox && trending) {
      trendingBox.innerHTML = trending.slice(0, 4).map((item, idx) => `
        <div class="ranked-job-item" onclick="window.location.hash = '#jobs/${item.slug}'">
          <div class="ranked-left">
            <span class="rank-number">${idx + 1}</span>
            <div class="ranked-details">
              <span class="ranked-title">${item.title}</span>
              <span class="ranked-sub">${item.organization}</span>
            </div>
          </div>
          <span class="status-pill-badge badge-new">${item.status_badge || 'Hot'}</span>
        </div>
      `).join('');
    }

    const closing = await JobVaniAPI.getClosingSoon();
    const closingBox = document.getElementById('detail-sidebar-closing');
    if (closingBox && closing) {
      closingBox.innerHTML = closing.slice(0, 4).map((item, idx) => `
        <div class="ranked-job-item" onclick="window.location.hash = '#jobs/${item.slug}'">
          <div class="ranked-left">
            <span class="rank-number closing-rank">${idx + 1}</span>
            <div class="ranked-details">
              <span class="ranked-title">${item.title}</span>
              <span class="ranked-sub">Last Date: ${item.last_date}</span>
            </div>
          </div>
          <span class="status-pill-badge badge-urgent">${item.urgency_badge}</span>
        </div>
      `).join('');
    }
  },

  // FAQ Accordion Toggle
  toggleFaq(btnEl) {
    const parent = btnEl.closest('.faq-item');
    if (parent) {
      parent.classList.toggle('open');
    }
  },

  // Interactive Age Eligibility Checker
  checkAgeEligibility(minAge, maxAge) {
    const yearInput = document.getElementById('calc-birth-year');
    const catSelect = document.getElementById('calc-category-select');
    const resultBox = document.getElementById('age-calc-result-box');
    if (!yearInput || !resultBox) return;

    const birthYear = parseInt(yearInput.value);
    if (!birthYear || birthYear < 1960 || birthYear > 2026) {
      resultBox.style.display = 'block';
      resultBox.style.color = '#dc2626';
      resultBox.textContent = 'Please enter a valid 4-digit birth year (e.g. 1998)';
      return;
    }

    const currentYear = 2026;
    const approxAge = currentYear - birthYear;
    let allowedMax = maxAge;
    const cat = catSelect ? catSelect.value : 'gen';

    if (cat === 'obc') allowedMax += 3;
    else if (cat === 'scst') allowedMax += 5;
    else if (cat === 'pwd') allowedMax += 10;

    resultBox.style.display = 'block';
    if (approxAge >= minAge && approxAge <= allowedMax) {
      resultBox.style.color = '#16a34a';
      resultBox.innerHTML = `✅ Eligible! Your age is approximately <strong>${approxAge} years</strong>. You are within the allowed range of <strong>${minAge} to ${allowedMax} years</strong> for your selected category.`;
    } else if (approxAge < minAge) {
      resultBox.style.color = '#dc2626';
      resultBox.innerHTML = `❌ Underage: Your age is approximately <strong>${approxAge} years</strong>. The minimum age required is <strong>${minAge} years</strong>.`;
    } else {
      resultBox.style.color = '#dc2626';
      resultBox.innerHTML = `❌ Overage: Your age is approximately <strong>${approxAge} years</strong>. The maximum age permitted for your category is <strong>${allowedMax} years</strong>.`;
    }
  },

  // Admit Cards View
  async renderAdmitCardsView() {
    const view = document.getElementById('general-section-container');
    if (!view) return;
    view.classList.add('active');

    const items = await JobVaniAPI.getAdmitCards();
    view.innerHTML = `
      <div class="container">
        <div class="section-title-row" style="margin-bottom: 30px;">
          <h1 class="section-main-heading"><span class="heading-blue-dot"></span> Latest Admit Cards (Hall Tickets)</h1>
        </div>
        <div class="jobs-four-col-grid">
          ${items.map(item => {
            const badge = this.getOrgBadge(item.organization, item.category);
            return `
              <div class="job-card">
                <div class="job-card-top">
                  <div class="job-org-badge" style="background: ${badge.bg}; color: ${badge.color};">
                    ${badge.icon}
                  </div>
                  <div class="job-header-info">
                    <div class="job-pill-row">
                      <span class="pill-govt-verified"><i class="fa-solid fa-check" style="font-size:0.6rem;"></i> Verified</span>
                      <span class="pill-sector-tag">${item.category || 'Admit Card'}</span>
                    </div>
                    <p class="job-card-org" title="${item.organization}">${item.organization}</p>
                  </div>
                </div>

                <h3 class="job-card-title" title="${item.exam_name}">${item.exam_name}</h3>

                <div class="job-chips-grid">
                  <div class="chip-item">
                    <i class="fa-regular fa-calendar-check"></i>
                    <span>Release: ${item.release_date}</span>
                  </div>
                  <div class="chip-item chip-vacancies">
                    <i class="fa-regular fa-clock"></i>
                    <span>Exam: ${item.exam_date}</span>
                  </div>
                </div>

                <div class="job-meta-bar">
                  <div class="meta-salary" style="color: #059669;">
                    <i class="fa-solid fa-circle-check"></i>
                    <span>${item.status || 'Available Now'}</span>
                  </div>
                </div>

                <div class="job-card-actions">
                  <a href="${item.download_url}" target="_blank" class="btn-card-apply" style="flex:1;">
                    <i class="fa-solid fa-download" style="font-size:0.75rem;"></i>
                    <span>Download Hall Ticket</span>
                  </a>
                  ${item.official_website_url ? `
                  <a href="${item.official_website_url}" target="_blank" class="btn-card-secondary" title="Official Website">
                    <i class="fa-solid fa-globe"></i>
                  </a>
                  ` : ''}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  },

  // Results View
  async renderResultsView() {
    const view = document.getElementById('general-section-container');
    if (!view) return;
    view.classList.add('active');

    const items = await JobVaniAPI.getResults();
    view.innerHTML = `
      <div class="container">
        <div class="section-title-row" style="margin-bottom: 30px;">
          <h1 class="section-main-heading"><span class="heading-blue-dot"></span> Declared Examination Results & Merit Lists</h1>
        </div>
        <div class="jobs-four-col-grid">
          ${items.map(item => {
            const badge = this.getOrgBadge(item.organization, item.exam_stage);
            return `
              <div class="job-card">
                <div class="job-card-top">
                  <div class="job-org-badge" style="background: ${badge.bg}; color: ${badge.color};">
                    ${badge.icon}
                  </div>
                  <div class="job-header-info">
                    <div class="job-pill-row">
                      <span class="pill-govt-verified"><i class="fa-solid fa-check" style="font-size:0.6rem;"></i> Verified Result</span>
                      <span class="pill-sector-tag">${item.exam_stage || 'Final'}</span>
                    </div>
                    <p class="job-card-org" title="${item.organization}">${item.organization}</p>
                  </div>
                </div>

                <h3 class="job-card-title" title="${item.exam_name}">${item.exam_name}</h3>

                <div class="job-chips-grid">
                  <div class="chip-item chip-vacancies">
                    <i class="fa-regular fa-calendar-check"></i>
                    <span>Declared: ${item.result_date}</span>
                  </div>
                  <div class="chip-item chip-qual">
                    <i class="fa-solid fa-award"></i>
                    <span>${item.exam_stage || 'Score Card'}</span>
                  </div>
                </div>

                <div class="job-meta-bar">
                  <div class="meta-salary" style="color: #059669;">
                    <i class="fa-solid fa-square-poll-vertical"></i>
                    <span>${item.status || 'Declared (PDF)'}</span>
                  </div>
                </div>

                <div class="job-card-actions">
                  <a href="${item.view_result_url}" target="_blank" class="btn-card-apply" style="flex:1;">
                    <i class="fa-solid fa-file-arrow-down" style="font-size:0.75rem;"></i>
                    <span>Check Result / PDF</span>
                  </a>
                  ${item.official_website_url ? `
                  <a href="${item.official_website_url}" target="_blank" class="btn-card-secondary" title="Official Website">
                    <i class="fa-solid fa-globe"></i>
                  </a>
                  ` : ''}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  },

  // Answer Keys View
  async renderAnswerKeysView() {
    const view = document.getElementById('general-section-container');
    if (!view) return;
    view.classList.add('active');

    const items = await JobVaniAPI.getAnswerKeys();
    view.innerHTML = `
      <div class="container">
        <div class="section-title-row" style="margin-bottom: 30px;">
          <h1 class="section-main-heading"><span class="heading-blue-dot"></span> Official Answer Keys & Objection Portals</h1>
        </div>
        <div class="jobs-four-col-grid">
          ${items.map(item => {
            const badge = this.getOrgBadge(item.organization, '');
            return `
              <div class="job-card">
                <div class="job-card-top">
                  <div class="job-org-badge" style="background: ${badge.bg}; color: ${badge.color};">
                    ${badge.icon}
                  </div>
                  <div class="job-header-info">
                    <div class="job-pill-row">
                      <span class="pill-govt-verified"><i class="fa-solid fa-check" style="font-size:0.6rem;"></i> Official Key</span>
                      <span class="pill-sector-tag">${item.challenge_window || 'Active'}</span>
                    </div>
                    <p class="job-card-org" title="${item.organization}">${item.organization}</p>
                  </div>
                </div>

                <h3 class="job-card-title" title="${item.exam_name}">${item.exam_name}</h3>

                <div class="job-chips-grid">
                  <div class="chip-item">
                    <i class="fa-regular fa-clock"></i>
                    <span>Exam: ${item.exam_date}</span>
                  </div>
                  <div class="chip-item chip-vacancies">
                    <i class="fa-regular fa-calendar-check"></i>
                    <span>Released: ${item.release_date}</span>
                  </div>
                </div>

                <div class="job-meta-bar">
                  <div class="meta-salary" style="color: #0284c7;">
                    <i class="fa-solid fa-shield-halved"></i>
                    <span>Objection Window Active</span>
                  </div>
                </div>

                <div class="job-card-actions">
                  <a href="${item.download_url}" target="_blank" class="btn-card-apply" style="flex:1;">
                    <i class="fa-solid fa-key" style="font-size:0.75rem;"></i>
                    <span>Download Key (PDF)</span>
                  </a>
                  ${item.official_notice_url ? `
                  <a href="${item.official_notice_url}" target="_blank" class="btn-card-secondary" title="Official Website">
                    <i class="fa-solid fa-globe"></i>
                  </a>
                  ` : ''}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  },

  // Syllabus View
  async renderSyllabusView() {
    const view = document.getElementById('general-section-container');
    if (!view) return;
    view.classList.add('active');

    const items = await JobVaniAPI.getSyllabus();
    view.innerHTML = `
      <div class="container">
        <div class="section-title-row" style="margin-bottom: 30px;">
          <h1 class="section-main-heading"><span class="heading-blue-dot"></span> Exam Syllabus & Patterns</h1>
        </div>
        <div class="jobs-four-col-grid">
          ${items.map(item => `
            <div class="job-card">
              <div class="job-card-top">
                <div class="org-logo-circle">
                  <img src="${this.getOrgLogo('', item.category)}" class="org-logo-img" alt="${item.category}">
                </div>
                <div class="job-header-text">
                  <h3 class="job-card-title">${item.exam_name}</h3>
                  <p class="job-card-org">${item.category}</p>
                </div>
              </div>
              <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 16px;">${item.overview}</p>
              <div class="job-card-actions">
                <a href="${item.pdf_download_url}" target="_blank" class="btn-apply-now" style="width: 100%; text-align: center;">View Syllabus PDF</a>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  },

  // Current Affairs View
  async renderCurrentAffairsView() {
    const view = document.getElementById('general-section-container');
    if (!view) return;
    view.classList.add('active');

    const items = await JobVaniAPI.getCurrentAffairs();
    view.innerHTML = `
      <div class="container">
        <div class="section-title-row" style="margin-bottom: 30px;">
          <h1 class="section-main-heading"><span class="heading-blue-dot"></span> Daily Current Affairs & Exam GK</h1>
        </div>
        <div style="display: flex; flex-direction: column; gap: 20px;">
          ${items.map(item => `
            <div class="job-card" style="padding: 24px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                <span class="status-pill-badge badge-new">${item.category}</span>
                <span style="font-size: 0.8rem; color: var(--text-muted);"><i class="fa-regular fa-calendar"></i> ${item.date}</span>
              </div>
              <h2 style="font-size: 1.25rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">${item.title}</h2>
              <p style="color: var(--text-muted); font-size: 0.92rem; line-height: 1.6;">${item.content}</p>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  },

  // Saved Jobs View
  async renderSavedJobsView() {
    const view = document.getElementById('general-section-container');
    if (!view) return;
    view.classList.add('active');

    const bookmarks = await JobVaniAPI.getBookmarks();
    view.innerHTML = `
      <div class="container">
        <div class="section-title-row" style="margin-bottom: 30px;">
          <h1 class="section-main-heading"><span class="heading-blue-dot"></span> Saved Government Jobs (${bookmarks.length})</h1>
        </div>
        ${bookmarks.length === 0 ? '<p style="text-align: center; padding: 60px; color: var(--text-muted);">You have not bookmarked any jobs yet. Click the bookmark icon on any job card to save it here!</p>' : `
          <div class="jobs-four-col-grid">
            ${bookmarks.map(job => `
              <article class="job-card">
                <div class="job-card-top">
                  <div class="org-logo-circle">
                    <img src="${this.getOrgLogo(job.organization, job.category)}" class="org-logo-img" alt="${job.organization}">
                  </div>
                  <div class="job-header-text">
                    <h3 class="job-card-title" onclick="window.location.hash = '#jobs/${job.slug}'">${job.title}</h3>
                    <p class="job-card-org">${job.organization}</p>
                  </div>
                </div>
                <div class="job-specs-list">
                  <div class="spec-row"><span class="spec-label">Vacancies:</span><span class="spec-val">${job.vacancies}</span></div>
                  <div class="spec-row"><span class="spec-label">Last Date:</span><span class="spec-val">${job.last_date}</span></div>
                </div>
                <div class="job-card-actions">
                  <button class="btn-view-details" onclick="window.location.hash = '#jobs/${job.slug}'">View Details</button>
                  <a href="${job.official_apply_url || job.official_website_url}" target="_blank" class="btn-apply-now">Apply Now</a>
                </div>
              </article>
            `).join('')}
          </div>
        `}
      </div>
    `;
  },

  // Admin Dashboard
  async renderAdminDashboard() {
    const adminView = document.getElementById('admin-dashboard-container');
    if (!adminView) return;
    adminView.classList.add('active');

    const stats = await JobVaniAPI.getAdminOverview();
    const jobs = await JobVaniAPI.getJobs({ limit: 50 });

    adminView.innerHTML = `
      <div class="container">
        <div class="admin-header-row">
          <div class="admin-title-col">
            <h1>JobVani Admin Command Center</h1>
            <p>Monitor live statistics, trigger auto-scrapers, and manage government recruitments.</p>
          </div>
          <div class="admin-actions-bar">
            <button id="btn-trigger-scraper" class="btn-run-scraper" onclick="JobVaniApp.triggerScraperFromAdmin()">
              <i class="fa-solid fa-arrows-rotate"></i>
              <span>Run Auto-Pilot Scraper</span>
            </button>
            <button class="btn-admin-add" onclick="document.getElementById('admin-add-job-modal').classList.add('active')">
              <i class="fa-solid fa-plus"></i> Post Job
            </button>
          </div>
        </div>

        <!-- Stat Cards -->
        <div class="admin-stats-grid">
          <div class="admin-stat-card">
            <span class="stat-card-label">Total Jobs Ingested</span>
            <span class="stat-card-value">${stats ? stats.total_jobs : 0}</span>
          </div>
          <div class="admin-stat-card">
            <span class="stat-card-label">Total Job Views</span>
            <span class="stat-card-value">${stats ? stats.total_views.toLocaleString() : 0}</span>
          </div>
          <div class="admin-stat-card">
            <span class="stat-card-label">Apply Button Clicks</span>
            <span class="stat-card-value">${stats ? stats.total_clicks.toLocaleString() : 0}</span>
          </div>
          <div class="admin-stat-card">
            <span class="stat-card-label">Newsletter Subscribers</span>
            <span class="stat-card-value">${stats ? stats.total_subscribers : 0}</span>
          </div>
        </div>

        <!-- Jobs Management Table -->
        <div class="admin-table-card">
          <h3>Manage Active Recruitments (${jobs.length})</h3>
          <table class="admin-jobs-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Organization</th>
                <th>Category</th>
                <th>Last Date</th>
                <th>Views</th>
                <th>Clicks</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              ${jobs.map(j => `
                <tr>
                  <td><strong>${j.title}</strong></td>
                  <td>${j.organization}</td>
                  <td>${j.category}</td>
                  <td>${j.last_date}</td>
                  <td>${j.views_count}</td>
                  <td>${j.apply_clicks}</td>
                  <td>
                    <button class="btn-delete-row" onclick="JobVaniApp.deleteJobFromAdmin(${j.id})"><i class="fa-solid fa-trash-can"></i></button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  async triggerScraperFromAdmin() {
    const btn = document.getElementById('btn-trigger-scraper');
    if (btn) {
      btn.classList.add('running');
      btn.querySelector('span').textContent = 'Scraping Live Web...';
    }

    this.showToast('🚀 Auto-Pilot Scraper launched in background...');

    const res = await JobVaniAPI.runScraper();
    if (btn) {
      btn.classList.remove('running');
      btn.querySelector('span').textContent = 'Run Auto-Pilot Scraper';
    }

    if (res && res.status === 'success') {
      const j = res.total_new_jobs !== undefined ? res.total_new_jobs : (res.new_jobs_added || 0);
      const a = res.total_new_admit_cards || 0;
      const r = res.total_new_results || 0;
      const k = res.total_new_answer_keys || 0;
      this.showToast(`✅ Ingestion Complete: +${j} Jobs, +${a} Admit Cards, +${r} Results, +${k} Keys!`);
      this.renderAdminDashboard();
    } else {
      this.showToast('Notice: Scraper completed sync with official portals.');
      this.renderAdminDashboard();
    }
  },

  async deleteJobFromAdmin(id) {
    if (!confirm('Are you sure you want to delete this job recruitment?')) return;
    await JobVaniAPI.deleteJob(id);
    this.showToast('Job removed from database.');
    this.renderAdminDashboard();
  },

  // Bookmarking & Saved
  async loadSavedBookmarks() {
    const list = await JobVaniAPI.getBookmarks();
    if (list) {
      this.savedJobIds = new Set(list.map(j => j.id));
      const badge = document.getElementById('saved-badge-count');
      if (badge) badge.textContent = this.savedJobIds.size;
    }
  },

  async toggleBookmarkAction(jobId, btnEl) {
    const res = await JobVaniAPI.toggleBookmark(jobId);
    if (res) {
      if (res.is_bookmarked) {
        this.savedJobIds.add(jobId);
        this.showToast('Saved to your private library! 🔖');
        if (btnEl) {
          btnEl.classList.add('bookmarked');
          btnEl.innerHTML = '<i class="fa-solid fa-bookmark"></i><span>Saved</span>';
        }
      } else {
        this.savedJobIds.delete(jobId);
        this.showToast('Removed from saved jobs.');
        if (btnEl) {
          btnEl.classList.remove('bookmarked');
          btnEl.innerHTML = '<i class="fa-regular fa-bookmark"></i><span>Save</span>';
        }
      }
      const badge = document.getElementById('saved-badge-count');
      if (badge) badge.textContent = this.savedJobIds.size;
    }
  },

  // Global search & instant autocomplete
  bindGlobalEvents() {
    const searchInput = document.getElementById('global-search-input');
    const heroDropdown = document.getElementById('hero-instant-search-dropdown');
    const searchDrawer = document.getElementById('search-drawer');
    const backdrop = document.getElementById('search-backdrop');

    if (searchInput) {
      let timeout = null;
      searchInput.addEventListener('input', (e) => {
        clearTimeout(timeout);
        const query = e.target.value.trim();
        if (query.length < 2) {
          if (heroDropdown) heroDropdown.classList.remove('active');
          if (searchDrawer) searchDrawer.classList.remove('active');
          if (backdrop) backdrop.classList.remove('active');
          return;
        }

        timeout = setTimeout(async () => {
          const results = await JobVaniAPI.searchGlobal(query);
          this.renderInstantDropdown(results);
        }, 150);
      });

      searchInput.addEventListener('focus', () => {
        if (searchInput.value.trim().length >= 2) {
          if (heroDropdown) heroDropdown.classList.add('active');
        }
      });
    }

    // Click outside to close instant dropdown
    document.addEventListener('click', (e) => {
      if (heroDropdown && !e.target.closest('.hero-search-wrapper')) {
        heroDropdown.classList.remove('active');
      }
    });

    if (backdrop) {
      backdrop.addEventListener('click', () => {
        if (searchDrawer) searchDrawer.classList.remove('active');
        backdrop.classList.remove('active');
      });
    }

    // Keyboard shortcut (Ctrl + K or /)
    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey && e.key.toLowerCase() === 'k') || (e.key === '/' && document.activeElement.tagName !== 'INPUT')) {
        e.preventDefault();
        searchInput?.focus();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      if (e.key === 'Escape') {
        if (heroDropdown) heroDropdown.classList.remove('active');
        if (searchDrawer) searchDrawer.classList.remove('active');
        if (backdrop) backdrop.classList.remove('active');
      }
    });

    // Category pills filter
    document.querySelectorAll('.category-nav-card').forEach(card => {
      card.addEventListener('click', (e) => {
        document.querySelectorAll('.category-nav-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        const cat = card.dataset.category || 'All Jobs';
        this.currentCategory = cat;
        this.loadLatestJobsGrid();
        const target = document.getElementById('latest-jobs');
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });

    // Newsletter subscription form
    const newsForm = document.getElementById('newsletter-form-box');
    if (newsForm) {
      newsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = document.getElementById('newsletter-email-input');
        if (!input || !input.value) return;
        await JobVaniAPI.subscribe(input.value);
        this.showToast('Subscribed! You will receive instant job alerts. 📬');
        input.value = '';
      });
    }
  },

  renderInstantDropdown(res) {
    const dropdown = document.getElementById('hero-instant-search-dropdown');
    if (!dropdown || !res) return;

    dropdown.classList.add('active');

    if (res.total_matches === 0) {
      dropdown.innerHTML = '<p style="color: var(--text-muted); font-size: 0.86rem; padding: 12px; text-align: center;">No matching government recruitments or admit cards found.</p>';
      return;
    }

    let html = '';
    if (res.jobs && res.jobs.length > 0) {
      html += '<div class="instant-group-title"><i class="fa-solid fa-briefcase" style="margin-right: 4px;"></i> Government Jobs</div>';
      html += res.jobs.map(j => {
        const logo = this.getOrgLogo(j.subtitle, j.category);
        return `
          <div class="instant-hit-row" onclick="window.location.hash='#jobs/${j.slug}'; document.getElementById('hero-instant-search-dropdown').classList.remove('active');">
            <div class="instant-hit-left">
              <div class="instant-hit-logo">
                <img src="${logo}" alt="${j.subtitle}">
              </div>
              <div class="instant-hit-text">
                <div class="instant-hit-title">${j.title}</div>
                <div class="instant-hit-sub">${j.subtitle} &bull; <span style="color: var(--primary-blue); font-weight: 600;">${j.category}</span></div>
              </div>
            </div>
            <span class="status-pill-badge badge-new" style="font-size: 0.68rem;">View</span>
          </div>
        `;
      }).join('');
    }

    if (res.admit_cards && res.admit_cards.length > 0) {
      html += '<div class="instant-group-title" style="color: #16a34a; margin-top: 10px;"><i class="fa-regular fa-id-card" style="margin-right: 4px;"></i> Admit Cards</div>';
      html += res.admit_cards.map(a => `
        <div class="instant-hit-row" onclick="window.location.hash='#admit-card'; document.getElementById('hero-instant-search-dropdown').classList.remove('active');">
          <div class="instant-hit-left">
            <div class="instant-hit-text">
              <div class="instant-hit-title">${a.title}</div>
              <div class="instant-hit-sub">Exam Date: ${a.meta} &bull; ${a.subtitle}</div>
            </div>
          </div>
          <span class="status-pill-badge badge-urgent" style="font-size: 0.68rem;">Hall Ticket</span>
        </div>
      `).join('');
    }

    if (res.results && res.results.length > 0) {
      html += '<div class="instant-group-title" style="color: #9333ea; margin-top: 10px;"><i class="fa-solid fa-chart-line" style="margin-right: 4px;"></i> Declared Results</div>';
      html += res.results.map(r => `
        <div class="instant-hit-row" onclick="window.location.hash='#results'; document.getElementById('hero-instant-search-dropdown').classList.remove('active');">
          <div class="instant-hit-left">
            <div class="instant-hit-text">
              <div class="instant-hit-title">${r.title}</div>
              <div class="instant-hit-sub">Announced: ${r.meta} &bull; ${r.subtitle}</div>
            </div>
          </div>
          <span class="status-pill-badge badge-popular" style="font-size: 0.68rem;">Result</span>
        </div>
      `).join('');
    }

    dropdown.innerHTML = html;
  },

  showToast(message) {
    let container = document.getElementById('toast-box');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-box';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'jobvani-toast';
    toast.innerHTML = `<i class="fa-solid fa-circle-check" style="color: #0284c7;"></i><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => toast.remove(), 3500);
  }
};

// Start application
document.addEventListener('DOMContentLoaded', () => {
  window.JobVaniApp = JobVaniApp;
  JobVaniApp.init();
});
