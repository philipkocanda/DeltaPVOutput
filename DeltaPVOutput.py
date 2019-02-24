#A simple script to read values from a delta inverter and post them to
#PVoutput.org

import time, subprocess,serial
from delta25Inv import Delta25Inverter
from time import localtime, strftime
from config import Configuration
# from mysql import MysqlInserter
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
        if True:
            energyDay = int(inv.call('Energy Today'))
            validInv+=1
            totalWh+= energyDay

            t_energy = 'v1={0}'.format(energyDay)

            #instanteous power AC-side
            acPower = inv.call('AC Power')
            totalACPower+= int(acPower)
            t_power = 'v2={0}'.format(acPower)

            print(acPower)

            #instanteous power DC-side
            dcPower = inv.call('DC Power 1')
            totalDCPower+=int(dcPower)

            #DC Voltage
            dcVoltage = inv.call('DC Voltage 1')
            t_volts = 'v6={0}'.format(dcVoltage)

            #Temp - this appears to be onboard somewhere not the heatsink
            temp = inv.call('Temperature')
            avgTempDC += int(temp)
            t_temp = 'v5={0}'.format(temp)

            #energyTotal = int(inv.call('Energy Total'))
            dcCurrent = float(inv.call('DC Current 1'))
            acCurrent = float(inv.call('AC Current'))
            acVoltage = int(inv.call('AC Voltage'))
            acFrequency = float(inv.call('AC Frequency'))

            print('Updating Domoticz...')
            print(int(acPower))

            dz.updateElectricityMeter(Configuration.dzEnergyMeterDeviceId, int(acPower))
            dz.updateDeviceValue(Configuration.dzDcCurrentDeviceId, float(dcCurrent))
            dz.updateDeviceValue(Configuration.dzDcVoltageDeviceId, int(dcVoltage))
            dz.updateDeviceValue(Configuration.dzAcVoltageDeviceId, int(acVoltage))
            dz.updateDeviceValue(Configuration.dzAcCurrentDeviceId, float(acCurrent))
            dz.updateDeviceValue(Configuration.dzAcFrequencyDeviceId, float(acFrequency))
            dz.updateDeviceValue(Configuration.dzInverterTemperatureDeviceId, int(temp))

    connection.close()
