from Inverter import Inverter

# Delta Solivia 2.5 Inverter (2012/2013)
class Delta25Inverter(Inverter):

         #Known Commands
         ##code, name, format, divisor, units, response size

         # Source: https://forums.whirlpool.net.au/archive/1901079
    cmds = [
            ['\x00\x09','Serial',-1,0,'', 27],
            ['\x00\x08','Inverter Type',-1,0,'', 20],
            ['\x00\x0a','Revision',-1,0,'', 11],
            ['\x00\x07','Date Code',-1,0,'', 13],
            ['\x00\x04','Calibration Date',11,0,'', 12],
            ['\x00\x05','Calibration Time',12,0,'', 12],
            ['\x00\x06','Tester ID',0,1,'', 11],
            ['\x00\x40','Firmware version',10,0,'', 12],

            ['\x00\x20','Date',13,0,'', 13],
            ['\x00\x21','Time',12,0,'', 12],
            ['\x00\x00','Grid',1,0,'', 29],

            ['\x13\x03','Energy Today',0,1,'Wh', 17],
            #['\x13\x04','Runtime Today',0,0,'Minutes', 13],

            #['\x14\x03','Energy Total',1,1,'Wh', 17],

            ['\x10\x01','DC Current 1',0,10.0,'A', 11],
            ['\x10\x02','DC Voltage 1',0,1,'V', 11],
            ['\x10\x03','DC Power 1',0,1,'W', 11],

            ['\x10\x05','DC Voltage 2',0,1,'V', 11],
            ['\x10\x04','DC Current 2',0,10.0,'A', 11],
            ['\x10\x06','DC Power 2',0,1,'W', 11],

            ['\x11\x01','DC Current 1 Avg',0,10.0,'A', 11],
            ['\x11\x02','DC Voltage 1 Avg',0,1,'V', 11],
            ['\x11\x03','DC Power 1 Avg',0,1,'W', 11],

            ['\x11\x04','DC Current 2 Avg',0,10.0,'A', 11],
            ['\x11\x05','DC Voltage 2 Avg',0,1,'V', 11],
            ['\x11\x06','DC Power 2 Avg',0,1,'W', 11],

            ['\x10\x07','AC Current',0,10.0,'A', 11],
            ['\x10\x08','AC Voltage',0,1,'V~', 11],
            ['\x10\x09','AC Power',0,1,'W', 11],
            ['\x10\x0a','AC Frequency',0,100.0,'Hz', 11],

            ['\x11\x07','AC Current Avg',0,10.0,'A', 11],
            ['\x11\x08','AC Voltage Avg',0,1,'V~', 11],
            ['\x11\x09','AC Power Avg',0,1,'W', 11],
            ['\x11\x0a','AC Frequency Avg',0,100.0,'Hz', 11],

            ['\x20\x05','Temperature',0,1,'C', 11],

            ]


