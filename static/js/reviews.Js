document.addEventListener('DOMContentLoaded', () => {
    // Звездочный рейтинг
    document.querySelectorAll('.star-rating i').forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            document.getElementById('id_rating').value = rating;
            updateStars(rating);
        });
    });

    // AJAX для мастера
    const masterSelect = document.getElementById('id_master');
    if (masterSelect) {
        masterSelect.addEventListener('change', function() {
            const masterId = this.value;
            const infoDiv = document.getElementById('master-info');
            if (!masterId || !infoDiv) return;

            infoDiv.innerHTML = '<div class="spinner-border text-warning"></div>';

            fetch(`/api/master-info/?master_id=${masterId}`, {
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            })
            .then(response => {
                if (!response.ok) throw new Error('Ошибка загрузки данных');
                return response.json();
            })
            .then(data => {
                infoDiv.innerHTML = data.photo ? 
                    `<img src="${data.photo}" class="img-thumbnail mb-2" style="max-width: 200px;">
                     <p class="text-highlight">Опыт работы: ${data.experience} лет</p>` :
                    `<p class="text-highlight">Опыт работы: ${data.experience} лет</p>`;
            })
            .catch(error => {
                infoDiv.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
            });
        });
    }

    // Валидация формы
    const form = document.getElementById('review-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            ['id_client_name', 'id_text', 'id_rating', 'id_master'].forEach(id => {
                const field = document.getElementById(id);
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
                window.scrollTo({
                    top: form.querySelector('.is-invalid').offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    }
});

function updateStars(rating) {
    document.querySelectorAll('.star-rating i').forEach(star => {
        const starValue = parseInt(star.dataset.rating);
        star.classList.toggle('bi-star-fill', starValue <= rating);
        star.classList.toggle('bi-star', starValue > rating);
    });
}
const ratingInput = document.getElementById('id_rating');
if (!ratingInput.value) {
    const ratingContainer = document.querySelector('.star-rating');
    const error = document.createElement('div');
    error.className = 'invalid-feedback d-block';
    error.textContent = 'Пожалуйста, выберите оценку';
    ratingContainer.parentElement.appendChild(error);
    isValid = false;
}