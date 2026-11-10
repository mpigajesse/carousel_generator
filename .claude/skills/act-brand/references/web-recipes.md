# ACT — Web recipes

Snippets HTML/CSS prêts à copier-coller pour produire des pages web, mockups, posts visuels et
templates conformes à la charte ACT.

**Toujours** inclure les Google Fonts et les variables CSS de marque dans le `<head>` :

```html
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Poppins:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Pour les variables CSS, soit inclure `assets/act-tokens.css`, soit copier directement les `--act-*`
dans le `<style>` du document.

---

## 1. Boilerplate page complète

Squelette minimal d'une page ACT, avec tokens inlinés (autonome, sans dépendance externe sauf fonts).

```html
<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>[Titre] — ACT</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cg transform='translate(16 16) rotate(-43.264)'%3E%3Crect x='-9' y='-9' width='18' height='18' fill='%23D35400'/%3E%3C/g%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Poppins:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --act-orange: #D35400; --act-orange-hot: #FF6B00; --act-gold: #F39C12;
    --act-dark: #0A1410; --act-dark-deep: #070E1C;
    --act-green: #1B3022; --act-green-mid: #2C4A35;
    --act-cream: #FCF9F2; --act-muted: #6B7A72;
    --font-display: 'Lora', Georgia, serif;
    --font-body: 'Poppins', -apple-system, system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', Consolas, monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: var(--font-body);
    background: var(--act-dark);
    color: var(--act-cream);
    -webkit-font-smoothing: antialiased;
    line-height: 1.6;
  }
  ::selection { background: var(--act-orange); color: var(--act-cream); }
  .wrap { max-width: 1320px; margin: 0 auto; padding: 0 48px; }
  @media (max-width: 720px) { .wrap { padding: 0 24px; } }
  .d {
    display: inline-block; width: 10px; height: 10px;
    background: var(--act-orange);
    transform: rotate(-43.264deg);
    flex-shrink: 0;
  }
  h1, h2, h3 {
    font-family: var(--font-display);
    font-weight: 500;
    letter-spacing: -0.025em;
    line-height: 1.05;
    text-wrap: balance;
  }
  h1 em, h2 em, h3 em { color: var(--act-orange); font-style: italic; font-weight: 500; }
  .eyebrow {
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--act-orange);
    display: inline-flex;
    align-items: center;
    gap: 12px;
  }
</style>
</head>
<body>
  <main class="wrap">
    <!-- contenu ici -->
  </main>
</body>
</html>
```

---

## 2. Hero section (mode sombre, signature ACT)

```html
<section class="hero">
  <div class="hero-bg"></div>
  <div class="wrap">
    <div class="eyebrow"><span class="d"></span> Conseil · Ingénierie · Formation IA</div>
    <h1 style="font-size: clamp(54px, 8vw, 112px); margin: 24px 0 32px;">
      L'IA <em>opérationnelle</em>.<br>Vraiment.
    </h1>
    <p style="font-size: 20px; max-width: 580px; color: rgba(255,255,255,0.75); font-weight: 300;">
      [Promesse en 1-2 phrases — qui répond à la question : pourquoi ACT plutôt qu'un autre ?]
    </p>
    <div style="margin-top: 40px; display: flex; gap: 16px; flex-wrap: wrap;">
      <a href="#" class="act-btn act-btn--primary">Discuter d'un projet</a>
      <a href="#" class="act-btn act-btn--ghost">Voir nos formations</a>
    </div>
  </div>
</section>

<style>
  .hero { position: relative; padding: 140px 0; overflow: hidden; }
  .hero-bg {
    position: absolute; inset: 0;
    background:
      radial-gradient(ellipse 80% 50% at 20% 30%, rgba(211,84,0,0.28), transparent 60%),
      radial-gradient(ellipse 60% 60% at 85% 80%, rgba(27,48,34,0.5), transparent 60%);
  }
  .hero-bg::before {
    content: '';
    position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 80px 80px;
    mask-image: radial-gradient(ellipse 70% 60% at 50% 40%, black 20%, transparent 75%);
  }
  .hero > .wrap { position: relative; z-index: 2; }
  .act-btn {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 14px 28px;
    font: 600 13px/1 'Poppins', sans-serif;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    text-decoration: none;
    transition: background 0.2s, transform 0.15s;
  }
  .act-btn--primary { background: var(--act-orange); color: var(--act-cream); }
  .act-btn--primary:hover { background: var(--act-orange-hot); transform: translateY(-1px); }
  .act-btn--ghost {
    background: transparent; color: var(--act-cream);
    border: 1px solid var(--act-cream);
  }
  .act-btn--ghost:hover { background: var(--act-cream); color: var(--act-dark); }
</style>
```

---

## 3. Logo dans le markup

```html
<a href="/" class="act-logo" aria-label="ACT — Africa Centred Technology">
  <span class="act-logo-mark"></span>
  <span class="act-logo-txt">
    <span class="act-logo-sigle">ACT</span>
    <span class="act-logo-mention">Africa <em>Centred</em> Technology</span>
  </span>
</a>

<style>
  .act-logo {
    display: inline-flex; align-items: center; gap: 14px;
    text-decoration: none; color: inherit;
  }
  .act-logo-mark {
    width: 32px; height: 32px;
    background: var(--act-orange);
    transform: rotate(-43.264deg);
    flex-shrink: 0;
  }
  .act-logo-txt { display: flex; flex-direction: column; }
  .act-logo-sigle {
    font: 500 28px/1 'Lora', Georgia, serif;
    letter-spacing: -0.02em;
  }
  .act-logo-mention {
    font: 500 9px/1.2 'Poppins', sans-serif;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--act-muted);
    margin-top: 2px;
  }
  .act-logo-mention em {
    font: italic 500 10px/1.2 'Lora', serif;
    color: var(--act-orange);
    text-transform: none;
    letter-spacing: 0;
  }
</style>
```

---

## 4. Carte avec eyebrow + titre + texte + CTA

```html
<article class="act-card">
  <div class="eyebrow"><span class="d"></span> Cas client · Banque</div>
  <h3 style="font-size: 28px; margin: 16px 0;">Réduire le temps de traitement des dossiers de <em>38 %</em>.</h3>
  <p style="color: rgba(255,255,255,0.72); font-weight: 300; line-height: 1.65;">
    Mise en place d'un agent IA pour le pré-traitement des demandes de crédit, en 12 semaines,
    sur les 4 agences pilotes du groupe.
  </p>
  <a href="#" class="act-card-cta">Lire le cas →</a>
</article>

<style>
  .act-card {
    padding: 32px 28px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    transition: border-color 0.2s, transform 0.2s;
  }
  .act-card:hover {
    border-color: rgba(211,84,0,0.4);
    transform: translateY(-2px);
  }
  .act-card-cta {
    display: inline-block;
    margin-top: 20px;
    color: var(--act-orange);
    font: 600 12px/1 'Poppins', sans-serif;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    text-decoration: none;
    transition: gap 0.2s;
  }
  .act-card-cta:hover { color: var(--act-orange-hot); }
</style>
```

---

## 5. Liste à puces losange

```html
<ul class="act-list">
  <li>Première idée concrète, suivie d'un chiffre ou exemple.</li>
  <li>Deuxième idée — pas plus de 2 lignes par item idéalement.</li>
  <li>Troisième idée, qui termine sur une preuve.</li>
</ul>

<style>
  .act-list { list-style: none; padding: 0; }
  .act-list li {
    position: relative;
    padding: 6px 0 6px 22px;
    line-height: 1.6;
  }
  .act-list li::before {
    content: '';
    position: absolute;
    left: 0; top: 13px;
    width: 7px; height: 7px;
    background: var(--act-orange);
    transform: rotate(-43.264deg);
  }
</style>
```

---

## 6. Citation pull-quote

```html
<blockquote class="act-quote">
  <p>L'IA qui tient ses promesses — parce qu'on vous apprend à la <em>piloter</em>.</p>
  <cite>Manifeste ACT</cite>
</blockquote>

<style>
  .act-quote {
    padding: 32px 0 32px 32px;
    border-left: 3px solid var(--act-orange);
    max-width: 720px;
  }
  .act-quote p {
    font: italic 500 28px/1.4 'Lora', serif;
    color: var(--act-cream);
    margin-bottom: 16px;
  }
  .act-quote p em { color: var(--act-orange); font-style: italic; }
  .act-quote cite {
    font: 600 11px/1 'Poppins', sans-serif;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--act-muted);
    font-style: normal;
  }
</style>
```

---

## 7. Tableau

```html
<div class="act-table-wrap">
  <table class="act-table">
    <thead>
      <tr><th>Colonne 1</th><th>Colonne 2</th><th>Colonne 3</th></tr>
    </thead>
    <tbody>
      <tr><td>Cellule</td><td class="mono">42</td><td>Texte</td></tr>
      <tr><td>Cellule</td><td class="mono">128</td><td>Texte</td></tr>
    </tbody>
  </table>
</div>

<style>
  .act-table-wrap {
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
  }
  .act-table {
    width: 100%;
    border-collapse: collapse;
    font: 400 14px/1.5 'Poppins', sans-serif;
  }
  .act-table th, .act-table td {
    padding: 14px 20px;
    text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  .act-table th {
    background: var(--act-dark-deep);
    font: 600 11px/1 'Poppins', sans-serif;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--act-orange);
  }
  .act-table td.mono { font-family: var(--font-mono); font-size: 13px; }
  .act-table tr:last-child td { border-bottom: none; }
</style>
```

---

## 8. Section claire (mode "lite")

Pour alterner les sections claires et sombres dans une page longue :

```html
<section class="lite">
  <div class="wrap">
    <div class="eyebrow"><span class="d"></span> Section claire</div>
    <h2 style="font-size: clamp(36px, 5vw, 56px); margin: 24px 0;">Titre <em>en</em> mode clair.</h2>
    <p style="color: rgba(10,20,16,0.72); font-weight: 300; max-width: 640px; line-height: 1.7;">
      Texte sur fond crème pour rythmer la page longue et alléger la lecture.
    </p>
  </div>
</section>

<style>
  section.lite {
    background: var(--act-cream);
    color: var(--act-dark);
    padding: 120px 0;
  }
  section.lite .eyebrow { color: var(--act-orange); }
  section.lite h2 em { color: var(--act-orange); }
</style>
```

---

## 9. Footer minimal

```html
<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="foot-logo">ACT · Africa <em>Centred</em> Technology</div>
        <p class="foot-copy">Conseil, ingénierie & formation en Intelligence Artificielle.</p>
        <p class="foot-cities">Casablanca · Rabat · Dakar</p>
      </div>
      <div class="foot-col">
        <h5>Navigation</h5>
        <a href="#">Services</a>
        <a href="#">Formations</a>
        <a href="#">Cas clients</a>
        <a href="#">Blog</a>
      </div>
      <div class="foot-col">
        <h5>Contact</h5>
        <a href="mailto:hello@act-tech.com">hello@act-tech.com</a>
        <a href="tel:+212XXXXXXXXX">+212 X XX XX XX XX</a>
      </div>
    </div>
    <div class="foot-bar">
      <span>© 2026 ACT</span>
      <span>◆ L'IA opérationnelle. Vraiment.</span>
    </div>
  </div>
</footer>

<style>
  footer { padding: 64px 0 32px; background: var(--act-dark-deep); border-top: 1px solid rgba(255,255,255,0.08); }
  .foot-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 32px; }
  @media (max-width: 720px) { .foot-grid { grid-template-columns: 1fr; gap: 24px; } }
  .foot-logo { font: 500 22px/1 'Lora', serif; margin-bottom: 16px; }
  .foot-logo em { color: var(--act-orange); font-style: italic; }
  .foot-copy { font-size: 13px; color: rgba(255,255,255,0.6); margin-bottom: 12px; }
  .foot-cities { font: italic 500 14px/1 'Lora', serif; color: var(--act-orange); }
  .foot-col h5 {
    font: 600 10px/1 'Poppins', sans-serif;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--act-orange);
    margin-bottom: 14px;
  }
  .foot-col a {
    display: block;
    font-size: 13px;
    color: rgba(255,255,255,0.75);
    margin-bottom: 8px;
    text-decoration: none;
  }
  .foot-bar {
    margin-top: 48px; padding-top: 24px;
    border-top: 1px solid rgba(255,255,255,0.08);
    display: flex; justify-content: space-between;
    font: 400 11px/1 'JetBrains Mono', monospace;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.08em;
  }
</style>
```

---

## 10. Patterns d'animation discrète

```css
/* Fade-up au chargement, à appliquer aux éléments principaux */
.fade-up {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeUp 0.8s cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
}
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }
.d-1 { animation-delay: 0.1s; }
.d-2 { animation-delay: 0.25s; }
.d-3 { animation-delay: 0.4s; }
```

Appliquer `class="fade-up d-1"` aux éléments principaux du hero pour un chargement orchestré.
**Ne jamais** animer plus de 4-5 éléments en cascade — au-delà, ça devient distrayant.

---

## 11. Accessibilité — règles minimales

- Utiliser des balises sémantiques (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- `lang="fr"` sur le `<html>`
- `alt=""` ou descriptif sur toutes les `<img>` ; `aria-label` sur les liens icône-seule
- Contraste vérifié (voir `tokens.md > WCAG`) — ne **jamais** mettre Orange `#D35400` sur Dark `#0A1410` pour du body text
- `:focus-visible` toujours stylé (par défaut, le navigateur supprime l'outline avec `outline: none`)
- Tailles cliquables ≥ 44×44 px sur mobile (boutons, liens nav)
- `prefers-reduced-motion` respecté pour les animations

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

a:focus-visible, button:focus-visible {
  outline: 2px solid var(--act-orange);
  outline-offset: 3px;
}
```

---

## 12. Test rapide avant de livrer

Coller le HTML dans un navigateur et vérifier :

- [ ] Les 3 polices (Lora, Poppins, JetBrains Mono) chargent (sinon vérifier le `<link>` Google Fonts)
- [ ] Le losange est bien orienté à -43.264°, pas droit
- [ ] L'italique orange Lora apparaît sur les mots-clés des titres
- [ ] Le contraste texte/fond est lisible (zoomer à 200 % et vérifier)
- [ ] Le mobile rendu est lisible (DevTools → 375 px de large)
- [ ] Tous les CTA principaux sont en orange `#D35400` (pas de bleu, pas de violet)
