

from app.domain.entities.User import User
from app.infrastructure.db.UsersRepository import UserRepository


class GetUser:
    def __init__(self,repository : UserRepository):
        self.repository = repository

    def execute(self,username:str):
        return self.repository.get_user_access_token(username)