//import showPopup from './popup.js';

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


document.addEventListener('DOMContentLoaded', function()
{
    const addServiceBtn = document.querySelector('.btn_add_service');
    const delServiceBtn = document.querySelector('.delete-btn');
    const appointmentsTable = document.querySelector('#services-table');

    // Обработчик для общей кнопки "Добавить"
    addServiceBtn.addEventListener('click', function()
    {

    // Проверяем, не добавлено ли уже поле ввода
        if (document.querySelector('.add-service-container')) return;

        // Создаем контейнер для поля ввода и кнопки
        const container = document.createElement('div');
        container.className = 'add-service-container';
        container.style.margin = '20px 0';
        container.style.display = 'flex';
        container.style.gap = '10px';

        // Создаем поле ввода
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Введите наименование услуги';
        input.style.flexGrow = '1';
        input.style.padding = '8px';

        // Создаем кнопку "Добавить"
        const addBtn = document.createElement('button');
        addBtn.textContent = 'Добавить';
        addBtn.className = 'add-btn';
        addBtn.style.padding = '8px 16px';

        // Добавляем элементы в контейнер
        container.appendChild(input);
        container.appendChild(addBtn);

        // Вставляем контейнер после таблицы
        appointmentsTable.insertAdjacentElement('afterend', container);

        // Фокусируемся на поле ввода
        input.focus();

        // Обработчик для кнопки "Добавить"
        addBtn.addEventListener('click', function()
        {
            const serviceName = input.value.trim();
            if (!serviceName)
            {
                showPopup('Пожалуйста, введите название услуги', false);
                return;
            }

            // AJAX-запрос к серверу
            fetch(`/add/service?service_name=${serviceName}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data =>
            {
                if (data.success)
                {
                    // Обновляем таблицу без перезагрузки страницы
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `
                        <td>${serviceName}</td>
                        <td><button class="delete-btn" onclick=''>Удалить</button></td>
                    `;
                    document.querySelector('#services-table tbody').appendChild(newRow);
                    // Очищаем поле ввода
                    input.value = '';
                    showPopup(data.message, true);
                } else
                {
                    showPopup(data.message, false);
                }
            })
            .catch(error =>
            {
                const message = error.message.includes('Network Error')
                    ? 'Проблемы с соединением'
                    : error.message;
                showPopup(message, false);
            })
            .finally(() =>
            {
                addBtn.disabled = false;
            });
        });

        // Закрываем поле ввода при нажатии Esc
        input.addEventListener('keydown', function(e)
        {
            if (e.key === 'Escape')
            {
                container.remove();
            } else if (e.key === 'Enter')
            {
                addBtn.click();  // Добавляем по нажатию Enter
            }
        });
    });
});

function deleteService(id) {
    fetch(`/delete/service/?service_id=${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            showPopup('Не удалось удалить услугу', false);
        }
    });
}

// Обработчик для всех кнопок с классом 'submit-btn'
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.delete-btn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Находим родительский элемент <tr>
            const row = button.closest('tr');
            if (row) {
                row.style.display = 'none'; // скрываем строку

                // Создаем элемент popup
                showPopup('Услуга успешно удалена', true);
            }
        });
    });
});