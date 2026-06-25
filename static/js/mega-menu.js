(function () {
  'use strict';

  function initMegaMenu() {
    var wrap = document.querySelector('[data-mega-wrap]');
    if (!wrap) return;

    var navRow = wrap.closest('.header__nav-row');
    var trigger = wrap.querySelector('[data-mega-trigger]');
    var menu = navRow ? navRow.querySelector('[data-mega-menu]') : null;
    if (!trigger || !menu) return;

    var closeTimer = null;

    function openMenu() {
      clearTimeout(closeTimer);
      wrap.classList.add('is-open');
      menu.hidden = false;
      trigger.setAttribute('aria-expanded', 'true');
    }

    function closeMenu() {
      wrap.classList.remove('is-open');
      menu.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');
    }

    function scheduleClose() {
      closeTimer = setTimeout(closeMenu, 150);
    }

    [wrap, menu].forEach(function (el) {
      el.addEventListener('mouseenter', openMenu);
      el.addEventListener('mouseleave', scheduleClose);
    });

    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      if (wrap.classList.contains('is-open')) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target) && !menu.contains(e.target)) {
        closeMenu();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  function initMobileDrawer() {
    var openBtn = document.querySelector('[data-drawer-open]');
    var drawerRoot = document.getElementById('mobile-drawer');
    if (!openBtn || !drawerRoot) return;

    var closeBtns = drawerRoot.querySelectorAll('[data-drawer-close]');

    function openDrawer() {
      drawerRoot.hidden = false;
      document.body.classList.add('drawer-open');
    }

    function closeDrawer() {
      drawerRoot.hidden = true;
      document.body.classList.remove('drawer-open');
      openBtn.focus();
    }

    openBtn.addEventListener('click', openDrawer);
    closeBtns.forEach(function (btn) {
      btn.addEventListener('click', closeDrawer);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !drawerRoot.hidden) closeDrawer();
    });
  }

  function initCatalogFilters() {
    var toggle = document.querySelector('[data-filter-toggle]');
    var panel = document.querySelector('[data-filter-panel]');
    if (!toggle || !panel) return;

    toggle.addEventListener('click', function () {
      panel.classList.toggle('is-open');
      toggle.classList.toggle('is-active');
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initMegaMenu();
    initMobileDrawer();
    initCatalogFilters();
  });
})();
