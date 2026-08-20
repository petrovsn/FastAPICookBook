
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

def initiate_engine(filename = ":memory:", echo = False):
    #engine = create_async_engine(f"sqlite+aiosqlite:///{filename}", echo=echo, future=True)

    engine = create_async_engine(
    "postgresql+asyncpg://postgres:12345@localhost:5432/FastapiCookBookDb",
    echo=echo, future=True
)
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

    async def get_users(self, offset = None, limit = None):
        stmt = select(User)

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)

        result_dicts = [row.to_dict() for row in result.scalars()]
        return result_dicts

    async def get_user_by_id(self, user_id, for_update = False):
        user = await self.session.get(User, user_id, with_for_update= for_update)
        result_dict =  user.to_dict()
        result_dict["posts"] = [post.to_dict() for post in user.posts]
        return result_dict

    async def get_user_by_filter(self, filters):
        stmt = select(User)
        for key, value in filters.items():
            stmt = stmt.where(getattr(User, key) == value)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is not None:
            return user.to_dict()
        return None
    

    async def create_user(self, user_dto_dict):
        user = User(**user_dto_dict)
        self.session.add(user)
        await self.session.flush()
        return user.to_dict()

    async def update_user_by_id(self, user_id, user_dto_dict):
        user = await self.session.get(User, user_id)
        for key, value in user_dto_dict.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await self.session.flush()
        return user.to_dict()

    async def create_post(self, post_dto_dict):
        post = Post(**post_dto_dict)
        self.session.add(post)
        await self.session.flush()
        return post.to_dict()

    async def create_posts(self, posts_list: list[dict]):
        stmt = insert(Post)
        result = await self.session.execute(stmt, posts_list)
        return True

    async def get_posts(self, offset = None, limit = None):
        stmt = select(Post)

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)

        result_dicts = [row.to_dict() for row in result.scalars()]
        return result_dicts

    async def get_posts_cursored(self, offset = None, limit = None):
        stmt = select(Post).order_by(Post.id)

        if offset is not None:
            stmt = stmt.where(Post.id>offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)

        result_dicts = [row.to_dict() for row in result.scalars()]
        return result_dicts
    

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

