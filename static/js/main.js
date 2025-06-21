document.addEventListener('DOMContentLoaded', () => {
    // Инициализация иконок (ваш оригинальный код)
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
    
    // Звездочный рейтинг (ваш оригинальный код с улучшениями)
    const starRatings = document.querySelectorAll('.star-rating i');
    if (starRatings.length > 0) {
        starRatings.forEach(star => {
            // Добавлен эффект при наведении
            star.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.2)';
                this.style.transition = 'transform 0.2s ease';
            });
            
            star.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
            
            star.addEventListener('click', function() {
                const rating = this.dataset.rating;
                const ratingInput = document.getElementById('id_rating');
                if (ratingInput) {
                    ratingInput.value = rating;
                    updateStars(rating);
                    
                    // Добавлен эффект "вспышки"
                    const flash = document.createElement('div');
                    flash.className = 'rating-flash';
                    this.parentElement.appendChild(flash);
                    setTimeout(() => flash.remove(), 500);
                }
            });
        });
    }

    // Эффекты для карточек услуг (ваш код + новые эффекты)
    document.querySelectorAll('.service-card').forEach(card => {
        // Ваши оригинальные эффекты
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0,0,0,0.2)';
            
            // Добавлен эффект свечения
            this.style.filter = 'drop-shadow(0 10px 5px rgba(212, 175, 55, 0.3))';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
            this.style.filter = 'none';
        });
        
        // Новый эффект при клике
        card.addEventListener('click', function() {
            this.classList.add('card-clicked');
            setTimeout(() => this.classList.remove('card-clicked'), 300);
        });
    });

    // Прокрутка (ваш оригинальный код)
    const scrollToTopBtn = document.getElementById('scrollToTop');
    const scrollToBottomBtn = document.getElementById('scrollToBottom');
    
    if (scrollToTopBtn) {
        // Добавлена анимация пульсации
        setInterval(() => {
            scrollToTopBtn.style.transform = 'scale(1.1)';
            setTimeout(() => scrollToTopBtn.style.transform = 'scale(1)', 500);
        }, 3000);
        
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

    // AJAX для услуг мастера (ваш оригинальный код с улучшенной анимацией)
    const masterSelect = document.getElementById('id_master');
    const servicesSelect = document.getElementById('id_services');

    if (masterSelect && servicesSelect) {
        function loadMasterServices(masterId) {
            if (!masterId) return;
            
            // Добавлен красивый спиннер
            servicesSelect.disabled = true;
            servicesSelect.innerHTML = `
                <option value="">
                    <div class="spinner-border spinner-border-sm text-warning"></div> Загрузка...
                </option>`;
            
            fetch(`/api/master-services/?master_id=${masterId}`)
                .then(response => {
                    if (!response.ok) throw new Error('Ошибка сервера: ' + response.status);
                    return response.json();
                })
                .then(data => {
                    if (!servicesSelect) return;
                    
                    // Плавное появление вариантов
                    servicesSelect.style.opacity = '0';
                    servicesSelect.innerHTML = '';
                    
                    if (data.services && data.services.length > 0) {
                        data.services.forEach((service, index) => {
                            setTimeout(() => {
                                const option = document.createElement('option');
                                option.value = service.id;
                                option.textContent = `${service.name} - ${service.price} руб.`;
                                option.style.transition = 'all 0.3s ease';
                                option.style.opacity = '0';
                                servicesSelect.appendChild(option);
                                
                                setTimeout(() => {
                                    option.style.opacity = '1';
                                }, 50);
                            }, index * 100);
                        });
                    } else {
                        servicesSelect.innerHTML = '<option value="">Нет доступных услуг</option>';
                    }
                    
                    setTimeout(() => {
                        servicesSelect.style.opacity = '1';
                        servicesSelect.disabled = false;
                    }, 300);
                })
                .catch(error => {
                    if (!servicesSelect) return;
                    console.error('Ошибка загрузки услуг:', error);
                    servicesSelect.innerHTML = `
                        <option value="" class="text-danger">
                            <i class="bi bi-exclamation-triangle"></i> Ошибка: ${error.message}
                        </option>`;
                    servicesSelect.disabled = false;
                    servicesSelect.style.opacity = '1';
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

    // AJAX для информации о мастере (ваш код с анимациями)
    const masterInfoSelect = document.getElementById('id_master');
    const masterInfoDiv = document.getElementById('master-info');
    
    if (masterInfoSelect && masterInfoDiv) {
        masterInfoSelect.addEventListener('change', function() {
            const masterId = this.value;
            if (!masterId) return;

            // Улучшенный спиннер
            masterInfoDiv.innerHTML = `
                <div class="text-center py-3">
                    <div class="spinner-border text-warning" style="width: 3rem; height: 3rem;">
                        <span class="visually-hidden">Загрузка...</span>
                    </div>
                </div>`;
            
            fetch(`/api/master-info/?master_id=${masterId}`, {
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            })
            .then(response => {
                if (!response.ok) throw new Error('Ошибка загрузки данных');
                return response.json();
            })
            .then(data => {
                if (!masterInfoDiv) return;
                
                // Плавное появление информации
                masterInfoDiv.style.opacity = '0';
                
                setTimeout(() => {
                    masterInfoDiv.innerHTML = data.photo ? 
                        `<div class="animate__animated animate__fadeIn">
                            <img src="${data.photo}" class="img-thumbnail mb-2 master-photo" style="max-width: 200px;">
                            <p class="text-highlight">Опыт работы: ${data.experience} лет</p>
                        </div>` :
                        `<p class="text-highlight animate__animated animate__fadeIn">Опыт работы: ${data.experience} лет</p>`;
                    
                    masterInfoDiv.style.opacity = '1';
                }, 300);
            })
            .catch(error => {
                if (!masterInfoDiv) return;
                masterInfoDiv.innerHTML = `
                    <div class="alert alert-danger animate__animated animate__shakeX">
                        <i class="bi bi-exclamation-octagon"></i> ${error.message}
                    </div>`;
            });
        });
    }

    // Валидация формы (ваш оригинальный код с анимациями)
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
                        error.className = 'invalid-feedback animate__animated animate__fadeIn';
                        error.textContent = 'Обязательное поле';
                        field.parentNode.appendChild(error);
                    }
                    field.classList.add('is-invalid', 'animate__animated', 'animate__shakeX');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid', 'animate__animated', 'animate__shakeX');
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
            } else {
                // Анимация успешной отправки
                form.classList.add('animate__animated', 'animate__fadeOut');
                setTimeout(() => form.classList.remove('animate__animated', 'animate__fadeOut'), 500);
            }
        });
    }

    // Анимация при прокрутке (ваш код с дополнениями)
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.scroll-animate');
        elements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                el.classList.add('active');
                
                // Добавлен эффект для изображений
                const images = el.querySelectorAll('img');
                images.forEach(img => {
                    img.style.transform = 'scale(1)';
                    img.style.opacity = '1';
                });
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll();

    // Плавное появление страницы (ваш код)
    document.body.classList.add('loaded');
    
    // Новые эффекты ==============================================
    
    // Эффект параллакса для шапки
    const header = document.querySelector('.victory-header');
    if (header) {
        window.addEventListener('scroll', () => {
            const scrollPosition = window.pageYOffset;
            header.style.backgroundPositionY = `${scrollPosition * 0.5}px`;
        });
    }

    // Эффект "золотой пыли" при кликах
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-gold') || e.target.closest('.btn-gold')) {
            const dust = document.createElement('div');
            dust.className = 'gold-dust';
            dust.style.left = `${e.clientX}px`;
            dust.style.top = `${e.clientY}px`;
            document.body.appendChild(dust);
            setTimeout(() => dust.remove(), 1000);
        }
    });

    // Падающие листья
    function createLeaves() {
        const leavesContainer = document.createElement('div');
        leavesContainer.className = 'falling-leaves';
        document.body.appendChild(leavesContainer);
        
        for (let i = 0; i < 15; i++) {
            const leaf = document.createElement('span');
            leaf.style.left = Math.random() * 100 + 'vw';
            leaf.style.animationDuration = (Math.random() * 10 + 5) + 's';
            leaf.style.animationDelay = Math.random() * 5 + 's';
            leaf.style.width = (Math.random() * 20 + 10) + 'px';
            leaf.style.height = leaf.style.width;
            leavesContainer.appendChild(leaf);
        }
    }
    
    createLeaves();
    
    // Эффект "чернил" для текста
    const inkTexts = document.querySelectorAll('.ink-text');
    inkTexts.forEach(text => {
        text.style.backgroundSize = '0% 100%';
        setTimeout(() => {
            text.style.backgroundSize = '100% 100%';
        }, 100);
    });
});

// Ваша оригинальная функция с дополнением
function updateStars(rating) {
    const stars = document.querySelectorAll('.star-rating i');
    if (!stars.length) return;
    
    stars.forEach(star => {
        const starValue = parseInt(star.dataset.rating);
        const wasFilled = star.classList.contains('bi-star-fill');
        const nowFilled = starValue <= rating;
        
        star.classList.toggle('bi-star-fill', nowFilled);
        star.classList.toggle('bi-star', !nowFilled);
        
        // Анимация изменения
        if (wasFilled !== nowFilled) {
            star.classList.add('animate__animated');
            star.classList.add(nowFilled ? 'animate__bounceIn' : 'animate__flipOutY');
            
            setTimeout(() => {
                star.classList.remove('animate__animated', 'animate__bounceIn', 'animate__flipOutY');
            }, 1000);
        }
    });
}