document.addEventListener('DOMContentLoaded', () => {
  const navbarBurgers = document.querySelectorAll('.navbar-burger');

  navbarBurgers.forEach(burger => {
    burger.addEventListener('click', () => {
      const targetId = burger.dataset.target;
      const targetElement = document.getElementById(targetId);

      burger.classList.toggle('is-active');
      targetElement.classList.toggle('is-active');
    });
  });
});
