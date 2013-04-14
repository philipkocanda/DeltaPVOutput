#A simple script to read values from a delta inverter and post them to 
#PVoutput.org

import sys,time, subprocess,serial
from delta30EUG4TRInv import Delta30EU_G4_TR_Inverter
from time import localtime, strftime
from config import Configuration

if __name__ == '__main__':

    connection = serial.Serial('/dev/ttyUSB0',Configuration.serialBaud, timeout=Configuration.serialTimeoutSecs)
    localtime = time.localtime(time.time())   
 
    t_date = 'd={0}'.format(strftime('%Y%m%d'))
    t_time = 't={0}'.format(strftime('%H:%M'))

    for index in range(len(Configuration.SYSTEMIDS)):
        print "-------- Inverter with RS485 id: " + str(Configuration.RS485IDS[index]) + "--------"
        inv = Delta30EU_G4_TR_Inverter(Configuration.RS485IDS[index], connection) #init Inverter
        # Loop through all known commands
        for command in inv.cmds:
            code, commandName, format, divisor, unit, responseSize = command
            try:
                value = inv.call(commandName)
                print (commandName + ": " + str(value) + " " + str(unit))
            except Exception as e:
                print "######### Error getting data form inverter. Command: " + commandName + " exception: " + str(e) + " traceback line-no: " + str(sys.exc_traceback.tb_lineno)
    connection.close()
