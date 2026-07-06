(function () {
  'use strict';

  /* ── Badge update ───────────────────────────────────── */
  function updateBadge(count) {
    var badge = document.getElementById('cart-badge');
    if (!badge) return;

    badge.textContent = count > 0 ? count : '';

    if (count > 0) {
      badge.classList.remove('header__cart-badge--hidden');
    } else {
      badge.classList.add('header__cart-badge--hidden');
    }
  }

  /* ── Toast ──────────────────────────────────────────── */
  function showToast(message) {
    var container = document.getElementById('toast-container');
    if (!container) return;

    var toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML =
      '<span class="toast__icon">' +
        '<svg width="12" height="10" viewBox="0 0 12 10" fill="none" aria-hidden="true">' +
          '<path d="M1 5l3.5 3.5L11 1" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
        '</svg>' +
      '</span>' +
      '<span>' + escapeHtml(message) + '</span>';

    container.appendChild(toast);

    setTimeout(function () {
      toast.classList.add('toast--exit');
      toast.addEventListener('animationend', function () {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, { once: true });
    }, 3000);
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ── HTMX event listeners ───────────────────────────── */
  document.addEventListener('cartUpdated', function (e) {
    var count = (e.detail && e.detail.count !== undefined) ? e.detail.count : 0;
    updateBadge(count);

    if (window.location.pathname.startsWith('/cart')) {
      window.location.reload();
    }
  });

  document.addEventListener('showToast', function (e) {
    var message = e.detail && e.detail.message ? e.detail.message : 'Товар додано в кошик';
    showToast(message);
  });

  document.addEventListener('cartPageRefresh', function () {
    if (window.location.pathname.startsWith('/cart')) {
      window.location.reload();
    }
  });

  /* ── Qty controls on cart page ──────────────────────── */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-qty-dec], [data-qty-inc]');
    if (!btn) return;

    var form = btn.closest('.cart-item__qty-form');
    if (!form) return;

    var input = form.querySelector('.cart-item__qty-input');
    if (!input) return;

    var current = parseInt(input.value, 10) || 0;
    var isDec = btn.hasAttribute('data-qty-dec');
    var next = isDec ? Math.max(0, current - 1) : Math.min(99, current + 1);

    input.value = next;
    htmx.trigger(form, 'submit');
  });

})();
