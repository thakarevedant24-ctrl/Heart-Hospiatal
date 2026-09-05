/**
 * Harborlight Multispecialty Hospital - Frontend Core JS
 * Handles responsive navigation toggle, stats counter IntersectionObserver,
 * and horizontal carousel scrolling.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Hamburger Toggle
  const hamburgerBtn = document.getElementById('navbarHamburgerBtn');
  const navMenuWrapper = document.getElementById('navbarMenuWrapper');

  if (hamburgerBtn && navMenuWrapper) {
    hamburgerBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isExpanded = hamburgerBtn.getAttribute('aria-expanded') === 'true';
      hamburgerBtn.setAttribute('aria-expanded', !isExpanded);
      navMenuWrapper.classList.toggle('is-open');
      
      const icon = hamburgerBtn.querySelector('i');
      if (icon) {
        if (!isExpanded) {
          icon.classList.remove('bi-list');
          icon.classList.add('bi-x-lg');
        } else {
          icon.classList.remove('bi-x-lg');
          icon.classList.add('bi-list');
        }
      }
    });

    document.addEventListener('click', (e) => {
      if (!navMenuWrapper.contains(e.target) && !hamburgerBtn.contains(e.target)) {
        if (navMenuWrapper.classList.contains('is-open')) {
          navMenuWrapper.classList.remove('is-open');
          hamburgerBtn.setAttribute('aria-expanded', 'false');
          const icon = hamburgerBtn.querySelector('i');
          if (icon) {
            icon.classList.remove('bi-x-lg');
            icon.classList.add('bi-list');
          }
        }
      }
    });

    const navLinks = navMenuWrapper.querySelectorAll('a');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth < 768) {
          navMenuWrapper.classList.remove('is-open');
          hamburgerBtn.setAttribute('aria-expanded', 'false');
          const icon = hamburgerBtn.querySelector('i');
          if (icon) {
            icon.classList.remove('bi-x-lg');
            icon.classList.add('bi-list');
          }
        }
      });
    });
  }

  // 2. Animated Stats Bar Counters (IntersectionObserver)
  const statsSection = document.getElementById('statsSection');
  const counters = document.querySelectorAll('.stat-number');

  if (statsSection && counters.length > 0) {
    let animated = false;

    const animateCounters = () => {
      counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'), 10) || 0;
        const prefix = counter.getAttribute('data-prefix') || '';
        const suffix = counter.getAttribute('data-suffix') || '';
        const duration = 1800; // ms
        const startTime = performance.now();

        const updateCount = (currentTime) => {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          // Ease-out cubic easing function
          const easeOut = 1 - Math.pow(1 - progress, 3);
          const currentVal = Math.floor(easeOut * target);

          counter.textContent = prefix + currentVal.toLocaleString() + suffix;

          if (progress < 1) {
            requestAnimationFrame(updateCount);
          } else {
            counter.textContent = prefix + target.toLocaleString() + suffix;
          }
        };

        requestAnimationFrame(updateCount);
      });
    };

    const observerOptions = {
      root: null,
      threshold: 0.25
    };

    const statsObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !animated) {
          animated = true;
          animateCounters();
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    statsObserver.observe(statsSection);
  }

  // 3. Featured Doctors Carousel Scroll Buttons
  const doctorsScrollTrack = document.getElementById('doctorsScrollTrack');
  const scrollPrevBtn = document.getElementById('doctorsScrollPrev');
  const scrollNextBtn = document.getElementById('doctorsScrollNext');

  if (doctorsScrollTrack && scrollPrevBtn && scrollNextBtn) {
    scrollPrevBtn.addEventListener('click', () => {
      doctorsScrollTrack.scrollBy({ left: -320, behavior: 'smooth' });
    });
    scrollNextBtn.addEventListener('click', () => {
      doctorsScrollTrack.scrollBy({ left: 320, behavior: 'smooth' });
    });
  }

  // 4. Auto-dismiss alerts
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      if (window.bootstrap && window.bootstrap.Alert) {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        if (bsAlert) bsAlert.close();
      }
    }, 5000);
  });
});
