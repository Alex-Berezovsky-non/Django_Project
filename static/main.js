document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar');
    const navbarHeight = navbar ? navbar.offsetHeight : 0;
    let scrollTimeout;

    // Плавная прокрутка
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const target = document.querySelector(link.hash);
            if (!target) return;
            
            target.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start',
                inline: 'nearest'
            });
            
            history.pushState(null, null, link.hash);
            setActiveLink(link.hash.slice(1)); // Убираем #
        });
    });

    // Оптимизированный скролл
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(updateActiveSection, 100);
    });

    function updateActiveSection() {
        let activeSection = null;
        
        document.querySelectorAll('section[id]').forEach(section => {
            const { top } = section.getBoundingClientRect();
            if (top <= navbarHeight + 20 && // 20px допуск
                (!activeSection || top < activeSection.top)) {
                activeSection = { id: section.id, top };
            }
        });
        
        if (activeSection) setActiveLink(activeSection.id);
    }

    // Обновление активной ссылки
    function setActiveLink(sectionId) {
        document.querySelectorAll('.nav-link').forEach(link => {
            const isActive = link.hash === `#${sectionId}`;
            link.classList.toggle('active', isActive);
            link.setAttribute('aria-current', isActive ? 'page' : null);
        });
    }
});
