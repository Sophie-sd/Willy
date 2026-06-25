(function () {
  'use strict';

  var COOKIE_KEY = 'willi_cookies_accepted';

  function initCookieBanner() {
    var banner = document.getElementById('cookie-banner');
    if (!banner) return;
    if (localStorage.getItem(COOKIE_KEY)) return;

    requestAnimationFrame(function () {
      banner.classList.add('is-visible');
    });

    var acceptBtn = banner.querySelector('[data-cookie-accept]');
    if (acceptBtn) {
      acceptBtn.addEventListener('click', function () {
        localStorage.setItem(COOKIE_KEY, '1');
        banner.classList.remove('is-visible');
      });
    }
  }

  document.addEventListener('DOMContentLoaded', initCookieBanner);
})();
