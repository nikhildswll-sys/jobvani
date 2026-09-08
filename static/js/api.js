/**
 * JobVani - Client API Fetch Services
 */

const JobVaniAPI = {
  baseUrl: '',

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...(options.headers || {})
        },
        ...options
      });
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      return await response.json();
    } catch (err) {
      console.warn(`Error connecting to ${endpoint}:`, err);
      return null;
    }
  },

  getSettings() {
    return this.request('/api/settings');
  },

  getJobs(filters = {}) {
    const params = new URLSearchParams();
    if (filters.category) params.append('category', filters.category);
    if (filters.qualification) params.append('qualification', filters.qualification);
    if (filters.job_type) params.append('job_type', filters.job_type);
    if (filters.sort) params.append('sort', filters.sort);
    if (filters.limit) params.append('limit', filters.limit);
    return this.request(`/api/jobs?${params.toString()}`);
  },

  getJobBySlug(slug) {
    return this.request(`/api/jobs/${slug}`);
  },

  getTrending() {
    return this.request('/api/trending');
  },

  getClosingSoon() {
    return this.request('/api/closing-soon');
  },

  getAdmitCards(category = null) {
    const q = category ? `?category=${encodeURIComponent(category)}` : '';
    return this.request(`/api/admit-cards${q}`);
  },

  getResults() {
    return this.request('/api/results');
  },

  getAnswerKeys() {
    return this.request('/api/answer-keys');
  },

  getSyllabus(category = null) {
    const q = category ? `?category=${encodeURIComponent(category)}` : '';
    return this.request(`/api/syllabus${q}`);
  },

  getCurrentAffairs(period = null, category = null) {
    const params = new URLSearchParams();
    if (period) params.append('period', period);
    if (category) params.append('category', category);
    return this.request(`/api/current-affairs?${params.toString()}`);
  },

  searchGlobal(query) {
    return this.request(`/api/search?q=${encodeURIComponent(query)}`);
  },

  trackApplyClick(slug) {
    return this.request(`/api/jobs/${slug}/apply-click`, { method: 'POST' });
  },

  toggleBookmark(jobId) {
    return this.request('/api/bookmarks/toggle', {
      method: 'POST',
      body: JSON.stringify({ job_id: jobId, user_id: 'guest' })
    });
  },

  getBookmarks() {
    return this.request('/api/bookmarks?user_id=guest');
  },

  subscribe(email) {
    return this.request('/api/subscribe', {
      method: 'POST',
      body: JSON.stringify({ email })
    });
  },

  runScraper() {
    return this.request('/api/scraper/run', { method: 'POST' });
  },

  getAdminOverview() {
    return this.request('/api/admin/overview');
  },

  createJob(jobData) {
    return this.request('/api/jobs', {
      method: 'POST',
      body: JSON.stringify(jobData)
    });
  },

  deleteJob(jobId) {
    return this.request(`/api/jobs/${jobId}`, {
      method: 'DELETE'
    });
  }
};
