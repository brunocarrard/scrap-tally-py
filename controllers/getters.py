from controllers.db_connection import DatabaseConnection
import pyodbc

class Getters:
    def get_users():
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        
        # SFC (shop floor control) is operators, SFA (shop floor admin) should also have access?
        cursor.execute("SELECT UserCode, UserGrpCode FROM T_UserFunction WHERE UserGrpCode IN ('SFC', 'SFA') AND UserCode <> N''")
        rows = cursor.fetchall()

        results_dict = {}

        for row in rows:
            user_code = row[0].strip()
            user_group_code = row[1].strip()

            if user_code not in results_dict:
                results_dict[user_code] = []

            results_dict[user_code].append(user_group_code)

        cursor.close()
        cnxn.close()
        return results_dict