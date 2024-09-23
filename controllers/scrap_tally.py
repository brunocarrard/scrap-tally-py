from controllers.db_connection import DatabaseConnection
from controllers.getters import Getters
from datetime import datetime, timedelta

class ScrapTally:
    def postScrap(payload, defect):
        if payload.get('identity'):
            if payload.get('identity').startswith('LF'):
                lot_nr = payload.get('identity')
                certificate_code = ""
            else:
                lot_nr = ""
                certificate_code = payload.get('identity')
        else:
            lot_nr = ""
            certificate_code = ""
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        cursor.execute("""
            EXEC SIP_ins_LEG_ScrapTally ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?
                       """, (datetime.today().date(), payload.get('user'), payload.get('machCode'), str(payload.get('producedPart')), str(payload.get('rawMaterial')), payload.get('machGrpCode'), payload.get('qty'), defect, payload.get('comment'), certificate_code, lot_nr, payload.get('user')))
        cursor.commit()
        cursor.close()
        cnxn.close()

    def updateScrap(payload, defect, last_upd_on):
        if payload.get('identity'):
            if payload.get('identity').startswith('LF'):
                lot_nr = payload.get('identity')
                certificate_code = ""
            else:
                lot_nr = ""
                certificate_code = payload.get('identity')
        else:
            lot_nr = ""
            certificate_code = ""
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        cursor.execute("""
                    DECLARE @LastUpdatedOn nvarchar(30) = NULL           
                    EXEC SIP_upd_LEG_ScrapTally @old_ScrapTally = ?, 
                                                @old_LastUpdatedOn = ?, 
                                                @Date = ?,
                                                @Operator = ?, 
                                                @MachCode = ?, 
                                                @ProducedPart = ?,
                                                @RawMaterial = ?,
                                                @MachGrpCode = ?,
                                                @Qty = ?,
                                                @DefectCode = ?, 
                                                @Comment = ?,
                                                @CertificateCode = ?,
                                                @LotNr = ?,
                                                @LogProgramCode = ?, 
                                                @LastUpdatedOn =  @LastUpdatedOn OUTPUT,
                                                @IsahUserCode = ?
                       """, (
                           payload.get('scrapTally'),
                           last_upd_on,
                           datetime.today().date(),
                           payload.get('user'),
                           payload.get('machCode'),
                           str(payload.get('producedPart')),
                           str(payload.get('rawMaterial')),
                           payload.get('machGrpCode'),
                           payload.get('qty'),
                           defect,
                           payload.get('comment'),
                           certificate_code,
                           lot_nr,
                           0,
                           payload.get('user')
                       )
        )

        cursor.commit()
        cursor.close()
        cnxn.close()

    def deleteScrap(payload, last_upd_on):
        cnxn = DatabaseConnection.get_db_connection()
        cursor = cnxn.cursor()
        cursor.execute("""EXEC SIP_del_LEG_ScrapTally ?, ?, ?, ?
                       """, (
                           payload.get('scrapTally'),
                           last_upd_on,
                           payload.get('user'),
                           0
                       )
        )

        cursor.commit()
        cursor.close()
        cnxn.close()