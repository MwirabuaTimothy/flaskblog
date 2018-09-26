########################
#### helper methods ####
########################
 
def register(self, username, email, password, confirm):
    return self.app.post(
        '/register',
        data=dict(username=username, email=email, password=password, confirm=confirm),
        follow_redirects=True
    )
 
def login(self, email, password):
    return self.app.post(
        '/login',
        data=dict(email=email, password=password),
        follow_redirects=True
    )
 
def logout(self):
    return self.app.get(
        '/logout',
        follow_redirects=True
    )