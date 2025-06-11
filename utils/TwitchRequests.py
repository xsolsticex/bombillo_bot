import os
import requests


class TwitchRequests:

    
    def code_to_token(self,code: str):
        params = {
            "client_id":os.environ["CLIENT_ID"],
            "client_secret":os.environ["CLIENT_SECRET"],
            "redirect_uri":os.environ["REDIRECT_URI"],
            "code":code,
            "grant_type":"authorization_code"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }
        response = requests.post(os.environ["GET_TOKEN_URL"],data=params,headers=headers)
        if response.status_code == 200:
            data = response.json()
            access_token = data["access_token"]
            refresh_token = data["refresh_token"]

            return {"access_token":access_token,"refresh_token":refresh_token}
        return None