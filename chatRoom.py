from database import *


class ChatRoom:
    def __init__(self, roomName):
        self.name = roomName
        self.activeUsers = []
        pass

    def addUser(self, name):
        self.activeUsers.append(name)

    def getName(self):
        return self.name

    def getUserCount(self):
        return len(self.activeUsers)

    def removeUser(self, name):
        if name in self.activeUsers:
            self.activeUsers.remove(name)

    def getActiveUsers(self):
        return self.activeUsers


class ChatRoomManager:
    def __init__(self):
        self.activeRooms = []
        pass

    def getActiveChatRoomNames(self):
        roomNames = []
        for room in self.activeRooms:
            roomNames.append(room.getName())
        return roomNames

    def getActiveRoomAndUserCount(self):
        try:
            result = []
            for room in self.activeRooms:
                result.append((room.getName(), room.getUserCount()))
            return result
        except:
            print "Append error"

    def addRoomWithUser(self, roomName, userName):
        try:
            if chatRoomExists(roomName):
                if roomName not in [room.name for room in self.activeRooms]:
                    self.activeRooms.append(ChatRoom(roomName))
            else:
                insertNewChatRoom(roomName)
                self.activeRooms.append(ChatRoom(roomName))
            idx = self.getActiveRoomIdx(roomName)
            
            if idx is not None:
                self.activeRooms[idx].addUser(userName)
            else:
                print "Roomname not found in the active room list"
        except:
            print "Error in adding room"

    def getUsers(self, roomName):
        try:
            idx = self.getActiveRoomIdx(roomName)
            if idx is not None:
                return self.activeRooms[idx].getActiveUsers()
            else:
                print "Roomname not found in the active room list"
        except:
            print "RoomName not found!"

    def getActiveRoomIdx(self, roomName):
        for idx in range(len(self.activeRooms)):
            if self.activeRooms[idx].getName() == roomName:
                return idx
        return None

    def removeUserFromRoom(self, roomName, userName):
        try:
            idx = self.getActiveRoomIdx(roomName)
            if idx is not None:
                self.activeRooms[idx].removeUser(userName)
                if self.activeRooms[idx].getUserCount() == 0:
                    self.activeRooms.pop(idx)
        except:
            print "User removal error"
