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
  calculator: { title: 'Calculator', icon: '🧮' },
  calendar: { title: 'Calendar', icon: '📅' },
  browser: { title: 'Browser (demo)', icon: '🌐' },
  terminal: { title: 'Terminal (simulated)', icon: '⌨️' },
  monitor: { title: 'System Monitor (sample)', icon: '📊' },
  about: { title: 'About DevX OS', icon: 'ℹ️' }
};
let topWindow = 1;
let demoUserCounter = 3;
const openWindows = new Map();

function calculate(expression) {
  const tokens = expression.match(/\d*\.?\d+|[()+\-*/]/g) || [];
  if (!tokens.length || tokens.join('') !== expression.replace(/\s+/g, '')) {
    throw new Error('Enter a valid arithmetic expression.');
  }
  let position = 0;

  function parseExpression() {
    let value = parseTerm();
    while (tokens[position] === '+' || tokens[position] === '-') {
      const operator = tokens[position++];
      const next = parseTerm();
      value = operator === '+' ? value + next : value - next;
    }
    return value;
  }

  function parseTerm() {
    let value = parseFactor();
    while (tokens[position] === '*' || tokens[position] === '/') {
      const operator = tokens[position++];
      const next = parseFactor();
      if (operator === '/' && next === 0) throw new Error('Cannot divide by zero.');
      value = operator === '*' ? value * next : value / next;
    }
    return value;
  }

  function parseFactor() {
    const token = tokens[position++];
    if (token === '+') return parseFactor();
    if (token === '-') return -parseFactor();
    if (token === '(') {
      const value = parseExpression();
      if (tokens[position++] !== ')') throw new Error('Check the parentheses.');
      return value;
    }
    if (token === undefined || !/^\d*\.?\d+$/.test(token)) {
      throw new Error('Enter a valid arithmetic expression.');
    }
    return Number(token);
  }

  const result = parseExpression();
  if (position !== tokens.length || !Number.isFinite(result)) {
    throw new Error('Enter a valid arithmetic expression.');
  }
  return Number(result.toPrecision(12));
}

function renderCalendar(windowElement) {
  const now = new Date();
  const title = windowElement.querySelector('[data-calendar-title]');
  const grid = windowElement.querySelector('[data-calendar-grid]');
  title.textContent = now.toLocaleDateString([], { month: 'long', year: 'numeric' });
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  dayNames.forEach((day) => {
    const cell = document.createElement('span');
    cell.className = 'calendar-day-name';
    cell.textContent = day;
    grid.append(cell);
  });
  const firstWeekday = new Date(now.getFullYear(), now.getMonth(), 1).getDay();
  const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
  for (let blank = 0; blank < firstWeekday; blank += 1) grid.append(document.createElement('span'));
  for (let day = 1; day <= daysInMonth; day += 1) {
    const cell = document.createElement('span');
    cell.textContent = String(day);
    if (day === now.getDate()) cell.className = 'today';
    grid.append(cell);
  }
}

function focusWindow(app, windowElement) {
  topWindow += 1;
  windowElement.style.zIndex = String(topWindow);
  for (const entry of openWindows.values()) entry.taskButton.setAttribute('aria-pressed', 'false');
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
  if (app === 'calendar') renderCalendar(windowElement);

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
  const calculatorKey = event.target.closest('[data-calc-key]');
  if (calculatorKey) {
    const calculator = calculatorKey.closest('.window');
    const display = calculator.querySelector('.calc-display');
    const message = calculator.querySelector('[data-calc-status]');
    const key = calculatorKey.dataset.calcKey;
    if (key === 'clear') display.value = '';
    else if (key === 'backspace') display.value = display.value.slice(0, -1);
    else if (key === '=') {
      try {
        display.value = String(calculate(display.value));
        message.textContent = '';
      } catch (error) {
        message.textContent = error.message;
      }
    } else display.value += key === '×' ? '*' : key === '÷' ? '/' : key;
    if (key !== '=') message.textContent = '';
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

desktop.addEventListener('submit', (event) => {
  const browserForm = event.target.closest('[data-browser-form]');
  if (browserForm) {
    event.preventDefault();
    const page = browserForm.closest('.window').querySelector('[data-browser-page]');
    const address = browserForm.elements.address.value.trim().toLowerCase();
    if (address === 'devx://home') {
      page.innerHTML = '<h3>Welcome</h3><p>DevX OS browser preview. Try <code>devx://home</code> or <code>devx://about</code>.</p>';
    } else if (address === 'devx://about') {
      page.innerHTML = '<h3>About DevX OS</h3><p>This is a local sample page inside the browser preview. External websites are not loaded.</p>';
    } else {
      page.innerHTML = '<h3>Demo navigation only</h3><p>For safety, this browser preview only opens built-in devx://home and devx://about pages.</p>';
    }
    return;
  }

  const terminalForm = event.target.closest('[data-terminal-form]');
  if (!terminalForm) return;
  event.preventDefault();
  const output = terminalForm.closest('.window').querySelector('[data-terminal-output]');
  const input = terminalForm.elements.command;
  const command = input.value.trim().toLowerCase();
  const outputs = {
    help: 'Available demo commands: help, date, whoami, ls, clear',
    date: new Date().toString(),
    whoami: 'demo-user (temporary preview session)',
    ls: 'Documents/   Projects/   Welcome.txt'
  };
  if (command === 'clear') output.textContent = 'DevX OS Demo Terminal\nType "help" to see available demo commands.';
  else if (command) output.textContent += `\n$ ${input.value}\n${outputs[command] || 'Command not available in the safe demo terminal. Type "help" for options.'}`;
  input.value = '';
  output.scrollTop = output.scrollHeight;
});

desktop.addEventListener('pointerdown', (event) => {
  const windowElement = event.target.closest('.window');
  if (windowElement) focusWindow(windowElement.dataset.app, windowElement);
  const titlebar = event.target.closest('.window-titlebar');
  if (titlebar) beginDrag(event, titlebar);
});

desktop.addEventListener('keydown', (event) => {
  if (event.key !== 'Enter' || !event.target.matches('.calc-display')) return;
  event.preventDefault();
  const display = event.target;
  const message = display.closest('.window').querySelector('[data-calc-status]');
  try {
    display.value = String(calculate(display.value));
    message.textContent = '';
  } catch (error) {
    message.textContent = error.message;
  }
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
