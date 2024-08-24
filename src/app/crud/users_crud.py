from sqlalchemy import select

from app.database import async_session_maker
from app.models.user import UserModel


async def create_new_user(new_user_dict: dict):
    """Добавление записи в таблицу users."""
    async with async_session_maker() as session:
        db_user_info = UserModel(**new_user_dict)
        session.add(db_user_info)
        await session.commit()


async def get_user_by_login(login: str):
    """Получение данных пользователя по логину."""
    async with async_session_maker() as session:
        query = select(UserModel).where(UserModel.login == login)
        user = await session.execute(query)
        return user.scalars().first()


async def get_user_by_id(user_id: int):
    """Получение данных пользователя по id."""
    async with async_session_maker() as session:
        query = select(UserModel).where(UserModel.id == user_id)
        user = await session.execute(query)
        return user.scalars().first()
