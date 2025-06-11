

from app.domain.entities.User import User
from app.infrastructure.db.UsersRepository import UserRepository


class UpdateUser:
    def __init__(self,repository : UserRepository):
        self.repository = repository

    def execute(self,username:str,access_token:str,refresh_token:str):
        return self.repository.update_user(username,access_token,refresh_token)