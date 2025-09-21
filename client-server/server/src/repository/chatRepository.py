from  src.db.connection import ConnectionDB

class ChatRepository:

    def __init__(self,db:ConnectionDB):
        self.Db = db

    def firstConnection():
        pass    

    def insertNickName(self, nickName: str) -> None:
        
        self.Db.createConnection()
        sql = """
            INSERT INTO NickName (nickName) VALUES (%s)
          """
        self.Db.myCursor.execute(sql, (nickName,))
        self.Db.myDb.commit()
        self.Db.closeConnection()

    def insertRoomName(self, roomName: str) -> None:
        
        self.Db.createConnection()
        sql = """
            INSERT INTO Room (roomName) VALUES (%s)
          """
        self.Db.myCursor.execute(sql, (roomName,))
        self.Db.myDb.commit()
        self.Db.closeConnection()

    def isNameAlreadyTaken(self, nickName: str) -> bool:
        self.Db.createConnection()
        sql = """
           SELECT EXISTS(SELECT 1 FROM NickName WHERE nickName = %s)
        """
        self.Db.myCursor.execute(sql, (nickName,))
        row = self.Db.myCursor.fetchone()  
        
        self.Db.closeConnection()
        return row[0] > 0
    
    def isRoomNameAlreadyTaken(self, roomName: str) -> bool:
        self.Db.createConnection()
        sql = """
            SELECT EXISTS(SELECT 1 FROM Room WHERE roomName = %s)
        """
        self.Db.myCursor.execute(sql, (roomName,))
        row = self.Db.myCursor.fetchone()  
        
        self.Db.closeConnection()

        return row[0] > 0

