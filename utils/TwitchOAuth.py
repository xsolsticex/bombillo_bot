import asyncio
import os
import time
from urllib.parse import urlencode, urlparse, urlunparse
import webbrowser

import requests
from utils.FileManager import FileManager


class TwitchTokenValidator:

    def __init__(self):
        self.fm = FileManager()
        self.request_timeout = 2
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
    

    def validate_token(self,token:str):
        url = "https://id.twitch.tv/oauth2/validate"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return True
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }
        response = requests.post(url,params=params,headers=headers)
        if response.status_code == 200:
            data : dict = response.json()
            return {"access_token":data.get("access_token"),"refresh_token":data.get("refresh_token")}
        else:
            return {}
                