#A simple script to read values from a delta inverter and post them to 
#PVoutput.org

import time, subprocess,serial
from delta30EUG4TRInv import DeltaInverter
from time import localtime, strftime

#PVOutput.org API Values - UPDATE THESE TO YOURS!
SYSTEMID="123455"
APIKEY="a14990baf0290b91eb31a867b6e34531e2a3566b"

if __name__ == '__main__':

    #Edit your serial connection as required!!
    connection = serial.Serial('/dev/ttyUSB0',19200,timeout=0.5);
    localtime = time.localtime(time.time())   
 
    t_date = 'd={0}'.format(strftime('%Y%m%d'))
    t_time = 't={0}'.format(strftime('%H:%M'))

    inv1 = DeltaInverter(1) #init Inverter 1

    for code,cmd in sorted(inv1.cmds.iteritems()):
        commandName = cmd[0]
        unit = cmd[3]
        command = inv1.getCmdStringFor(commandName)
        connection.write(command)
        response = connection.read(100)
        print (commandName + ": " + str(inv1.getValueFromResponse(response)) + " " + str(unit))

    connection.close()
