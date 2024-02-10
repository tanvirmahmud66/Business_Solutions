document.addEventListener('DOMContentLoaded', function() {
    var currentUrl = window.location.pathname;
    var navItems = document.querySelectorAll('.navItem');

    navItems.forEach(function(navItem) {
        navItem.classList.remove('selected');
    });

    navItems.forEach(function(navItem) {
        var link = navItem.querySelector('a');
        var href = link.getAttribute('href');
        
        if (currentUrl === href || currentUrl.startsWith(href + '/')) {
            navItem.classList.add('selected');
        }
    });
});