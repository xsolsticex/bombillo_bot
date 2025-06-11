class User:
    def __init__(self,id,username,access_token,refresh_token):
        self.id = id
        self.username = username
        self.access_token = access_token
        self.refresh_token = refresh_token

    ## GETTERS

    def get_user_id(self):
        return self.id
    
    def get_username(self):
        return self.username
    
    def get_access_token(self):
        return self.access_token
    
    def get_refresh_token(self):
        return self.refresh_token
    

    # SETTERS
    def set_access_token(self,access_token):
        self.access_token = access_token
    
    def set_refresh_token(self,refresh_token):
        self.refresh_token = refresh_token

        