import datetime
import os
from typing import List, Type
import uuid
from sqlalchemy import DateTime, String, func, ForeignKey, Column, Integer, UUID
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

POSTGRES_USER = os.getenv("DB_USER", "user")
POSTGRES_PASSWORD = os.getenv("DB_PASSWORD", "password")
POSTGRES_DB = os.getenv("DB_NAME", "aiohttp")
POSTGRES_PORT = os.getenv("DB_PORT", "5431")
POSTGRES_HOST = os.getenv("DB_HOST", "localhost")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    tokens: Mapped[List["Token"]] = relationship(
        "Token", back_populates="user", cascade="all, delete-orphan"
    )
    advertisements: Mapped[List["Advertisement"]] = relationship(back_populates="author")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "reg_time": int(self.registration_time.timestamp()),
            # 'tokens': list(self.tokens)
        }


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    header: Mapped[str] = mapped_column(String(200), index=True, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    date_of_create: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete='CASCADE'))
    author: Mapped['User'] = relationship(back_populates="advertisements")

    @property
    def dict(self):
        return {
            'id': self.id,
            'header': self.header,
            'description': self.description,
            'date': self.date_of_create.isoformat(),
            'author_id': self.author_id,
        }


class Token(Base):
    __tablename__ = 'token'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID, server_default=func.gen_random_uuid(), unique=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete='CASCADE'))
    user: Mapped[User] = relationship(User, back_populates="tokens")

    @property
    def dict(self):
        return {"id": self.id, "token": str(self.token), "user_id": self.user_id}


MODEL_TYPE = Type[User | Token | Advertisement]
MODEL = User | Token | Advertisement


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
