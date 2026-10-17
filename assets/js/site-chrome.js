(function () {
  function loadPartial(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error('Failed to load ' + url);
      return r.text();
    });
  }

  function setActiveNav(root) {
    var path = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
    if (!path || path === '') path = 'index.html';
    var map = {
      'index.html': 'صفحه اصلی',
      'about.html': 'معرفی مجتمع',
      'info.html': 'دفاتر املاک',
      'homes.html': 'املاک',
      'home_detail.html': 'املاک',
      'blogs.html': 'مقالات',
      'blog_detail.html': 'مقالات'
    };
    var activeLabel = map[path];
    if (!activeLabel || !root) return;
    var links = root.querySelectorAll('nav a');
    links.forEach(function (a) {
      var label = (a.textContent || '').trim();
      var isActive = label === activeLabel;
      if (isActive) {
        a.className = 'text-primary dark:text-inverse-primary font-semibold border-b-2 border-secondary pb-1 text-label-lg font-label-lg transition-colors duration-200';
      } else if (a.closest('nav.hidden')) {
        a.className = 'text-on-surface-variant dark:text-surface-variant hover:text-primary dark:hover:text-inverse-primary transition-colors duration-200 text-label-lg font-label-lg';
      }
    });
  }

  var base = 'assets/partials/';
  var headerSlot = document.getElementById('site-header');
  var footerSlot = document.getElementById('site-footer');
  var mobileSlot = document.getElementById('site-mobile-menu');

  var tasks = [];
  if (headerSlot) {
    tasks.push(
      loadPartial(base + 'header.html').then(function (html) {
        headerSlot.outerHTML = html;
        setActiveNav(document.querySelector('header'));
      })
    );
  }
  if (mobileSlot) {
    tasks.push(
      loadPartial(base + 'mobile-menu.html').then(function (html) {
        mobileSlot.outerHTML = html;
      })
    );
  }
  if (footerSlot) {
    tasks.push(
      loadPartial(base + 'footer.html').then(function (html) {
        footerSlot.outerHTML = html;
      })
    );
  }

  Promise.all(tasks).catch(function (err) {
    console.error('site-chrome:', err);
  });
})();
