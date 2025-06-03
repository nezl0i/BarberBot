// Анимация появления элементов
function animateElements() {
    const elements = document.querySelectorAll('h1, table');
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 200 * index);
    });
}

// Функция для отображения popup
function showPopup(message, isSuccess) {
    const popup = document.createElement('div');
    popup.innerText = message;

    // Стиль popup
    Object.assign(popup.style, {
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        padding: '15px 30px',
        borderRadius: '8px',
        boxShadow: '0 4px 15px rgba(0,0,0,0.3)',
        fontSize: '18px',
        zIndex: '1000',
        opacity: '0',
        transition: 'opacity 0.3s ease',
        backgroundColor: isSuccess ? '#4BB543' : '#D9534F', // зеленый или красный
        color: 'white'
    });

    document.body.appendChild(popup);

    // Плавное появление
    requestAnimationFrame(() => {
        popup.style.opacity = '1';
    });

    // Удаление через 3 секунды
    setTimeout(() => {
        popup.style.opacity = '0';
        popup.addEventListener('transitionend', () => {
            if (popup.parentNode) {
                popup.parentNode.removeChild(popup);
            }
        });
    }, 3000);
}

function closeApplication(id) {
    fetch(`/applications/close?application_id=${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Обновить таблицу или перезагрузить страницу
            location.reload();
        } else {
            showPopup('Не удалось закрыть заявку', false);
        }
    });
}

function removeApplication(id) {
    fetch(`/applications/remove?application_id=${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Обновить таблицу или перезагрузить страницу
            location.reload();
        } else {
            showPopup('Не удалось отменить заявку', false);
        }
    });
}


// Запуск анимации при загрузке страницы
window.addEventListener('load', animateElements);

// Обработчик для прокрутки на мобильных устройствах
document.addEventListener('DOMContentLoaded', (event) => {
    const main = document.querySelector('main');
    let isScrolling;

    main.addEventListener('scroll', function () {
        window.clearTimeout(isScrolling);
        isScrolling = setTimeout(function () {
            console.log('Scrolling has stopped.');
        }, 66);
    }, false);
});

// Обработчик для всех кнопок с классом 'submit-btn'
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.submit-btn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Находим родительский элемент <tr>
            const row = button.closest('tr');
            if (row) {
                row.style.display = 'none'; // скрываем строку

                // Создаем элемент popup
                showPopup('Заявка успешно закрыта', true);
            }
        });
    });
});

// Обработчик для всех кнопок с классом 'reset-btn'
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.reset-btn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Находим родительский элемент <tr>
            const row = button.closest('tr');
            if (row) {
                row.style.display = 'none'; // скрываем строку
                // Создаем элемент popup
                showPopup('Заявка успешно отменена', true);
            }
        });
    });
});