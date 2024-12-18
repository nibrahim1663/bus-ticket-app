# Database connection
import mysql.connector

def get_connection():
    return mysql.connector.connect(
       host="bus-system-mysql-server.mysql.database.azure.com",
        user="nawriz",
        password="Dina@1989",
        database="bus_system_DB",
        ssl_ca="C:\Users\Abo Danny\Desktop\DigiCertGlobalRootCA.crt.pem"
    )


