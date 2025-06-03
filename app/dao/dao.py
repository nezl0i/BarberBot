from selectors import SelectSelector

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.config import settings
from app.dao.base import BaseDAO
from app.api.models import User, Service, Application, Master
from app.database import async_session_maker


class UserDAO(BaseDAO):
    model = User


class ServiceDAO(BaseDAO):
    model = Service


class MasterDAO(BaseDAO):
    model = Master


class ApplicationDAO(BaseDAO):
    model = Application

    @classmethod
    async def create_list_app(cls, applications, is_admin: bool = False):
        return [
            {
                "application_id": app.id,
                "service_name": app.service.service_name,  # Название услуги
                "master_name": app.master.master_name,  # Имя мастера
                "appointment_date": app.appointment_date,
                "appointment_time": '{:%H:%M}'.format(app.appointment_time),
                "gender": app.gender.value,
                "is_admin": is_admin,
                "is_closed": "Закрыта" if app.is_closed else "В работе"
            }
            for app in applications
        ]


    @classmethod
    async def get_applications_by_user(cls, user_id: int):
        """
        Возвращает все заявки пользователя по user_id с дополнительной информацией
        о мастере и услуге.

        Аргументы:
            user_id: Идентификатор пользователя.

        Возвращает:
            Список заявок пользователя с именами мастеров и услуг.
        """
        async with async_session_maker() as session:
            try:
                # Используем joinedload для ленивой загрузки связанных объектов
                query = (
                    select(cls.model)
                    .options(joinedload(cls.model.master), joinedload(cls.model.service), joinedload(cls.model.user))
                    .filter_by(user_id=user_id)
                )
                result = await session.execute(query)
                applications = result.scalars().all()

                return await cls.create_list_app(applications, False)
            except SQLAlchemyError as e:
                print(f"Error while fetching applications for user {user_id}: {e}")
                return None
            except AttributeError as e:
                print(f"Error for user {user_id}: {e}")
                return None

    @classmethod
    async def get_all_applications(cls, archive=False):
        """
        Возвращает все заявки в базе данных с дополнительной информацией о мастере и услуге.

        Возвращает:
            Список всех заявок с именами мастеров и услуг.
        """
        async with async_session_maker() as session:
            try:
                # Используем joinedload для загрузки связанных данных
                if archive:
                    query = (
                        select(cls.model)
                        .options(joinedload(cls.model.master), joinedload(cls.model.service))
                        .filter_by(is_closed=True)
                    )
                else:
                    query = (
                        select(cls.model)
                        .options(joinedload(cls.model.master), joinedload(cls.model.service))
                        .filter_by(is_closed=False)
                    )
                result = await session.execute(query)
                applications = result.scalars().all()
                return await cls.create_list_app(applications, True)

            except SQLAlchemyError as e:
                print(f"Error while fetching all applications: {e}")
                return None

