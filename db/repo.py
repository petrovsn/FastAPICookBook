
from sqlalchemy import create_engine

from sqlalchemy import event, update, insert, delete, delete, select
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from db.models import Base, User, Post
import random
from utils.singleton import SingletonMeta
import asyncio



@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Проверяем, что мы работаем именно с SQLite
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

async def initiate_database(engine):
    names = ["Alice", "Bob", "Charly"]
    posts = ["Hello, world!", "I love you!", "I hate everything about you", "Cats are best", "Peace!"]
    async with AsyncSession(engine) as session:
        await session.execute(insert(User),[{"name":name} for name in names])
        for post in posts:
            random_user_id = random.randint(1,3)
            user = await session.get(User, random_user_id)
            user.posts.append(Post(text = post))
            await session.flush()
        await session.commit()

def initiate_engine(filename = ":memory:", echo = True):
    engine = create_async_engine(f"sqlite+aiosqlite:///{filename}", echo=echo, future=True)
    return engine

class Engine(metaclass = SingletonMeta):
    def __init__(self):
        self.engine = initiate_engine("resources/db.db")

    def get(self):
        return self.engine

class DatabaseUnitOfWork:
    def __init__(self):
        self.session = AsyncSession(Engine().get())

    async def __aenter__(self):
        return RepoImpl(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # Произошло исключение — откатываем транзакцию
            await self.session.rollback()
        else:
            # Всё успешно — фиксируем
            await self.session.commit()
        # Закрываем сессию (освобождаем соединение)
        await self.session.close()


class RepoImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self):
        result = await self.session.execute(select(User))
        return [
        {
            "id": row.id,
            "name": row.name,
        }
        for row in result.scalars()
    ]

    async def get_user_by_id(self, user_id):
        user = await self.session.get(User, user_id)
        return {
            "id": user.id,
            "name": user.name,
            "posts": [{"id": post.id, "text": post.text, "user_id":user.id} for post in user.posts]
        }

    async def initiate_database(self):
        async with Engine().get().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        names = ["Alice", "Bob", "Charly"]
        posts = ["Hello, world!", "I love you!", "I hate everything about you", "Cats are best", "Peace!"]
        await self.session.execute(insert(User),[{"name":name} for name in names])
        for post in posts:
            random_user_id = random.randint(1,3)
            user = await self.session.get(User, random_user_id)
            user.posts.append(Post(text = post))
            await self.session.flush()
