/* ============================================
   LIBERTY BELL MORTGAGE — Main JS
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

  // --- NAV SCROLL BEHAVIOR ---
  const nav = document.querySelector('.nav');
  window.addEventListener('scroll', () => {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 40);
  });

  // --- MOBILE NAV ---
  const hamburger    = document.querySelector('.nav-hamburger');
  const mobileNav    = document.querySelector('.mobile-nav');
  const mobileClose  = document.querySelector('.mobile-nav-close');
  const mobileOverlay = document.querySelector('.mobile-nav-overlay');

  function closeMobileNav() {
    if (mobileNav) mobileNav.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (hamburger) {
    hamburger.addEventListener('click', () => {
      if (mobileNav) mobileNav.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  }
  if (mobileClose)   mobileClose.addEventListener('click', closeMobileNav);
  if (mobileOverlay) mobileOverlay.addEventListener('click', closeMobileNav);

  // --- HERO CALCULATOR ---
  let hcTerm = 30;

  function heroCalc() {
    const priceEl = document.getElementById('hc-price');
    const downEl  = document.getElementById('hc-down');
    const rateEl  = document.getElementById('hc-rate');
    const amtEl   = document.getElementById('hc-amount');
    const intEl   = document.getElementById('hc-total-interest');
    const hintEl  = document.getElementById('hc-down-pct');
    const loanEl  = document.getElementById('hc-loan-amt');
    const termEl  = document.getElementById('hc-term-display');

    if (!priceEl || !downEl || !rateEl || !amtEl) return;

    const price     = parseFloat(priceEl.value) || 0;
    const down      = parseFloat(downEl.value)  || 0;
    const rate      = parseFloat(rateEl.value)  || 0;
    const principal = Math.max(0, price - down);
    const mo        = rate / 100 / 12;
    const n         = hcTerm * 12;

    // Down payment hint
    if (hintEl) {
      if (price > 0) {
        const pct = Math.round((down / price) * 100);
        hintEl.textContent = pct + '% down · $' + Math.round(principal).toLocaleString() + ' loan';
        hintEl.style.color = pct < 20 ? '#e53e3e' : '';
      } else {
        hintEl.textContent = '';
      }
    }

    // Breakdown
    if (loanEl) loanEl.textContent = '$' + Math.round(principal).toLocaleString();
    if (termEl) termEl.textContent = hcTerm + ' years';

    // Guard: need valid inputs to calculate
    if (price <= 0 || rate <= 0 || principal <= 0) {
      amtEl.textContent = '$—';
      if (intEl) intEl.textContent = '$—';
      return;
    }

    // Standard amortization formula
    const monthly = principal * (mo * Math.pow(1 + mo, n)) / (Math.pow(1 + mo, n) - 1);

    amtEl.textContent = '$' + Math.round(monthly).toLocaleString();

    if (intEl) {
      const totalInterest = (monthly * n) - principal;
      intEl.textContent = '$' + Math.round(totalInterest).toLocaleString();
    }
  }

  // Term tab switching
  document.querySelectorAll('.hc-tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.hc-tab').forEach(function(t) {
        t.classList.remove('active');
      });
      tab.classList.add('active');
      hcTerm = parseInt(tab.dataset.term, 10);
      heroCalc();
    });
  });

  // Input listeners
  ['hc-price', 'hc-down', 'hc-rate'].forEach(function(id) {
    var el = document.getElementById(id);
    if (el) el.addEventListener('input', heroCalc);
  });

  // Run on load with default values
  heroCalc();

  // --- SMOOTH SCROLL ---
  document.querySelectorAll('a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      var href = a.getAttribute('href');
      if (href === '#') return;
      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        closeMobileNav();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // --- SCROLL REVEAL ---
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function(el) { observer.observe(el); });
  } else {
    // Fallback for older browsers — just show everything
    revealEls.forEach(function(el) { el.classList.add('revealed'); });
  }

}); // end DOMContentLoaded