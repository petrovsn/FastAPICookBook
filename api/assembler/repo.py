from db.repo import DatabaseUnitOfWork

async def get_uow_db():
    async with DatabaseUnitOfWork() as repo:
        yield repo