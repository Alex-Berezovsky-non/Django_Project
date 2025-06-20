document.addEventListener('DOMContentLoaded', () => {
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
    
    // Звездочный рейтинг (с проверкой наличия)
    const starRatings = document.querySelectorAll('.star-rating i');
    if (starRatings.length > 0) {
        starRatings.forEach(star => {
            star.addEventListener('click', function() {
                const rating = this.dataset.rating;
                const ratingInput = document.getElementById('id_rating');
                if (ratingInput) {
                    ratingInput.value = rating;
                    updateStars(rating);
                }
            });
        });
    }

    // Эффекты при наведении на карточки услуг (с проверкой)
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

    // Прокрутка вверх/вниз (с проверкой)
    const scrollToTopBtn = document.getElementById('scrollToTop');
    const scrollToBottomBtn = document.getElementById('scrollToBottom');
    
    if (scrollToTopBtn) {
        scrollToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    if (scrollToBottomBtn) {
        scrollToBottomBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        });
    }

    // AJAX для загрузки услуг мастера (с улучшенной обработкой ошибок)
    const masterSelect = document.getElementById('id_master');
    const servicesSelect = document.getElementById('id_services');

    if (masterSelect && servicesSelect) {
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
                    if (!servicesSelect) return;
                    
                    servicesSelect.innerHTML = '';
                    
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
                    if (!servicesSelect) return;
                    console.error('Ошибка загрузки услуг:', error);
                    servicesSelect.innerHTML = `<option value="">Ошибка: ${error.message}</option>`;
                    servicesSelect.disabled = false;
                });
        }

        masterSelect.addEventListener('change', function() {
            loadMasterServices(this.value);
        });
        
        if (masterSelect.value) {
            loadMasterServices(masterSelect.value);
        } else {
            servicesSelect.innerHTML = '<option value="">Сначала выберите мастера</option>';
        }
    }

    // AJAX для информации о мастере (с проверкой)
    const masterInfoSelect = document.getElementById('id_master');
    const masterInfoDiv = document.getElementById('master-info');
    
    if (masterInfoSelect && masterInfoDiv) {
        masterInfoSelect.addEventListener('change', function() {
            const masterId = this.value;
            if (!masterId) return;

            masterInfoDiv.innerHTML = '<div class="spinner-border text-warning"></div>';

            fetch(`/api/master-info/?master_id=${masterId}`, {
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            })
            .then(response => {
                if (!response.ok) throw new Error('Ошибка загрузки данных');
                return response.json();
            })
            .then(data => {
                if (!masterInfoDiv) return;
                masterInfoDiv.innerHTML = data.photo ? 
                    `<img src="${data.photo}" class="img-thumbnail mb-2 master-photo" style="max-width: 200px;">
                     <p class="text-highlight">Опыт работы: ${data.experience} лет</p>` :
                    `<p class="text-highlight">Опыт работы: ${data.experience} лет</p>`;
            })
            .catch(error => {
                if (!masterInfoDiv) return;
                masterInfoDiv.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
            });
        });
    }

    // Валидация формы (с проверкой)
    const form = document.getElementById('review-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            ['id_client_name', 'id_text', 'id_rating', 'id_master'].forEach(id => {
                const field = document.getElementById(id);
                if (!field) return;
                
                const errorDiv = field.parentNode.querySelector('.invalid-feedback');
                
                if (!field.value.trim()) {
                    if (!errorDiv) {
                        const error = document.createElement('div');
                        error.className = 'invalid-feedback';
                        error.textContent = 'Обязательное поле';
                        field.parentNode.appendChild(error);
                    }
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                    if (errorDiv) errorDiv.remove();
                }
            });

            if (!isValid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    window.scrollTo({
                        top: firstInvalid.offsetTop - 100,
                        behavior: 'smooth'
                    });
                }
            }
        });
    }

    // Анимация при прокрутке
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.scroll-animate');
        elements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                el.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll();

    // Плавное появление страницы
    document.body.classList.add('loaded');
});

function updateStars(rating) {
    const stars = document.querySelectorAll('.star-rating i');
    if (!stars.length) return;
    
    stars.forEach(star => {
        const starValue = parseInt(star.dataset.rating);
        star.classList.toggle('bi-star-fill', starValue <= rating);
        star.classList.toggle('bi-star', starValue > rating);
    });
}