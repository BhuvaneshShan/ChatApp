import MySQLdb
import sys

db = None
cur = None

try:
    db = MySQLdb.connect(host="chatdb.cgurr1edtxag.us-west-2.rds.amazonaws.com",
                              user="bhuvanesh",
                              passwd="bhuvanesh",
                              port=3306,
                              db="chatdb")
    cur = db.cursor()
    print 'CONNECTION ESTABLISHED!'
except:
    print 'Execption caught:', sys.exc_info()[0], sys.exc_info()[1]


def recordExists(table, field, value):
    numrows = 0
    try:
        numrows = cur.execute(
            'SELECT * FROM ' + table + ' WHERE ' + field + ' = ' + value)
    except:
        print 'Execution error'
    if numrows == 0:
        return False
    else:
        return True


def insertNewUser(username):
    try:
        cur.execute("INSERT INTO user (name) VALUES ('" + username + "')")
        print 'user inserted successfully'
    except:
        print 'Insertion error'


def userExists(username):
    numrows = 0
    try:
        numrows = cur.execute(
            "SELECT * FROM user WHERE name = '" + username + "'")
    except:
        print 'Execution error'
    if numrows == 0:
        return False
    else:
        return True


def chatRoomExists(roomname):
    numrows = 0
    try:
        numrows = cur.execute(
            "SELECT * FROM room WHERE name = '" + roomname + "'")
    except:
        print 'Execution error'
    if numrows == 0:
        return False
    else:
        return True


def insertNewChatRoom(roomname):
    try:
        cur.execute("INSERT INTO room (name) VALUES ('" + roomname + "')")
        print "new room inserted"
    except:
        print 'Insertion error'
