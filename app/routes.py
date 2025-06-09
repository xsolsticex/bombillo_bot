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
    if oauth.validate_token(token.get("access_token"),token.get("refresh_token")):
        #fm.write_file(token)
        return {"Status":"Success!"}
    else:
        return {"Status":"Failed!"}
    

@main.route("/token")
def send_token_client():
    client_key = os.getenv("X-API-KEY")
    if client_key == request.headers.get("X-API-KEY"):
        data : dict = fm.read_file()
        access_token = data.get("erbocatalomo")["access_token"]
        refresh_token  = data.get("erbocatalomo")["refresh_token"]
        if not oauth.validate_token(access_token,refresh_token):
            print("Token is not valid")
            oauth.refresh_token(refresh_token)
            #fm.write_file(data)
            print("Token updated")
            data : dict = fm.read_file()
            print("==================")
        else:
            print("Token is valid")
        return {"access_token":data.get("erbocatalomo")["access_token"],"refresh_token":data.get("erbocatalomo")["refresh_token"]}
    return {"status":"Abort"},401


@main.route("/info/<username>")
def send_info(username:str):
    client_key = os.getenv("X-API-KEY")
    if client_key == request.headers.get("X-API-KEY"):
        data : dict = fm.read_file()
        print(data[username])
        return data[username],200
    else:
        return {"Status":"No Authorized"},401

