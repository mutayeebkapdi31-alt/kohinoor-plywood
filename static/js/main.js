(() => {
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (menu && nav) menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') === 'true';
    menu.setAttribute('aria-expanded', String(!open));
    nav.classList.toggle('open', !open);
    document.body.classList.toggle('menu-open', !open);
  });

  // Ply Finder: client-side step navigation; final recommendation is calculated server-side.
  const finder = document.querySelector('.finder-card');
  if (finder) {
    let step = 1;
    const steps = [...finder.querySelectorAll('.finder-step')];
    const next = finder.querySelector('#nextStep');
    const prev = finder.querySelector('#prevStep');
    const submit = finder.querySelector('#findGrade');
    const fill = finder.querySelector('.progress-fill');
    const label = finder.querySelector('#stepNumber');
    const show = () => {
      steps.forEach((el, i) => el.classList.toggle('active', i === step - 1));
      prev.disabled = step === 1;
      next.classList.toggle('hidden', step === 4);
      submit.classList.toggle('hidden', step !== 4);
      fill.style.width = `${step * 25}%`;
      label.textContent = `0${step} OF 04`;
    };
    next.addEventListener('click', () => {
      const current = steps[step - 1];
      const checked = current.querySelector('input[type=radio]:checked');
      const required = current.querySelector('input[required]');
      if (required && !checked) { required.focus(); current.classList.add('needs-choice'); return; }
      step = Math.min(4, step + 1); show();
    });
    prev.addEventListener('click', () => { step = Math.max(1, step - 1); show(); });
    finder.addEventListener('change', () => steps.forEach(s => s.classList.remove('needs-choice')));
    show();
  }

  // Two-step quote form. Browser validation checks step one before advancing.
  document.querySelectorAll('[data-multistep]').forEach(form => {
    const first = form.querySelector('[data-form-step="1"]');
    const second = form.querySelector('[data-form-step="2"]');
    form.querySelector('[data-next-form]').addEventListener('click', () => {
      const required = [...first.querySelectorAll('[required]')];
      const invalid = required.find(input => !input.checkValidity());
      if (invalid) { invalid.reportValidity(); return; }
      first.classList.remove('active'); second.classList.add('active');
      second.querySelector('input')?.focus();
    });
    form.querySelector('[data-prev-form]').addEventListener('click', () => {
      second.classList.remove('active'); first.classList.add('active');
    });
  });

  // Lightweight scroll reveal with reduced-motion support.
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('revealed'); observer.unobserve(entry.target); }
    }), { threshold: 0.12 });
    document.querySelectorAll('.section, .product-card, .reason, .audience-grid a').forEach(el => {
      el.classList.add('reveal'); observer.observe(el);
    });
  }

  // Track conversion intent. Replace console stub with approved GA4/GTM event wiring before launch.
  document.querySelectorAll('a[href*="wa.me"]').forEach(link => link.addEventListener('click', () => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({event: 'whatsapp_click', link_text: link.textContent.trim(), page_path: location.pathname});
  }));
  document.querySelectorAll('a[href^="tel:"]').forEach(link => link.addEventListener('click', () => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({event: 'phone_click', page_path: location.pathname});
  }));
  document.querySelectorAll('form').forEach(form => form.addEventListener('submit', () => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({event: 'lead_form_submit', form_name: form.getAttribute('action') || location.pathname});
  }));
})();
