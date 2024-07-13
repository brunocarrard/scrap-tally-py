from controllers.db_connection import DatabaseConnection

class Getters:
    def get_users():
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        
        # SFC (shop floor control) is operators, SFA (shop floor admin) should also have access?
        cursor.execute("""SELECT DISTINCT u.Usercode, e.[FullName] 
                       FROM T_UserFunction U INNER JOIN T_employee E on U.UserCode = E.EmpId 
                       WHERE UserGrpCode IN ('SFC', 'SFA') AND UserCode <> N''""")

        # cursor.execute("SELECT UserCode, UserGrpCode FROM T_UserFunction WHERE UserGrpCode IN ('SFC', 'SFA') AND UserCode <> N''")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append({"id":row[0].strip(), "description":row[1].strip()})

        cursor.close()
        cnxn.close()
        return result
    
    def get_processes():
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()

        cursor.execute("""SELECT MachGrpCode, Description FROM T_MachGrp WHERE MachGrpCode <> N'' AND Description NOT IN (
                       'External Diecutting', 
                       'External e-Cote', 
                       'External Power Cote', 
                       'External Machining', 
                       'External Zinc Coating', 
                       'Metal Bending Machine', 
                       'Metal Brake Press Machine', 
                       'Metal Laser Cutter Machine', 
                       'Metal Saw Machine', 
                       'Metal Welding Machine', 
                       'DO NOT USE', 
                       'Chop Saw')""")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append({"id":row[0].strip(), "description":row[1].strip()})

        cursor.close()
        cnxn.close()
        return result
    
    def get_machines(process):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()

        query = """SELECT MachCode, Description from T_Mach WHERE MachGrpCode = ? AND MachGrpCode <> N'' AND Description NOT IN (
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
            result.append({"id":row[0].strip(), "description":row[1].strip()})
        
        cursor.close()
        cnxn.close()
        return result
    
    def get_defect_types(): 
        cnxn = DatabaseConnection.get_db_connection() 
        cursor = cnxn.cursor() 
        cursor.execute("SELECT DISTINCT DefectType FROM ST_LEG_Defect WHERE DefectType <> N''")

        rows = cursor.fetchall() 
        result = [] 

        for row in rows: 
            result.append(row[0].strip()) 
        
        cursor.close()
        cnxn.close()
        return result
    
    def get_defect_conditions(defect_type): 
        cnxn = DatabaseConnection.get_db_connection() 
        cursor = cnxn.cursor() 
        query = "SELECT DefectCode, DefectCondition from ST_LEG_Defect WHERE DefectType = ? AND DefectType <> N''"
    
        cursor.execute(query, (defect_type,)) 
        rows = cursor.fetchall() 

        result = [] 

        for row in rows: 
            result.append({"id":row[0].strip(), "description":row[1].strip()}) 
            
        cursor.close() 
        cnxn.close() 
        return result