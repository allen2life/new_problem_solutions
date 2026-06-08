(function () {
  const blocks = document.querySelectorAll('pre.mermaid');

  if (!blocks.length || typeof window.mermaid === 'undefined') return;

  window.mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'strict',
    theme: 'default',
  });

  window.mermaid.run({ nodes: blocks }).catch((error) => {
    for (const block of blocks) {
      block.classList.add('mermaid-render-failed');
    }
    console.error('Mermaid render failed:', error);
  });
}());
