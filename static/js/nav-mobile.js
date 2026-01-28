(function () {
  const burger = document.querySelector('.lf-burger');
  const mobile = document.getElementById('lfMobileMenu');
  const closeBtn = document.querySelector('.lf-mobile__close');

  if (!burger || !mobile || !closeBtn) return;

  function openMenu() {
    mobile.classList.add('is-open');
    burger.setAttribute('aria-expanded', 'true');
    mobile.setAttribute('aria-hidden', 'false');
  }

  function closeMenu() {
    mobile.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    mobile.setAttribute('aria-hidden', 'true');
  }

  burger.addEventListener('click', openMenu);
  closeBtn.addEventListener('click', closeMenu);

  mobile.addEventListener('click', (e) => {
    if (e.target === mobile) closeMenu();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMenu();
  });
})();
