const adminDialog = document.getElementById('admin-dialog');
const openAdminButton = document.getElementById('open-admin');

if (adminDialog instanceof HTMLDialogElement && openAdminButton instanceof HTMLButtonElement) {
  const passwordForm = document.getElementById('admin-password-form');
  const passwordInput = document.getElementById('admin-password');
  const confirmationWrap = document.getElementById('admin-confirmation-wrap');
  const confirmationInput = document.getElementById('admin-password-confirm');
  const instructions = document.getElementById('admin-password-instructions');
  const authStatus = document.getElementById('admin-auth-status');
  const statusPanel = document.getElementById('admin-status-panel');
  const serverStatus = document.getElementById('admin-server-status');
  const serverMessage = document.getElementById('admin-server-message');
  const lastChecked = document.getElementById('admin-last-checked');
  const expandAdminButton = document.getElementById('expand-admin');
  const storageSaltKey = 'developerhcr-admin-salt';
  const storageVerifierKey = 'developerhcr-admin-verifier';
  const passwordLength = 12;

  if (
    passwordForm instanceof HTMLFormElement &&
    passwordInput instanceof HTMLInputElement &&
    confirmationWrap instanceof HTMLDivElement &&
    confirmationInput instanceof HTMLInputElement &&
    instructions instanceof HTMLParagraphElement &&
    authStatus instanceof HTMLParagraphElement &&
    statusPanel instanceof HTMLElement &&
    serverStatus instanceof HTMLElement &&
    serverMessage instanceof HTMLElement &&
    lastChecked instanceof HTMLElement &&
    expandAdminButton instanceof HTMLButtonElement
  ) {
    const showPasswordForm = () => {
      passwordForm.hidden = false;
      statusPanel.hidden = true;
      passwordInput.value = '';
      confirmationInput.value = '';
      authStatus.textContent = '';
      let isFirstVisit = false;
      try {
        isFirstVisit = !localStorage.getItem(storageSaltKey);
      } catch {
        authStatus.textContent = 'Browser storage is unavailable. The dashboard cannot set up its local demo password.';
      }
      confirmationWrap.hidden = !isFirstVisit;
      confirmationInput.required = isFirstVisit;
      instructions.textContent = isFirstVisit
        ? 'Set a password for this browser to continue. Use at least 12 characters.'
        : 'Enter the password configured for this browser.';
      document.getElementById('admin-submit').textContent = isFirstVisit ? 'Set password and continue' : 'Unlock dashboard';
    };

    const deriveVerifier = async (password, salt) => {
      const passwordKey = await crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode(password),
        'PBKDF2',
        false,
        ['deriveBits']
      );
      const verifier = await crypto.subtle.deriveBits(
        { name: 'PBKDF2', hash: 'SHA-256', salt, iterations: 150000 },
        passwordKey,
        256
      );
      return Array.from(new Uint8Array(verifier), (byte) => byte.toString(16).padStart(2, '0')).join('');
    };

    const encodeBytes = (bytes) => Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');

    const checkServerStatus = async () => {
      serverStatus.textContent = 'Checking...';
      serverStatus.className = '';
      serverMessage.textContent = 'Checking whether the website is responding...';
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 8000);
      try {
        const response = await fetch('Backend.html', { cache: 'no-store', signal: controller.signal });
        if (!response.ok) {
          serverStatus.textContent = 'Server check failed';
          serverStatus.className = 'status-bad';
          serverMessage.textContent = `The public status page returned HTTP ${response.status}.`;
        } else {
          serverStatus.textContent = 'Server is running';
          serverStatus.className = 'status-good';
          serverMessage.textContent = `Website responded with HTTP ${response.status}. Hosted on GitHub Pages, so your PC can stay off.`;
        }
      } catch (error) {
        serverStatus.textContent = 'Server status unavailable';
        serverStatus.className = 'status-bad';
        serverMessage.textContent = error.name === 'AbortError'
          ? 'The status check timed out. Try refreshing in a moment.'
          : 'Could not reach the public status page. Check your connection and try again.';
        console.error('Unable to check the website status page.', error);
      } finally {
        clearTimeout(timeout);
      }
      lastChecked.textContent = `Last checked: ${new Date().toLocaleString()}`;
    };

    openAdminButton.addEventListener('click', () => {
      showPasswordForm();
      adminDialog.showModal();
      passwordInput.focus();
    });

    document.getElementById('close-admin').addEventListener('click', () => adminDialog.close());

    expandAdminButton.addEventListener('click', () => {
      const isExpanded = adminDialog.classList.toggle('is-expanded');
      expandAdminButton.setAttribute('aria-expanded', String(isExpanded));
    });

    adminDialog.addEventListener('close', () => {
      adminDialog.classList.remove('is-expanded');
      expandAdminButton.setAttribute('aria-expanded', 'false');
    });

    passwordForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (!passwordForm.reportValidity()) return;

      const password = passwordInput.value;
      if (password.length < passwordLength) {
        authStatus.textContent = `Use a password with at least ${passwordLength} characters.`;
        return;
      }

      try {
        const savedSalt = localStorage.getItem(storageSaltKey);
        const savedVerifier = localStorage.getItem(storageVerifierKey);
        if (!savedSalt || !savedVerifier) {
          if (confirmationInput.value !== password) {
            authStatus.textContent = 'The passwords do not match.';
            return;
          }
          const salt = crypto.getRandomValues(new Uint8Array(16));
          const verifier = await deriveVerifier(password, salt);
          localStorage.setItem(storageSaltKey, encodeBytes(salt));
          localStorage.setItem(storageVerifierKey, verifier);
        } else {
          const saltBytes = savedSalt.match(/.{2}/g)?.map((byte) => Number.parseInt(byte, 16));
          if (!saltBytes || saltBytes.length !== 16 || saltBytes.some((byte) => Number.isNaN(byte))) {
            authStatus.textContent = 'The saved local password data is invalid. Clear this site’s local storage to set it up again.';
            return;
          }
          const verifier = await deriveVerifier(password, new Uint8Array(saltBytes));
          if (verifier !== savedVerifier) {
            authStatus.textContent = 'Incorrect password.';
            return;
          }
        }
        authStatus.textContent = '';
        passwordForm.hidden = true;
        statusPanel.hidden = false;
        await checkServerStatus();
      } catch (error) {
        authStatus.textContent = 'Could not access browser storage or password encryption. Open this site over HTTPS and try again.';
        console.error('Unable to unlock the local admin dashboard.', error);
      }
    });

    document.getElementById('refresh-admin-status').addEventListener('click', checkServerStatus);
    document.getElementById('lock-admin').addEventListener('click', showPasswordForm);
  }
}
