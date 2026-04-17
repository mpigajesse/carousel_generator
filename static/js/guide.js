// guide.js — CarouselGen guide page interactivity
'use strict';

// ─── Mobile sidebar toggle (global — called by onclick in HTML) ───────────────
function toggleGuideNav() {
  const sidebar = document.getElementById('guide-sidebar');
  const backdrop = document.getElementById('guide-backdrop');
  if (!sidebar) return;

  const isOpen = sidebar.classList.contains('open');

  if (isOpen) {
    sidebar.classList.remove('open');
    backdrop?.classList.remove('visible');
  } else {
    sidebar.classList.add('open');
    backdrop?.classList.add('visible');
  }
}

// ─── Main init ────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const main = document.getElementById('guide-main');
  if (!main) return;

  // ── 1. Reading progress ──────────────────────────────────────────────────
  const readingBar = document.getElementById('guide-reading-bar');
  const progressFill = document.getElementById('guide-progress-fill');
  const readPct = document.getElementById('guide-read-pct');

  let ticking = false;

  function updateProgress() {
    const scrollTop = main.scrollTop;
    const scrollHeight = main.scrollHeight - main.clientHeight;
    const ratio = scrollHeight > 0 ? Math.min(scrollTop / scrollHeight, 1) : 0;
    const pct = Math.round(ratio * 100);

    if (readingBar) readingBar.style.transform = `scaleX(${ratio})`;
    if (progressFill) progressFill.style.width = `${ratio * 100}%`;
    if (readPct) readPct.textContent = `${pct}%`;

    ticking = false;
  }

  main.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(updateProgress);
      ticking = true;
    }
  }, { passive: true });

  // ── 2. Scrollspy — active section highlighting ───────────────────────────
  const navItems = document.querySelectorAll('.guide-nav-item[data-section]');
  const navList = document.querySelector('.guide-nav');

  function setActiveNav(sectionId) {
    navItems.forEach(item => {
      if (item.dataset.section === sectionId) {
        item.classList.add('active');
        // Scroll the active nav item into view within the sidebar
        item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } else {
        item.classList.remove('active');
      }
    });
  }

  const observerOptions = {
    root: main,
    rootMargin: '-10% 0px -60% 0px',
    threshold: 0,
  };

  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        setActiveNav(entry.target.id);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.guide-section').forEach(section => {
    sectionObserver.observe(section);
  });

  // ── 3. Smooth scrolling for nav clicks ──────────────────────────────────
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const sectionId = item.dataset.section;
      const target = document.getElementById(sectionId);
      if (!target) return;

      target.scrollIntoView({ behavior: 'smooth', block: 'start' });

      // Close sidebar on mobile if open
      const sidebar = document.getElementById('guide-sidebar');
      if (sidebar?.classList.contains('open')) {
        toggleGuideNav();
      }
    });
  });

  // ── 4. Copy code buttons ─────────────────────────────────────────────────
  document.querySelectorAll('.guide-code-copy').forEach(btn => {
    btn.addEventListener('click', () => {
      const wrap = btn.closest('.guide-code-wrap');
      const codeBlock = wrap?.querySelector('.guide-code-block');
      if (!codeBlock) return;

      const text = codeBlock.textContent ?? '';

      navigator.clipboard.writeText(text).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Copié !';
        btn.classList.add('copied');

        setTimeout(() => {
          btn.textContent = originalText;
          btn.classList.remove('copied');
        }, 2000);
      }).catch(() => {
        // Fallback for environments without clipboard API
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);

        const originalText = btn.textContent;
        btn.textContent = 'Copié !';
        btn.classList.add('copied');

        setTimeout(() => {
          btn.textContent = originalText;
          btn.classList.remove('copied');
        }, 2000);
      });
    });
  });
});
