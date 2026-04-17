// ── State ──
let slides = [];
let selectedTheme = 'kente_tech';
let selectedFormat = 'png';
let selectedPlatform = 'linkedin';
let themeColors = {};
let parsedMarkdownData = null;
let lastPayload = null;
let isRethemeRunning = false;
let _badgeEnabled = false;   // badge masqué tant que l'utilisateur n'a pas importé
let _pendingMdItems = [];    // tous les items parsés depuis le modal (multi-fichiers)

// ── Multi-job tracker ──
const activeJobs = new Map(); // jobId → { name, total, startTime, current, status, phase, files, error }
let _pollTimer  = null;
let _overlayJob = null;        // jobId affiché dans l'overlay plein-panneau

// ── Multi-MD state ──
let mdBlocks     = [];         // [{ id, content, parsed }]  — onglet Paste
let mdFileQueue  = [];         // [{ name, size, content, parsed }] — onglet Upload
let _mdBlockIdSeq = 0;

// ── Init ──
document.addEventListener('DOMContentLoaded', async () => {
  initResponsive();
  await loadThemes();
  addSlide('cover');
  addSlide('content');
  addSlide('compare');
});

// ── Sidebar toggle ──
function isMobileView() { return window.innerWidth < 768; }

function toggleSidebar() {
  if (isMobileView()) {
    const shell    = document.querySelector('.shell');
    const backdrop = document.getElementById('sidebar-backdrop');
    const isOpen   = shell.classList.toggle('sidebar-open');
    if (backdrop) backdrop.classList.toggle('visible', isOpen);
  } else {
    const shell = document.querySelector('.shell');
    const btn   = document.getElementById('btn-hamburger');
    const isCollapsed = shell.classList.toggle('sidebar-collapsed');
    if (btn) btn.classList.toggle('is-open', !isCollapsed);
  }
}

function closeSidebar() {
  const shell    = document.querySelector('.shell');
  const backdrop = document.getElementById('sidebar-backdrop');
  shell.classList.remove('sidebar-open');
  if (backdrop) backdrop.classList.remove('visible');
}

function initResponsive() {
  // On mobile the sidebar starts hidden (drawer, closed)
  // On desktop/tablet it starts open
  const btn = document.getElementById('btn-hamburger');
  if (!isMobileView() && btn) btn.classList.add('is-open');
  // Handle resize: if going desktop→mobile, clean up desktop state
  window.addEventListener('resize', () => {
    const shell = document.querySelector('.shell');
    if (!isMobileView()) {
      // On desktop: remove mobile-only classes
      shell.classList.remove('sidebar-open');
      const backdrop = document.getElementById('sidebar-backdrop');
      if (backdrop) backdrop.classList.remove('visible');
    }
  }, { passive: true });
}

// ── Platform ──
function setPlatform(platform, el) {
  selectedPlatform = platform;

  // Sync nav-tabs (new visual system)
  document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
  const navTab = document.getElementById('nav-' + platform);
  if (navTab) navTab.classList.add('active');

  // Sync hidden plat-btns (legacy JS compat)
  document.querySelectorAll('.plat-btn').forEach(b => b.classList.remove('active'));
  const platBtn = document.getElementById('plat-' + platform);
  if (platBtn) platBtn.classList.add('active');

  // Show/hide IG-only slide type buttons
  document.querySelectorAll('.ig-only').forEach(b => {
    b.style.display = platform === 'instagram' ? '' : 'none';
  });

  // Update theme hint
  const hint = document.getElementById('theme-platform-hint');
  if (hint) hint.textContent = platform === 'instagram' ? '— IG' : '— LI';

  // Auto-select a matching default theme for each platform
  const igDefault = 'ig_aurora_dark';
  const liDefault = 'kente_tech';
  const defaultTheme = platform === 'instagram' ? igDefault : liDefault;
  if (themeColors[defaultTheme]) selectedTheme = defaultTheme;

  // Re-render theme grid with platform filter
  renderThemeGrid();
}

// ── Themes ──
async function loadThemes() {
  try {
    const res = await fetch('api/themes');
    if (!res.ok) throw new Error(`Status: ${res.status}`);
    const text = await res.text();
    try {
      themeColors = JSON.parse(text);
      renderThemeGrid();
    } catch (e) {
      console.error("Réponse non-JSON reçue de l'API:", text);
      showStatus("Erreur de chargement des thèmes (réponse invalide)", 'error');
    }
  } catch (e) {
    console.error("Erreur de chargement des thèmes:", e);
    showStatus("L'API des thèmes est inaccessible (404 ou erreur réseau)", 'error');
  }
}

function renderThemeGrid() {
  const grid = document.getElementById('theme-grid');
  const themeLabels = {
    // LinkedIn themes
    kente_tech:        'Kente Tech',
    dark_purple:       'Dark Purple',
    dark_blue:         'Dark Blue',
    dark_green:        'Dark Green',
    dark_red:          'Dark Red',
    dark_orange:       'Dark Orange',
    neon_synthwave:    'Synthwave',
    ocean_breeze:      'Ocean',
    royal_gold:        'Royal Gold',
    forest_night:      'Forest',
    crimson_tide:      'Crimson',
    cosmic_void:       'Cosmic',
    tropical_breeze:   'Tropical',
    volcanic_fire:     'Volcanic',
    aurora_borealis:   'Aurora',
    savanna_gold:      'Savanna',
    // Instagram themes
    ig_aurora_dark:    'Aurora Dark',
    ig_sunset_vibes:   'Sunset',
    ig_minimal_white:  'Minimal',
    ig_cream_luxury:   'Luxury',
    ig_neon_pulse:     'Neon Pulse',
    ig_ocean_deep:     'Ocean Deep',
    ig_rose_pop:       'Rose Pop',
    ig_sage_earth:     'Sage Earth',
    ig_midnight_gold:  'Midnight Gold',
    ig_coral_burst:    'Coral Burst',
    random:            'Aléatoire',
  };

  // Filter themes by platform
  const filtered = Object.entries(themeColors).filter(([name, t]) => {
    if (name === 'random') return true;
    if (selectedPlatform === 'instagram') return t.platform === 'instagram';
    return t.platform === 'linkedin' || t.platform === 'all';
  });

  grid.innerHTML = filtered.map(([name, t]) => {
    const isLight = t.is_light;
    const lightStyle = isLight
      ? `border:1px solid #ddd;background:#f5f5f5;color:#333;`
      : '';
    return `
    <div class="theme-pill ${name === selectedTheme ? 'active' : ''}"
         data-theme="${name}"
         onclick="selectTheme('${name}', this)"
         style="${lightStyle}">
      <div style="background:linear-gradient(90deg,${t.accent1},${t.accent2});height:5px;border-radius:3px;margin-bottom:6px"></div>
      <span style="font-size:10px">${themeLabels[name] || name}</span>
      ${isLight ? '<span class="theme-platform-tag" style="color:#888">☀ Light</span>' : ''}
    </div>
  `}).join('');
}

function selectTheme(name, el) {
  selectedTheme = name;
  document.querySelectorAll('.theme-pill').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
}

function setFormat(fmt) {
  selectedFormat = fmt;
  // Synchronise TOUS les boutons format (sidebar + modal) selon le format choisi
  document.querySelectorAll('.fmt-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.fmt === fmt);
  });
}

// ── Slide management ──
function addSlide(type) {
  const id = Date.now();
  const defaults = {
    cover:   { type:'cover',   badge:'Module 01', title:'Mon Titre', code:'model.fit()_', cta:'Swipe pour apprendre' },
    content: { type:'content', badge:'',       title:'Nouveau Sujet', body:'Ton contenu ici...' },
    compare: { type:'compare', badge:'',       title:'Comparaison', columns:[
      { title:'Option A', body:'Description A', tag:'Tag A' },
      { title:'Option B', body:'Description B', tag:'Tag B' },
    ]},
    quote:   { type:'quote',   title:'La simplicité est la sophistication suprême.', author:'Léonard de Vinci' },
    stat:    { type:'stat',    badge:'Chiffres clés', title:'En quelques chiffres', stats:[
      { value:'87%', label:'des entreprises utilisent l\'IA' },
      { value:'3x',  label:'plus de productivité' },
    ]},
    cta:     { type:'cta',     badge:'', title:'Prêt à passer à l\'action ?', body:'Rejoins des milliers de professionnels qui transforment leur carrière.', cta:'Suivez-moi' },
  };
  slides.push({ id, ...defaults[type] });
  renderSlides();
}

function removeSlide(id) {
  slides = slides.filter(s => s.id !== id);
  renderSlides();
}

function moveSlide(id, dir) {
  const i = slides.findIndex(s => s.id === id);
  const j = i + dir;
  if (j < 0 || j >= slides.length) return;
  [slides[i], slides[j]] = [slides[j], slides[i]];
  renderSlides();
}

function toggleSlide(id) {
  const body = document.getElementById('sbody-' + id);
  body.classList.toggle('open');
}

// ── Image picker : fichier local → base64 ──
function pickImageFile(slideId) {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.onchange = e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      const dataUrl = ev.target.result;
      updateSlide(slideId, 'image_url', dataUrl);
      // Mettre à jour le champ texte (vide, l'aperçu suffit)
      const urlInput = document.getElementById('img-url-' + slideId);
      if (urlInput) urlInput.value = '';
      updateImgPreview(slideId, dataUrl);
    };
    reader.readAsDataURL(file);
  };
  input.click();
}

/* ── Image preview helpers ── */
const _imgDebounce = {};   // slideId → timer handle

function scheduleImgPreview(slideId, src) {
  clearTimeout(_imgDebounce[slideId]);
  const trimmed = (src || '').trim();
  if (!trimmed) {
    // Clear immediately on empty input
    _applyImgPreview(slideId, '');
    return;
  }
  // Debounce remote URL fetches; data: URLs are instant
  const delay = trimmed.startsWith('data:') ? 0 : 600;
  _imgDebounce[slideId] = setTimeout(() => _applyImgPreview(slideId, trimmed), delay);
}

function _applyImgPreview(slideId, src) {
  const wrap    = document.getElementById('img-wrap-' + slideId);
  const preview = document.getElementById('img-preview-' + slideId);
  if (!wrap || !preview) return;

  // Always trim — guards against copy-pasted URLs with trailing spaces
  const cleanSrc = (src || '').trim();

  if (!cleanSrc) {
    wrap.classList.remove('visible', 'loading', 'img-error');
    preview.src = '';
    preview.classList.remove('loaded');
    return;
  }

  // Reset states and show loading skeleton
  wrap.classList.remove('img-error');
  wrap.classList.add('visible', 'loading');
  preview.classList.remove('loaded');
  preview.src = cleanSrc;
}

function onImgPreviewLoad(slideId) {
  const wrap    = document.getElementById('img-wrap-' + slideId);
  const preview = document.getElementById('img-preview-' + slideId);
  if (!wrap || !preview) return;
  wrap.classList.remove('loading', 'img-error');
  preview.classList.add('loaded');
}

function onImgPreviewError(slideId) {
  const wrap    = document.getElementById('img-wrap-' + slideId);
  const preview = document.getElementById('img-preview-' + slideId);
  if (!wrap || !preview) return;
  // Only show error if we actually tried to load something
  if (!preview.src || preview.src === window.location.href) return;
  // Some servers block browser preview (hotlink protection / CORS) but Playwright
  // can still download the image for generation. Show a softer warning, not a hard error.
  wrap.classList.remove('loading');
  wrap.classList.add('img-warn');
  preview.classList.remove('loaded');
}

// Legacy alias — still called from pickImageFile
function updateImgPreview(slideId, src) {
  scheduleImgPreview(slideId, src);
}

function updateSlide(id, key, value) {
  const s = slides.find(s => s.id === id);
  if (!s) return;
  if (key.startsWith('col.')) {
    const [, ci, ck] = key.split('.');
    s.columns[ci][ck] = value;
  } else {
    s[key] = value;
  }
  // Update preview title
  const preview = document.getElementById('stitle-' + id);
  if (preview && (key === 'title')) preview.textContent = value || '—';
}

function updateStat(slideId, statIdx, key, value) {
  const s = slides.find(s => s.id === slideId);
  if (!s || !s.stats) return;
  if (!s.stats[statIdx]) s.stats[statIdx] = {};
  s.stats[statIdx][key] = value;
}

function addStat(slideId) {
  const s = slides.find(s => s.id === slideId);
  if (!s) return;
  if (!s.stats) s.stats = [];
  s.stats.push({ value: '', label: '' });
  renderSlides();
}

function renderSlides() {
  const list = document.getElementById('slides-list');
  if (slides.length === 0) {
    list.innerHTML = `<div class="empty-state"><div class="empty-state-icon">◫</div><p>Aucune slide. Ajoute-en une ci-dessous.</p></div>`;
  } else {
    list.innerHTML = slides.map((s, i) => renderSlideCard(s, i)).join('');
  }
  _updateSlideBadge(slides.length);
}

function _updateSlideBadge(count) {
  if (!_badgeEnabled) return; // ignorer pendant l'init ou si pas d'import
  const badge = document.getElementById('slide-count-badge');
  if (!badge) return;
  const prev = badge.textContent;
  if (count === 0) {
    badge.classList.add('hidden');
    return;
  }
  badge.classList.remove('hidden');
  const newVal = String(count);
  if (prev === newVal) return; // pas de changement → pas d'animation
  badge.textContent = newVal;
  // Déclencher l'animation pop en retirant puis remettant la classe
  badge.classList.remove('pop');
  requestAnimationFrame(() => {
    requestAnimationFrame(() => badge.classList.add('pop'));
  });
}

function renderSlideCard(s, i) {
  const badgeClass = {
    cover:'badge-cover', content:'badge-content', compare:'badge-compare',
    quote:'badge-quote', stat:'badge-stat', cta:'badge-cta',
  }[s.type] || 'badge-content';
  const badgeLabel = {
    cover:'Couverture', content:'Contenu', compare:'Comparaison',
    quote:'Citation', stat:'Statistiques', cta:'Call To Action',
  }[s.type] || s.type;

  let fields = '';

  if (s.type === 'cover') {
    fields = `
      <div class="field-row">
        <div class="field"><label>Titre principal</label><input type="text" value="${esc(s.title)}" oninput="updateSlide(${s.id},'title',this.value)"></div>
        <div class="field"><label>Badge</label><input type="text" value="${esc(s.badge||'')}" oninput="updateSlide(${s.id},'badge',this.value)"></div>
      </div>
      <div class="field-row">
        <div class="field"><label>CTA</label><input type="text" value="${esc(s.cta||'')}" oninput="updateSlide(${s.id},'cta',this.value)"></div>
        <div class="field"><label>Sous-titre / Body</label><input type="text" value="${esc(s.body||'')}" oninput="updateSlide(${s.id},'body',this.value)"></div>
      </div>
      <div class="field-row">
        <div class="field"><label>Code terminal (LinkedIn)</label><input type="text" value="${esc(s.code||'')}" oninput="updateSlide(${s.id},'code',this.value)"></div>
      </div>
      <div class="field">
        <label>Image (URL ou fichier local, optionnel)</label>
        <div class="field-img-wrap">
          <input type="text" id="img-url-${s.id}"
            value="${esc(s.image_url && !s.image_url.startsWith('data:') ? s.image_url : '')}"
            placeholder="https://images.unsplash.com/…"
            oninput="updateSlide(${s.id},'image_url',this.value.trim());scheduleImgPreview(${s.id},this.value)">
          <button class="btn-img-pick" onclick="pickImageFile(${s.id})" type="button">📁 Fichier</button>
        </div>
        <div id="img-wrap-${s.id}" class="field-img-preview-wrap${s.image_url ? ' visible loading' : ''}">
          <img id="img-preview-${s.id}"
            class="field-img-preview${s.image_url ? '' : ''}"
            src="${s.image_url ? esc(s.image_url) : ''}"
            alt="aperçu"
            onload="onImgPreviewLoad(${s.id})"
            onerror="onImgPreviewError(${s.id})">
        </div>
      </div>`;
  } else if (s.type === 'content') {
    fields = `
      <div class="field-row">
        <div class="field"><label>Titre</label><input type="text" value="${esc(s.title)}" oninput="updateSlide(${s.id},'title',this.value)"></div>
        <div class="field"><label>Badge</label><input type="text" value="${esc(s.badge||'')}" oninput="updateSlide(${s.id},'badge',this.value)"></div>
      </div>
      <div class="field"><label>Contenu (HTML autorisé)</label>
        <textarea oninput="updateSlide(${s.id},'body',this.value)">${esc(s.body||'')}</textarea>
      </div>
      <div class="field">
        <label>Image (URL ou fichier local, optionnel)</label>
        <div class="field-img-wrap">
          <input type="text" id="img-url-${s.id}"
            value="${esc(s.image_url && !s.image_url.startsWith('data:') ? s.image_url : '')}"
            placeholder="https://images.unsplash.com/…"
            oninput="updateSlide(${s.id},'image_url',this.value.trim());scheduleImgPreview(${s.id},this.value)">
          <button class="btn-img-pick" onclick="pickImageFile(${s.id})" type="button">📁 Fichier</button>
        </div>
        <div id="img-wrap-${s.id}" class="field-img-preview-wrap${s.image_url ? ' visible loading' : ''}">
          <img id="img-preview-${s.id}"
            class="field-img-preview"
            src="${s.image_url ? esc(s.image_url) : ''}"
            alt="aperçu"
            onload="onImgPreviewLoad(${s.id})"
            onerror="onImgPreviewError(${s.id})">
        </div>
      </div>`;
  } else if (s.type === 'compare') {
    const c = s.columns || [{},{}];
    fields = `
      <div class="field-row">
        <div class="field"><label>Titre</label><input type="text" value="${esc(s.title)}" oninput="updateSlide(${s.id},'title',this.value)"></div>
        <div class="field"><label>Badge</label><input type="text" value="${esc(s.badge||'')}" oninput="updateSlide(${s.id},'badge',this.value)"></div>
      </div>
      <div class="cols-grid">
        ${[0,1].map(ci => `
          <div class="col-block">
            <div class="col-block-label">Colonne ${ci+1}</div>
            <div class="field"><label>Titre</label><input type="text" value="${esc(c[ci]?.title||'')}" oninput="updateSlide(${s.id},'col.${ci}.title',this.value)"></div>
            <div class="field"><label>Corps</label><textarea oninput="updateSlide(${s.id},'col.${ci}.body',this.value)">${esc(c[ci]?.body||'')}</textarea></div>
            <div class="field"><label>Tag</label><input type="text" value="${esc(c[ci]?.tag||'')}" oninput="updateSlide(${s.id},'col.${ci}.tag',this.value)"></div>
          </div>`).join('')}
      </div>
      <div class="field">
        <label>Image (URL ou fichier local, optionnel)</label>
        <div class="field-img-wrap">
          <input type="text" id="img-url-${s.id}"
            value="${esc(s.image_url && !s.image_url.startsWith('data:') ? s.image_url : '')}"
            placeholder="https://images.unsplash.com/…"
            oninput="updateSlide(${s.id},'image_url',this.value.trim());scheduleImgPreview(${s.id},this.value)">
          <button class="btn-img-pick" onclick="pickImageFile(${s.id})" type="button">📁 Fichier</button>
        </div>
        <div id="img-wrap-${s.id}" class="field-img-preview-wrap${s.image_url ? ' visible loading' : ''}">
          <img id="img-preview-${s.id}"
            class="field-img-preview"
            src="${s.image_url ? esc(s.image_url) : ''}"
            alt="aperçu"
            onload="onImgPreviewLoad(${s.id})"
            onerror="onImgPreviewError(${s.id})">
        </div>
      </div>`;
  } else if (s.type === 'quote') {
    fields = `
      <div class="field">
        <label>Citation (texte principal)</label>
        <textarea oninput="updateSlide(${s.id},'title',this.value)">${esc(s.title||'')}</textarea>
      </div>
      <div class="field-row">
        <div class="field"><label>Auteur</label><input type="text" value="${esc(s.author||'')}" oninput="updateSlide(${s.id},'author',this.value)"></div>
        <div class="field"><label>Badge (optionnel)</label><input type="text" value="${esc(s.badge||'')}" oninput="updateSlide(${s.id},'badge',this.value)"></div>
      </div>`;
  } else if (s.type === 'stat') {
    const stats = s.stats || [{value:'',label:''},{value:'',label:''}];
    fields = `
      <div class="field-row">
        <div class="field"><label>Titre</label><input type="text" value="${esc(s.title||'')}" oninput="updateSlide(${s.id},'title',this.value)"></div>
        <div class="field"><label>Badge</label><input type="text" value="${esc(s.badge||'')}" oninput="updateSlide(${s.id},'badge',this.value)"></div>
      </div>
      <div class="cols-grid">
        ${stats.map((st, si) => `
          <div class="col-block">
            <div class="col-block-label">Stat ${si+1}</div>
            <div class="field"><label>Valeur</label><input type="text" placeholder="87%" value="${esc(st.value||'')}" oninput="updateStat(${s.id},${si},'value',this.value)"></div>
            <div class="field"><label>Libellé</label><input type="text" placeholder="Adoption IA" value="${esc(st.label||'')}" oninput="updateStat(${s.id},${si},'label',this.value)"></div>
          </div>`).join('')}
      </div>
      <button class="add-btn" style="margin-top:8px" onclick="addStat(${s.id})">＋ Ajouter une stat</button>`;
  } else if (s.type === 'cta') {
    fields = `
      <div class="field-row">
        <div class="field"><label>Titre accrocheur</label><input type="text" value="${esc(s.title||'')}" oninput="updateSlide(${s.id},'title',this.value)"></div>
        <div class="field"><label>Badge (optionnel)</label><input type="text" value="${esc(s.badge||'')}" oninput="updateSlide(${s.id},'badge',this.value)"></div>
      </div>
      <div class="field"><label>Sous-texte</label>
        <textarea oninput="updateSlide(${s.id},'body',this.value)">${esc(s.body||'')}</textarea>
      </div>
      <div class="field"><label>Bouton CTA</label>
        <input type="text" value="${esc(s.cta||'')}" oninput="updateSlide(${s.id},'cta',this.value)" placeholder="ex: Suivez-moi · Téléchargez">
      </div>`;
  }

  return `
    <div class="slide-card">
      <div class="slide-card-head" onclick="toggleSlide(${s.id})">
        <div class="slide-num">${i+1}</div>
        <div class="slide-title-preview" id="stitle-${s.id}">${esc(s.title||'Sans titre')}</div>
        <span class="slide-type-badge ${badgeClass}">${badgeLabel}</span>
        <div class="slide-actions" onclick="event.stopPropagation()">
          <button class="icon-btn" onclick="moveSlide(${s.id},-1)" title="Monter">↑</button>
          <button class="icon-btn" onclick="moveSlide(${s.id},1)"  title="Descendre">↓</button>
          <button class="icon-btn danger" onclick="removeSlide(${s.id})" title="Supprimer">X</button>
        </div>
      </div>
      <div class="slide-body" id="sbody-${s.id}">
        ${fields}
      </div>
    </div>`;
}

function esc(str) {
  return String(str || '')
    .replace(/&/g,'&amp;').replace(/"/g,'&quot;')
    .replace(/'/g,'&#39;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ────────────────────────────────────────────
//  MULTI-JOB TRACKER
// ────────────────────────────────────────────

function _ensurePoller() {
  if (_pollTimer) return;
  _pollTimer = setInterval(_pollAllJobs, 500);
}

async function _pollAllJobs() {
  const running = [...activeJobs.entries()].filter(([, m]) => m.status === 'running');
  if (!running.length) { clearInterval(_pollTimer); _pollTimer = null; return; }

  await Promise.all(running.map(async ([jobId, meta]) => {
    try {
      const res  = await fetch('api/status/' + jobId);
      const data = await res.json();
      Object.assign(meta, {
        current: data.current_slide ?? meta.current,
        total:   data.total_slides  ?? meta.total,
        status:  data.status,
        phase:   data.phase || meta.phase,
        files:   data.files  || [],
        error:   data.error,
      });
      _updateJobCard(jobId);
      if (jobId === _overlayJob) _syncOverlay(meta);
      if (data.status === 'done' || data.status === 'error') {
        _onJobDone(jobId, meta);
      }
    } catch (_) {}
  }));
}

function _syncOverlay(meta) {
  const pct = meta.total > 0 ? Math.round((meta.current / meta.total) * 85) + 5 : 8;
  const label = meta.phase === 'rendering' && meta.total > 0
    ? `Capture slide ${meta.current + 1} / ${meta.total}…`
    : ({ preparing: 'Préparation…', done: 'Terminé !' }[meta.phase] || 'Génération…');
  setProgress(pct, label, meta.current, meta.total);
}

function _onJobDone(jobId, meta) {
  _updateJobCard(jobId);
  _refreshPanelBadge();

  if (jobId === _overlayJob) {
    if (meta.status === 'done') {
      setProgress(100, 'Terminé !', meta.total, meta.total);
      setTimeout(() => {
        showProgress(false);
        renderPreview(meta.files, jobId);
        renderRethemeBar();
        switchTab('preview', document.querySelectorAll('.tab')[1]);
      }, 700);
      showStatus(`${meta.files.length} slide(s) générées avec succès.`, 'success');
    } else {
      showProgress(false);
      showStatus('Erreur : ' + (meta.error || 'inconnue'), 'error');
    }
    document.getElementById('btn-generate').disabled = false;
  }

  // Vérifier si TOUS les jobs sont terminés (done ou error)
  const allFinished = [...activeJobs.values()].every(m => m.status === 'done' || m.status === 'error');
  if (allFinished) {
    const doneCount  = [...activeJobs.values()].filter(m => m.status === 'done').length;
    const errorCount = [...activeJobs.values()].filter(m => m.status === 'error').length;
    if (doneCount > 0) {
      _playDoneSound();
      _startBadgeCountdown(60);
    }
  }
}

// ── Notification sonore & toast ──────────────────────────────────

function _playDoneSound() {
  try {
    const ctx  = new (window.AudioContext || window.webkitAudioContext)();
    // 3 notes ascendantes façon chime
    const notes = [
      { freq: 880,  t: 0,    dur: .35, vol: .55 },
      { freq: 1100, t: .18,  dur: .35, vol: .48 },
      { freq: 1320, t: .34,  dur: .6,  vol: .4  },
    ];
    notes.forEach(({ freq, t, dur, vol }) => {
      const osc  = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, ctx.currentTime + t);
      gain.gain.setValueAtTime(0, ctx.currentTime + t);
      gain.gain.linearRampToValueAtTime(vol, ctx.currentTime + t + .02);
      gain.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + t + dur);
      osc.start(ctx.currentTime + t);
      osc.stop(ctx.currentTime + t + dur + .05);
    });
    // Fermer le contexte proprement après la dernière note
    setTimeout(() => ctx.close(), 1500);
  } catch (_) { /* AudioContext non supporté : ignorer silencieusement */ }
}


// ── Badge countdown après génération ─────────────────────────────
let _badgeCountdownTimer = null;
let _badgeCountdownSec   = 0;

function _startBadgeCountdown(seconds = 60) {
  _cancelBadgeCountdown();
  const badge = document.getElementById('slide-count-badge');
  if (!badge || badge.classList.contains('hidden')) return;

  _badgeCountdownSec = seconds;
  badge.classList.remove('pop');
  badge.classList.add('countdown');
  badge.textContent = `${_badgeCountdownSec}s`;

  _badgeCountdownTimer = setInterval(() => {
    _badgeCountdownSec--;
    if (_badgeCountdownSec <= 0) {
      _cancelBadgeCountdown();
      badge.classList.add('fade-out');
      setTimeout(() => {
        badge.classList.remove('fade-out', 'countdown');
        badge.classList.add('hidden');
        badge.textContent = '';
        _badgeEnabled = false; // remettre à zéro → prochain import réactive le badge
      }, 420);
    } else {
      badge.textContent = `${_badgeCountdownSec}s`;
    }
  }, 1000);
}

function _cancelBadgeCountdown() {
  clearInterval(_badgeCountdownTimer);
  _badgeCountdownTimer = null;
  const badge = document.getElementById('slide-count-badge');
  if (badge) badge.classList.remove('countdown', 'fade-out');
}

// Lance un job et l'ajoute au tracker
function _startJobTracking(jobId, name, totalSlides, isOverlay = true) {
  const meta = {
    name, total: totalSlides, startTime: Date.now(),
    current: 0, status: 'running', phase: 'preparing', files: [], error: null,
  };
  activeJobs.set(jobId, meta);
  if (isOverlay) _overlayJob = jobId;
  _addJobCard(jobId, name);
  _refreshPanelBadge();
  _ensurePoller();
}

// ────────────────────────────────────────────
//  JOBS PANEL
// ────────────────────────────────────────────

function toggleJobsPanel() {
  document.getElementById('jobs-panel').classList.toggle('collapsed');
}

function _refreshPanelBadge() {
  const panel   = document.getElementById('jobs-panel');
  const badge   = document.getElementById('jobs-badge');
  const running = [...activeJobs.values()].filter(m => m.status === 'running').length;
  const errors  = [...activeJobs.values()].filter(m => m.status === 'error').length;
  const total   = activeJobs.size;

  badge.textContent = running > 0 ? running : total;
  badge.className   = 'jobs-panel-badge' +
    (running > 0 ? '' : errors > 0 ? ' has-error' : ' all-done');

  panel.classList.toggle('visible', total > 0);
}

function _elapsedStr(startTime) {
  const s  = Math.floor((Date.now() - startTime) / 1000);
  const mm = String(Math.floor(s / 60)).padStart(2, '0');
  const ss = String(s % 60).padStart(2, '0');
  return `${mm}:${ss}`;
}

function _addJobCard(jobId, name) {
  const list = document.getElementById('jobs-panel-list');
  const card = document.createElement('div');
  card.className = 'jcard jrunning';
  card.id = `jcard-${CSS.escape(jobId)}`;
  card.innerHTML = `
    <div class="jcard-top">
      <div class="jcard-dot"></div>
      <div class="jcard-name" title="${esc(name)}">${esc(name)}</div>
      <div class="jcard-time" id="jtime-${CSS.escape(jobId)}">00:00</div>
    </div>
    <div class="jcard-bar-track"><div class="jcard-bar-fill" id="jbar-${CSS.escape(jobId)}"></div></div>
    <div class="jcard-meta" id="jmeta-${CSS.escape(jobId)}">Préparation…</div>`;
  list.prepend(card);

  // Timer interne de la card
  const timerEl = card.querySelector(`#jtime-${CSS.escape(jobId)}`);
  const meta    = activeJobs.get(jobId);
  const t = setInterval(() => {
    if (!meta || meta.status !== 'running') { clearInterval(t); return; }
    if (timerEl) timerEl.textContent = _elapsedStr(meta.startTime);
  }, 1000);
}

function _updateJobCard(jobId) {
  const meta  = activeJobs.get(jobId);
  if (!meta) return;
  const card  = document.getElementById(`jcard-${CSS.escape(jobId)}`);
  const bar   = document.getElementById(`jbar-${CSS.escape(jobId)}`);
  const metaEl= document.getElementById(`jmeta-${CSS.escape(jobId)}`);
  if (!card) return;

  const pct = meta.total > 0 ? Math.round((meta.current / meta.total) * 100) : 0;
  if (bar) bar.style.width = (meta.status === 'done' ? 100 : pct) + '%';

  if (meta.status === 'running') {
    if (metaEl) metaEl.textContent = meta.total > 0
      ? `Slide ${meta.current} / ${meta.total} capturées`
      : 'Préparation…';
  } else if (meta.status === 'done') {
    card.className = 'jcard jdone';
    if (metaEl) metaEl.innerHTML = '';
    // Ajouter boutons d'action
    if (!card.querySelector('.jcard-actions')) {
      const acts = document.createElement('div');
      acts.className = 'jcard-actions';
      acts.innerHTML = `
        <button class="jcard-btn success" onclick="viewJobInLibrary('${esc(jobId)}')">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
          Voir dans la bibliothèque
        </button>
        <button class="jcard-btn" onclick="this.closest('.jcard').remove();activeJobs.delete('${esc(jobId)}');_refreshPanelBadge()">✕</button>`;
      card.appendChild(acts);
    }
  } else if (meta.status === 'error') {
    card.className = 'jcard jerror';
    if (metaEl) metaEl.textContent = meta.error || 'Erreur';
    if (!card.querySelector('.jcard-actions')) {
      const acts = document.createElement('div');
      acts.className = 'jcard-actions';
      acts.innerHTML = `<button class="jcard-btn" onclick="this.closest('.jcard').remove();activeJobs.delete('${esc(jobId)}');_refreshPanelBadge()">Fermer</button>`;
      card.appendChild(acts);
    }
  }
}

function viewJobInLibrary(jobId) {
  window.location.href = '/generator#' + encodeURIComponent(jobId);
}

// ────────────────────────────────────────────
//  GENERATE — multi-job compatible
// ────────────────────────────────────────────

async function startGenerate() {
  if (slides.length === 0) return showStatus('Ajoute au moins une slide.', 'error');

  _cancelBadgeCountdown();

  const btn = document.getElementById('btn-generate');
  btn.disabled = true;

  // CAS MULTI : plusieurs fichiers MD importés → générer tous en parallèle
  if (_pendingMdItems.length > 1) {
    showStatus(`Lancement de ${_pendingMdItems.length} générations…`, 'success');
    const items = [..._pendingMdItems];
    _pendingMdItems = []; // vider pour éviter double-lancement

    showProgress(true, items[0].data.slides.length);

    await Promise.all(items.map(async (item, idx) => {
      const payload = {
        theme:    selectedTheme,
        format:   selectedFormat,
        platform: selectedPlatform,
        footer:   item.data.footer || { series: item.name, author: document.getElementById('footer-author').value },
        slides:   item.data.slides,
      };
      try {
        const res  = await fetch('api/generate', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
        const resp = await res.json();
        if (resp.error) { showStatus(`Erreur "${item.name}" : ${resp.error}`, 'error'); return; }
        _startJobTracking(resp.job_id, item.name, item.data.slides.length, idx === 0);
      } catch (e) {
        showStatus(`Erreur réseau "${item.name}"`, 'error');
      }
    }));
    return;
  }

  // CAS SIMPLE : générer le contenu actuel de l'éditeur
  _pendingMdItems = [];
  const name = document.getElementById('footer-series').value || 'Carousel';
  showProgress(true, slides.length);

  const payload = {
    theme:    selectedTheme,
    format:   selectedFormat,
    platform: selectedPlatform,
    footer: {
      series: document.getElementById('footer-series').value,
      author: document.getElementById('footer-author').value,
    },
    slides: slides.map(({ id, ...rest }) => rest),
  };
  lastPayload = payload;

  try {
    const res  = await fetch('api/generate', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    const data = await res.json();
    if (data.error) { showStatus(data.error, 'error'); showProgress(false); btn.disabled = false; return; }
    _startJobTracking(data.job_id, name, slides.length, true);
  } catch(e) {
    showStatus('Erreur réseau: ' + e.message, 'error');
    showProgress(false);
    btn.disabled = false;
  }
}

// ── Re-theme : régénère avec un autre thème, mêmes slides ──
async function reTheme(themeName) {
  if (!lastPayload || isRethemeRunning) return;
  if (themeName === selectedTheme) return;

  isRethemeRunning = true;
  selectedTheme = themeName;

  // Sync le sélecteur de la sidebar
  document.querySelectorAll('.theme-pill').forEach(p => {
    p.classList.toggle('active', p.dataset.theme === themeName);
  });

  // Afficher le spinner dans la barre
  const spinner = document.getElementById('retheme-spinner');
  spinner.classList.add('visible');

  // Griser les pills pendant la régénération
  document.querySelectorAll('.retheme-pill').forEach(p => {
    p.style.opacity = p.dataset.theme === themeName ? '1' : '0.4';
    p.style.pointerEvents = 'none';
  });

  const payload = { ...lastPayload, theme: themeName };
  lastPayload = payload;

  try {
    const res  = await fetch('api/generate', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    const data = await res.json();
    if (data.error) { showStatus(data.error, 'error'); return; }
    pollStatus(data.job_id, true);
  } catch(e) {
    showStatus('Erreur réseau: ' + e.message, 'error');
    isRethemeRunning = false;
    spinner.classList.remove('visible');
    document.querySelectorAll('.retheme-pill').forEach(p => {
      p.style.opacity = '';
      p.style.pointerEvents = '';
    });
  }
}

// ── Re-theme bar ──
function renderRethemeBar() {
  const bar = document.getElementById('retheme-bar');
  const scroll = document.getElementById('retheme-scroll');
  if (!bar || !scroll) return;

  const themeLabels = {
    kente_tech:'Kente Tech', dark_purple:'Dark Purple', dark_blue:'Dark Blue',
    dark_green:'Dark Green', dark_red:'Dark Red', dark_orange:'Dark Orange',
    neon_synthwave:'Synthwave', ocean_breeze:'Ocean', royal_gold:'Royal Gold',
    forest_night:'Forest', crimson_tide:'Crimson', cosmic_void:'Cosmic',
    tropical_breeze:'Tropical', volcanic_fire:'Volcanic', aurora_borealis:'Aurora',
    savanna_gold:'Savanna', ig_aurora_dark:'Aurora Dark', ig_sunset_vibes:'Sunset',
    ig_minimal_white:'Minimal', ig_cream_luxury:'Luxury', ig_neon_pulse:'Neon Pulse',
    ig_ocean_deep:'Ocean Deep', ig_rose_pop:'Rose Pop', ig_sage_earth:'Sage Earth',
    ig_midnight_gold:'Midnight', ig_coral_burst:'Coral', random:'Aléatoire',
  };

  // Filtrer par plateforme actuelle
  const filtered = Object.entries(themeColors).filter(([name, t]) => {
    if (name === 'random') return true;
    return selectedPlatform === 'instagram' ? t.platform === 'instagram' : t.platform === 'linkedin';
  });

  const isIG = selectedPlatform === 'instagram';

  scroll.innerHTML = filtered.map(([name, t]) => {
    const isActive = name === selectedTheme;
    const activeClass = isActive ? (isIG ? 'active-ig' : 'active') : '';
    const lightTag = t.is_light ? '<span class="retheme-pill-light-tag">☀</span>' : '';
    return `
      <div class="retheme-pill ${activeClass}" data-theme="${name}" onclick="reTheme('${name}')" title="${themeLabels[name] || name}">
        ${lightTag}
        <div class="retheme-pill-swatch" style="background:linear-gradient(90deg,${t.accent1},${t.accent2})"></div>
        <div class="retheme-pill-name">${themeLabels[name] || name}</div>
      </div>`;
  }).join('');

  // Mettre à jour le "thème actuel"
  const current = themeColors[selectedTheme];
  if (current) {
    document.getElementById('retheme-current-swatch').style.background =
      `linear-gradient(90deg,${current.accent1},${current.accent2})`;
    document.getElementById('retheme-current-name').textContent =
      themeLabels[selectedTheme] || selectedTheme;
  }

  bar.classList.add('visible');
}

// Re-thème : polling simple car c'est un job secondaire (pas d'overlay plein-panneau)
async function pollStatus(jobId, isRetheme = false) {
  if (!isRetheme) return; // Les vrais jobs passent par _startJobTracking()

  const interval = setInterval(async () => {
    let data;
    try { const r = await fetch('api/status/' + jobId); data = await r.json(); }
    catch (_) { return; }

    if (data.status === 'done') {
      clearInterval(interval);
      document.getElementById('retheme-spinner').classList.remove('visible');
      isRethemeRunning = false;
      document.querySelectorAll('.retheme-pill').forEach(p => { p.style.opacity = ''; p.style.pointerEvents = ''; });
      renderPreview(data.files, jobId);
      renderRethemeBar();
      showStatus(`Thème appliqué : ${selectedTheme}`, 'success');
    }
    if (data.status === 'error') {
      clearInterval(interval);
      document.getElementById('retheme-spinner').classList.remove('visible');
      isRethemeRunning = false;
      document.querySelectorAll('.retheme-pill').forEach(p => { p.style.opacity = ''; p.style.pointerEvents = ''; });
      showStatus('Erreur re-thème : ' + (data.error || 'inconnue'), 'error');
    }
  }, 500);
}

// ── Preview ──
function renderPreview(files, jobId) {
  const grid = document.getElementById('preview-grid');
  const pngFiles = files.filter(f => f.endsWith('.png'));
  const finalPdf = files.find(f => f.endsWith('.pdf'));

  document.getElementById('preview-empty').style.display = 'none';
  document.getElementById('preview-content').style.display = 'block';

  if (finalPdf) {
    document.getElementById('preview-count').textContent = 'Document PDF généré';
    document.querySelector('.btn-presentation').style.display = 'none';
    grid.innerHTML = `
      <div style="width: 100%; height: 60vh; max-height: 800px; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); grid-column: 1 / -1; overflow: hidden; margin-bottom: 20px;">
        <embed src="/${finalPdf}#toolbar=0&navpanes=0&view=FitH" type="application/pdf" width="100%" height="100%" />
      </div>
      <div style="grid-column: 1 / -1; text-align: center;">
        <a href="/${finalPdf}" target="_blank" class="btn-presentation" style="display: inline-flex;">Ouvrir le PDF en plein écran</a>
      </div>
    `;
  } else {
    const isIG = selectedPlatform === 'instagram';
    document.getElementById('preview-count').textContent = `${pngFiles.length} slide(s) générée(s)`;
    document.querySelector('.btn-presentation').style.display = 'inline-flex';

    // Platform badge in header
    const existingBadge = document.querySelector('.ig-platform-badge');
    if (existingBadge) existingBadge.remove();
    if (isIG) {
      const badge = document.createElement('div');
      badge.className = 'ig-platform-badge';
      badge.innerHTML = '📸 Instagram 1080×1080';
      document.querySelector('.preview-header').prepend(badge);
    }

    // Construire un préfixe de nom de fichier depuis le series + jobId
    const seriesRaw = document.getElementById('footer-series').value || 'carousel';
    const seriesSlug = seriesRaw.replace(/[^a-zA-Z0-9À-ÿ]+/g, '_').replace(/^_|_$/g, '').slice(0, 30);

    grid.innerHTML = pngFiles.map((f, i) => {
      const num      = String(i + 1).padStart(2, '0');
      const dlName   = `${seriesSlug}_slide_${num}.png`;
      const label    = `Slide ${num}`;
      return `
        <div class="preview-item ${isIG ? 'ig-ratio' : ''}" style="cursor:pointer;" onclick="openPresentationMode(${i})">
          <img src="/${f}" alt="slide ${i+1}" loading="lazy" style="${isIG ? 'aspect-ratio:4/5;' : 'aspect-ratio:1;'}">
          <div class="preview-item-footer">
            <span class="preview-item-name">${label}</span>
            <a class="preview-item-dl"
               href="/${f}"
               download="${dlName}"
               onclick="event.stopPropagation()"
               title="Télécharger ${dlName}">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              PNG
            </a>
          </div>
        </div>`;
    }).join('');
  }

  document.getElementById('btn-dl-all').dataset.job = jobId;
}

function downloadAll() {
  const jobId = document.getElementById('btn-dl-all').dataset.job;
  if (jobId) window.location.href = 'api/download/' + jobId;
}

// ── UI helpers ──
function switchTab(tab, el) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('editor-area').classList.toggle('hidden', tab !== 'editor');
  document.getElementById('preview-area').classList.toggle('active', tab === 'preview');
}

function goBackToEditor() {
  // Retour à l'éditeur depuis l'aperçu
  const editorTab = document.querySelector('.tab');   // premier tab = Éditeur
  switchTab('editor', editorTab);
  // Scroll en haut de la liste de slides
  const slidesList = document.getElementById('slides-list');
  if (slidesList) slidesList.scrollTop = 0;
}

/* ── Timer interne génération ── */
let _genTimerInterval = null;
let _genStartTime     = null;

function _updateGenTimer() {
  if (!_genStartTime) return;
  const s = Math.floor((Date.now() - _genStartTime) / 1000);
  const mm = String(Math.floor(s / 60)).padStart(2, '0');
  const ss = String(s % 60).padStart(2, '0');
  const el = document.getElementById('gen-timer');
  if (el) el.textContent = `${mm}:${ss}`;
}

function _initGenDots(n) {
  const wrap = document.getElementById('gen-dots');
  if (!wrap) return;
  wrap.innerHTML = '';
  // Limiter l'affichage à 40 dots max pour éviter débordement visuel
  const display = Math.min(n, 40);
  for (let i = 0; i < display; i++) {
    const d = document.createElement('div');
    d.className = 'gen-dot';
    d.id = `gdot-${i}`;
    wrap.appendChild(d);
  }
}

function _updateGenDots(completedCount, total) {
  const display = Math.min(total, 40);
  for (let i = 0; i < display; i++) {
    const d = document.getElementById(`gdot-${i}`);
    if (!d) continue;
    if (i < completedCount) {
      d.className = 'gen-dot done';
    } else if (i === completedCount) {
      d.className = 'gen-dot active';
    } else {
      d.className = 'gen-dot';
    }
  }
}

function showProgress(visible, totalSlides = 0) {
  const overlay = document.getElementById('gen-overlay');
  if (!overlay) return;

  if (visible) {
    overlay.style.display = 'flex';
    _initGenDots(totalSlides);
    document.getElementById('gen-phase').textContent   = 'Préparation…';
    document.getElementById('gen-counter').textContent = `0 / ${totalSlides} slides`;
    document.getElementById('gen-bar-fill').style.width = '2%';
    document.getElementById('gen-timer').textContent   = '00:00';
    _genStartTime = Date.now();
    _genTimerInterval = setInterval(_updateGenTimer, 1000);
    // Basculer sur l'onglet preview pour que l'overlay soit visible
    const previewTab = document.querySelectorAll('.tab')[1];
    if (previewTab) switchTab('preview', previewTab);
  } else {
    overlay.style.display = 'none';
    if (_genTimerInterval) { clearInterval(_genTimerInterval); _genTimerInterval = null; }
    _genStartTime = null;
  }
}

function setProgress(pct, label, currentSlide, totalSlides) {
  const fill = document.getElementById('gen-bar-fill');
  if (fill) fill.style.width = pct + '%';
  if (label) {
    const ph = document.getElementById('gen-phase');
    if (ph) ph.textContent = label;
  }
  if (currentSlide !== undefined && totalSlides !== undefined) {
    const ctr = document.getElementById('gen-counter');
    if (ctr) ctr.textContent = `${currentSlide} / ${totalSlides} slides`;
    _updateGenDots(currentSlide, totalSlides);
  }
}

function showStatus(msg, type) {
  const el = document.getElementById('status-msg');
  el.textContent = msg;
  el.className = `status-msg visible ${type}`;
  setTimeout(() => el.classList.remove('visible'), 5000);
}

// ── Markdown Import ──
// ─────────────────────────────────────────────
//  MARKDOWN MODAL — multi-blocs / multi-fichiers
// ─────────────────────────────────────────────

function openMarkdownModal() {
  document.getElementById('md-modal').classList.add('visible');
  document.getElementById('md-preview').style.display = 'none';
  parsedMarkdownData = null;
  _pendingMdItems = [];
  mdBlocks = [];
  mdFileQueue = [];
  _renderMdBlocks();
  _renderFileQueue();
  // Reset bouton + badge (pas encore de contenu parsé)
  const applyBtn = document.getElementById('md-apply-btn');
  if (applyBtn) {
    applyBtn.disabled = true;
    applyBtn.textContent = '← Importer dans l\'éditeur';
    applyBtn.title = '';
    applyBtn.onclick = applyMarkdownImport;
  }
  _badgeEnabled = false;
  const badge = document.getElementById('slide-count-badge');
  if (badge) { badge.classList.add('hidden'); badge.textContent = ''; }
  // Sync format buttons in modal with current selectedFormat
  document.querySelectorAll('.fmt-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.fmt === selectedFormat);
  });
  // Ajouter un premier bloc vide
  addMdBlock();
}

function closeMarkdownModal() {
  document.getElementById('md-modal').classList.remove('visible');
}

function switchMdTab(tab, el) {
  document.querySelectorAll('.md-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.md-tab-content').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('tab-' + tab).classList.add('active');
}

// ── Multi-bloc paste ──

function addMdBlock(content = '') {
  const id = ++_mdBlockIdSeq;
  mdBlocks.push({ id, content, parsed: null });
  _renderMdBlocks();
  // Focus sur le nouveau textarea
  setTimeout(() => {
    const ta = document.getElementById(`mdta-${id}`);
    if (ta) ta.focus();
  }, 50);
}

function removeMdBlock(id) {
  mdBlocks = mdBlocks.filter(b => b.id !== id);
  _renderMdBlocks();
  _refreshMdButtons();
}

function _renderMdBlocks() {
  const list = document.getElementById('md-blocks-list');
  if (!list) return;
  list.innerHTML = mdBlocks.map((b, idx) => `
    <div class="md-block-item" id="mdblock-${b.id}">
      <div class="md-block-header">
        <span class="md-block-num">Carousel ${idx + 1}</span>
        <span class="md-block-title" id="mdbtitle-${b.id}">—</span>
        ${mdBlocks.length > 1
          ? `<button class="md-block-remove" onclick="removeMdBlock(${b.id})" title="Supprimer">✕</button>`
          : ''}
      </div>
      <textarea class="md-block-textarea" id="mdta-${b.id}"
        placeholder="# Titre du carousel

## Slide 1 : Introduction
Votre contenu ici...

## Slide 2 : Points clés
- Point 1
- Point 2"
        oninput="_onBlockInput(${b.id})">${esc(b.content)}</textarea>
      <div class="md-block-status" id="mdst-${b.id}"></div>
    </div>`).join('');
}

let _blockParseTimers = {};
function _onBlockInput(id) {
  clearTimeout(_blockParseTimers[id]);
  _blockParseTimers[id] = setTimeout(() => _parseBlock(id), 600);
}

async function _parseBlock(id) {
  const block = mdBlocks.find(b => b.id === id);
  if (!block) return;
  const ta = document.getElementById(`mdta-${id}`);
  const content = ta ? ta.value : '';
  block.content = content;

  const statusEl = document.getElementById(`mdst-${id}`);
  const titleEl  = document.getElementById(`mdbtitle-${id}`);

  if (!content.trim()) {
    block.parsed = null;
    if (statusEl) { statusEl.className = 'md-block-status'; statusEl.textContent = ''; }
    if (titleEl) titleEl.textContent = '—';
    _refreshMdButtons();
    return;
  }

  if (statusEl) { statusEl.className = 'md-block-status'; statusEl.textContent = 'Analyse…'; }

  try {
    const res  = await fetch('api/import-markdown', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ content }),
    });
    const data = await res.json();
    if (data.error) {
      block.parsed = null;
      if (statusEl) { statusEl.className = 'md-block-status err'; statusEl.textContent = '✕ ' + data.error; }
      if (titleEl) titleEl.textContent = '—';
    } else {
      block.parsed = data;
      const n     = data.slides.length;
      const title = data.slides[0]?.title || 'Sans titre';
      if (statusEl) { statusEl.className = 'md-block-status ok'; statusEl.textContent = `✓ ${n} slide(s) détectées`; }
      if (titleEl) titleEl.textContent = title;
      // Compat: si 1 seul bloc, alimenter parsedMarkdownData pour le bouton "Charger dans l'éditeur"
      if (mdBlocks.length === 1) parsedMarkdownData = data;
    }
  } catch (e) {
    if (statusEl) { statusEl.className = 'md-block-status err'; statusEl.textContent = '✕ Erreur réseau'; }
  }
  _refreshMdButtons();
}

// ── Multi-file upload ──

function handleFileUpload(event) {
  const files = Array.from(event.target.files);
  files.forEach(f => {
    if (!f.name.match(/\.(md|markdown)$/i)) return;
    if (mdFileQueue.find(q => q.name === f.name)) return; // dédoublonnage
    mdFileQueue.push({ name: f.name, size: f.size, content: null, parsed: null, error: null });
    _readFile(f);
  });
  event.target.value = ''; // permettre re-sélection
  _renderFileQueue();
}

function _readFile(file) {
  const reader = new FileReader();
  reader.onload = async (e) => {
    const item = mdFileQueue.find(q => q.name === file.name);
    if (!item) return;
    item.content = e.target.result;
    _renderFileQueue();
    // Parser côté serveur
    try {
      const res  = await fetch('api/import-markdown', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ content: item.content }),
      });
      const data = await res.json();
      if (data.error) { item.error = data.error; }
      else { item.parsed = data; }
    } catch (_) { item.error = 'Erreur réseau'; }
    _renderFileQueue();
    _refreshMdButtons();
  };
  reader.readAsText(file);
}

function removeFileFromQueue(name) {
  mdFileQueue = mdFileQueue.filter(q => q.name !== name);
  _renderFileQueue();
  _refreshMdButtons();
}

function _renderFileQueue() {
  const list = document.getElementById('md-files-list');
  if (!list) return;
  list.innerHTML = mdFileQueue.map(q => {
    const kb = (q.size / 1024).toFixed(1);
    let statusHtml = '<span style="color:var(--muted)">Lecture…</span>';
    if (q.error)  statusHtml = `<span class="md-file-item-status err">✕</span>`;
    else if (q.parsed) statusHtml = `<span class="md-file-item-status ok">✓ ${q.parsed.slides.length} slides</span>`;
    return `
      <div class="md-file-item">
        <span class="md-file-item-icon">📄</span>
        <span class="md-file-item-name" title="${esc(q.name)}">${esc(q.name)}</span>
        <span class="md-file-item-size">${kb} KB</span>
        ${statusHtml}
        <button class="md-file-remove" onclick="removeFileFromQueue('${esc(q.name)}')" title="Retirer">✕</button>
      </div>`;
  }).join('');
}

function _refreshMdButtons() {
  const activeTab = document.querySelector('.md-tab.active')?.dataset?.tab ||
    (document.getElementById('tab-paste').classList.contains('active') ? 'paste' : 'upload');

  let validItems = [];

  if (activeTab !== 'upload') { // paste tab
    validItems = mdBlocks.filter(b => b.parsed).map(b => ({
      name: b.parsed.slides[0]?.title || `Carousel ${b.id}`,
      data: b.parsed,
    }));
  } else {
    validItems = mdFileQueue.filter(q => q.parsed).map(q => ({
      name: q.name.replace(/\.(md|markdown)$/i, ''),
      data: q.parsed,
    }));
  }

  // Stocker TOUS les items parsés — utilisés par startGenerate() pour le multi
  _pendingMdItems = validItems;
  parsedMarkdownData = validItems.length > 0 ? validItems[0].data : null;

  const applyBtn = document.getElementById('md-apply-btn');
  if (!applyBtn) return;

  const count = validItems.length;
  applyBtn.disabled = count === 0;
  applyBtn.onclick = applyMarkdownImport;

  // Calcul du total de slides sur tous les éléments valides
  const totalSlides = validItems.reduce((acc, item) => acc + (item.data.slides?.length || 0), 0);

  if (count > 1) {
    const perFile = validItems.map(item => item.data.slides?.length || 0).join(' + ');
    applyBtn.textContent = `← Importer dans l'éditeur`;
    applyBtn.title = `${count} fichiers · ${totalSlides} slides (${perFile})`;
  } else {
    applyBtn.textContent = '← Importer dans l\'éditeur';
    applyBtn.title = '';
  }

  // Mettre à jour le badge du bouton "Générer" en temps réel depuis le modal
  if (totalSlides > 0) {
    _badgeEnabled = true;
    _cancelBadgeCountdown();
    _updateSlideBadge(totalSlides);
  } else {
    _badgeEnabled = false;
    const badge = document.getElementById('slide-count-badge');
    if (badge) { badge.classList.add('hidden'); badge.textContent = ''; }
  }
}

// ── Drag & Drop ──
document.addEventListener('DOMContentLoaded', () => {
  const drop = document.getElementById('md-file-drop');
  if (!drop) return;
  drop.addEventListener('dragover',  e => { e.preventDefault(); drop.classList.add('dragover'); });
  drop.addEventListener('dragleave', () => drop.classList.remove('dragover'));
  drop.addEventListener('drop', e => {
    e.preventDefault(); drop.classList.remove('dragover');
    const files = Array.from(e.dataTransfer.files).filter(f => f.name.match(/\.(md|markdown)$/i));
    files.forEach(f => {
      if (!mdFileQueue.find(q => q.name === f.name))
        mdFileQueue.push({ name: f.name, size: f.size, content: null, parsed: null, error: null });
      _readFile(f);
    });
    _renderFileQueue();
  });
});

// ── Actions du modal ──

function applyMarkdownImport() {
  if (!_pendingMdItems.length) return showStatus('Aucune donnée valide', 'error');

  // Charger le 1er item dans l'éditeur pour prévisualisation
  const first = _pendingMdItems[0].data;
  slides = first.slides.map((s, i) => ({ id: Date.now() + i, ...s }));
  if (first.footer?.series) document.getElementById('footer-series').value = first.footer.series;
  if (first.footer?.author) document.getElementById('footer-author').value = first.footer.author;

  _badgeEnabled = true;
  _cancelBadgeCountdown();

  // Badge = total slides de TOUS les fichiers qui seront générés
  const totalSlides = _pendingMdItems.reduce((acc, item) => acc + (item.data.slides?.length || 0), 0);
  _updateSlideBadge(totalSlides);

  renderSlides();
  closeMarkdownModal();

  const n = _pendingMdItems.length;
  const reorg = first.structure_analysis?.reorganization_applied ? ' (réorganisé)' : '';
  if (n > 1) {
    const perFile = _pendingMdItems.map(item => `${item.name} (${item.data.slides?.length || 0} slides)`).join(', ');
    showStatus(`${n} fichiers prêts · ${totalSlides} slides au total — ${perFile} — clique "Générer le carousel"`, 'success');
  } else {
    showStatus(`${slides.length} slide(s) importées${reorg} — choisis la plateforme et clique "Générer le carousel"`, 'success');
  }
}

async function generateFromMarkdown() {
  _cancelBadgeCountdown(); // annuler le décompte si l'utilisateur relance en multi
  // Collecter tous les blocs/fichiers valides et lancer N générations en parallèle
  const activeTab = document.getElementById('tab-paste').classList.contains('active') ? 'paste' : 'upload';
  let items = [];

  if (activeTab === 'paste') {
    items = mdBlocks.filter(b => b.parsed).map(b => ({
      name: b.parsed.slides[0]?.title || `Carousel ${b.id}`,
      data: b.parsed,
    }));
  } else {
    items = mdFileQueue.filter(q => q.parsed).map(q => ({
      name: q.name.replace(/\.(md|markdown)$/i, ''),
      data: q.parsed,
    }));
  }

  if (!items.length) return showStatus('Aucun contenu valide à générer', 'error');

  closeMarkdownModal();
  showStatus(`Lancement de ${items.length} génération(s) — ${selectedPlatform.toUpperCase()} · ${selectedFormat.toUpperCase()} · ${selectedTheme}`, 'success');

  // Lancer toutes les générations simultanément
  await Promise.all(items.map(async (item, idx) => {
    const payload = {
      theme:    selectedTheme,
      format:   selectedFormat,
      platform: selectedPlatform,
      footer:   item.data.footer || { series: item.name, author: document.getElementById('footer-author').value },
      slides:   item.data.slides,
    };
    try {
      const res  = await fetch('api/generate', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
      const resp = await res.json();
      if (resp.error) { showStatus(`Erreur "${item.name}" : ${resp.error}`, 'error'); return; }
      // 1er job → overlay plein-panneau, les autres → panel seulement
      const isOverlay = idx === 0;
      if (isOverlay) showProgress(true, item.data.slides.length);
      _startJobTracking(resp.job_id, item.name, item.data.slides.length, isOverlay);
    } catch (e) {
      showStatus(`Erreur réseau "${item.name}"`, 'error');
    }
  }));
}

// Compat: analyse intelligente (appelée par _parseBlock si besoin direct)
function showStructureAnalysis() {} // No-op — info désormais dans les status des blocs

function renderMarkdownPreview(data) {
  const preview = document.getElementById('md-preview');
  const list    = document.getElementById('md-preview-list');
  if (!preview || !list) return;
  preview.style.display = 'block';
  const TYPE_LABELS = { cover:'Couverture', content:'Contenu', compare:'Comparaison', quote:'Citation', stat:'Stats', cta:'CTA' };
  const TYPE_COLORS = { cover:'#f06292', content:'#38c8a8', compare:'#7c6af7', quote:'#fbbf24', stat:'#22d3ee', cta:'#f87171' };
  list.innerHTML = data.slides.map((s, i) => `
    <div class="md-preview-item">
      <div class="md-preview-item-num">${i + 1}</div>
      <div class="md-preview-item-title">${esc(s.title || 'Sans titre')}</div>
      <div class="md-preview-item-type" style="color:${TYPE_COLORS[s.type]||'#aaa'};background:${TYPE_COLORS[s.type]||'#aaa'}22">
        ${TYPE_LABELS[s.type] || s.type}
      </div>
    </div>`).join('');
}

// ════════════════════════════════════════
// PRESENTATION MODE
// ════════════════════════════════════════
let presentationFiles = [];
let presentationCurrentIndex = 0;

function openPresentationMode(startIndex = 0) {
  // Récupérer les fichiers depuis le preview
  const previewItems = document.querySelectorAll('#preview-grid .preview-item img');
  if (previewItems.length === 0) {
    showStatus('Aucune slide à afficher', 'error');
    return;
  }
  
  presentationFiles = Array.from(previewItems).map(img => img.src);
  presentationCurrentIndex = startIndex >= 0 && startIndex < presentationFiles.length ? startIndex : 0;
  
  const overlay = document.getElementById('presentation-overlay');
  overlay.style.display = 'flex';
  
  // Empêcher le scroll du body
  document.body.style.overflow = 'hidden';
  
  renderPresentationSlide();
  renderPresentationThumbnails();
  
  // Ajouter l'écouteur clavier
  document.addEventListener('keydown', presentationKeyHandler);
  
  // Activer le vrai plein écran si disponible
  const elem = document.documentElement;
  if (elem.requestFullscreen) {
    elem.requestFullscreen().catch(err => {
      console.log('Fullscreen not available:', err.message);
    });
  } else if (elem.webkitRequestFullscreen) { /* Safari */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE11 */
    elem.msRequestFullscreen();
  }
}

function closePresentationMode() {
  const overlay = document.getElementById('presentation-overlay');
  overlay.style.display = 'none';
  document.body.style.overflow = '';
  
  // Retirer l'écouteur clavier
  document.removeEventListener('keydown', presentationKeyHandler);
  
  // Quitter le plein écran si actif
  if (document.exitFullscreen && document.fullscreenElement) {
    document.exitFullscreen();
  } else if (document.webkitExitFullscreen && document.webkitFullscreenElement) {
    document.webkitExitFullscreen();
  }
}

function presentationKeyHandler(e) {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
    e.preventDefault();
    presentationNext();
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
    e.preventDefault();
    presentationPrev();
  } else if (e.key === 'Escape') {
    closePresentationMode();
  }
}

function renderPresentationSlide() {
  const slide = document.getElementById('presentation-slide');
  const counter = document.getElementById('presentation-counter');
  const progressFill = document.getElementById('presentation-progress-fill');
  
  slide.src = presentationFiles[presentationCurrentIndex];
  counter.textContent = `${presentationCurrentIndex + 1} / ${presentationFiles.length}`;
  
  const progress = ((presentationCurrentIndex + 1) / presentationFiles.length) * 100;
  progressFill.style.width = progress + '%';
  
  // Mettre à jour les thumbnails
  document.querySelectorAll('.presentation-thumbnail').forEach((thumb, i) => {
    thumb.classList.toggle('active', i === presentationCurrentIndex);
  });
  
  // Scroll to active thumbnail
  const activeThumb = document.querySelector('.presentation-thumbnail.active');
  if (activeThumb) {
    activeThumb.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }
}

function renderPresentationThumbnails() {
  const container = document.getElementById('presentation-thumbnails');
  container.innerHTML = presentationFiles.map((src, i) => 
    `<img class="presentation-thumbnail ${i === presentationCurrentIndex ? 'active' : ''}" 
          src="${src}" 
          onclick="presentationGoTo(${i})" 
          alt="Slide ${i+1}">`
  ).join('');
}

function presentationGoTo(index) {
  if (index >= 0 && index < presentationFiles.length) {
    presentationCurrentIndex = index;
    renderPresentationSlide();
  }
}

function presentationNext() {
  if (presentationCurrentIndex < presentationFiles.length - 1) {
    presentationCurrentIndex++;
    renderPresentationSlide();
  }
}

function presentationPrev() {
  if (presentationCurrentIndex > 0) {
    presentationCurrentIndex--;
    renderPresentationSlide();
  }
}

// ── Toast système ──
function showToast(msg, type = 'success') {
  let wrap = document.getElementById('_toast-wrap');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.id = '_toast-wrap';
    wrap.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:8px';
    document.body.appendChild(wrap);
  }
  const colors = {
    success: { bg: 'rgba(18,24,38,.97)', border: 'rgba(52,211,153,.35)', text: '#34d399', icon: '<polyline points="20 6 9 17 4 12"/>' },
    error:   { bg: 'rgba(18,24,38,.97)', border: 'rgba(248,113,113,.35)', text: '#f87171', icon: '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>' },
    info:    { bg: 'rgba(18,24,38,.97)', border: 'rgba(108,92,231,.35)',  text: '#8b7cf8', icon: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>' },
  };
  const c = colors[type] || colors.success;
  const el = document.createElement('div');
  el.style.cssText = `display:flex;align-items:center;gap:10px;padding:12px 18px;
    background:${c.bg};border:1px solid ${c.border};border-radius:9px;
    color:${c.text};font-size:13px;font-weight:600;font-family:'DM Sans',sans-serif;
    box-shadow:0 8px 24px rgba(0,0,0,.4);
    animation:_toastIn .22s ease both;`;
  // Icon is trusted static SVG path data; message appended as text node (XSS prevention)
  el.insertAdjacentHTML('afterbegin', `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">${c.icon}</svg>`);
  el.appendChild(document.createTextNode(msg));
  wrap.appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; el.style.transition = 'opacity .3s'; setTimeout(() => el.remove(), 300); }, 3200);
}
if (!document.getElementById('_toast-style')) {
  const s = document.createElement('style');
  s.id = '_toast-style';
  s.textContent = '@keyframes _toastIn{from{opacity:0;transform:translateX(14px)}to{opacity:1;transform:translateX(0)}}';
  document.head.appendChild(s);
}

// ── Notifications de session ──
(function() {
  const p = new URLSearchParams(location.search);
  const t = p.get('toast');
  if (t === 'connected') {
    showToast('Connexion réussie — bienvenue !', 'success');
    history.replaceState({}, '', location.pathname);
  }
})();
