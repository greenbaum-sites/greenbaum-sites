(function () {
  'use strict';

  var style = document.createElement('style');
  style.textContent =
    '.lens-nav-back,' +
    '.lens-nav-taxonomy {' +
    '  position: fixed;' +
    '  z-index: 60;' +
    '  top: 1.5rem;' +
    '  font-family: "JetBrains Mono", monospace;' +
    '  font-size: 0.45rem;' +
    '  font-weight: 300;' +
    '  letter-spacing: 0.15em;' +
    '  text-transform: uppercase;' +
    '  color: var(--text-dim);' +
    '  text-decoration: none;' +
    '  padding: 0.4em 0;' +
    '  transition: color 0.3s ease;' +
    '  opacity: 0;' +
    '  animation: softIn 1s ease 1s forwards;' +
    '}' +
    '.lens-nav-back:hover,' +
    '.lens-nav-taxonomy:hover { color: var(--gold); }' +
    '.lens-nav-back { left: 2rem; }' +
    '.lens-nav-taxonomy { right: 2rem; }' +
    '@media (prefers-reduced-motion: reduce) {' +
    '  .lens-nav-back,' +
    '  .lens-nav-taxonomy {' +
    '    animation-duration: 0.01ms !important;' +
    '    animation-delay: 0.01ms !important;' +
    '  }' +
    '}' +
    '@media (max-width: 768px) {' +
    '  .lens-nav-back { left: 1rem; top: 1rem; font-size: 0.4rem; }' +
    '  .lens-nav-taxonomy { right: 1rem; top: 1rem; font-size: 0.4rem; }' +
    '}';
  document.head.appendChild(style);

  var backLink = document.createElement('a');
  backLink.className = 'lens-nav-back';
  backLink.href = '/lens/';
  backLink.textContent = '← All seats';

  var taxonomyLink = document.createElement('a');
  taxonomyLink.className = 'lens-nav-taxonomy';
  taxonomyLink.href = '/fm/';
  taxonomyLink.textContent = 'Full taxonomy →';

  document.body.appendChild(backLink);
  document.body.appendChild(taxonomyLink);

  backLink.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
  taxonomyLink.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
})();
