#A simple script to read values from a delta inverter and post them to 
#PVoutput.org

import time, subprocess,serial
from delta30EUG4TRInv import DeltaInverter
from time import localtime, strftime
from config import Configuration

if __name__ == '__main__':

    #Edit your serial connection as required!!
    connection = serial.Serial('/dev/ttyUSB0',19200,timeout=0.5);
    localtime = time.localtime(time.time())   
 
    t_date = 'd={0}'.format(strftime('%Y%m%d'))
    t_time = 't={0}'.format(strftime('%H:%M'))

    inv1 = DeltaInverter(Configuration.RS485IDS[0])
    commandName = 'AC Power'
    command = inv1.getCmdStringFor(commandName)
    connection.write(command)
    response = connection.read(100)
    p1 = inv1.getValueFromResponse(response)
    print ("1: " + commandName + ": " + str(p1) + " W")

    inv1 = DeltaInverter(Configuration.RS485IDS[1])
    commandName = 'AC Power'
    command = inv1.getCmdStringFor(commandName)
    connection.write(command)
    response = connection.read(100)
    p2 = inv1.getValueFromResponse(response)
    print ("2: " + commandName + ": " + str(p2) + " W")

    print ("Total: " + commandName + ": " + str(int(p1) + int(p2)) + " W\n")

    inv1 = DeltaInverter(Configuration.RS485IDS[0])
    commandName = 'DC Power'
    command = inv1.getCmdStringFor(commandName)
    connection.write(command)
    response = connection.read(100)
    p1 = inv1.getValueFromResponse(response)
    print ("1: " + commandName + ": " + str(p1) + " W")

    inv1 = DeltaInverter(Configuration.RS485IDS[1])
    commandName = 'DC Power'
    command = inv1.getCmdStringFor(commandName)
    connection.write(command)
    response = connection.read(100)
    p2 = inv1.getValueFromResponse(response)
    print ("2: " + commandName + ": " + str(p2) + " W")

    print ("Total: " + commandName + ": " + str(int(p1) + int(p2)) + " W")

    connection.close()
