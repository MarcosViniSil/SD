from  src.db.connection import ConnectionDB
from src.models import Interaction

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

    def getAllRooms(self) -> list:
        self.Db.createConnection()
        sql = """
            SELECT roomName,id FROM Room 
          """
        self.Db.myCursor.execute(sql)
        row = self.Db.myCursor.fetchall()  
        self.Db.closeConnection()

        return row

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
    
    def isRoomExists(self, roomId: int) -> bool:
        self.Db.createConnection()
        sql = """
            SELECT EXISTS(SELECT 1 FROM Room WHERE id = %s)
        """
        self.Db.myCursor.execute(sql, (roomId,))
        row = self.Db.myCursor.fetchone()  
        
        self.Db.closeConnection()
        return row[0] > 0
    
    
    def isIdemKeyAlreadyExists(self, idemKey: str) -> bool:
        self.Db.createConnection()
        sql = """
            SELECT EXISTS(SELECT 1 FROM Interaction WHERE idemKey = %s)
        """
        self.Db.myCursor.execute(sql, (idemKey,))
        row = self.Db.myCursor.fetchone()  
        self.Db.closeConnection()
        return row[0] > 0
    
    def getNickNameId(self,nickName:str) -> int:
        self.Db.createConnection()
        sql = """
            SELECT id FROM NickName WHERE nickName = %s
        """
        self.Db.myCursor.execute(sql, (nickName,))
        row = self.Db.myCursor.fetchone()  
        
        self.Db.closeConnection()
        if row is None:
            return -1
        return row[0]
    
        
    def createInteraction(self,interaction : Interaction,nickNameId:int,roomId:int,timesTampServer:int) -> int:
        self.Db.createConnection()
        sql = """
            INSERT INTO Interaction (nickNameId,roomId,idemKey,messageInteraction,timestamp_client,timestamp_server)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.Db.myCursor.execute(sql, (nickNameId,roomId,interaction.idemKey,interaction.message,
                                       interaction.timestampClient,timesTampServer))
        self.Db.myDb.commit()
        self.Db.closeConnection()

