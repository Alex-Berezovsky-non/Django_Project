document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar');
    const navbarHeight = navbar ? navbar.offsetHeight + 20 : 0;

    // Плавная прокрутка с короткой анимацией
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const target = document.querySelector(link.hash);
            if (!target) return;

            const start = window.pageYOffset;
            const targetPos = target.offsetTop - navbarHeight;
            const distance = targetPos - start;
            const startTime = performance.now();
            const duration = 300; // Укороченная длительность анимации

            function animateScroll(time) {
                const elapsed = time - startTime;
                const progress = Math.min(elapsed / duration, 1);
                window.scrollTo(0, start + distance * easeInOutQuad(progress));
                
                if (progress < 1) {
                    requestAnimationFrame(animateScroll);
                }
            }

            function easeInOutQuad(t) {
                return t < 0.5 ? 2*t*t : -1 + (4-2*t)*t;
            }

            requestAnimationFrame(animateScroll);
            history.replaceState(null, null, link.hash);
        });
    });

    // Обновление активной ссылки при скролле
    let isScrolling;
    window.addEventListener('scroll', () => {
        if (isScrolling) cancelAnimationFrame(isScrolling);
        isScrolling = requestAnimationFrame(updateActiveSection);
    });

    function updateActiveSection() {
        let activeSection = null;
        document.querySelectorAll('section[id]').forEach(section => {
            const { top } = section.getBoundingClientRect();
            if (top <= navbarHeight && (!activeSection || top < activeSection.top)) {
                activeSection = section.id;
            }
        });
        
        if (activeSection) {
            document.querySelectorAll('.nav-link').forEach(link => {
                const isActive = link.hash === `#${activeSection}`;
                link.classList.toggle('active', isActive);
                link.setAttribute('aria-current', isActive ? 'page' : null);
            });
        }
    }
});