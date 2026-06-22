(function () {
  const storageKey = 'rbook.problem.fontScale';
  const minScale = 0.8;
  const maxScale = 2.5;
  const step = 0.1;

  const readable = document.querySelector('[data-problem-readable]');
  const toolbar = document.querySelector('.problem-floating-toolbar');
  const problemPage = document.querySelector('.problem-page');

  if (!readable || !toolbar || !problemPage) return;

  function clamp(value) {
    return Math.min(maxScale, Math.max(minScale, value));
  }

  function readScale() {
    const stored = Number.parseFloat(window.localStorage.getItem(storageKey));
    return Number.isFinite(stored) ? clamp(stored) : 1;
  }

  function writeScale(scale) {
    const normalized = Number(scale.toFixed(1));
    readable.style.fontSize = `${normalized}em`;
    window.localStorage.setItem(storageKey, String(normalized));
  }

  function resetScale() {
    readable.style.fontSize = '';
    window.localStorage.removeItem(storageKey);
  }

  function changeScale(action) {
    const current = readScale();

    if (action === 'increase') {
      writeScale(clamp(current + step));
      return;
    }

    if (action === 'decrease') {
      writeScale(clamp(current - step));
      return;
    }

    if (action === 'reset') {
      resetScale();
    }
  }

  const initialScale = readScale();
  if (initialScale !== 1) {
    readable.style.fontSize = `${initialScale}em`;
  }

  problemPage.addEventListener('click', (event) => {
    const fontButton = event.target.closest('[data-problem-font]');
    if (fontButton) {
      changeScale(fontButton.dataset.problemFont);
      return;
    }

    const topButton = event.target.closest('[data-scroll-top]');
    if (topButton) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    const printButton = event.target.closest('[data-problem-print]');
    if (printButton) {
      window.print();
    }
  });
}());
