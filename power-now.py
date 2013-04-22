#A simple script to read values from a delta inverter and post them to 
#PVoutput.org

import time, subprocess,serial
from delta30EUG4TRInv import Delta30EU_G4_TR_Inverter
from time import localtime, strftime
from config import Configuration
from mysql import MysqlInserter

if __name__ == '__main__':

    connection = serial.Serial('/dev/ttyUSB0',Configuration.serialBaud, timeout=Configuration.serialTimeoutSecs)
    localtime = time.localtime(time.time())   
 
    t_date = 'd={0}'.format(strftime('%Y%m%d'))
    t_time = 't={0}'.format(strftime('%H:%M'))

    inv1 = Delta30EU_G4_TR_Inverter(Configuration.RS485IDS[0], connection)
    inv2 = Delta30EU_G4_TR_Inverter(Configuration.RS485IDS[1], connection)

    acPower1 = inv1.call('AC Power')
    print ("1: AC Power: " + str(acPower1) + " W")

    dcPower1 = inv1.call('DC Power')
    print ("1: DC Power: " + str(dcPower1) + " W")

    dcVoltage1 = inv1.call('DC Voltage')
    print ("1: DC Voltage: " + str(dcVoltage1) + " V")

    dcCurrent1 = inv1.call('DC Current')
    print ("1: DC Current: " + str(dcCurrent1) + " A")

    try:
        print "1: Efficiency: %.2f%%" % (100.0*int(acPower1)/int(dcPower1))
    except:
        pass

    energyDay1 = inv1.call('Energy Day')
    print ("1: Energy Day: " + str(energyDay1) + " wh\n")

    acPower2 = inv2.call('AC Power')
    print ("2: AC Power: " + str(acPower2) + " W")

    dcPower2 = inv2.call('DC Power')
    print ("2: DC Power: " + str(dcPower2) + " W")

    dcVoltage2 = inv2.call('DC Voltage')
    print ("2: DC Voltage: " + str(dcVoltage2) + " V")

    dcCurrent2 = inv2.call('DC Current')
    print ("2: DC Current: " + str(dcCurrent2) + " A")

    try:
        print "2: Efficiency: %.2f%%" % (100.0*int(acPower2)/int(dcPower2))
    except:
        pass

    energyDay2 = inv2.call('Energy Day')
    print ("2: Energy Day: " + str(energyDay2) + " Wh\n")

    connection.close()

    try:
        print ("Total: AC Power: " + str(int(acPower1) + int(acPower2)) + " W")
    except:
        pass
    try:
        print ("Total DC Power: " + str(int(dcPower1) + int(dcPower2)) + " W")
    except:
        pass
    try:
        print ("Total Energy Day: " + str(int(energyDay1) + int(energyDay2)) + " Wh\n")
    except:
        pass
        

    try:
        m = MysqlInserter()
        m.insert(1, dcVoltage1, dcPower1, acPower1)
        m.insert(2, dcVoltage2, dcPower2, acPower2)
    except:
        print "Error inserting into mysql"
