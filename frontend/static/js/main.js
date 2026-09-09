/**
 * City Heart Hospital — Mumbai - Frontend Core JS
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

  // 5. Client-Side Services Grid Filtering
  const filterTabs = document.querySelectorAll('#servicesFilterTabs .filter-btn');
  const serviceCards = document.querySelectorAll('#servicesGridContainer .service-card-wrapper');

  if (filterTabs.length > 0 && serviceCards.length > 0) {
    filterTabs.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const filterVal = btn.getAttribute('data-filter');

        // Update active class on tabs
        filterTabs.forEach(t => {
          t.classList.remove('btn-primary-custom');
          t.classList.add('btn-outline-custom');
        });
        btn.classList.remove('btn-outline-custom');
        btn.classList.add('btn-primary-custom');

        // Filter cards
        serviceCards.forEach(card => {
          const cardDept = card.getAttribute('data-dept');
          if (filterVal === 'all' || cardDept === filterVal) {
            card.style.display = 'block';
            card.style.opacity = '0';
            setTimeout(() => {
              card.style.transition = 'opacity 0.25s ease';
              card.style.opacity = '1';
            }, 10);
          } else {
            card.style.display = 'none';
          }
        });

        // Update URL query parameter cleanly without reloading page
        const newUrl = filterVal === 'all' 
          ? window.location.pathname 
          : `${window.location.pathname}?department=${filterVal}`;
        window.history.replaceState({ path: newUrl }, '', newUrl);
      });
    });
  }

  // 6. Back to Top Button
  const backToTopBtn = document.getElementById('backToTopBtn');
  if (backToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 280) {
        backToTopBtn.classList.add('show');
      } else {
        backToTopBtn.classList.remove('show');
      }
    }, { passive: true });

    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // 7. Scroll-Reveal Animations (IntersectionObserver)
  const revealElements = document.querySelectorAll('.reveal-on-scroll, [data-aos]');
  if (revealElements.length > 0) {
    // Accessibility check: immediately show if user prefers reduced motion or no IntersectionObserver
    if (!window.IntersectionObserver || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
      revealElements.forEach(el => el.classList.add('is-revealed', 'aos-animate'));
    } else {
      document.body.classList.add('js-anim');
      const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed', 'aos-animate');
            observer.unobserve(entry.target);
          }
        });
      }, {
        root: null,
        rootMargin: '0px 0px -20px 0px',
        threshold: 0.05
      });

      revealElements.forEach(el => {
        // Immediately reveal if already visible in initial viewport
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          el.classList.add('is-revealed', 'aos-animate');
        } else {
          revealObserver.observe(el);
        }
      });
    }
  }

  // 8. Full-Bleed Hero Slider Controller (Matching Reference Design)
  const heroSlides = document.querySelectorAll('#heroSlidesWrapper .hero-slide-item');
  const heroCaptions = document.querySelectorAll('#heroCardContent .hero-slide-caption');
  const heroDots = document.querySelectorAll('#heroSliderDots .hero-slider-dot');
  const heroPrevBtn = document.getElementById('heroPrevBtn');
  const heroNextBtn = document.getElementById('heroNextBtn');
  const heroSection = document.getElementById('heroSliderSection');

  if (heroSlides.length > 0) {
    let currentIdx = 0;
    let slideTimer = null;
    const slideDuration = 5500; // 5.5s autoplay interval

    // Preload background images
    heroSlides.forEach(slide => {
      const bgStyle = slide.style.backgroundImage;
      if (bgStyle) {
        const match = bgStyle.match(/url\(['"]?(.*?)['"]?\)/);
        if (match && match[1]) {
          const img = new Image();
          img.src = match[1];
        }
      }
    });

    const showSlide = (index) => {
      currentIdx = (index + heroSlides.length) % heroSlides.length;
      heroSlides.forEach((slide, i) => {
        slide.classList.toggle('is-active', i === currentIdx);
      });
      heroCaptions.forEach((cap, i) => {
        cap.classList.toggle('is-active', i === currentIdx);
      });
      heroDots.forEach((dot, i) => {
        dot.classList.toggle('is-active', i === currentIdx);
      });
    };

    const nextSlide = () => showSlide(currentIdx + 1);
    const prevSlide = () => showSlide(currentIdx - 1);

    const startAutoplay = () => {
      stopAutoplay();
      if (heroSlides.length > 1) {
        slideTimer = setInterval(() => {
          if (!document.hidden) nextSlide();
        }, slideDuration);
      }
    };

    const stopAutoplay = () => {
      if (slideTimer) {
        clearInterval(slideTimer);
        slideTimer = null;
      }
    };

    if (heroPrevBtn) {
      heroPrevBtn.addEventListener('click', () => {
        prevSlide();
        startAutoplay();
      });
    }

    if (heroNextBtn) {
      heroNextBtn.addEventListener('click', () => {
        nextSlide();
        startAutoplay();
      });
    }

    heroDots.forEach((dot, idx) => {
      dot.addEventListener('click', () => {
        showSlide(idx);
        startAutoplay();
      });
    });

    if (heroSection) {
      heroSection.addEventListener('mouseenter', stopAutoplay);
      heroSection.addEventListener('mouseleave', startAutoplay);
      heroSection.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
          prevSlide();
          startAutoplay();
        } else if (e.key === 'ArrowRight') {
          nextSlide();
          startAutoplay();
        }
      });
    }

    startAutoplay();
  }
});

