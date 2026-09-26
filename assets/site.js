// Ngôn ngữ (vi/en) và giao diện (theo máy / sáng / tối) cho trang TÔI ĐI.
// Chạy sớm trong <head> để không nháy sai ngôn ngữ / màu.
(function () {
  var root = document.documentElement;
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch (e) {} }

  var qs = new URLSearchParams(location.search).get('lang');
  var lang = qs || get('toidi-lang') || ((navigator.language || '').toLowerCase().indexOf('en') === 0 ? 'en' : 'vi');
  if (lang !== 'en') lang = 'vi';
  root.setAttribute('data-lang', lang);
  root.setAttribute('lang', lang);

  var theme = get('toidi-theme'); // null = theo máy
  if (theme === 'light' || theme === 'dark') root.setAttribute('data-theme', theme);

  window.toidi = {
    lang: function () { return root.getAttribute('data-lang'); },
    setLang: function (l) {
      root.setAttribute('data-lang', l); root.setAttribute('lang', l); set('toidi-lang', l);
      document.dispatchEvent(new CustomEvent('toidi-lang'));
    },
    cycleTheme: function () {
      var cur = root.getAttribute('data-theme');
      var next = cur === null ? 'light' : cur === 'light' ? 'dark' : null;
      next ? root.setAttribute('data-theme', next) : root.removeAttribute('data-theme');
      set('toidi-theme', next);
      return next;
    },
    themeLabel: function () {
      var t = root.getAttribute('data-theme'), en = root.getAttribute('data-lang') === 'en';
      if (t === 'light') return en ? '☀ Light' : '☀ Sáng';
      if (t === 'dark') return en ? '☾ Dark' : '☾ Tối';
      return en ? '◐ System' : '◐ Theo máy';
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    var lb = document.getElementById('lang-btn'), tb = document.getElementById('theme-btn');
    function paint() {
      if (lb) lb.textContent = toidi.lang() === 'en' ? 'Tiếng Việt' : 'English';
      if (tb) tb.textContent = toidi.themeLabel();
    }
    if (lb) lb.addEventListener('click', function () { toidi.setLang(toidi.lang() === 'en' ? 'vi' : 'en'); paint(); });
    if (tb) tb.addEventListener('click', function () { toidi.cycleTheme(); paint(); });
    document.addEventListener('toidi-lang', paint);
    paint();
    var y = document.getElementById('year');
    if (y) y.textContent = new Date().getFullYear();
  });
})();
