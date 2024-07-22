from controllers.db_connection import DatabaseConnection
from datetime import datetime, timedelta

class Getters:
    def get_users():
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        
        # SFC (shop floor control) is operators, SFA (shop floor admin) should also have access?
        cursor.execute("""SELECT DISTINCT u.Usercode, e.[FullName] 
                       FROM T_UserFunction U INNER JOIN T_employee E on U.UserCode = E.EmpId 
                       WHERE UserGrpCode IN ('SFC', 'SFA') AND UserCode <> N''""")

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

        # All processes have each defect type so there is no need to get them by process
        cursor.execute("SELECT DISTINCT DefectType FROM ST_LEG_Defect WHERE DefectType <> N''")

        rows = cursor.fetchall() 
        result = [] 

        for row in rows: 
            result.append(row[0].strip()) 
        
        cursor.close()
        cnxn.close()
        return result
    
    def get_defect_conditions(process, defect_type): 
        # Filter by both process (MachGrpCode from T_Mach) and defect type
        process_defect_codes = {
            "ROUT": ["DEL", "DSU", "DIS", "TIC", "MSH", "PIT", "SCR", "SCRS", "2LG", "2SH", "OFL", "WMU", "HOL", "WRP", "DDC", "MOV", "NSQ", "CWS", "RHL", "SMD", "DCT", "PCT", "MIA", "TLD", "IRT", "BSD"],
            "KNIF": ["DEL", "DSU", "DIS", "TIC", "MSH", "PIT", "SCR", "SCRS", "2LG", "2SH", "OFL", "WMU", "HOL", "WRP", "DDC", "MOV", "NSQ", "CWS", "RHL", "SMD", "DCT", "PCT", "MIA", "TLD", "IRT", "BSD"],
            "TENR": ["DEL", "DSU", "DIS", "FRE", "TIC", "MSH", "PIT", "SCR", "SCRS", "2LG", "2SH", "OFL", "WMU", "HOL", "WRP", "DDC", "MOV", "NSQ", "CWS", "RHL", "SMD", "DCT", "PCT", "MIA", "TLD", "IRT", "BSD"],
            "BOX": ["DEL", "DSU", "FRE", "TIC", "MSH", "PIT", "SCR", "SCRS", "2LG", "2SH", "OFL", "WMU", "HOL", "WRP", "DDC", "CWS", "SMD", "MIA", "TLD", "IRT"],
            "ASSY": ["MSH", "SCR", "SCRS", "2LG", "2SH", "OFL", "WMU", "HOL", "WRP", "DDC", "MOV", "NSQ", "CWS", "SMD"],
            "KIT": ["MSH", "SCR", "SCRS", "2LG", "2SH", "OFL", "WMU", "HOL", "WRP", "DDC", "MOV", "NSQ", "CWS", "SMD"],
            "BRUN": ["SCR", "SCRS", "2LG", "2SH", "OFL", "WMU", "HOL", "WRP", "DDC", "MOV", "NSQ", "CWS", "SMD"],
            "DIEC": ["SCR", "SCRS", "2LG", "2SH", "OFL", "WMU", "HOL", "WRP", "DDC", "MOV", "NSQ", "CWS", "SMD"],
            "WJET": ["MSH", "SCR", "SCRS", "2LG", "2SH", "OFL", "WMU", "HOL", "WRP", "DDC", "MOV", "NSQ", "CWS", "SMD"],
            "RUBB": ["WRP", "DDC", "MOV", "NSQ", "RHD", "SMD", "DCT", "PCT", "MIA", "TLD", "IRT", "BSD"],
            "PU": ["DEL", "DSU", "WRP", "DDC", "RHL", "RHD", "SMD", "TLD", "IRT"]
        }

        cnxn = DatabaseConnection.get_db_connection() 
        cursor = cnxn.cursor() 
        query = "SELECT DefectCode, DefectCondition from ST_LEG_Defect WHERE DefectType = ? AND DefectType <> N''"
    
        cursor.execute(query, (defect_type,)) 
        rows = cursor.fetchall() 

        result = [] 

        for row in rows:
            if row[0].strip() in process_defect_codes[process]:
                result.append({"id":row[0].strip(), "description":row[1].strip()})
            
        cursor.close() 
        cnxn.close() 
        return result
    

    def get_parts(process):
        current_monday = datetime.today() - timedelta(days=datetime.today().weekday())
        current_friday = current_monday + timedelta(days=4)

        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        cursor.execute("""
            SELECT DISTINCT P.PartCode, P.Description
            FROM T_ProdBillOfOper BOO
            INNER JOIN T_ProductionHeader PH ON BOO.ProdHeaderDossierCode = PH.ProdHeaderDossierCode
            INNER JOIN T_Part P ON P.PartCode = PH.PartCode
            WHERE BOO.StartDate BETWEEN ? AND ?
                AND BOO.MachGrpCode = ?
                       """, (current_monday, current_friday, process))
        rows = cursor.fetchall() 
        result = [] 

        for row in rows:
            result.append({"id":row[0].strip(), "description":row[1].strip()})
        
        cursor.close()
        cnxn.close()
        return result
    
    def get_part_type(part):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()

        query = """SELECT DISTINCT T_Part.SalesPartGrpCode, T_SalesPartGrp.Description FROM T_Part 
        INNER JOIN T_SalesPartGrp ON T_Part.SalesPartGrpCode = T_SalesPartGrp.SalesPartGrpCode
        WHERE T_Part.PartCode = ?"""
    
        cursor.execute(query, part)
        row = cursor.fetchone()

        result = [{"id":row[0].strip(), "description":row[1].strip()}]

        return result
    
    def get_defect(type, condition):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        cursor.execute("""
            SELECT DefectCode FROM ST_LEG_Defect WHERE DefectType = ? AND DefectCondition = ?
                       """, (type, condition))
        result = cursor.fetchone()[0].strip()
        cursor.close()
        cnxn.close()

        return result