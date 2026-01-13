// gestion du menu

const container_menu = document.getElementById('menu');

const links = container_menu.querySelectorAll('a');
const currentUrl = window.location.href;

links.forEach(link => {
    // On vérifie si l'URL du lien est contenue dans l'URL actuelle
    if (currentUrl.includes(link.href)) {
        link.classList.add('header__a--activate');
        link.classList.remove('header__a--no_activate');
    } else {
        link.classList.remove('header__a--activate');
        link.classList.add('header__a--no_activate');
    }
});

// gestion du thème clair et du thème sombre

const currentTheme = localStorage.getItem('theme')
const btnToggleTheme = document.querySelector('#theme_toggle');
// on sélectionne la balise HTML
const root = document.documentElement;

// on applique le thème au chargement
root.setAttribute('data-theme', currentTheme);

btnToggleTheme.addEventListener('click', (event) => {
    if (root.getAttribute('data-theme') === 'dark') {
        root.setAttribute('data-theme', 'light')
        localStorage.setItem('theme', 'light');
    } else {
        root.setAttribute('data-theme', 'dark')
        localStorage.setItem('theme', 'dark');
    }
});