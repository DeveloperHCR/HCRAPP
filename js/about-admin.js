(function () {
  const openBtn = document.getElementById('open-admin');
  const dialog = document.getElementById('admin-dialog');
  const form = document.getElementById('admin-password-form');
  const input = document.getElementById('admin-password');
  const status = document.getElementById('admin-auth-status');
  const closeBtn = document.getElementById('close-admin');

  if (!(openBtn instanceof HTMLButtonElement) || !(dialog instanceof HTMLDialogElement) || !(form instanceof HTMLFormElement) || !(input instanceof HTMLInputElement) || !(status instanceof HTMLElement)) {
    return;
  }

  const LOCAL_BASE = 'http://127.0.0.1:3383';

  function setStatus(msg, isError) {
    status.textContent = msg || '';
    status.style.color = isError ? '#fda4af' : '';
  }

  async function checkLocalService() {
    try {
      const res = await fetch(LOCAL_BASE + '/api/public/info', { method: 'GET', mode: 'cors', cache: 'no-store' });
      if (!res.ok) return { ok: false };
      const data = await res.json().catch(() => ({}));
      return { ok: true, data };
    } catch (_) {
      return { ok: false };
    }
  }

  openBtn.addEventListener('click', async () => {
    setStatus('Checking local service...', false);
    if (typeof dialog.showModal === 'function') {
      dialog.showModal();
    } else {
      dialog.setAttribute('open', 'open');
    }
    input.value = '';
    input.focus();
    const info = await checkLocalService();
    if (info.ok) {
      const req = info.data && info.data.admin_password_required;
      if (req === false) {
        setStatus('Local service detected. Password is not required by default (configurable). Click Open to continue.', false);
      } else {
        setStatus('Local service detected. Enter admin password to open Local Setup.', false);
      }
    } else {
      setStatus('Local service is not running on 127.0.0.1:3383. Start it with: python3 termux.py', true);
    }
  });

  if (closeBtn instanceof HTMLButtonElement) {
    closeBtn.addEventListener('click', () => {
      if (typeof dialog.close === 'function') dialog.close();
      else dialog.removeAttribute('open');
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const password = input.value || '';
    setStatus('Authenticating with local service...', false);
    try {
      const res = await fetch(LOCAL_BASE + '/api/auth/login', {
        method: 'POST',
        mode: 'cors',
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      });
      let data = {};
      try { data = await res.json(); } catch (_) {}
      if (!res.ok || !data || !data.ok) {
        setStatus((data && data.error) ? data.error : 'Authentication failed. Check password and local service.', true);
        return;
      }
      setStatus('Authenticated. Opening Local Setup...', false);
      const url = data.dashboard_url || (LOCAL_BASE + '/admin');
      // Open localhost dashboard (served by local.py) after server-side authentication.
      window.open(url, '_blank', 'noopener');
      if (typeof dialog.close === 'function') dialog.close();
      else dialog.removeAttribute('open');
      form.reset();
    } catch (err) {
      setStatus('Could not reach local service at 127.0.0.1:3383. Start it with: python3 termux.py', true);
    }
  });
})();
