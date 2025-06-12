import os
from flask import Blueprint,request,jsonify

from app.application.use_cases.CreateUser import CreateUser
from app.application.use_cases.GetBroadcasterTokens import GetBroadcasterTokens
from app.application.use_cases.GetUser import GetUser
from app.application.use_cases.UpdateUser import UpdateUser
from app.domain.entities.User import User
from app.infrastructure.db.UsersRepository import UserRepository



from utils.FileManager import FileManager
from utils.TwitchOAuth import TwitchTokenValidator
from utils.TwitchRequests import TwitchRequests


main = Blueprint("main",__name__)
tr = TwitchRequests()
oauth = TwitchTokenValidator()
rp = UserRepository()


@main.route("/confirm")
def get_token():

    auth_code = request.args.get("code")

    token = tr.code_to_token(auth_code)

    
    data : User = oauth.validate_token(token.get("access_token"))
    if data:
        data.set_refresh_token(token.get("refresh_token"))
        cu  = CreateUser(rp)
        gu = GetUser(rp)
        user_exist = gu.execute(data.username)
        if user_exist == None:
            cu.execute(data)
        return {"Status":"Success!"}
       
    else:
        return {"Status":"Failed!"}
    

@main.route("/token/<username>")
def send_token_client(username="erbocatalomo"):
    client_key = os.getenv("X-API-KEY")
    if client_key == request.headers.get("X-API-KEY"):
        gu = GetUser(rp)
        access_token,refresh_token = gu.execute(username)
        # data : dict = fm.read_file()
        # access_token = data.get("erbocatalomo")["access_token"]
        # refresh_token  = data.get("erbocatalomo")["refresh_token"]
        if not oauth.validate_token(access_token,refresh_token):
            print("Token is not valid")
            new_data = oauth.refresh_token(refresh_token)
            uu = UpdateUser(rp)
            access_token = new_data.get("access_token")
            refresh_token= new_data.get("refresh_token")
            uu.execute(username="erbocatalomo",access_token=access_token,refresh_token=refresh_token)
            print("Token updated")
        else:
            print("Token is valid")
        # access_token = data.get("erbocatalomo")["access_token"]
        # refresh_token  = data.get("erbocatalomo")["refresh_token"]
        # user_id  = data.get("erbocatalomo")["user_id"]
        # cursor.execute(f"INSERT INTO usuarios (user_id,nombre_usuario,access_token,refresh_token) VALUES ('{user_id}','erbocatalomo','{access_token}','{refresh_token}')")
        # db.close_connection()
        return {"access_token":access_token,"refresh_token":refresh_token}
    return {"status":"Abort"},401


@main.route("/info/<username>")
def send_info(username:str):
    bt = GetBroadcasterTokens(rp)
    client_key = os.getenv("X-API-KEY")
    if client_key == request.headers.get("X-API-KEY"):
        access_token,broadcaster_id = bt.execute(username=username)
        # data : dict = fm.read_file()

        return {"access_token":access_token,"broadcaster_id":broadcaster_id},200
    else:
        return {"Status":"No Authorized"},401

