from controllers.db_connection import DatabaseConnection

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
    
    def get_processes():
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()

        cursor.execute("""SELECT MachGrpCode FROM T_MachGrp WHERE MachGrpCode <> N'' AND MachGrpCode NOT IN (
                       'EXDC', 
                       'EXEC', 
                       'EXPC', 
                       'EXTR', 
                       'EXZC', 
                       'MBM', 
                       'MBPM', 
                       'MLCM', 
                       'MSM', 
                       'MWM', 
                       'PACK', 
                       'PPAP', 
                       'SAW')""")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0].strip())

        cursor.close()
        cnxn.close()
        return result
    
    def get_machines(process):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()

        query = """SELECT Description from T_Mach WHERE MachGrpCode = ? AND MachGrpCode <> N'' AND Description NOT IN (
        'Boxing MINN', 
        'External e-Cote', 
        'External Power Code', 
        'External Zinc Coating', 
        'DO NOT USE', 
        'Knife MINN 1', 
        'Knife - Peter Wall (Norwich)', 
        'Metal Bending Machine 1', 
        'Metal Brake Press MAchine', 
        'Metal Laser Cutter Machine', 
        'Metal Saw Machine 1', 
        'Metal Welding Machine 1', 
        'Chop Saw',  
        'Tenoner MINN')"""
        
        cursor.execute(query, (process,))
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0].strip())
        
        cursor.close()
        cnxn.close()
        return result