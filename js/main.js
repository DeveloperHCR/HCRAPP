const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => nav.classList.toggle('open'));
}

const sharedStyles = document.createElement('style');
sharedStyles.textContent = `
  body.light-mode {
    --bg: #edf4fa;
    --bg-strong: #f8fbff;
    --panel: rgba(255, 255, 255, 0.84);
    --panel-strong: #ffffff;
    --card: rgba(255, 255, 255, 0.94);
    --text: #15283b;
    --muted: #52677d;
    --primary: #087f9d;
    --secondary: #6d4ad1;
    --accent: #a65308;
    --success: #08754f;
    --border: rgba(31, 57, 82, 0.16);
    --shadow: 0 18px 45px rgba(36, 61, 84, 0.14);
    --glow: 0 0 22px rgba(8, 127, 157, 0.16);
    color-scheme: light;
    background:
      radial-gradient(circle at top, rgba(8, 145, 178, 0.1), transparent 34%),
      radial-gradient(circle at right, rgba(109, 74, 209, 0.08), transparent 25%),
      linear-gradient(135deg, #ffffff, #edf4fa 48%, #f8fbff);
  }

  body.light-mode::before {
    background-image: linear-gradient(rgba(21, 40, 59, 0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(21, 40, 59, 0.035) 1px, transparent 1px);
  }

  body.light-mode::after { opacity: 0.25; }
  body.light-mode .site-header { background: rgba(248, 251, 255, 0.9); }
  body.light-mode .main-nav a { color: #31475d; }
  body.light-mode .main-nav a:hover,
  body.light-mode .main-nav a.active { color: var(--primary); background: rgba(8, 127, 157, 0.1); }
  body.light-mode .glass-panel,
  body.light-mode .project-card,
  body.light-mode .info-card,
  body.light-mode .panel,
  body.light-mode .detail-card {
    background: rgba(255, 255, 255, 0.9);
    border-color: var(--border);
    box-shadow: var(--shadow);
  }
  body.light-mode .site-footer { background: rgba(237, 244, 250, 0.92); }
  body.light-mode .page-banner {
    background: linear-gradient(135deg, rgba(8, 145, 178, 0.08), rgba(109, 74, 209, 0.06));
    border-bottom-color: var(--border);
  }
  body.light-mode .meta-chip,
  body.light-mode .tag,
  body.light-mode .admin-btn {
    color: var(--muted);
    border-color: var(--border);
    background: rgba(8, 127, 157, 0.06);
  }
  body.light-mode .btn-secondary {
    color: #4a347f;
    background: rgba(109, 74, 209, 0.08);
    border-color: rgba(109, 74, 209, 0.24);
  }
  body.light-mode input,
  body.light-mode textarea,
  body.light-mode select {
    color: var(--text);
    background: rgba(255, 255, 255, 0.94);
    border-color: var(--border);
  }
  body.light-mode .status-pill { background: rgba(255, 255, 255, 0.92); }
  body.light-mode .admin-dashboard[open] { background: #ffffff; color: var(--text); }
  body.light-mode .admin-status-card { background: rgba(8, 127, 157, 0.05); border-color: var(--border); }
  body.light-mode .admin-warning { background: rgba(166, 83, 8, 0.07); }

  .brand-logo { flex: 0 0 auto; min-width: 0; }
  .brand-logo a { display: inline-flex; align-items: center; line-height: 1; white-space: nowrap; }
  .site-logo { flex: 0 0 auto; display: block; }
  .nav-container { align-items: center; }
  .main-nav { flex: 1 1 auto; min-width: 0; }
  .main-nav ul { justify-content: flex-end; flex-wrap: nowrap; gap: 0.2rem; }
  .main-nav a {
    padding: 0.48rem clamp(0.28rem, 0.45vw, 0.5rem);
    font-size: clamp(0.74rem, 0.82vw, 0.88rem);
    white-space: nowrap;
  }

  .theme-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
    gap: 0.35rem;
    padding: 0.55rem 0.85rem;
    border-radius: 999px;
    border: 1px solid rgba(103, 232, 249, 0.28);
    background: rgba(103, 232, 249, 0.08);
    color: var(--text, #eef6ff);
    cursor: pointer;
    font-size: 0.82rem;
    font-weight: 700;
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  }

  .theme-toggle:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 18px rgba(103, 232, 249, 0.2);
  }

  .theme-label-dark { display: none; }
  body.light-mode .theme-label-light { display: none; }
  body.light-mode .theme-label-dark { display: inline; }

  .hero-section {
    grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
    gap: clamp(2rem, 5vw, 4.5rem);
    padding-top: clamp(3rem, 6vw, 5rem);
  }
  .hero-content { max-width: 660px; }
  .hero-content h1 { max-width: 12ch; }
  .hero-content > p { max-width: 58ch; }
  .hero-artwork { width: min(100%, 520px); justify-self: end; }
  .hero-artwork .artwork-img { min-height: clamp(320px, 38vw, 460px); }

  .hero-badges { align-items: center; }
  .hero-badges img { max-width: 100%; height: auto; }

  @media (max-width: 1100px) and (min-width: 861px) {
    .nav-container { flex-wrap: wrap; padding-block: 0.5rem; }
    .main-nav { order: 3; flex: 1 0 100%; }
    .main-nav ul { justify-content: center; flex-wrap: wrap; }
  }
  @media (max-width: 860px) {
    .hero-section { grid-template-columns: 1fr; gap: 1.5rem; }
    .hero-artwork { justify-self: center; width: 100%; }
    .hero-content h1 { max-width: none; }
    .hero-content > p { max-width: none; }
  }
  @media (max-width: 620px) {
    .nav-container { gap: 0.4rem; }
    .brand-logo a { font-size: 1.05rem; gap: 0.45rem; }
    .site-logo { width: 34px; height: 34px; }
    .theme-toggle { width: 44px; height: 40px; padding: 0.4rem; }
    .theme-label-light, .theme-label-dark { display: none !important; }
    .menu-toggle, .language-select { min-height: 40px; }
  }
  @media (max-width: 420px) {
    .nav-container { width: calc(100% - 1rem); }
    .brand-logo a { font-size: 0.98rem; gap: 0.35rem; letter-spacing: 0.02em; }
    .site-logo { width: 32px; height: 32px; }
    .language-select { min-width: 72px; font-size: 0.9rem; }
  }

  @media (pointer: coarse) {
    .btn, .main-nav a, .menu-toggle, .theme-toggle, .language-select, .project-link, .update-links a {
      min-height: 44px;
    }
    .main-nav a { align-items: center; }
  }

  .reveal-card {
    opacity: 0;
    transform: translateY(18px);
    transition: opacity 0.5s ease, transform 0.5s ease, box-shadow 0.25s ease;
  }

  .reveal-card.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .status-pill {
    position: fixed;
    right: 1.25rem;
    bottom: 1.25rem;
    z-index: 20;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.8rem;
    border-radius: 999px;
    background: rgba(7, 19, 31, 0.82);
    border: 1px solid rgba(103, 232, 249, 0.24);
    color: var(--text, #eef6ff);
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    box-shadow: 0 14px 28px rgba(2, 8, 12, 0.35);
    backdrop-filter: blur(12px);
  }

  .status-pill::before {
    content: "";
    width: 0.55rem;
    height: 0.55rem;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 12px rgba(52, 211, 153, 0.9);
  }

  .repo-updates { margin-top: 1.5rem; }
  .repo-updates .update-meta { display: flex; flex-wrap: wrap; gap: 0.75rem; margin: 0.9rem 0 0; }
  .repo-updates .update-meta .meta-chip { text-transform: none; letter-spacing: 0; }
  .repo-updates .update-links { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1rem; }
  .repo-updates .update-links a { color: var(--primary); font-weight: 700; }
`;
document.head.appendChild(sharedStyles);

const yearNode = document.getElementById('year');
if (yearNode) {
  yearNode.textContent = new Date().getFullYear();
}

const contactForm = document.getElementById('contact-form');
if (contactForm instanceof HTMLFormElement) {
  contactForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const formData = new FormData(contactForm);
    const name = String(formData.get('name') || '').trim();
    const email = String(formData.get('email') || '').trim();
    const message = String(formData.get('message') || '').trim();
    const status = document.getElementById('contact-form-status');
    if (!name || !email || !message) {
      if (status) {
        status.textContent = 'Please fill in your name, email, and message.';
      }
      return;
    }

    const subject = `Website message from ${name}`;
    const body = `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`;
    const mailto = `mailto:developerhcr@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

    if (status) {
      status.textContent = 'Your email app should open with the message ready. Review it and press Send there. If it does not open, email developerhcr@gmail.com directly.';
    }

    window.location.href = mailto;
  });
}

const footerBottom = document.querySelector('.footer-bottom');
if (footerBottom && !footerBottom.querySelector('.site-views')) {
  const viewsLink = document.createElement('a');
  viewsLink.className = 'site-views';
  viewsLink.href = 'https://visitor-badge.laobi.icu/';
  viewsLink.target = '_blank';
  viewsLink.rel = 'noreferrer';
  viewsLink.title = 'Counts page loads, not unique visitors';
  viewsLink.style.display = 'inline-flex';
  viewsLink.style.marginTop = '0.5rem';

  const viewsBadge = document.createElement('img');
  viewsBadge.src = 'https://visitor-badge.laobi.icu/badge?page_id=DeveloperHCR.HCRAPP-website&left_text=website%20views&logo=github&right_color=0891b2';
  viewsBadge.alt = 'Website page views; each page load counts';
  viewsBadge.width = 138;
  viewsBadge.height = 20;
  viewsLink.append(viewsBadge);
  footerBottom.append(viewsLink);
}

const currentPage = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
const links = document.querySelectorAll('.main-nav a');
links.forEach((link) => {
  const href = (link.getAttribute('href') || '').toLowerCase();
  if (href === currentPage || (currentPage === '' && href === 'index.html')) {
    link.classList.add('active');
  }
});
const navContainer = document.querySelector('.nav-container');
let themeToggle = navContainer?.querySelector('.theme-toggle');
if (navContainer && !themeToggle) {
  themeToggle = document.createElement('button');
  themeToggle.type = 'button';
  themeToggle.className = 'theme-toggle';
  themeToggle.setAttribute('aria-label', 'Toggle light and dark mode');
  const icon = document.createElement('span');
  icon.className = 'theme-icon';
  icon.setAttribute('aria-hidden', 'true');
  icon.textContent = '☼';
  const lightModeLabel = document.createElement('span');
  lightModeLabel.className = 'theme-label-light';
  lightModeLabel.textContent = 'Light mode';
  const darkModeLabel = document.createElement('span');
  darkModeLabel.className = 'theme-label-dark';
  darkModeLabel.textContent = 'Dark mode';
  themeToggle.append(icon, lightModeLabel, darkModeLabel);
  const menuToggle = navContainer.querySelector('.menu-toggle');
  if (menuToggle) {
    navContainer.insertBefore(themeToggle, menuToggle);
  } else {
    navContainer.appendChild(themeToggle);
  }
}

const SITE_STYLE_PRESETS = {
  'cyan-dark':   { light:false, primary:'#67e8f9', secondary:'#8b5cf6', accent:'#f59e0b', success:'#34d399', bg:'#07131f', bgStrong:'#020b12', panel:'rgba(10,20,30,0.8)', panelStrong:'#0a1724', card:'rgba(13,27,40,0.9)', text:'#eef6ff', muted:'#9fb7c8', border:'rgba(148,163,184,0.18)', bodyBg:'radial-gradient(circle at top, rgba(103,232,249,0.14), transparent 30%), radial-gradient(circle at right, rgba(139,92,246,0.12), transparent 24%), linear-gradient(135deg, #020b12, #0b1724 35%, #07131f)' },
  'light':       { light:true,  primary:'#087f9d', secondary:'#6d4ad1', accent:'#a65308', success:'#08754f', bg:'#edf4fa', bgStrong:'#f8fbff', panel:'rgba(255,255,255,0.84)', panelStrong:'#ffffff', card:'rgba(255,255,255,0.94)', text:'#15283b', muted:'#52677d', border:'rgba(31,57,82,0.16)', bodyBg:'radial-gradient(circle at top, rgba(8,145,178,0.1), transparent 34%), radial-gradient(circle at right, rgba(109,74,209,0.08), transparent 25%), linear-gradient(135deg, #ffffff, #edf4fa 48%, #f8fbff)' },
  'violet-dark': { light:false, primary:'#a78bfa', secondary:'#22d3ee', accent:'#f59e0b', success:'#34d399', bg:'#120b24', bgStrong:'#070514', panel:'rgba(24,16,44,0.82)', panelStrong:'#140d24', card:'rgba(28,20,48,0.92)', text:'#f3efff', muted:'#b7a9d6', border:'rgba(167,139,250,0.2)', bodyBg:'radial-gradient(circle at top, rgba(167,139,250,0.16), transparent 30%), radial-gradient(circle at right, rgba(34,211,238,0.10), transparent 24%), linear-gradient(135deg, #070514, #120b24 35%, #1a1033)' },
  'ocean-dark':  { light:false, primary:'#38bdf8', secondary:'#34d399', accent:'#f59e0b', success:'#34d399', bg:'#041926', bgStrong:'#021019', panel:'rgba(8,30,44,0.82)', panelStrong:'#061d2b', card:'rgba(10,34,50,0.92)', text:'#eafaff', muted:'#9cc3d4', border:'rgba(56,189,248,0.2)', bodyBg:'radial-gradient(circle at top, rgba(56,189,248,0.14), transparent 30%), radial-gradient(circle at right, rgba(52,211,153,0.10), transparent 24%), linear-gradient(135deg, #021019, #041926 35%, #06283a)' },
  'sunset-dark': { light:false, primary:'#fb7185', secondary:'#f59e0b', accent:'#f59e0b', success:'#34d399', bg:'#1f1020', bgStrong:'#120812', panel:'rgba(42,20,36,0.82)', panelStrong:'#241222', card:'rgba(48,24,40,0.92)', text:'#fff1f2', muted:'#d8b4b8', border:'rgba(251,113,133,0.2)', bodyBg:'radial-gradient(circle at top, rgba(251,113,133,0.14), transparent 30%), radial-gradient(circle at right, rgba(245,158,11,0.12), transparent 24%), linear-gradient(135deg, #120812, #1f1020 35%, #2a1420)' },
  'forest-dark': { light:false, primary:'#34d399', secondary:'#a3e635', accent:'#f59e0b', success:'#34d399', bg:'#071a14', bgStrong:'#030e0b', panel:'rgba(10,32,24,0.82)', panelStrong:'#081f17', card:'rgba(12,36,28,0.92)', text:'#ecfdf5', muted:'#9fc7b4', border:'rgba(52,211,153,0.2)', bodyBg:'radial-gradient(circle at top, rgba(52,211,153,0.13), transparent 30%), radial-gradient(circle at right, rgba(163,230,53,0.10), transparent 24%), linear-gradient(135deg, #030e0b, #071a14 35%, #0b2a1f)' },
  'rose-dark':   { light:false, primary:'#f472b6', secondary:'#818cf8', accent:'#f59e0b', success:'#34d399', bg:'#1c1020', bgStrong:'#100812', panel:'rgba(36,18,38,0.82)', panelStrong:'#211024', card:'rgba(40,22,42,0.92)', text:'#fdf2f8', muted:'#d8b4cc', border:'rgba(244,114,182,0.2)', bodyBg:'radial-gradient(circle at top, rgba(244,114,182,0.14), transparent 30%), radial-gradient(circle at right, rgba(129,140,248,0.10), transparent 24%), linear-gradient(135deg, #100812, #1c1020 35%, #281428)' },
  'amber-dark':  { light:false, primary:'#f59e0b', secondary:'#f97316', accent:'#f59e0b', success:'#34d399', bg:'#1b1408', bgStrong:'#100c04', panel:'rgba(38,28,10,0.82)', panelStrong:'#221a08', card:'rgba(42,32,12,0.92)', text:'#fffbeb', muted:'#d6c29b', border:'rgba(245,158,11,0.2)', bodyBg:'radial-gradient(circle at top, rgba(245,158,11,0.13), transparent 30%), radial-gradient(circle at right, rgba(249,115,22,0.10), transparent 24%), linear-gradient(135deg, #100c04, #1b1408 35%, #2a200c)' },
  'mono-dark':   { light:false, primary:'#e5e7eb', secondary:'#9ca3af', accent:'#d4d4d8', success:'#a3a3a3', bg:'#111318', bgStrong:'#090a0d', panel:'rgba(24,27,34,0.9)', panelStrong:'#171a21', card:'rgba(28,31,38,0.94)', text:'#f3f4f6', muted:'#a1a1aa', border:'rgba(229,231,235,0.16)', bodyBg:'radial-gradient(circle at top, rgba(229,231,235,0.08), transparent 30%), linear-gradient(135deg, #090a0d, #111318 35%, #171a22)' }
};

function getSavedSiteStyle() {
  try {
    const style = localStorage.getItem('developerhcr-style');
    if (style && SITE_STYLE_PRESETS[style]) return style;
    const theme = localStorage.getItem('developerhcr-theme') || 'dark';
    return theme === 'light' ? 'light' : 'cyan-dark';
  } catch (error) {
    return 'cyan-dark';
  }
}

function applySiteStyle(styleName, persist) {
  const style = SITE_STYLE_PRESETS[styleName] ? styleName : 'cyan-dark';
  const p = SITE_STYLE_PRESETS[style];
  document.body.classList.toggle('light-mode', !!p.light);
  const root = document.documentElement;
  const vars = {
    '--bg': p.bg, '--bg-strong': p.bgStrong, '--panel': p.panel, '--panel-strong': p.panelStrong, '--card': p.card,
    '--text': p.text, '--muted': p.muted, '--primary': p.primary, '--secondary': p.secondary, '--accent': p.accent,
    '--success': p.success, '--border': p.border
  };
  Object.keys(vars).forEach((k) => root.style.setProperty(k, vars[k]));
  document.body.style.background = p.bodyBg;
  if (persist) {
    try {
      localStorage.setItem('developerhcr-style', style);
      localStorage.setItem('developerhcr-theme', p.light ? 'light' : 'dark');
    } catch (error) {}
  }
  return style;
}

let savedStyle = applySiteStyle(getSavedSiteStyle(), false);

if (themeToggle) {
  themeToggle.setAttribute('aria-pressed', String(document.body.classList.contains('light-mode')));
  themeToggle.addEventListener('click', () => {
    savedStyle = document.body.classList.contains('light-mode') ? 'cyan-dark' : 'light';
    applySiteStyle(savedStyle, true);
    themeToggle.setAttribute('aria-pressed', String(document.body.classList.contains('light-mode')));
  });
}
const heroArtwork = document.querySelector('.hero-artwork .glass-panel');
if (heroArtwork && window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
  heroArtwork.addEventListener('pointermove', (event) => {
    const rect = heroArtwork.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width - 0.5) * 12;
    const y = ((event.clientY - rect.top) / rect.height - 0.5) * -12;
    heroArtwork.style.transform = `perspective(1200px) rotateX(${y}deg) rotateY(${x}deg)`;
  });

  heroArtwork.addEventListener('pointerleave', () => {
    heroArtwork.style.transform = 'perspective(1200px) rotateX(0deg) rotateY(0deg)';
  });
}

const revealTargets = document.querySelectorAll('.project-card, .info-card, .panel');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  revealTargets.forEach((card) => {
    card.classList.add('reveal-card');
    observer.observe(card);
  });
} else {
  revealTargets.forEach((card) => card.classList.add('visible'));
}

const statusPill = document.createElement('div');
statusPill.className = 'status-pill';
statusPill.textContent = 'system online';
document.body.appendChild(statusPill);

const secretSequence = 'devhcr';
let secretInput = '';
const activateSecretMode = () => {
  document.body.classList.add('secret-mode');
  const secretIndicator = document.getElementById('secret-indicator');
  if (secretIndicator) {
    secretIndicator.textContent = 'stealth mode active';
  }
  if (statusPill) {
    statusPill.textContent = 'stealth mode';
    statusPill.style.borderColor = 'rgba(103, 232, 249, 0.48)';
  }
  if (console && console.info) {
    console.info('DeveloperHCR stealth mode enabled. Hidden mode is active.');
  }
};

document.addEventListener('keydown', (event) => {
  secretInput += event.key.toLowerCase();
  if (secretInput.length > secretSequence.length) {
    secretInput = secretInput.slice(-secretSequence.length);
  }
  if (secretInput === secretSequence) {
    activateSecretMode();
    secretInput = '';
  }
});
