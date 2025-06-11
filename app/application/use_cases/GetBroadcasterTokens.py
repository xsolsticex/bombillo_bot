
from app.domain.entities.User import User
from app.infrastructure.db.UsersRepository import UserRepository


class GetBroadcasterTokens:
    def __init__(self,repository : UserRepository):
        self.repository = repository

    def execute(self,username:str):
        return self.repository.get_broadcaster_tokens(username)