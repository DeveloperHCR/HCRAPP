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

  .brand-logo { flex: 0 0 auto; }
  .brand-logo a { white-space: nowrap; }
  .site-logo { flex: 0 0 auto; }
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

  @media (max-width: 1100px) and (min-width: 861px) {
    .nav-container { flex-wrap: wrap; padding-block: 0.5rem; }
    .main-nav { order: 3; flex: 1 0 100%; }
    .main-nav ul { justify-content: center; flex-wrap: wrap; }
  }
  @media (max-width: 620px) {
    .theme-toggle { width: 42px; height: 38px; padding: 0.4rem; }
    .theme-label-light, .theme-label-dark { display: none !important; }
  }
  @media (max-width: 860px) {
    .hero-section { grid-template-columns: 1fr; gap: 1.5rem; }
    .hero-artwork { justify-self: center; }
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

let savedTheme = 'dark';
try {
  savedTheme = localStorage.getItem('developerhcr-theme') || 'dark';
} catch (error) {
  console.error('Unable to read the saved color theme.', error);
}
document.body.classList.toggle('light-mode', savedTheme === 'light');

if (themeToggle) {
  themeToggle.setAttribute('aria-pressed', String(savedTheme === 'light'));
  themeToggle.addEventListener('click', () => {
    const isLightMode = document.body.classList.toggle('light-mode');
    themeToggle.setAttribute('aria-pressed', String(isLightMode));
    try {
      localStorage.setItem('developerhcr-theme', isLightMode ? 'light' : 'dark');
    } catch (error) {
      console.error('Unable to save the selected color theme.', error);
    }
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
