(function () {
  const storageKey = 'rbook.theme';
  const modes = new Set(['auto', 'light', 'dark']);
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

  function readMode() {
    try {
      const value = window.localStorage.getItem(storageKey);
      return modes.has(value) ? value : 'auto';
    } catch (error) {
      return 'auto';
    }
  }

  function writeMode(mode) {
    try {
      window.localStorage.setItem(storageKey, mode);
    } catch (error) {
      // Theme switching should still work for this page even when storage is blocked.
    }
  }

  function resolveTheme(mode) {
    if (mode === 'light' || mode === 'dark') return mode;
    return mediaQuery.matches ? 'dark' : 'light';
  }

  function applyTheme(mode) {
    const resolvedTheme = resolveTheme(mode);
    document.documentElement.setAttribute('data-bs-theme', resolvedTheme);
    document.documentElement.dataset.themeMode = mode;

    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) {
      themeColor.setAttribute('content', resolvedTheme === 'dark' ? '#111827' : '#1f2937');
    }

    for (const input of document.querySelectorAll('[data-theme-mode]')) {
      input.checked = input.value === mode;
    }
  }

  function setMode(mode) {
    const nextMode = modes.has(mode) ? mode : 'auto';
    writeMode(nextMode);
    applyTheme(nextMode);
  }

  window.rbookTheme = {
    apply: applyTheme,
    getMode: readMode,
    setMode,
  };

  applyTheme(readMode());

  document.addEventListener('change', (event) => {
    const input = event.target.closest('[data-theme-mode]');
    if (!input) return;
    setMode(input.value);
  });

  mediaQuery.addEventListener('change', () => {
    if (readMode() === 'auto') {
      applyTheme('auto');
    }
  });
}());
