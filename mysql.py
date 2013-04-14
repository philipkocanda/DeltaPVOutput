import time, subprocess,serial,MySQLdb
from delta30EUG4TRInv import Delta30EU_G4_TR_Inverter
from time import localtime, strftime
from config import Configuration

class MysqlInserter:

    def __init__(self):
        pass

    def insert(self, inverterId, dcVoltage, dcPower, acPower):
        if Configuration.mysqlUser == '':
            # Skip if mysql is not configured
            return

        con = MySQLdb.connect(host=Configuration.mysqlHost,user=Configuration.mysqlUser, passwd=Configuration.mysqlPw,db=Configuration.mysqlDb)

        con.query("SELECT count(*) from Measurement")
        r = con.store_result()
        print(str(r.fetch_row()[0][0]) + " results stored in mysql")

        try:
            inverterIdNum = int(inverterId)
        except:
            inverterIdNum = -1

        try:
            acPowerNum = int(acPower)
        except:
            acPowerNum = -1

        try:
            dcPowerNum = int(dcPower)
        except:
            dcPowerNum = -1

        try:
            dcVoltageNum = int(dcVoltage)
        except:
            dcVoltageNum = -1


        c = con.cursor()
        print("inserting: " + str(inverterIdNum) + str(dcVoltageNum) + str(dcPowerNum) + str(acPowerNum))
        try:
            c.execute("""INSERT INTO Measurement (inverterId, dcVoltage, dcPower, acPower) VALUES (%s,%s,%s,%s)""",(inverterIdNum, dcVoltageNum, dcPowerNum, acPowerNum))
            con.commit()
        except Error as e:
            con.rollback()
            print "Something went wrong inserting into mysql. " + e

        con.close()
