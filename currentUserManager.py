from flask import *
from flask_socketio import *


class CurrentUserManager:
    def __init__(self):
        self.currentUsers = []

    def addUserDetails(self, username, sessionid):
        self.currentUsers.append((username, sessionid))

    def getSessionid(self, username):
        for userDetails in self.currentUsers:
            if userDetails[0] == username:
                return userDetails[1]
        return None

    def removeUser(self, username):
        idx = -1
        for i in range(len(self.currentUsers)):
            if self.currentUsers[i][0] == username:
                idx = i
                break
        if idx > -1:
            self.currentUsers.pop(idx)

