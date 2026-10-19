/**
 * تبدیل خودکار ارقام لاتین به فارسی در صفحات fa
 * ورودی‌ها، textarea، select، code و pre دست نخورده می‌مانند.
 */
(function () {
  var lang = (document.documentElement.lang || 'fa').slice(0, 2);
  if (lang === 'en') return;

  var map = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
  function toFa(s) {
    return String(s).replace(/[0-9]/g, function (d) { return map[+d]; });
  }

  var SKIP = /^(SCRIPT|STYLE|TEXTAREA|INPUT|SELECT|CODE|PRE|KBD|SAMP)$/i;

  function walk(node) {
    if (!node) return;
    if (node.nodeType === 3) {
      var t = node.nodeValue;
      if (t && /[0-9]/.test(t)) node.nodeValue = toFa(t);
      return;
    }
    if (node.nodeType !== 1) return;
    if (SKIP.test(node.tagName)) return;
    if (node.hasAttribute && node.hasAttribute('data-no-fa-num')) return;
    var kids = node.childNodes;
    for (var i = 0; i < kids.length; i++) walk(kids[i]);
  }

  function run() {
    walk(document.body);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
