import sys,time, subprocess,serial,MySQLdb
from delta30EUG4TRInv import Delta30EU_G4_TR_Inverter
from time import localtime, strftime
from config import Configuration


def checkSystemDate(date, sysId, dbWh):
    # Get pvoutput data
    cmd = ['/usr/bin/curl',
           '-s',
           '-H', 'X-Pvoutput-Apikey: ' + Configuration.APIKEY,
           '-H', 'X-Pvoutput-SystemId: ' + sysId,
           'http://pvoutput.org/service/r2/getoutput.jsp?df=' + date + '\&dt=' + date]
    ret = subprocess.check_output(cmd)
    # print ret
    if "Bad request 400: No system or data found" == ret:
        print "NO DATA FOR DAY"
        pvoWh = -1
        pvDate = "n/a"
    else:
        try:
            tokens = ret.split(",")
            pvDate = tokens[0]
            pvoWh = int(tokens[1])
        except:
            print ret
            sys.exit()
    print("dbdate: " + date + " pvdate: " + pvDate + " " + sysId + " pvoWh: " + str(pvoWh) + " dbWh:" + str(
        dbWh)) + " match: " + str(pvoWh == dbWh)
    if dbWh > pvoWh:
        print "PV is missing data!"
        cmd = ['/usr/bin/curl',
               '-XPOST',
               '-H', 'X-Pvoutput-Apikey: ' + Configuration.APIKEY,
               '-H', 'X-Pvoutput-SystemId: ' + sysId,
               '-d', 'data=' + date + "," + str(dbWh),
               'http://pvoutput.org/service/r2/addoutput.jsp?df=' + date + '\&dt=' + date]
        ret = subprocess.check_output(cmd)
        print ret


if __name__ == '__main__':

    con = MySQLdb.connect(host=Configuration.mysqlHost,user=Configuration.mysqlUser, passwd=Configuration.mysqlPw,db=Configuration.mysqlDb)
    cur = con.cursor()

    # Get db data
    sql = "select DATE_FORMAT(date(tsmp),'%Y%m%d'), inverterId, max(whDay) from Measurement where tsmp between '2014-08-12' and '2015-03-26' group by date(tsmp), inverterId order by date(tsmp), inverterId"
    #print(sql)
    cur.execute(sql)
    print(str(cur.rowcount) + " results")
    dbTotalWh = 0;
    for row in cur.fetchall() :
        newDate = str(row[0])
        if 'date' in locals() and newDate != date:
#            print("check total for date: " + date)
            checkSystemDate(date, Configuration.TOTALSYSTEMID, dbTotalWh)
            dbTotalWh = 0

        date = newDate
        sysId = Configuration.SYSTEMIDS[Configuration.RS485IDS.index(row[1])]
        dbWh = row[2]
        dbTotalWh += dbWh
        checkSystemDate(date, sysId, dbWh)

    con.close()

