export function showPopup(message, isSuccess) {
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
