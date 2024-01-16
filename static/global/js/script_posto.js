// Função para lidar com o comportamento do menu
document.addEventListener('click', function(event) {
    const isMenuOpen = document.body.classList.contains('menu-open');
    const isInsideMenu = document.querySelector('.menu').contains(event.target);
    const isMenuToggle = document.querySelector('.menu-toggle').contains(event.target);
    if (isMenuOpen && !isInsideMenu && !isMenuToggle) {
        document.body.classList.remove('menu-open');
    }
  });
  
  document.querySelector('.menu-toggle').addEventListener('click', function() {
    document.body.classList.toggle('menu-open');
  });
  
  