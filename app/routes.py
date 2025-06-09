import os
from flask import Blueprint,request,jsonify

from utils.FileManager import FileManager
from utils.TwitchOAuth import TwitchTokenValidator
from utils.TwitchRequests import TwitchRequests


main = Blueprint("main",__name__)
fm = FileManager()
tr = TwitchRequests()
oauth = TwitchTokenValidator()

@main.route("/confirm")
def get_token():
    
    auth_code = request.args.get("code")
    token = tr.code_to_token(auth_code)
    if token:
        fm.write_file(token)
        return {"Status":"Success!"}
    else:
        return {"Status":"Failed!"}
    

@main.route("/token")
def send_token_client():
    client_key = os.getenv("X-API-KEY")
    if client_key == request.headers.get("X-API-KEY"):
        data : dict = fm.read_file()
        access_token = data.get("access_token")
        refresh_token  = data.get("refresh_token")
        if not oauth.validate_token(access_token):
            print("Token is not valid")
            data = oauth.refresh_token(refresh_token)
            fm.write_file(data)
            print("Token updated")
        return data
    return {"status":"Abort"},401
