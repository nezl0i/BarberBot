from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.config import settings

base_site = settings.BASE_SITE

def main_keyboard(user_id: int, first_name: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    url_applications = f"{base_site}/applications?user_id={user_id}"
    url_add_application = f'{base_site}/form?user_id={user_id}&first_name={first_name}'
    kb.button(text="🌐 Мои заявки", web_app=WebAppInfo(url=url_applications))
    kb.button(text="📝 Оставить заявку", web_app=WebAppInfo(url=url_add_application))
    kb.button(text="ℹ️ О нас")
    if user_id in settings.ADMIN_IDS:
        kb.button(text="🔑 Админ панель")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def back_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="🔙 Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    url_applications = f"{base_site}/admin?admin_id={user_id}"
    url_archive_applications = f"{base_site}/archive/admin?admin_id={user_id}"
    url_add_master = f"{base_site}/masters?admin_id={user_id}"
    url_add_service = f"{base_site}/service?admin_id={user_id}"
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 На главную", callback_data="back_home")
    kb.button(text="📝 Текущие заявки", web_app=WebAppInfo(url=url_applications))
    kb.button(text="🗑 Архивные заявки", web_app=WebAppInfo(url=url_archive_applications))
    kb.button(text="✂️ Добавить мастера", web_app=WebAppInfo(url=url_add_master))
    kb.button(text="📘 Добавить услугу", web_app=WebAppInfo(url=url_add_service))
    kb.adjust(1)
    return kb.as_markup()


def app_keyboard(user_id: int, first_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    url_add_application = f'{base_site}/form?user_id={user_id}&first_name={first_name}'
    kb.button(text="📝 Оставить заявку", web_app=WebAppInfo(url=url_add_application))
    kb.adjust(1)
    return kb.as_markup()