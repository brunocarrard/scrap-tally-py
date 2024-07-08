from controllers.db_connection import DatabaseConnection
import pyodbc

class Getters:
    def get_users():
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        
        # SFC (shop floor control) is operators, SFA (shop floor admin) should also have access?
        cursor.execute("SELECT UserCode, UserGrpCode FROM T_UserFunction WHERE UserGrpCode IN ('SFC', 'SFA') AND UserCode <> N''")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0].strip())

        cursor.close()
        cnxn.close()
        return result