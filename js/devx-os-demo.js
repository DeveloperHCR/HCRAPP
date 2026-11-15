const desktop = document.getElementById('desktop');
const windowsHost = document.getElementById('windows');
const taskItems = document.getElementById('task-items');
const startButton = document.getElementById('start-button');
const startMenu = document.getElementById('start-menu');
const status = document.getElementById('demo-status');
const appDetails = {
  welcome: { title: 'Welcome to DevX OS', icon: '◈' },
  files: { title: 'File Manager', icon: '📁' },
  notes: { title: 'Notes', icon: '📝' },
  settings: { title: 'Settings', icon: '⚙️' },
  admin: { title: 'Admin Panel', icon: '🛡️' },
  about: { title: 'About DevX OS', icon: 'ℹ️' }
};
let topWindow = 1;
let demoUserCounter = 3;
const openWindows = new Map();

function focusWindow(app, windowElement) {
  topWindow += 1;
  windowElement.style.zIndex = String(topWindow);
  openWindows.get(app).taskButton.setAttribute('aria-pressed', 'true');
}

function setMinimized(app, minimized) {
  const entry = openWindows.get(app);
  if (!entry) return;
  entry.element.hidden = minimized;
  entry.taskButton.setAttribute('aria-pressed', String(!minimized));
  if (!minimized) focusWindow(app, entry.element);
}

function closeWindow(app) {
  const entry = openWindows.get(app);
  if (!entry) return;
  entry.element.remove();
  entry.taskButton.remove();
  openWindows.delete(app);
}

function openApp(app) {
  const details = appDetails[app];
  if (!details) return;
  startMenu.hidden = true;
  startButton.setAttribute('aria-expanded', 'false');

  if (openWindows.has(app)) {
    setMinimized(app, false);
    return;
  }

  const template = document.querySelector(`template[data-app-content="${app}"]`);
  const windowElement = document.createElement('section');
  windowElement.className = 'window';
  windowElement.dataset.app = app;
  windowElement.setAttribute('aria-label', details.title);

  const titlebar = document.createElement('header');
  titlebar.className = 'window-titlebar';
  const title = document.createElement('span');
  title.className = 'window-title';
  title.textContent = `${details.icon}  ${details.title}`;
  const controls = document.createElement('div');
  controls.className = 'window-controls';
  controls.innerHTML = '<button type="button" data-window-action="minimize" aria-label="Minimize window">−</button><button type="button" data-window-action="maximize" aria-label="Maximize or restore window">□</button><button type="button" class="close" data-window-action="close" aria-label="Close window">×</button>';
  titlebar.append(title, controls);

  const body = document.createElement('div');
  body.className = 'window-body';
  body.append(template.content.cloneNode(true));
  windowElement.append(titlebar, body);
  windowsHost.append(windowElement);

  const taskButton = document.createElement('button');
  taskButton.type = 'button';
  taskButton.className = 'task-item';
  taskButton.setAttribute('aria-label', `Show ${details.title}`);
  taskButton.setAttribute('aria-pressed', 'true');
  const taskIcon = document.createElement('span');
  taskIcon.textContent = details.icon;
  const taskTitle = document.createElement('span');
  taskTitle.textContent = details.title;
  taskButton.append(taskIcon, taskTitle);
  taskItems.append(taskButton);
  openWindows.set(app, { element: windowElement, taskButton });
  focusWindow(app, windowElement);
  status.textContent = `${details.title} opened`;
}

function beginDrag(event, titlebar) {
  if (event.target.closest('button') || event.button !== 0 || titlebar.parentElement.classList.contains('maximized')) return;
  const windowElement = titlebar.parentElement;
  const app = windowElement.dataset.app;
  const desktopBounds = desktop.getBoundingClientRect();
  const windowBounds = windowElement.getBoundingClientRect();
  const originX = event.clientX;
  const originY = event.clientY;
  const offsetX = windowBounds.left - desktopBounds.left;
  const offsetY = windowBounds.top - desktopBounds.top;
  windowElement.style.transform = 'none';
  windowElement.style.left = `${offsetX}px`;
  windowElement.style.top = `${offsetY}px`;
  focusWindow(app, windowElement);

  function move(moveEvent) {
    const maxX = desktop.clientWidth - windowElement.offsetWidth;
    const maxY = desktop.clientHeight - windowElement.offsetHeight - 48;
    const nextX = Math.max(0, Math.min(maxX, offsetX + moveEvent.clientX - originX));
    const nextY = Math.max(42, Math.min(maxY, offsetY + moveEvent.clientY - originY));
    windowElement.style.left = `${nextX}px`;
    windowElement.style.top = `${nextY}px`;
  }
  function stop() {
    document.removeEventListener('pointermove', move);
    document.removeEventListener('pointerup', stop);
  }
  document.addEventListener('pointermove', move);
  document.addEventListener('pointerup', stop, { once: true });
  event.preventDefault();
}

desktop.addEventListener('click', (event) => {
  const appButton = event.target.closest('[data-open-app]');
  if (appButton) {
    openApp(appButton.dataset.openApp);
    return;
  }
  const adminAction = event.target.closest('[data-admin-action]');
  if (adminAction && adminAction.closest('.window[data-app="admin"]')) {
    const dashboard = adminAction.closest('.admin-dashboard');
    const userTable = dashboard.querySelector('[data-admin-users]');
    const message = dashboard.querySelector('[data-admin-status]');
    if (adminAction.dataset.adminAction === 'refresh') {
      message.textContent = `Sample dashboard refreshed at ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}.`;
    } else if (adminAction.dataset.adminAction === 'add-user') {
      demoUserCounter += 1;
      const userNumber = demoUserCounter;
      const row = userTable.insertRow();
      const name = `Demo User ${userNumber}`;
      const nameCell = row.insertCell();
      nameCell.textContent = name;
      row.insertCell().textContent = 'Viewer';
      const statusCell = row.insertCell();
      statusCell.className = 'status-good';
      statusCell.textContent = 'Active';
      const actionCell = row.insertCell();
      const removeButton = document.createElement('button');
      removeButton.type = 'button';
      removeButton.dataset.adminAction = 'remove-user';
      removeButton.setAttribute('aria-label', `Remove ${name}`);
      removeButton.textContent = 'Remove';
      actionCell.append(removeButton);
      dashboard.querySelector('[data-user-count]').textContent = String(userTable.rows.length);
      message.textContent = `${name} added to this demo.`;
    } else if (adminAction.dataset.adminAction === 'remove-user') {
      const name = adminAction.closest('tr').cells[0].textContent;
      adminAction.closest('tr').remove();
      dashboard.querySelector('[data-user-count]').textContent = String(userTable.rows.length);
      message.textContent = `${name} removed from this demo.`;
    }
    return;
  }
  const windowElement = event.target.closest('.window');
  if (!windowElement) return;
  const app = windowElement.dataset.app;
  const action = event.target.closest('[data-window-action]')?.dataset.windowAction;
  if (action === 'close') closeWindow(app);
  else if (action === 'minimize') setMinimized(app, true);
  else if (action === 'maximize') {
    windowElement.classList.toggle('maximized');
    status.textContent = windowElement.classList.contains('maximized') ? `${appDetails[app].title} maximized` : `${appDetails[app].title} restored`;
  } else focusWindow(app, windowElement);
});

desktop.addEventListener('pointerdown', (event) => {
  const titlebar = event.target.closest('.window-titlebar');
  if (titlebar) beginDrag(event, titlebar);
});

taskItems.addEventListener('click', (event) => {
  const taskButton = event.target.closest('.task-item');
  if (!taskButton) return;
  const [app, entry] = [...openWindows].find(([, item]) => item.taskButton === taskButton) || [];
  if (!entry) return;
  setMinimized(app, !entry.element.hidden);
});

startButton.addEventListener('click', () => {
  startMenu.hidden = !startMenu.hidden;
  startButton.setAttribute('aria-expanded', String(!startMenu.hidden));
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && !startMenu.hidden) {
    startMenu.hidden = true;
    startButton.setAttribute('aria-expanded', 'false');
  }
});

function updateClock() {
  const now = new Date();
  document.getElementById('task-clock').textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  document.getElementById('desktop-date').textContent = now.toLocaleDateString([], { month: 'short', day: 'numeric' });
}
updateClock();
window.setInterval(updateClock, 30000);
openApp(window.location.hash === '#admin-panel' ? 'admin' : 'welcome');
