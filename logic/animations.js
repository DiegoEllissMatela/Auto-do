/**
 * Auto Do - GSAP Animations & Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
  // Check if GSAP is available
  if (typeof gsap === 'undefined') {
    console.warn('GSAP not loaded. Fallbacks active.');
    return;
  }

  // Register ScrollTrigger if available
  if (typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
  }

  // Hero Section Entrance Timeline
  const heroTl = gsap.timeline({ defaults: { ease: 'power3.out', duration: 0.8 } });

  heroTl
    .from('.badge-pill', { opacity: 0, y: -20, duration: 0.6 })
    .from('h1', { opacity: 0, y: 30, duration: 0.9 }, '-=0.3')
    .from('[data-purpose="hero-description"]', { opacity: 0, y: 20 }, '-=0.5')
    .from('[data-purpose="hero-actions"]', { opacity: 0, y: 20, stagger: 0.15 }, '-=0.5')
    .from('[data-purpose="hero-metrics"]', { opacity: 0, y: 20 }, '-=0.4')
    .from('.autodo-app-shell', { 
      opacity: 0, 
      scale: 0.92, 
      y: 40, 
      rotationX: 8,
      transformPerspective: 1000,
      duration: 1.1,
      ease: 'back.out(1.4)'
    }, '-=0.8');

  // Subtle 3D Tilt Effect on App Shell based on mouse movement
  const heroMockup = document.querySelector('.autodo-app-shell');
  const heroVisualContainer = document.querySelector('[data-purpose="hero-app-mockup"]');

  if (heroVisualContainer && heroMockup) {
    heroVisualContainer.addEventListener('mousemove', (e) => {
      const rect = heroVisualContainer.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      
      const rotateX = (-y / rect.height) * 12;
      const rotateY = (x / rect.width) * 12;

      gsap.to(heroMockup, {
        rotateX: rotateX,
        rotateY: rotateY,
        transformPerspective: 1000,
        ease: 'power1.out',
        duration: 0.5
      });
    });

    heroVisualContainer.addEventListener('mouseleave', () => {
      gsap.to(heroMockup, {
        rotateX: 0,
        rotateY: 0,
        ease: 'power2.out',
        duration: 0.8
      });
    });
  }

  // Scroll Triggered Stagger for Feature Cards
  if (typeof ScrollTrigger !== 'undefined') {
    gsap.utils.toArray('.feature-card').forEach((card, index) => {
      gsap.from(card, {
        scrollTrigger: {
          trigger: card,
          start: 'top 85%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        y: 40,
        duration: 0.7,
        delay: (index % 3) * 0.15,
        ease: 'power2.out'
      });
    });

    gsap.utils.toArray('.step-card').forEach((step, index) => {
      gsap.from(step, {
        scrollTrigger: {
          trigger: step,
          start: 'top 85%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        scale: 0.95,
        y: 30,
        duration: 0.6,
        delay: index * 0.15,
        ease: 'back.out(1.2)'
      });
    });
  }
});
