function adjustFontSize() {
  const slideEl = document.querySelector('.slide');
  const footer = document.getElementById('slide-footer');
  const coverTitle = document.getElementById('cover-title');
  const mainTitle = document.getElementById('slide-title');
  const body = document.getElementById('slide-body');
  const topbar = document.querySelector('.slide-topbar');

  if (!slideEl || !footer) return;

  const slideH = 1080;
  const topbarH = topbar ? topbar.getBoundingClientRect().height + 24 : 80;
  const footerH = footer.getBoundingClientRect().height;
  const availH = slideH - topbarH - footerH - 60;

  let iterations = 0;
  const maxIter = 100;

  function contentBottom() {
    const content = document.querySelector('.content');
    if (!content) return 0;
    // Layout héro : vérifier le bas du caption (dernier enfant visible)
    if (!content.lastElementChild) return 0;
    return content.lastElementChild.getBoundingClientRect().bottom;
  }

  function footerTop() {
    return footer.getBoundingClientRect().top;
  }

  function isOverflowing() {
    return contentBottom() > footerTop() - 12;
  }

  while (isOverflowing() && iterations < maxIter) {
    // Cover titles
    if (coverTitle) {
      const sz = parseFloat(window.getComputedStyle(coverTitle).fontSize);
      if (sz > 32) coverTitle.style.fontSize = (sz - 2) + 'px';
    }
    // Content titles
    if (mainTitle) {
      const sz = parseFloat(window.getComputedStyle(mainTitle).fontSize);
      if (sz > 24) mainTitle.style.fontSize = (sz - 1) + 'px';
    }
    // Body text
    if (body) {
      const sz = parseFloat(window.getComputedStyle(body).fontSize);
      if (sz > 13) {
        body.style.fontSize = (sz - 0.7) + 'px';
        body.style.lineHeight = '1.4';
      }
    }
    // Sub-headings
    document.querySelectorAll('.slide-h3').forEach(el => {
      const sz = parseFloat(window.getComputedStyle(el).fontSize);
      if (sz > 18) el.style.fontSize = (sz - 1) + 'px';
    });
    // Bullets
    document.querySelectorAll('.bullets li').forEach(el => {
      const sz = parseFloat(window.getComputedStyle(el).fontSize);
      if (sz > 13) el.style.fontSize = (sz - 0.7) + 'px';
    });
    // Compare
    document.querySelectorAll('.compare-head, .compare-body').forEach(el => {
      const sz = parseFloat(window.getComputedStyle(el).fontSize);
      if (sz > 14) el.style.fontSize = (sz - 1) + 'px';
    });
    // Images Markdown en bloc
    document.querySelectorAll('.slide-figure').forEach(el => {
      const sz = parseFloat(el.style.maxHeight) || 220;
      if (sz > 60) el.style.maxHeight = (sz - 8) + 'px';
    });
    // Caption héro : réduire fonte si débordement
    const caption = document.getElementById('slide-body');
    if (caption && caption.closest('.content-hero')) {
      const sz = parseFloat(window.getComputedStyle(caption).fontSize);
      if (sz > 14) caption.style.fontSize = (sz - 1) + 'px';
    }
    iterations++;
  }
}

// Dynamic cover title sizing
function sizeCoverTitle() {
  const el = document.getElementById('cover-title');
  if (!el) return;
  const len = el.textContent.trim().length;
  let size;
  if (len < 20)       size = 110;
  else if (len < 35)  size = 90;
  else if (len < 55)  size = 72;
  else if (len < 80)  size = 58;
  else                size = 48;
  el.style.fontSize = size + 'px';
}

// Scheduling: see slide-core.js (included after this file)
