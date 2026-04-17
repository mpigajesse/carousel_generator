// guide-interactive.js — Guide page interactive enhancements
'use strict';

document.addEventListener('DOMContentLoaded', () => {

  // ─── 1. Theme swatch selection ───────────────────────────────────────────
  const swatches = document.querySelectorAll('.guide-theme-swatch');
  swatches.forEach(sw => {
    sw.addEventListener('click', () => {
      swatches.forEach(s => {
        s.classList.remove('is-selected');
        s.style.borderColor = '';
      });
      sw.classList.add('is-selected');
      sw.style.borderColor = 'rgba(108,99,255,0.5)';
    });
  });

  // ─── 2. FAQ accordion — close others when one opens ──────────────────────
  const faqs = document.querySelectorAll('details.guide-faq-item');
  faqs.forEach(faq => {
    faq.addEventListener('toggle', () => {
      if (faq.open) {
        faqs.forEach(other => {
          if (other !== faq && other.open) {
            other.open = false;
          }
        });
      }
    });
  });

  // ─── 3. Slide mock hover glow ─────────────────────────────────────────────
  document.querySelectorAll('.guide-slide-mock').forEach(mock => {
    mock.addEventListener('mouseenter', () => {
      mock.style.boxShadow = '0 0 0 1px rgba(108,99,255,0.3), 0 8px 32px rgba(108,99,255,0.15)';
      mock.style.transform = 'translateY(-2px)';
      mock.style.transition = 'all 220ms cubic-bezier(0.16,1,0.3,1)';
    });
    mock.addEventListener('mouseleave', () => {
      mock.style.boxShadow = '';
      mock.style.transform = '';
    });
  });

  // ─── 4. Guide section entry animations via IntersectionObserver ──────────
  const sections = document.querySelectorAll('.guide-section');
  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        sectionObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  sections.forEach(s => {
    s.style.opacity = '0';
    s.style.transform = 'translateY(16px)';
    s.style.transition = 'opacity 400ms cubic-bezier(0.16,1,0.3,1), transform 400ms cubic-bezier(0.16,1,0.3,1)';
    sectionObserver.observe(s);
  });

  // ─── 5. Keyboard navigation hint toast ───────────────────────────────────
  function showToast(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.style.cssText = `
      position: fixed; bottom: 24px; right: 24px; z-index: 1000;
      background: rgba(12,12,20,0.95); border: 1px solid rgba(108,99,255,0.3);
      backdrop-filter: blur(12px); border-radius: 10px;
      padding: 12px 16px; font-size: 13px; color: rgba(226,226,232,0.85);
      max-width: 300px; line-height: 1.5;
      animation: slideIn 300ms cubic-bezier(0.16,1,0.3,1);
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(8px)';
      toast.style.transition = 'all 200ms ease';
      setTimeout(() => toast.remove(), 200);
    }, duration);
  }

  const previewSection = document.querySelector('#preview');
  if (previewSection && !localStorage.getItem('guide_kbd_hint_shown')) {
    const hintObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          showToast('Conseil : utilisez ← → pour naviguer en mode présentation');
          localStorage.setItem('guide_kbd_hint_shown', '1');
          hintObserver.unobserve(previewSection);
        }
      });
    }, { threshold: 0.1 });
    hintObserver.observe(previewSection);
  }

});
