/**
 * Harborlight Multispecialty Hospital - Frontend Core JS
 * Handles responsive hamburger navigation toggle and general UI interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Hamburger Toggle
  const hamburgerBtn = document.getElementById('navbarHamburgerBtn');
  const navMenuWrapper = document.getElementById('navbarMenuWrapper');

  if (hamburgerBtn && navMenuWrapper) {
    hamburgerBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isExpanded = hamburgerBtn.getAttribute('aria-expanded') === 'true';
      hamburgerBtn.setAttribute('aria-expanded', !isExpanded);
      navMenuWrapper.classList.toggle('is-open');
      
      // Toggle icon between list and x
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

    // Close menu when clicking outside
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

    // Close menu when clicking any nav link
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

  // Auto-dismiss alerts
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
