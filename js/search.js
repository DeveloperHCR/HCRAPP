const engineMenuButton = document.getElementById('engine-menu-button');
const engineMenu = document.getElementById('engine-menu');

if (engineMenuButton instanceof HTMLButtonElement && engineMenu instanceof HTMLElement) {
  const closeEngineMenu = () => {
    engineMenu.hidden = true;
    engineMenuButton.setAttribute('aria-expanded', 'false');
  };

  engineMenuButton.addEventListener('click', () => {
    engineMenu.hidden = !engineMenu.hidden;
    engineMenuButton.setAttribute('aria-expanded', String(!engineMenu.hidden));
  });

  document.addEventListener('click', (event) => {
    if (
      event.target instanceof Node &&
      !engineMenuButton.contains(event.target) &&
      !engineMenu.contains(event.target)
    ) {
      closeEngineMenu();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !engineMenu.hidden) {
      closeEngineMenu();
      engineMenuButton.focus();
    }
  });
}

try {
  document.body.classList.toggle('light-mode', localStorage.getItem('developerhcr-theme') === 'light');
} catch (error) {
  console.error('Unable to read the saved color theme.', error);
}
