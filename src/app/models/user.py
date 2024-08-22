from sqlalchemy import BigInteger, Boolean, Integer, MetaData, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

metadata = MetaData()


class UserModel(Base):
    """Модель для создания таблицы users."""

    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth_schema'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False,
    )
    password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    balance: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
