// Simple language switch using data-en / data-ru attributes
(function () {
  const btnEn = document.getElementById('btn-en');
  const btnRu = document.getElementById('btn-ru');

  function setLanguage(lang) {
    const elements = document.querySelectorAll('[data-en]');
    elements.forEach((el) => {
      const text = el.getAttribute(lang === 'en' ? 'data-en' : 'data-ru');
      if (text !== null) {
        el.textContent = text;
      }
    });

    document.documentElement.setAttribute('lang', lang);

    if (lang === 'en') {
      btnEn.classList.add('active');
      btnRu.classList.remove('active');
      btnEn.setAttribute('aria-pressed', 'true');
      btnRu.setAttribute('aria-pressed', 'false');
    } else {
      btnRu.classList.add('active');
      btnEn.classList.remove('active');
      btnRu.setAttribute('aria-pressed', 'true');
      btnEn.setAttribute('aria-pressed', 'false');
    }

    // Optionally store preference
    try {
      localStorage.setItem('xanaka_lang', lang);
    } catch (e) {
      // ignore
    }
  }

  btnEn.addEventListener('click', () => setLanguage('en'));
  btnRu.addEventListener('click', () => setLanguage('ru'));

  // Init language from localStorage or default to EN
  const storedLang = (function () {
    try {
      return localStorage.getItem('xanaka_lang');
    } catch (e) {
      return null;
    }
  })();

  setLanguage(storedLang === 'ru' ? 'ru' : 'en');
})();

// Mobile burger menu
(function () {
  const burger = document.getElementById('burger');
  const nav = document.querySelector('.main-nav');

  if (!burger || !nav) return;

  burger.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    burger.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
    });
  });
})();

// Forms: basic handling + UTM extraction
(function () {
  // Fill current year in footer
  const yearSpan = document.getElementById('year');
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  // Extract UTM params and put into hidden inputs
  const params = new URLSearchParams(window.location.search);
  const utmSource = document.getElementById('utm_source');
  const utmMedium = document.getElementById('utm_medium');
  const utmCampaign = document.getElementById('utm_campaign');

  if (utmSource && params.get('utm_source')) {
    utmSource.value = params.get('utm_source');
  }
  if (utmMedium && params.get('utm_medium')) {
    utmMedium.value = params.get('utm_medium');
  }
  if (utmCampaign && params.get('utm_campaign')) {
    utmCampaign.value = params.get('utm_campaign');
  }

  // Hero mini form
  const heroForm = document.getElementById('hero-form');
  const heroStatus = document.getElementById('hero-form-status');

  if (heroForm && heroStatus) {
    heroForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(heroForm);
      const name = formData.get('name');
      const phone = formData.get('phone');

      if (!name || !phone) {
        heroStatus.textContent =
          document.documentElement.lang === 'ru'
            ? 'Пожалуйста, заполните имя и телефон.'
            : 'Please fill in name and phone.';
        return;
      }

      heroStatus.textContent =
        document.documentElement.lang === 'ru'
          ? 'Спасибо! Мы свяжемся с вами в ближайшее время.'
          : 'Thank you! We will contact you shortly.';
      heroForm.reset();
    });
  }

  // Contact form
  const contactForm = document.getElementById('contact-form');
  const contactStatus = document.getElementById('contact-form-status');

  if (contactForm && contactStatus) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(contactForm);

      const requiredFields = ['name', 'email', 'phone'];
      for (const field of requiredFields) {
        if (!formData.get(field)) {
          contactStatus.textContent =
            document.documentElement.lang === 'ru'
              ? 'Пожалуйста, заполните обязательные поля (имя, email, телефон).'
              : 'Please fill in required fields (name, email, phone).';
          return;
        }
      }

      if (!contactForm.querySelector('#consent').checked) {
        contactStatus.textContent =
          document.documentElement.lang === 'ru'
            ? 'Необходимо согласиться с обработкой персональных данных.'
            : 'You need to accept the personal data processing.';
        return;
      }

      contactStatus.textContent =
        document.documentElement.lang === 'ru'
          ? 'Спасибо! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.'
          : 'Thank you! Your request has been sent. We will contact you shortly.';
      contactForm.reset();
    });
  }
})();
