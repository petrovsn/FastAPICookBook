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
    async def execute(self, offset = None, limit = None):
        result:list[User] = await self.repo.get_users(offset, limit)
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
        result = await self.repo.update_user_by_id(user_id, user_patch)
        return result 
import asyncio
class TransferMoneyCase(UseCase):
    async def execute(self, from_user_id: int, to_user_id: int, amount: int):
        from_user_dto = await self.repo.get_user_by_id(from_user_id, for_update=True)
        if from_user_dto is None:
            raise Exception("no sender user")
        to_user_dto = await self.repo.get_user_by_id(to_user_id, for_update=True)
        if to_user_dto is None:
            raise Exception("no receiver user")

        if from_user_dto["money"]<amount:
            raise Exception("not enough money")

        new_from_user = await self.repo.update_user_by_id(from_user_id, {"money":from_user_dto["money"]-amount})

        await asyncio.sleep(15)

        new_to_user = await self.repo.update_user_by_id(to_user_id, {"money":to_user_dto["money"]+amount})
        return {
            "new_from_user":new_from_user,
            "new_to_user": new_to_user
        }
        
        
class CreatePost(UseCase):
    async def execute(self, user_id: int, post_text:str):
        user_dto = await self.repo.get_user_by_id(user_id, for_update=True)
        if user_dto is None:
            raise Exception("no user")

        post_dto = {
            "user_id":user_id,
            "text":post_text
        }

        result = await self.repo.create_post(post_dto)
        return result
        

class CreatePosts(UseCase):
    async def execute(self, user_id: int, posts_count:int):
        user_dto = await self.repo.get_user_by_id(user_id, for_update=True)
        if user_dto is None:
            raise Exception("no user")

        posts_data = [{"user_id":user_id, "text": f"post #{i} by {user_dto['name']}"} for i in range(posts_count)]

        result = await self.repo.create_posts(posts_data)
        return result

class GetPosts(UseCase):
    async def execute(self, offset = None, limit = None, mode = "offset"):
        result = []
        if mode == "offset":
            result:list[dict] = await self.repo.get_posts(offset, limit)
        elif mode == "cursor":
            result:list[dict] = await self.repo.get_posts_cursored(offset, limit)
        return result