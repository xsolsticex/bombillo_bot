import os


import requests
from utils.FileManager import FileManager


class TwitchTokenValidator:

    def __init__(self):
        self.fm = FileManager()
        self.request_timeout = 2
        self.document = {}
    def code_to_token(self,code: str):
        params = {
            "client_id":os.getenv("CLIENT_ID"),
            "client_secret":os.getenv("CLIENT_SECRET"),
            "redirect_uri":os.getenv("REDIRECT_URI"),
            "code":code,
            "grant_type":"authorization_code"
        }

        headers = {
            "User-Agent": os.getenv("AGENTS")
        }
        response = requests.post(os.getenv("GET_TOKEN_URL"),data=params,headers=headers)
        data = response.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        return {"access_token":access_token,"refresh_token":refresh_token}
    

    def validate_token(self,token:str,refresh_token:str):
        url = "https://id.twitch.tv/oauth2/validate"
        headers = {
            "User-Agent": os.getenv("AGENTS"),
            "Authorization": f"Bearer {token}"
        }
        print(token)
        response = requests.get(url,headers=headers)
        print(token)
        if response.status_code == 200:
            print("Entra")
            datos = response.json()
            login = datos.get("login")
            user_id = datos.get("user_id")
            if self.fm.file_exists():
                self.document = self.fm.read_file()
            self.document[login] = {"access_token":token,"refresh_token":refresh_token,"user_id":user_id}
            self.fm.write_file(self.document)
            return True
        print(response.json())
        return False
    
    def refresh_token(self,refresh_token:str):
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id":os.getenv("CLIENT_ID"),
            "client_secret":os.getenv("CLIENT_SECRET"),
            "redirect_uri":os.getenv("REDIRECT_URI"),
            "refresh_token":refresh_token,
            "grant_type":"refresh_token"
        }
        headers = {
            "User-Agent": os.getenv("AGENTS")
        }
        response = requests.post(url,params=params,headers=headers)
        if response.status_code == 200:
            data : dict = response.json()
            access_token  = data.get("access_token")
            refresh_token = data.get("refresh_token")
            self.validate_token(access_token,refresh_token)
            return {"access_token":data.get("access_token"),"refresh_token":data.get("refresh_token")}
        else:
            return {}
                