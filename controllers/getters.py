from controllers.db_connection import DatabaseConnection
from datetime import datetime, timedelta

class Getters:
    def get_users():
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        
        # SFC (shop floor control) is operators, SFA (shop floor admin) should also have access?
        cursor.execute("""
            SELECT DISTINCT u.Usercode, e.[FullName] 
            FROM T_UserFunction U
            INNER JOIN UserRegistration UR ON U.UserCode = UR.UserCode
            INNER JOIN T_employee E on UR.EmpId = E.EmpId
            WHERE UserGrpCode = 'SFC' AND U.UserCode <> N'' AND U.ActiveInd = 1
        """)

        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append({"id":row[0].strip(), "description":row[1].strip()})

        cursor.close()
        cnxn.close()
        return result
    
    def get_part_certificate_lotnr(part):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        
        # SFC (shop floor control) is operators, SFA (shop floor admin) should also have access?
        cursor.execute("""
            SELECT  CASE
                        WHEN CertificateCode <> '' THEN CertificateCode
                        ELSE LotNr
                    END 'indentity'
            FROM T_Inventory WHERE PartCode = ?
        """, part)

        rows = cursor.fetchall()

        result = []

        for row in rows:
            if row[0].strip() != "":
                result.append({"id":row[0].strip(), "description":row[0].strip()})

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
        current_monday = (datetime.today() - timedelta(days=datetime.today().weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
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
            result.append({"id":row[0].strip(), "description":row[0].strip()})
        
        cursor.close()
        cnxn.close()
        return result
    
    def get_raw_materials(produced_part):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        cursor.execute("""
            SELECT BOM.SubPartCode, BOM.[Description]
            FROM T_Part P
            LEFT JOIN T_BillOfMat BOM ON P.PartCode = BOM.PartCode
            WHERE p.partcode = ?
                    """, (produced_part))
        rows = cursor.fetchall() 
        result = [] 

        for row in rows:
            result.append({"id":row[0].strip(), "description":row[0].strip()})
        
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
    
    def get_scrap_table(page, user_code):
        per_page = 10
        offset = (page - 1) * per_page
        current_monday = (datetime.today() - timedelta(days=datetime.today().weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        current_friday = current_monday + timedelta(days=4)
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        SQL = """
            SELECT  ST.*,
                    E.FullName,
                    MG.Description 'MachGrpDescription',
                    M.Description 'MachDescription',
                    P.Description 'ProducedPartDescription',
                    P2.Description 'RawMaterialDescription',
                    D.DefectType,
                    D.DefectCondition
            FROM ST_LEG_ScrapTally ST
            LEFT JOIN UserRegistration UR ON ST.Operator = UR.UserCode
            LEFT JOIN T_Employee E ON UR.EmpId = E.EmpId
            LEFT JOIN T_MachGrp MG ON ST.MachGrpCode = MG.MachGrpCode
            LEFT JOIN T_Mach M ON M.MachCode = ST.MachCode
            LEFT JOIN T_Part P ON ST.ProducedPart = P.PartCode
            LEFT JOIN T_Part P2 ON ST.RawMaterial = P2.PartCode
            LEFT JOIN ST_LEG_Defect D ON ST.DefectCode = D.DefectCode
            WHERE Date BETWEEN ? AND ?
                       """
        if user_code is not None:
            SQL += " AND ST.Operator = ?"
        SQL += " ORDER BY Date DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        if user_code is not None:
            cursor.execute(SQL, (current_monday, current_friday, user_code, offset, per_page + 1))
        else:
            cursor.execute(SQL, (current_monday, current_friday, offset, per_page + 1))
        items = cursor.fetchall()
        page = []
        for index, item in enumerate(items):
            if index != 10:
                item_dict = {
                    "scrapTally": 0,
                    "operator": {},
                    "process": {},
                    "machine": {},
                    "producedPart": {},
                    "rawMaterial": {},
                    "defectType": {},
                    "defectCondition": {},
                    "date": datetime.today().date(),
                    "qty": 0,
                    "comment": "",
                    "identity": "",
                    "processed": False
                }
                for column, value in zip(cursor.description, item):
                # Check if the value is a string and strip whitespace if it is
                    column_name = column[0]
                    if column_name == "ScrapTally":
                        item_dict["scrapTally"] = value
                    if column_name == "Operator":
                        item_dict["operator"]["id"] = value.strip()
                    elif column_name == "FullName":
                        item_dict["operator"]["description"] = value.strip()
                    elif column_name == "MachGrpCode":  
                        item_dict["process"]["id"] = value.strip()
                    elif column_name == "MachGrpDescription":  
                        item_dict["process"]["description"] = value.strip()
                    elif column_name == "MachCode":  
                        item_dict["machine"]["id"] = value.strip()
                    elif column_name == "MachDescription":  
                        item_dict["machine"]["description"] = value.strip()
                    elif column_name == "ProducedPart":  
                        item_dict["producedPart"]["id"] = value.strip()
                    elif column_name == "ProducedPartDescription":  
                        item_dict["producedPart"]["description"] = value.strip()
                    elif column_name == "RawMaterial":  
                        item_dict["rawMaterial"]["id"] = value.strip()
                    elif column_name == "RawMaterialDescription":  
                        item_dict["rawMaterial"]["description"] = value.strip()
                    elif column_name == "DefectType":  
                        item_dict["defectType"]["description"] = value.strip()
                    elif column_name == "DefectCondition": 
                        item_dict["defectCondition"]["description"] = value.strip()
                    elif column_name == "Date":  
                        item_dict["date"] = value.date()
                    elif column_name == "Qty":  
                        item_dict["qty"] = value
                    elif column_name == "Comment": 
                        item_dict["comment"] = value.strip()
                    elif column_name == "ProcessedInd": 
                        item_dict["processed"] = value
                    elif column_name == "LotNr" and value.strip() != "": 
                        item_dict["identity"] = value.strip()
                    elif column_name == "CertificateCode" and value.strip() != "": 
                        item_dict["identity"] = value.strip()
                page.append(item_dict)
        cursor.close()
        cnxn.close()
        if len(items) < 11:
            result = {
                "last_page": True,
                "page": page
            }
        else:
            result = {
                "last_page": False,
                "page": page
            }
        return result
    
    def get_last_upd_on(scrap_tally):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        query = "SELECT LastUpdatedOn FROM ST_LEG_ScrapTally WHERE ScrapTally = ?"
        cursor.execute(query, (scrap_tally))
        
        result = cursor.fetchone().LastUpdatedOn

        cursor.close()
        cnxn.close()

        return result