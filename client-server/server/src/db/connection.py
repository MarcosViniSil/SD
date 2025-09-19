import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os

class ConnectionDB:

    def __init__(self):
        self.HOST_DATABASE     = os.environ["HOST_DATABASE"] 
        self.PORT_DATABASE     = os.environ["PORT_DATABASE"]
        self.USER_DATABASE     = os.environ["USER_DATABASE"]
        self.PASSWORD_DATABASE = os.environ["PASSWORD_DATABASE"]
        self.NAME_DATABASE     = os.environ["NAME_DATABASE"]
        self.myCursor = None
        self.myDb = None

    def createConnection(self) -> None:
        try:
            self.myDb = mysql.connector.connect(host=self.HOST_DATABASE,port=self.PORT_DATABASE,user=self.USER_DATABASE,password=self.PASSWORD_DATABASE,database=self.NAME_DATABASE,connection_timeout=2)
            self.myCursor = self.myDb.cursor()
        except Exception as e:
            raise
    
    def closeConnection(self) -> None:
        if self.myCursor:
            self.myCursor.close()
        if self.myDb:
            self.myDb.close()


if __name__ == "__main__":
    connection = ConnectionDB()
    connection.createConnection()
    print("Conexão com o banco de dados estabelecida com sucesso!")
    connection.closeConnection()