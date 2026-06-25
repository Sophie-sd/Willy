(function () {
  'use strict';

  function initHeroBanner() {
    var root = document.querySelector('[data-hero-banner]');
    if (!root) return;

    var viewport = root.querySelector('.hero-banner__viewport');
    var track = root.querySelector('[data-hero-track]');
    var slides = root.querySelectorAll('[data-hero-slide]');
    var prevBtn = root.querySelector('[data-hero-prev]');
    var nextBtn = root.querySelector('[data-hero-next]');
    var dotsWrap = root.querySelector('[data-hero-dots]');
    if (!track || slides.length === 0) return;

    var index = 0;
    var timer = null;
    var touchStartX = 0;
    var touchDeltaX = 0;
    var isDragging = false;
    var autoplayMs = 6000;

    function slideWidth() {
      if (viewport) return viewport.clientWidth;
      if (slides[0]) return slides[0].getBoundingClientRect().width;
      return root.clientWidth;
    }

    function goTo(i) {
      index = (i + slides.length) % slides.length;
      track.style.transform = 'translate3d(-' + (index * slideWidth()) + 'px, 0, 0)';

      if (dotsWrap) {
        var dots = dotsWrap.querySelectorAll('[data-hero-dot]');
        dots.forEach(function (dot, di) {
          dot.classList.toggle('is-active', di === index);
          dot.setAttribute('aria-selected', di === index ? 'true' : 'false');
        });
      }
    }

    function next() {
      goTo(index + 1);
    }

    function prev() {
      goTo(index - 1);
    }

    function startAutoplay() {
      stopAutoplay();
      if (slides.length < 2) return;
      timer = setInterval(next, autoplayMs);
    }

    function stopAutoplay() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    }

    if (dotsWrap && slides.length > 1) {
      slides.forEach(function (_, i) {
        var dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'hero-banner__dot' + (i === 0 ? ' is-active' : '');
        dot.setAttribute('data-hero-dot', '');
        dot.setAttribute('aria-label', 'Слайд ' + (i + 1));
        dot.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
        dot.addEventListener('click', function () {
          goTo(i);
          startAutoplay();
        });
        dotsWrap.appendChild(dot);
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        prev();
        startAutoplay();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        next();
        startAutoplay();
      });
    }

    root.addEventListener('mouseenter', stopAutoplay);
    root.addEventListener('mouseleave', startAutoplay);

    track.addEventListener('touchstart', function (e) {
      if (slides.length < 2) return;
      touchStartX = e.touches[0].clientX;
      touchDeltaX = 0;
      isDragging = true;
      track.classList.add('is-dragging');
      stopAutoplay();
    }, { passive: true });

    track.addEventListener('touchmove', function (e) {
      if (!isDragging) return;
      touchDeltaX = e.touches[0].clientX - touchStartX;
    }, { passive: true });

    track.addEventListener('touchend', function () {
      if (!isDragging) return;
      track.classList.remove('is-dragging');
      isDragging = false;
      if (Math.abs(touchDeltaX) > 50) {
        if (touchDeltaX < 0) next();
        else prev();
      }
      startAutoplay();
    });

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stopAutoplay();
      else startAutoplay();
    });

    window.addEventListener('resize', function () {
      goTo(index);
    }, { passive: true });

    window.addEventListener('orientationchange', function () {
      setTimeout(function () {
        goTo(index);
      }, 100);
    });

    goTo(0);
    startAutoplay();
  }

  document.addEventListener('DOMContentLoaded', initHeroBanner);
})();
