import MySQLdb


def createDB():
    '''
    try:
        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root")
        cur = db.cursor()
        cur.execute("CREATE DATABASE chatDB")
    except:
        pass
    '''
    # create table for user
    db = MySQLdb.connect(host="chatdb.cgurr1edtxag.us-west-2.rds.amazonaws.com",
                              user="bhuvanesh",
                              passwd="bhuvanesh",
                              port=3306,
                              db="chatdb")
    cur = db.cursor()
    try:
        cur.execute(
            "CREATE TABLE user(id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, name TEXT NOT NULL)")
    except:
        print "user table creation error"
    try:
        cur.execute(
            "CREATE TABLE room(id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, name TEXT NOT NULL)")
    except:
        print "room table creation error"


if __name__ == '__main__':
    createDB()
