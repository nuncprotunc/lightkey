/**
 * LightKey — Shared Main JS
 *
 * Loaded by every page. Handles scroll reveals and any
 * site-wide behaviour that isn't component injection.
 */

(function() {
  'use strict';

  /* ── Scroll reveal ── */
  function initReveal() {
    var els = document.querySelectorAll('.lk-reveal');
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) {
      els.forEach(function(el) { el.classList.add('is-visible'); });
      return;
    }
    var obs = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    els.forEach(function(el) { obs.observe(el); });
  }

  document.addEventListener('DOMContentLoaded', initReveal);
})();
