


from app.domain.entities.User import User
from app.infrastructure.db.UsersRepository import UserRepository


class CreateUser:
    def __init__(self,repository : UserRepository):
        self.repository = repository

    def execute(self,user:User):
        self.repository.guardar(user)