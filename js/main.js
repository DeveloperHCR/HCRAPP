const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => nav.classList.toggle('open'));
}
const yearNode = document.getElementById('year');
if (yearNode) {
  yearNode.textContent = new Date().getFullYear();
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
  viewsBadge.src = 'https://visitor-badge.laobi.icu/badge?page_id=DeveloperHCR.HCRAPP&left_text=website%20views&logo=github&right_color=0891b2';
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
