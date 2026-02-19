/**
 * LightKey — Shared Component System
 *
 * Injects nav and footer into every page automatically.
 * New pages only need:
 *   <div id="lk-nav"></div>
 *   <div id="lk-footer"></div>
 *   <script src="/js/components.js"></script>
 *
 * Nav links, footer text, and branding are maintained here — one place only.
 */

const LK = {

  nav: `
    <nav class="lk-nav" role="navigation" aria-label="Site navigation">
      <div class="lk-nav-inner">
        <div class="lk-brand-wrap">
        <a href="/" class="lk-brand" aria-label="LightKey home">
          <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M6 32 L6 18 Q6 6 18 6 Q30 6 30 18 L30 32" stroke="#5C4D3A" stroke-width="1.5" fill="none"/>
            <path d="M14 6 L15 2 L21 2 L22 6" stroke="#9A5530" stroke-width="1.5" fill="rgba(154,85,48,0.08)"/>
            <circle cx="18" cy="3.5" r="0.8" fill="#9A5530"/>
            <line x1="18" y1="4.3" x2="18" y2="5.5" stroke="#9A5530" stroke-width="0.8"/>
            <line x1="10" y1="12" x2="8" y2="16" stroke="#5C4D3A" stroke-width="0.6" opacity="0.3"/>
            <line x1="26" y1="12" x2="28" y2="16" stroke="#5C4D3A" stroke-width="0.6" opacity="0.3"/>
            <line x1="6" y1="32" x2="30" y2="32" stroke="#5C4D3A" stroke-width="1.5"/>
            <line x1="10" y1="31" x2="26" y2="31" stroke="#3D7A8A" stroke-width="0.6" opacity="0.5"/>
          </svg>
          <span class="lk-brand-text">
            <span class="lk-brand-name">LightKey</span>
            <span class="lk-brand-tag">A <a href="https://glasscase.org">GlassCase</a> Initiative</span>
          </span>
        </a>
        </div>
        <div class="lk-nav-right">
          <nav class="lk-desktop-nav" aria-label="Main links">
            <span class="lk-nav-future">Pathways <span class="lk-nav-badge">Building</span></span>
            <span class="lk-nav-future">Guides <span class="lk-nav-badge">Building</span></span>
            <span class="lk-nav-future">About <span class="lk-nav-badge">Building</span></span>
          </nav>
          <button class="lk-a11y-toggle" id="lkReadingToggle"
                  aria-pressed="false"
                  aria-label="Toggle relaxed reading spacing"
                  title="Wider line spacing for easier reading">
            <span class="toggle-icon" aria-hidden="true">Aa</span>
            <span>Relaxed reading</span>
          </button>
          <button class="lk-mobile-btn" id="lkMobileBtn"
                  aria-label="Toggle menu" aria-expanded="false">
            <span></span><span></span><span></span>
          </button>
        </div>
      </div>
    </nav>
  `,

  mobileMenu: `
    <div class="lk-mobile-menu" id="lkMobileMenu" aria-hidden="true">
      <div class="lk-mobile-menu-header">
        <div class="lk-mobile-menu-title">LightKey</div>
        <div class="lk-mobile-menu-subtitle">A GlassCase Initiative</div>
      </div>
      <nav aria-label="Mobile navigation">
        <a href="/" data-nav="home">Home</a>
        <span class="lk-mobile-future">Pathways <span class="lk-nav-badge">Building</span></span>
        <span class="lk-mobile-future">Guides <span class="lk-nav-badge">Building</span></span>
        <span class="lk-mobile-future">About <span class="lk-nav-badge">Building</span></span>
      </nav>
    </div>
    <div class="lk-mobile-overlay" id="lkMobileOverlay"></div>
  `,

  footer: `
    <footer class="lk-footer">
      <div class="lk-footer-bottom">
        <div class="lk-footer-copyright">
          &copy; 2026 LightKey &middot; A GlassCase Initiative &middot; <a href="https://glasscase.org">glasscase.org</a>
        </div>
        <p class="lk-footer-disclaimer">Led by Jay Spudvilas (Jayden Spudvilas-Powell). Built in Australia. Made for everyone who believes fairness should be visible.</p>
        <p class="lk-footer-disclaimer">Information only, not legal advice.</p>
      </div>
    </footer>
  `
};

function lkInjectComponents() {
  const navEl    = document.getElementById('lk-nav');
  const menuEl   = document.getElementById('lk-mobile-menu');
  const footerEl = document.getElementById('lk-footer');

  if (navEl)    navEl.outerHTML    = LK.nav;
  if (menuEl)   menuEl.outerHTML   = LK.mobileMenu;
  if (footerEl) footerEl.outerHTML = LK.footer;

  lkSetActiveNav();
  lkInitMobileMenu();
  lkInitReadingToggle();
}

function lkSetActiveNav() {
  const path = window.location.pathname;
  let key = 'home';
  if (path.startsWith('/pathways'))  key = 'pathways';
  else if (path.startsWith('/guides'))    key = 'guides';
  else if (path.startsWith('/about'))     key = 'about';
  else if (path.startsWith('/resources')) key = 'resources';

  const link = document.querySelector('.lk-mobile-menu [data-nav="' + key + '"]');
  if (link) link.classList.add('active');
}

function lkInitMobileMenu() {
  const btn     = document.getElementById('lkMobileBtn');
  const menu    = document.getElementById('lkMobileMenu');
  const overlay = document.getElementById('lkMobileOverlay');
  if (!btn || !menu || !overlay) return;

  function open() {
    menu.classList.add('active');
    overlay.classList.add('active');
    btn.setAttribute('aria-expanded', 'true');
    menu.setAttribute('aria-hidden', 'false');
  }
  function close() {
    menu.classList.remove('active');
    overlay.classList.remove('active');
    btn.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-hidden', 'true');
  }

  btn.addEventListener('click', function() {
    menu.classList.contains('active') ? close() : open();
  });
  overlay.addEventListener('click', close);
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') close();
  });
}

function lkInitReadingToggle() {
  const btn = document.getElementById('lkReadingToggle');
  if (!btn) return;
  btn.addEventListener('click', function() {
    const pressed = btn.getAttribute('aria-pressed') === 'true';
    btn.setAttribute('aria-pressed', String(!pressed));
    document.body.classList.toggle('reading-relaxed', !pressed);
  });
}

document.addEventListener('DOMContentLoaded', lkInjectComponents);
