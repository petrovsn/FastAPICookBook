from core.entities import User
from db.repo import RepoImpl

class UseCase:
    def __init__(self, db_repo):
        self.repo:RepoImpl = db_repo

    async def execute(*args, **kwargs):
        ...

class InitiateDb(UseCase):
    async def execute(self):
        result = await self.repo.initiate_database()
        return result

class GetUsers(UseCase):
    async def execute(self):
        result:list[User] = await self.repo.get_users()
        return result

class GetUser(UseCase):
    async def execute(self, user_id):
        result:User= await self.repo.get_user_by_id(user_id)
        return result 

class GetUserByName(UseCase):
    async def execute(self, user_name):
        result:User= await self.repo.get_user_by_filter({"name":user_name})
        return result 

class CreateUser(UseCase):
    async def execute(self, user_patch: dict):
        result:User= await self.repo.create_user(user_patch)
        return result 

class UpdateUser(UseCase):
    async def execute(self, user_id, user_patch: dict):
        result:User= await self.repo.update_user_by_id(user_id, user_patch)
        return result 

