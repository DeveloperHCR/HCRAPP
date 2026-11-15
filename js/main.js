const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => nav.classList.toggle('open'));
}

const advancedModeStyles = document.createElement('style');
advancedModeStyles.textContent = `
  body.advanced-mode {
    --bg: #040b12;
    --bg-strong: #01070d;
    --card: rgba(12, 22, 33, 0.9);
    --panel: rgba(9, 18, 28, 0.82);
    --panel-strong: rgba(8, 16, 24, 0.92);
    --border: rgba(103, 232, 249, 0.24);
    --shadow: 0 28px 60px rgba(2, 8, 12, 0.7);
  }

  body.advanced-mode::before {
    background-image: linear-gradient(rgba(103, 232, 249, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(103, 232, 249, 0.05) 1px, transparent 1px);
    background-size: 26px 26px;
  }

  body.advanced-mode .site-header {
    background: rgba(4, 14, 20, 0.78);
    border-bottom-color: rgba(103, 232, 249, 0.2);
    box-shadow: 0 12px 26px rgba(2, 8, 12, 0.3);
  }

  body.advanced-mode .glass-panel,
  body.advanced-mode .project-card,
  body.advanced-mode .info-card,
  body.advanced-mode .panel {
    background: linear-gradient(180deg, rgba(13, 24, 34, 0.9), rgba(8, 16, 24, 0.9));
    border-color: rgba(103, 232, 249, 0.22);
    box-shadow: 0 24px 60px rgba(2, 8, 12, 0.5);
  }

  body.advanced-mode .btn-primary {
    background: linear-gradient(135deg, #67e8f9, #8b5cf6);
    box-shadow: 0 12px 35px rgba(103, 232, 249, 0.28);
  }

  body.advanced-mode .project-card:hover,
  body.advanced-mode .info-card:hover,
  body.advanced-mode .glass-panel:hover {
    transform: translateY(-4px) scale(1.005);
    border-color: rgba(103, 232, 249, 0.5);
    box-shadow: 0 26px 70px rgba(12, 18, 30, 0.7);
  }

  body.advanced-mode .main-nav a.active,
  body.advanced-mode .main-nav a:hover {
    box-shadow: inset 0 0 0 1px rgba(103, 232, 249, 0.25);
  }

  body.advanced-mode .status-pill {
    background: rgba(4, 15, 20, 0.9);
    border-color: rgba(103, 232, 249, 0.35);
  }

  .advanced-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.55rem 0.85rem;
    border-radius: 999px;
    border: 1px solid rgba(103, 232, 249, 0.28);
    background: rgba(103, 232, 249, 0.08);
    color: var(--text, #eef6ff);
    cursor: pointer;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  }

  .advanced-toggle:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 18px rgba(103, 232, 249, 0.2);
  }

  body.advanced-mode .advanced-toggle {
    background: rgba(103, 232, 249, 0.18);
    border-color: rgba(103, 232, 249, 0.4);
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
document.head.appendChild(advancedModeStyles);

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
const advancedToggle = document.createElement('button');
advancedToggle.type = 'button';
advancedToggle.className = 'advanced-toggle';
advancedToggle.setAttribute('aria-label', 'Toggle advanced mode');
advancedToggle.textContent = 'Advanced mode';
const navContainer = document.querySelector('.nav-container');
if (navContainer && !navContainer.querySelector('.advanced-toggle')) {
  const menuToggle = navContainer.querySelector('.menu-toggle');
  if (menuToggle) {
    navContainer.insertBefore(advancedToggle, menuToggle.nextSibling);
  } else {
    navContainer.appendChild(advancedToggle);
  }
}

const savedAdvancedMode = localStorage.getItem('developerhcr-advanced-mode') === 'true';
document.body.classList.toggle('advanced-mode', savedAdvancedMode);
advancedToggle.textContent = savedAdvancedMode ? 'Premium on' : 'Advanced mode';
advancedToggle.addEventListener('click', () => {
  const isNowAdvanced = !document.body.classList.contains('advanced-mode');
  document.body.classList.toggle('advanced-mode', isNowAdvanced);
  advancedToggle.textContent = isNowAdvanced ? 'Premium on' : 'Advanced mode';
  localStorage.setItem('developerhcr-advanced-mode', String(isNowAdvanced));
});
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
