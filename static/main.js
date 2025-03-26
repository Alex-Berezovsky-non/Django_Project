// Плавная прокрутка для якорей
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Анимация при загрузке страницы
window.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.animate-on-load');
    elements.forEach(el => {
        el.style.opacity = '0';
        setTimeout(() => {
            el.style.transition = 'opacity 1s';
            el.style.opacity = '1';
        }, 100);
    });
});

// Обработка формы (пример)
document.querySelector('.contact-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Форма отправлена!');
});