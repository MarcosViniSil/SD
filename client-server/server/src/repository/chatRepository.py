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

    def isNameAlreadyTaken(self, nickName: str) -> bool:
        self.Db.createConnection()
        sql = """
            SELECT id FROM NickName WHERE nickName = %s LIMIT 1
        """
        self.Db.myCursor.execute(sql, (nickName,))
        row = self.Db.myCursor.fetchone()  
        
        self.Db.closeConnection()

        return row is not None

