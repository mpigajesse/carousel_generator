// ── slide-core.js — Shared font-sizing schedule for all slide formats ──
// Included before slide-linkedin.js / slide-instagram.js.
// Requires adjustFontSize() and sizeCoverTitle() to be defined by the
// platform-specific file that follows this one.

sizeCoverTitle();
adjustFontSize();
setTimeout(adjustFontSize, 200);
setTimeout(adjustFontSize, 500);
setTimeout(adjustFontSize, 900);

// Re-trigger adjustFontSize when the hero image finishes loading/decoding
// (critical for PDF slides where the flex:1 layout depends on actual height)
const heroImg = document.querySelector('.content-hero-image-wrap img');
if (heroImg && !heroImg.complete) {
  heroImg.addEventListener('load', () => {
    adjustFontSize();
    setTimeout(adjustFontSize, 100);
  });
} else if (heroImg && heroImg.complete) {
  // Image already loaded (base64) — force a deferred recalculation
  setTimeout(adjustFontSize, 50);
}
