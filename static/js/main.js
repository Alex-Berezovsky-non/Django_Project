// main.js
document.addEventListener('DOMContentLoaded', () => {
    // Анимация при загрузке
    document.querySelectorAll('.victory-animate').forEach(el => {
        el.style.opacity = '0';
        setTimeout(() => {
            el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 100);
    });

    // Звездочный рейтинг
    document.querySelectorAll('.star-rating i').forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            document.getElementById('id_rating').value = rating;
            updateStars(rating);
        });
    });

    // Анимация при прокрутке
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.scroll-animate');
        elements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll();

    // Эффекты при наведении на карточки услуг
    document.querySelectorAll('.service-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0,0,0,0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        });
    });

    // Инициализация иконок
    function checkIconsLoaded() {
        if (document.querySelector('.bi') && getComputedStyle(document.querySelector('.bi')).fontFamily.includes('bootstrap-icons')) {
            document.documentElement.classList.add('icons-loaded');
            return true;
        }
        return false;
    }
    
    if (checkIconsLoaded()) return;
    
    let checkCount = 0;
    const checkInterval = setInterval(() => {
        if (checkIconsLoaded() || checkCount++ > 20) {
            clearInterval(checkInterval);
            document.documentElement.classList.add('icons-loaded');
        }
    }, 100);
});

function updateStars(rating) {
    document.querySelectorAll('.star-rating i').forEach(star => {
        const starValue = parseInt(star.dataset.rating);
        star.classList.toggle('bi-star-fill', starValue <= rating);
        star.classList.toggle('bi-star', starValue > rating);
    });
}

// AJAX для загрузки услуг мастера
document.addEventListener('DOMContentLoaded', function() {
    const masterSelect = document.getElementById('id_master');
    const servicesSelect = document.getElementById('id_services');

    function loadMasterServices(masterId) {
        if (!masterId) return;
        servicesSelect.disabled = true;
        servicesSelect.innerHTML = '<option value="">Загрузка услуг...</option>';
        
        fetch(`/api/master-services/?master_id=${masterId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сервера: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                servicesSelect.innerHTML = '';
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                if (data.services && data.services.length > 0) {
                    data.services.forEach(service => {
                        const option = document.createElement('option');
                        option.value = service.id;
                        option.textContent = `${service.name} - ${service.price} руб.`;
                        servicesSelect.appendChild(option);
                    });
                } else {
                    servicesSelect.innerHTML = '<option value="">Нет доступных услуг</option>';
                }
                servicesSelect.disabled = false;
            })
            .catch(error => {
                console.error('Ошибка загрузки услуг:', error);
                servicesSelect.innerHTML = `<option value="">Ошибка: ${error.message}</option>`;
                servicesSelect.disabled = false;
            });
    }

    if (masterSelect) {
        masterSelect.addEventListener('change', function() {
            loadMasterServices(this.value);
        });
        
        if (masterSelect.value) {
            loadMasterServices(masterSelect.value);
        } else {
            servicesSelect.innerHTML = '<option value="">Сначала выберите мастера</option>';
        }
    }
});