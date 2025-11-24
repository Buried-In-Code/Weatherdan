function getPreferredTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
  applyTheme(e.matches ? 'dark' : 'light');
});

applyTheme(getPreferredTheme());
