(function () {
  'use strict';

  function initCarousels() {
    var carousels = document.querySelectorAll('[data-carousel]');
    carousels.forEach(function (carousel) {
      var track = carousel.querySelector('[data-carousel-track]');
      var prevBtn = carousel.querySelector('[data-carousel-prev]');
      var nextBtn = carousel.querySelector('[data-carousel-next]');
      if (!track) return;

      var slideWidth = function () {
        var slide = track.querySelector('[data-carousel-slide]');
        if (!slide) return 296;
        var style = window.getComputedStyle(track);
        var gap = parseFloat(style.gap) || 16;
        return slide.offsetWidth + gap;
      };

      if (prevBtn) {
        prevBtn.addEventListener('click', function () {
          track.scrollBy({ left: -slideWidth(), behavior: 'smooth' });
        });
      }

      if (nextBtn) {
        nextBtn.addEventListener('click', function () {
          track.scrollBy({ left: slideWidth(), behavior: 'smooth' });
        });
      }
    });
  }

  document.addEventListener('DOMContentLoaded', initCarousels);
})();
