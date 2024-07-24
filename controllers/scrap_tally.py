from controllers.db_connection import DatabaseConnection
from controllers.getters import Getters
from datetime import datetime, timedelta

class ScrapTally:
    def postScrap(payload, defect):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        cursor.execute("""
            EXEC SIP_ins_LEG_ScrapTally ?, ?, ?, ?, ?, ?, ?, ?, 0, ?
                       """, (datetime.today().date(), payload.get('machCode'), str(payload.get('partCode')), payload.get('machGrpCode'), payload.get('fullSheetInd'), payload.get('qty'), defect, payload.get('comment'), payload.get('user')))
        cursor.commit()
        cursor.close()
        cnxn.close()

    def updateScrap(payload):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        cursor.execute("""
            EXEC SIP_upd_LEG_ScrapTally ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                       """, (
                           payload.get('ScrapTally'),
                           payload.get('LastUpdatedOn'),
                           datetime.today().date(),
                           payload.get('MachCode'),
                           str(payload.get('PartCode')),
                           payload.get('MachGrpCode'),
                           payload.get('FullSheetInd'),
                           payload.get('Qty'),
                           payload.get('DefectCode'),
                           payload.get('Comment'),
                           0,
                           payload.get('LastUpdatedOn'),
                           payload.get('User')
                       )
        )

        cursor.commit()
        cursor.close()
        cnxn.close()