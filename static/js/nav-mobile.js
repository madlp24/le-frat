(function () {
  const burger = document.querySelector('.lf-burger');
  const mobile = document.getElementById('lfMobileMenu');
  const closeBtn = document.querySelector('.lf-mobile__close');

  if (!burger || !mobile || !closeBtn) return;

  function openMenu() {
    mobile.hidden = false; // remove from layout so it can show
    mobile.classList.add('is-open');
    burger.setAttribute('aria-expanded', 'true');
    mobile.setAttribute('aria-hidden', 'false');

    // move focus into the menu (prevents aria-hidden + focus warning)
    closeBtn.focus();
  }

  function closeMenu() {
    mobile.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    mobile.setAttribute('aria-hidden', 'true');

    mobile.hidden = true;

    // return focus to the burger button
    burger.focus();
  }

  burger.addEventListener('click', () => {
    mobile.classList.contains('is-open') ? closeMenu() : openMenu();
  });

  closeBtn.addEventListener('click', closeMenu);

  // click outside the panel closes
  mobile.addEventListener('click', (e) => {
    if (e.target === mobile) closeMenu();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMenu();
  });
})();
