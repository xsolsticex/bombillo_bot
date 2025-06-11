import os
import psycopg2

from app.domain.entities.User import User
from dotenv import load_dotenv


class UserRepository:

    def __init__(self):
        load_dotenv()
        self.host = os.getenv("HOST")
        self.conn = psycopg2.connect(self.host)
        self.cursor = self.conn.cursor()

    def guardar(self,usuario : User):
        with self.conn:
            statement = f"INSERT INTO usuarios (user_id,nombre_usuario,access_token,refresh_token) VALUES ('{usuario.id}','{usuario.username}','{usuario.access_token}','{usuario.refresh_token}')"
            cursor = self.conn.cursor()
            cursor.execute(statement)

    def get_user_by_id(self,id:int):
        with self.conn:
            statement = f"SELECT * FROM usuarios WHERE user_id = {id}"
            cursor = self.conn.cursor()
            cursor.execute(statement)
            data = cursor.fetchone()
            return data
        return None

    def get_user_access_token(self,username:str="erbocatalomo"):
        with self.conn:
            statement = f"SELECT * FROM usuarios WHERE nombre_usuario = '{username}'"
            cursor = self.conn.cursor()
            cursor.execute(statement)
            data = cursor.fetchone()
            _,_,token,refresh_token = data
            return [token,refresh_token]
        return None
    
    def get_broadcaster_tokens(self,username:str="erbocatalomo"):
        with self.conn:
            statement = f"SELECT * FROM usuarios WHERE nombre_usuario = '{username}'"
            cursor = self.conn.cursor()
            cursor.execute(statement)
            data = cursor.fetchone()
            broadcaster_id,_,token,_ = data
            return [token,broadcaster_id]
        return None
    

    
    def update_user(self,username:str,access_token:str,refresh_token:str):
        with self.conn:
            statement = f"UPDATE usuarios SET access_token = '{access_token}', refresh_token = '{refresh_token}' WHERE nombre_usuario = '{username}'"
            cursor = self.conn.cursor()
            cursor.execute(statement)
            return True
        return False