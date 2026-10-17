(function() {
  var btn = document.getElementById('mobile-menu-btn');
  var panel = document.getElementById('mobile-menu-panel');
  var backdrop = document.getElementById('mobile-menu-backdrop');
  var closeBtn = document.getElementById('mobile-menu-close');
  var icon = document.getElementById('mobile-menu-icon');
  if (!btn || !panel) return;
  function openMenu() {
    panel.classList.add('open');
    if (backdrop) backdrop.classList.add('open');
    document.body.classList.add('menu-open');
    btn.setAttribute('aria-expanded', 'true');
    if (icon) icon.textContent = 'close';
  }
  function closeMenu() {
    panel.classList.remove('open');
    if (backdrop) backdrop.classList.remove('open');
    document.body.classList.remove('menu-open');
    btn.setAttribute('aria-expanded', 'false');
    if (icon) icon.textContent = 'menu';
  }
  btn.addEventListener('click', function() {
    if (panel.classList.contains('open')) closeMenu(); else openMenu();
  });
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (backdrop) backdrop.addEventListener('click', closeMenu);
  panel.querySelectorAll('a').forEach(function(a) { a.addEventListener('click', closeMenu); });
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeMenu(); });
})();
