from flask import *
from flask_socketio import *
from enum import Enum, unique
from database import *
from chatRoom import *
from currentUserManager import *

'''
To identify type of message
'''
@unique
class MsgType(Enum):
    ROOMS = 1
    JOIN = 2
    LEAVE = 3
    QUIT = 4
    PRIVATE = 5
    BROADCAST = 6
    NONE = 7

'''
Class that handles the incoming message
'''
class MessageProcessor:
    def __init__(self):
        self.chatRoomMgr = ChatRoomManager()
        self.curUserMgr = CurrentUserManager()

    '''
    Function to be called for server to respond to users message
    '''
    def processMessage(self, message):
        if 'username' in session:
            msgType = self.parse(message['data'])
            if msgType == MsgType.ROOMS:
                self.sendActiveRoomList()
            elif msgType == MsgType.JOIN:
                self.addUserToRoom(message['data'])
            elif msgType == MsgType.LEAVE:
                self.removeUserFromRoom()
            elif msgType == MsgType.QUIT:
                self.disconnect()
            elif msgType == MsgType.PRIVATE:
                self.sendPrivateMessage(session['username'], message['data'])
            elif msgType == MsgType.BROADCAST:
                self.sendToAll(session['username'], message['data'])
            else:
                if session['chatroom'] != "":
                    self.sendToRoom(
                        session['username'], session['chatroom'], message['data'])
                else:
                    # Broadcast message
                    self.sendToAll(session['username'], message['data'])
        else:
            self.addUser(message['data'])

    '''
    Function to identify message type
    '''
    def parse(self, message):
        message = message.strip(' \t\n\r')
        if message.startswith('/rooms'):
            return MsgType.ROOMS
        elif message.startswith('/join'):
            return MsgType.JOIN
        elif message.startswith('/leave'):
            return MsgType.LEAVE
        elif message.startswith('/quit'):
            return MsgType.QUIT
        elif message.startswith('/private'):
            return MsgType.PRIVATE
        elif message.startswith('/broadcast'):
            return MsgType.BROADCAST
        else:
            return MsgType.NONE

    '''
    Function to handle user's name
    and insert into db if not already present
    '''
    def addUser(self, message):
        username = message.strip(' \t\r\n')
        username = username.split(' ', 1)[0]
        if len(username) > 0:
            if userExists(username):
                self.sendMessage('Server', 'Sorry, Name taken! Login name?')
                # Implement login with password for old uses in future
            else:
                insertNewUser(username)
                session['username'] = username
                session['chatroom'] = ""
                self.curUserMgr.addUserDetails(username, request.sid)
                self.sendMessage('Server', 'Welcome ' + session['username'])
        else:
            self.sendMessage('Server', 'Enter valid username without space!')

    '''
    Function to send to the web client of the user alone
    '''
    def sendMessage(self, sender, message):
        emit('messageToUser', {'clientName': sender, 'data': message})

    '''
    Function to send private messages
    '''
    def sendPrivateMessage(self, sender, messageWithRecipient):
        try:
            messageWithRecipient = messageWithRecipient[len('/private'):]
            recipient = messageWithRecipient.strip(' ')
            recipient = recipient.split(' ', 1)[0]
            recipient = recipient.strip('@')
            print 'Recipient:', recipient
            recipientSessionId = self.curUserMgr.getSessionid(recipient)
            if recipientSessionId is not None:
                print 'Sending msg to', recipient
                emit('messageToUser', {
                     'clientName': sender, 'data': messageWithRecipient}, room=recipientSessionId)
            else:
                sendMessage(
                    'Server', 'User ' + recipient + ' is offline or hasnt joined chat!')
        except:
            print 'Error in sending private message!'

    '''
    Function to send message to particular chatroom
    '''
    def sendToRoom(self, sender, chatroom, message):
        emit(
            'messageToUser', {'clientName': sender, 'data': message}, room=chatroom)

    '''
    Function to send broadcast message to all online users
    '''
    def sendToAll(self, sender, message):
        if message.startswith('/broadcast'):
            message = message[len('/broadcast'):]
        emit(
            'messageToUser', {'clientName': sender, 'data': message}, broadcast=True)

    '''
    Function to serve the user with active chat room names and user count
    '''
    def sendActiveRoomList(self):
        try:
            rooms = self.chatRoomMgr.getActiveRoomAndUserCount()
            if len(rooms) == 0:
                self.sendMessage(
                    'Server', 'No active chat room available. Create one using: /join <roomname>')
            else:
                self.sendMessage('Server', 'List of Active Chat Rooms')

                for room in rooms:
                    self.sendMessage(
                        'Server', ' # ' + room[0] + '(' + str(room[1]) + ')')

                self.sendMessage('Server', 'End of list')
        except:
            print 'Room list Retrieval error'

    '''
    Function to add user to a chat room
    '''
    def addUserToRoom(self, message):
        try:
            message = message.strip(' \t\n\r')
            if (' ' in message) is True:
                msgtype, roomName = message.split(' ')
                if roomName != "":
                    if session['chatroom'] == "" or session['chatroom'] is None:

                        self.chatRoomMgr.addRoomWithUser(
                            roomName, session['username'])

                        session['chatroom'] = roomName
                        join_room(session['chatroom'])

                        self.sendMessage(
                            'Server', 'Entering room: ' + roomName)

                        users = self.chatRoomMgr.getUsers(roomName)
                        for user in users:
                            name = user
                            if user is session['username']:
                                name += ' (**this is you)'
                            self.sendMessage('Server', ' # ' + name)

                        self.sendMessage('Server', 'End of list')
                        self.sendToRoom('Server', session[
                                        'chatroom'], 'User ' + session['username'] + ' has joined the chatroom!')
                    else:
                        if session['chatroom'] == roomName:
                            self.sendMessage(
                                'Server', 'You have already joined the room ' + roomName)
                        else:
                            self.sendMessage(
                                'Server', 'Leave current chat room before joining another!')
                else:
                    self.sendMessage('Server', 'Enter a room name!')
            else:
                self.sendMessage('Server', 'Enter a room name with a space')
        except:
            print 'User addition to room error'

    '''
    Function to remove user from a chat room
    '''
    def removeUserFromRoom(self):
        try:
            if session['chatroom'] != "":
                self.chatRoomMgr.removeUserFromRoom(
                    session['chatroom'], session['username'])

                self.sendMessage('Server', 'You left the chat room!')

                leave_room(session['chatroom'])

                self.sendToRoom('Server', session['chatroom'], 'User ' + session['username'] + ' has left the room!')

                session['chatroom'] = ""
            else:
                self.sendMessage(
                    'Server', 'Ah Ah... Play by the game! Join a room first before trying to leave!')
        except:
            print 'User removal error!'

    '''
    Function to disconnect user
    '''
    def disconnect(self):
        try:
            if session['chatroom'] != "":
                self.removeUserFromRoom()
            self.sendMessage('Server', 'Bye! See you soon!')
            self.curUserMgr.removeUser(session['username'])
            session.clear()
            disconnect()
        except:
            print 'Disconnection error'
