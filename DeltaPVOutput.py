#A simple script to read values from a delta inverter and post them to
#PVoutput.org

import time, subprocess,serial
from delta25Inv import Delta25Inverter
from time import localtime, strftime
from config import Configuration
from mysql import MysqlInserter
from domoticz import Domoticz

#PVOutput.org API Values - UPDATE THESE TO YOURS!

#Array of SystemID's that correlate to the inverter number
#ie. the first systemID will be inverter 1, second inverter 2 etc
#the numebr of systemIDs must still be the same as the number of inverter- even if they
#are empty.
#an empty string means don't individually update this inverter on pvoutput.org - just do the totals

if __name__ == '__main__':

    connection = serial.Serial('/dev/ttyUSB0',Configuration.serialBaud, timeout=Configuration.serialTimeoutSecs)
    localtime = time.localtime(time.time())

    t_date = 'd={0}'.format(strftime('%Y%m%d'))
    t_time = 't={0}'.format(strftime('%H:%M'))

    totalWh =0
    totalACPower =0
    totalDCPower =0
    avgTempDC=0
    validInv =0

    for index in range(len(Configuration.SYSTEMIDS)):
        inv = Delta25Inverter(Configuration.RS485IDS[index], connection) #init Inverter
        dz = Domoticz()
        #Get the Daily Energy thus far
        try:
            energyDay = int(inv.call('Energy Today'))
            validInv+=1
            totalWh+= energyDay

            t_energy = 'v1={0}'.format(energyDay)

            #instanteous power AC-side
            acPower = inv.call('AC Power 1')
            totalACPower+= int(acPower)
            t_power = 'v2={0}'.format(acPower)

            #instanteous power DC-side
            dcPower = inv.call('DC Power 1')
            totalDCPower+=int(dcPower)

            #DC Voltage
            dcVoltage = inv.call('DC Voltage 1')
            t_volts = 'v6={0}'.format(dcVoltage)

            #Temp - this appears to be onboard somewhere not the heatsink
            temp = inv.call('AC Temperature')
            avgTempDC += int(temp)
            t_temp = 'v5={0}'.format(temp)

            energyTotal = int(inv.call('Energy Total'))
            dcCurrent = int(inv.call('DC Current 1'))
            acCurrent = int(inv.call('AC Current'))
            acVoltage = int(inv.call('AC Voltage'))
            acFrequency = int(inv.call('AC Frequency'))

            dz.updateElectricityMeter(Configuration.dzEnergyMeterDeviceId, int(acPower), energyTotal)
            dz.updateDeviceValue(Configuration.dzDcCurrentDeviceId, int(dcCurrent))
            dz.updateDeviceValue(Configuration.dzDcVoltageDeviceId, int(dcVoltage))
            dz.updateDeviceValue(Configuration.dzAcVoltageDeviceId, int(acVoltage))
            dz.updateDeviceValue(Configuration.dzAcCurrentDeviceId, int(acCurrent))
            dz.updateDeviceValue(Configuration.dzAcFrequencyDeviceId, float(acFrequency))
            dz.updateDeviceValue(Configuration.dzInverterTemperatureDeviceId, int(temp))

            if not Configuration.SYSTEMIDS[index]=="":
                #Send it all off to PVOutput.org
                cmd = ['/usr/bin/curl',
                    '-d', t_date,
                    '-d', t_time,
                    '-d', t_energy,
                    '-d', t_power,
                    '-d', t_volts,
                    '-d', t_temp,
                    '-H', 'X-Pvoutput-Apikey: ' + Configuration.APIKEY,
                    '-H', 'X-Pvoutput-SystemId: ' + Configuration.SYSTEMIDS[index],
                    'http://pvoutput.org/service/r1/addstatus.jsp']
                ret = subprocess.call (cmd)
            try:
                m = MysqlInserter()
                m.insert(Configuration.RS485IDS[index], dcVoltage, dcPower, acPower)
            except:
                print "Error inserting into mysql"
        except:
            print "No or failed response from inverter %d - shutdown? No Data sent to PVOutput.org"% (index+1)

    if validInv >1 and totalACPower >0:
        print "%d awake Inverters" % validInv
        avgTempDC=avgTempDC/validInv

        t_energy = 'v1={0}'.format(totalWh)
        t_power = 'v2={0}'.format(totalACPower)
        t_temp = 'v5={0}'.format(avgTempDC)

        #Send it all off to PVOutput.org
        cmd = ['/usr/bin/curl',
               '-d', t_date,
                '-d', t_time,
                '-d', t_energy,
                '-d', t_power,
                '-d', t_temp,
                '-H', 'X-Pvoutput-Apikey: ' + Configuration.APIKEY,
                '-H', 'X-Pvoutput-SystemId: ' + Configuration.TOTALSYSTEMID,
                'http://pvoutput.org/service/r1/addstatus.jsp']
        ret = subprocess.call (cmd)
    else:
       print "No response from any inverter - shutdown? No Data sent to PVOutput.org"

    connection.close()
