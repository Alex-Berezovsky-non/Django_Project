document.addEventListener('DOMContentLoaded', function() {
    // Плавная прокрутка
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    // Параллакс-эффект
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        
        // Для заголовков
        document.querySelectorAll('h1').forEach(h1 => {
            h1.style.transform = `translateX(${scrolled * 0.1}px)`;
        });

        // Для карточек
        document.querySelectorAll('.card').forEach((card, index) => {
            card.style.transform = `translateY(${scrolled * 0.05 * (index % 2 ? -1 : 1)}px)`;
        });
    });

    // Анимация статусов
    document.querySelectorAll('.status').forEach(status => {
        status.style.animation = 'colorPulse 2s infinite';
    });

    // Обработка форм
    document.querySelector('.contact-form')?.addEventListener('submit', (e) => {
        e.preventDefault();
        const form = e.target;
        form.classList.add('processing');
        setTimeout(() => {
            form.classList.remove('processing');
            alert('Форма отправлена!');
        }, 1500);
    });
});

