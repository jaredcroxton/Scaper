/* ==========================================================================
   SCAPER - Dashboard Application
   ========================================================================== */

(function () {
  'use strict';

  // ── State ──────────────────────────────────────────────────────────
  const state = {
    articles: [],
    savedIds: new Set(),
    currentView: 'dashboard',   // 'dashboard' | 'saved'
    currentSource: 'all',
    currentSort: 'date',
    searchQuery: '',
    lastUpdated: null,
  };

  // ── DOM Refs ───────────────────────────────────────────────────────
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  const els = {
    sidebar: $('#sidebar'),
    sidebarToggle: $('#sidebarToggle'),
    mobileMenu: $('#mobileMenu'),
    searchInput: $('#searchInput'),
    refreshBtn: $('#refreshBtn'),
    articlesGrid: $('#articlesGrid'),
    loadingState: $('#loadingState'),
    emptyState: $('#emptyState'),
    modalOverlay: $('#modalOverlay'),
    modalContent: $('#modalContent'),
    modalClose: $('#modalClose'),
    toastContainer: $('#toastContainer'),
    savedCount: $('#savedCount'),
    viewTitle: $('#viewTitle'),
    // Stats
    statTotal: $('#statTotal'),
    statSources: $('#statSources'),
    statSourceNames: $('#statSourceNames'),
    statSaved: $('#statSaved'),
    statTopScore: $('#statTopScore'),
    statTopSub: $('#statTopSub'),
    lastUpdated: $('#lastUpdated'),
  };

  // ── Helpers ────────────────────────────────────────────────────────
  function timeAgo(dateStr) {
    const now = new Date();
    const date = new Date(dateStr);
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return 'just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  }

  function formatNumber(n) {
    if (n === null || n === undefined) return '';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
    return n.toString();
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ── LocalStorage ───────────────────────────────────────────────────
  function loadSaved() {
    try {
      const data = JSON.parse(localStorage.getItem('scaper_saved_articles') || '[]');
      state.savedIds = new Set(data.map((s) => s.id));
    } catch {
      state.savedIds = new Set();
    }
  }

  function persistSaved() {
    const arr = Array.from(state.savedIds).map((id) => ({
      id,
      saved_at: new Date().toISOString(),
    }));
    localStorage.setItem('scaper_saved_articles', JSON.stringify(arr));
  }

  function toggleSave(articleId) {
    if (state.savedIds.has(articleId)) {
      state.savedIds.delete(articleId);
      showToast('Article removed from saved', 'info');
    } else {
      state.savedIds.add(articleId);
      showToast('Article saved!', 'success');
    }
    persistSaved();
    updateSavedCount();
    renderArticles();
  }

  // ── Data Loading ───────────────────────────────────────────────────
  async function loadArticles() {
    els.loadingState.style.display = '';
    els.emptyState.style.display = 'none';

    try {
      const resp = await fetch('../data/articles.json?t=' + Date.now());
      if (!resp.ok) throw new Error('Data not found');
      const data = await resp.json();

      state.articles = data.articles || [];
      state.lastUpdated = data.last_updated;

      updateStats(data);
      renderArticles();
      els.lastUpdated.textContent = 'Updated ' + timeAgo(data.last_updated);
    } catch (e) {
      console.warn('Could not load articles:', e.message);
      // Show demo/empty state
      state.articles = [];
      els.loadingState.style.display = 'none';
      els.emptyState.style.display = '';
      els.lastUpdated.textContent = 'No data yet';
    }
  }

  // ── Stats ──────────────────────────────────────────────────────────
  function updateStats(data) {
    animateNumber(els.statTotal, data.total_articles || 0);
    animateNumber(els.statSources, (data.sources_scraped || []).length);
    els.statSourceNames.textContent = (data.sources_scraped || []).join(', ') || '-';
    animateNumber(els.statSaved, state.savedIds.size);

    const topArticle = state.articles.reduce(
      (top, a) => (a.score !== null && a.score > (top.score || 0) ? a : top),
      { score: 0 }
    );
    animateNumber(els.statTopScore, topArticle.score || 0);
    if (topArticle.source) {
      els.statTopSub.textContent = topArticle.source;
    }
  }

  function updateSavedCount() {
    els.savedCount.textContent = state.savedIds.size;
    els.statSaved.textContent = state.savedIds.size;
  }

  function animateNumber(el, target) {
    const start = parseInt(el.textContent) || 0;
    if (start === target) { el.textContent = target; return; }

    const duration = 500;
    const startTime = performance.now();

    function tick(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
      el.textContent = Math.round(start + (target - start) * eased);
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // ── Filtering ──────────────────────────────────────────────────────
  function getFilteredArticles() {
    let articles = [...state.articles];

    // View filter
    if (state.currentView === 'saved') {
      articles = articles.filter((a) => state.savedIds.has(a.id));
    }

    // Source filter
    if (state.currentSource !== 'all') {
      if (state.currentSource === 'reddit') {
        articles = articles.filter((a) => a.source_type === 'reddit');
      } else if (state.currentSource === 'newsletter') {
        articles = articles.filter((a) => a.source_type === 'newsletter');
      } else {
        articles = articles.filter((a) => a.source === state.currentSource);
      }
    }

    // Search filter
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      articles = articles.filter(
        (a) =>
          a.title.toLowerCase().includes(q) ||
          (a.summary && a.summary.toLowerCase().includes(q)) ||
          a.source.toLowerCase().includes(q)
      );
    }

    // Sort
    if (state.currentSort === 'score') {
      articles.sort((a, b) => (b.score || 0) - (a.score || 0));
    } else {
      articles.sort((a, b) => new Date(b.published_at) - new Date(a.published_at));
    }

    return articles;
  }

  // ── Render ─────────────────────────────────────────────────────────
  function renderArticles() {
    const articles = getFilteredArticles();

    els.loadingState.style.display = 'none';

    if (articles.length === 0) {
      els.articlesGrid.innerHTML = '';
      els.emptyState.style.display = '';
      return;
    }

    els.emptyState.style.display = 'none';

    const html = articles
      .map(
        (a) => `
      <article class="article-card ${state.savedIds.has(a.id) ? 'saved' : ''}" data-id="${escapeHtml(a.id)}">
        <div class="card-top">
          <span class="source-badge ${a.source_type === 'reddit' ? 'reddit' : 'newsletter'}">
            ${a.source_type === 'reddit' ? redditIcon() : newsletterIcon()}
            ${escapeHtml(a.source)}
          </span>
          <button class="save-btn ${state.savedIds.has(a.id) ? 'saved' : ''}" data-save="${escapeHtml(a.id)}" title="${state.savedIds.has(a.id) ? 'Unsave' : 'Save'} article">
            ${bookmarkIcon(state.savedIds.has(a.id))}
          </button>
        </div>
        <h3 class="card-title">${escapeHtml(a.title)}</h3>
        ${a.summary ? `<p class="card-summary">${escapeHtml(a.summary)}</p>` : ''}
        <div class="card-footer">
          <div class="card-meta">
            ${a.score !== null ? `<span class="card-score">${upvoteIcon()} ${formatNumber(a.score)}</span>` : ''}
            ${a.comments_count !== null ? `<span class="card-comments">${commentIcon()} ${formatNumber(a.comments_count)}</span>` : ''}
            ${a.author ? `<span class="card-meta-item">${escapeHtml(a.author)}</span>` : ''}
          </div>
          <span class="card-time">${timeAgo(a.published_at)}</span>
        </div>
      </article>
    `
      )
      .join('');

    els.articlesGrid.innerHTML = html;
  }

  // ── SVG Icons ──────────────────────────────────────────────────────
  function redditIcon() {
    return '<svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor"><circle cx="6" cy="6" r="6"/><circle cx="4.2" cy="5.4" r="0.9" fill="white"/><circle cx="7.8" cy="5.4" r="0.9" fill="white"/><path d="M4 7.5C4.5 8.2 5.2 8.5 6 8.5C6.8 8.5 7.5 8.2 8 7.5" stroke="white" stroke-width="0.7" fill="none" stroke-linecap="round"/></svg>';
  }

  function newsletterIcon() {
    return '<svg width="12" height="12" viewBox="0 0 12 12" fill="none"><rect x="1" y="2.5" width="10" height="7" rx="1.5" stroke="currentColor" stroke-width="1"/><path d="M1.5 3.5L6 6.5L10.5 3.5" stroke="currentColor" stroke-width="1" stroke-linecap="round"/></svg>';
  }

  function bookmarkIcon(filled) {
    if (filled) {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M4 2H12C12.5523 2 13 2.44772 13 3V14L8 10.5L3 14V3C3 2.44772 3.44772 2 4 2Z"/></svg>';
    }
    return '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M4 2H12C12.5523 2 13 2.44772 13 3V14L8 10.5L3 14V3C3 2.44772 3.44772 2 4 2Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>';
  }

  function upvoteIcon() {
    return '<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 2L12 8H9V12H5V8H2L7 2Z" fill="currentColor"/></svg>';
  }

  function commentIcon() {
    return '<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 3C2 2.44772 2.44772 2 3 2H11C11.5523 2 12 2.44772 12 3V9C12 9.55228 11.5523 10 11 10H5L2 13V3Z" stroke="currentColor" stroke-width="1.2"/></svg>';
  }

  function externalIcon() {
    return '<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M6 2H3C2.44772 2 2 2.44772 2 3V11C2 11.5523 2.44772 12 3 12H11C11.5523 12 12 11.5523 12 11V8M8 2H12M12 2V6M12 2L6 8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }

  // ── Modal ──────────────────────────────────────────────────────────
  function openModal(articleId) {
    const article = state.articles.find((a) => a.id === articleId);
    if (!article) return;

    const isSaved = state.savedIds.has(article.id);

    els.modalContent.innerHTML = `
      <div class="modal-source">
        <span class="source-badge ${article.source_type === 'reddit' ? 'reddit' : 'newsletter'}">
          ${article.source_type === 'reddit' ? redditIcon() : newsletterIcon()}
          ${escapeHtml(article.source)}
        </span>
      </div>
      <h2 class="modal-title">${escapeHtml(article.title)}</h2>
      <div class="modal-meta">
        ${article.author ? `<span class="modal-meta-item"><strong>By</strong> ${escapeHtml(article.author)}</span>` : ''}
        <span class="modal-meta-item">${timeAgo(article.published_at)}</span>
        ${article.score !== null ? `<span class="modal-meta-item">${upvoteIcon()} ${formatNumber(article.score)} upvotes</span>` : ''}
        ${article.comments_count !== null ? `<span class="modal-meta-item">${commentIcon()} ${formatNumber(article.comments_count)} comments</span>` : ''}
      </div>
      ${article.summary ? `<p class="modal-summary">${escapeHtml(article.summary)}</p>` : ''}
      <div class="modal-actions">
        <a href="${escapeHtml(article.url)}" target="_blank" rel="noopener" class="btn-primary">
          Read Full Article ${externalIcon()}
        </a>
        <button class="btn-secondary" data-modal-save="${escapeHtml(article.id)}">
          ${bookmarkIcon(isSaved)}
          ${isSaved ? 'Unsave' : 'Save Article'}
        </button>
      </div>
    `;

    els.modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    els.modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  // ── Toast ──────────────────────────────────────────────────────────
  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      ${type === 'success' ? '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8.5L6.5 12L13 4" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' : ''}
      ${message}
    `;
    els.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(8px)';
      toast.style.transition = '0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2500);
  }

  // ── Event Binding ──────────────────────────────────────────────────
  function bindEvents() {
    // Sidebar toggle
    els.sidebarToggle.addEventListener('click', () => {
      els.sidebar.classList.toggle('collapsed');
    });

    // Mobile menu
    els.mobileMenu.addEventListener('click', () => {
      els.sidebar.classList.toggle('open');
    });

    // Close sidebar on outside click (mobile)
    document.addEventListener('click', (e) => {
      if (
        window.innerWidth <= 768 &&
        els.sidebar.classList.contains('open') &&
        !els.sidebar.contains(e.target) &&
        e.target !== els.mobileMenu
      ) {
        els.sidebar.classList.remove('open');
      }
    });

    // Search
    els.searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value;
      renderArticles();
    });

    // Keyboard shortcut for search
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== els.searchInput) {
        e.preventDefault();
        els.searchInput.focus();
      }
      if (e.key === 'Escape') {
        if (els.modalOverlay.classList.contains('active')) {
          closeModal();
        } else {
          els.searchInput.blur();
          state.searchQuery = '';
          els.searchInput.value = '';
          renderArticles();
        }
      }
    });

    // Refresh
    els.refreshBtn.addEventListener('click', () => {
      els.refreshBtn.classList.add('spinning');
      loadArticles().then(() => {
        els.refreshBtn.classList.remove('spinning');
        showToast('Data refreshed!', 'success');
      });
    });

    // View navigation (Dashboard / Saved)
    $$('.nav-item[data-view]').forEach((item) => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        $$('.nav-item[data-view]').forEach((i) => i.classList.remove('active'));
        item.classList.add('active');

        state.currentView = item.dataset.view;
        els.viewTitle.textContent =
          state.currentView === 'saved' ? 'Saved Articles' : 'Latest Articles';
        renderArticles();
      });
    });

    // Source filters
    $$('.source-filter').forEach((item) => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        $$('.source-filter').forEach((i) => i.classList.remove('active'));
        item.classList.add('active');
        state.currentSource = item.dataset.source;
        renderArticles();
      });
    });

    // Sort buttons
    $$('.sort-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        $$('.sort-btn').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        state.currentSort = btn.dataset.sort;
        renderArticles();
      });
    });

    // Article card clicks (event delegation)
    els.articlesGrid.addEventListener('click', (e) => {
      // Save button
      const saveBtn = e.target.closest('[data-save]');
      if (saveBtn) {
        e.stopPropagation();
        toggleSave(saveBtn.dataset.save);
        return;
      }

      // Card click -> open modal
      const card = e.target.closest('.article-card');
      if (card) {
        openModal(card.dataset.id);
      }
    });

    // Modal close
    els.modalClose.addEventListener('click', closeModal);
    els.modalOverlay.addEventListener('click', (e) => {
      if (e.target === els.modalOverlay) closeModal();
    });

    // Modal save button
    els.modalContent.addEventListener('click', (e) => {
      const saveBtn = e.target.closest('[data-modal-save]');
      if (saveBtn) {
        toggleSave(saveBtn.dataset.modalSave);
        closeModal();
      }
    });
  }

  // ── Init ───────────────────────────────────────────────────────────
  function init() {
    loadSaved();
    updateSavedCount();
    bindEvents();
    loadArticles();
  }

  // Go!
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
