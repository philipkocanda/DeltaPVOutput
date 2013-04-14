from Inverter import Inverter
class Delta30EU_G4_TR_Inverter(Inverter):

         #Known Commands
         ##code, name, format, divisor, units, response size
    
    cmds = [
            ['\x00\x09','Serial',-1,0,'', 27],
            ['\x00\x08','Inverter Type',-1,0,'', 20],
            ['\x00\x0a','Revision',-1,0,'', 11],
            ['\x00\x07','Date Code',-1,0,'', 13],
            ['\x00\x04','Calibration Date',11,0,'', 12],
            ['\x00\x05','Calibration Time',12,0,'', 12],
            ['\x00\x06','Tester ID',0,1,'', 11],
            ['\x00\x40','System Controller version',10,0,'', 12],
            ['\x00\x50','IT Grid Monitor version',10,0,'', 12],
            ['\x00\x43','DC Controller version',10,0,'', 12],
            ['\x00\x3f','AC Controller version',10,0,'', 12],
##            ['\x00\xc2','Backlight status',0,0,'', 9],
##            ['\x00\xc1','Contrast',0,1,'', 9],
            ['\x00\x20','Date',13,0,'', 13],
            ['\x00\x21','Time',12,0,'', 12],
            ['\x00\x00','Grid',1,0,'', 29],
            ['\x12\x0b','Feed in Tariff',2,100.0,'', 13],
            ['\x15\x01','Energy Day',3,1,'Wh', 17],
            ['\x16\x01','Energy Week',3,1,'Wh', 17],
            ['\x17\x01','Energy Month',3,1,'Wh', 17],
            ['\x18\x01','Energy Year',3,1,'Wh', 17],
            ['\x19\x01','Energy Total',3,1,'Wh', 17],
            ['\x15\x03','Revenue Day',3,100.0,'Wh', 17],
            ['\x16\x03','Revenue Week',3,100.0,'Wh', 17],
            ['\x17\x03','Revenue Month',3,100.0,'Wh', 17],
            ['\x18\x03','Revenue Year',3,100.0,'Wh', 17],
            ['\x19\x03','Revenue Total',3,100.0,'Wh', 17],

            ['\x34\x06','Max Active Power Day',0,1,'W', 11],
            ['\x35\x06','Max Active Power Week',0,1,'W', 11],
            ['\x36\x06','Max Active Power Month',0,1,'W', 11],
            ['\x37\x06','Max Active Power Year',0,1,'W', 11],
            ['\x38\x06','Max Active Power Total',0,1,'W', 11],

            ['\x34\x05','Max Current Day',0,100.0,'A', 11],
            ['\x35\x05','Max Current Week',0,100.0,'A', 11],
            ['\x36\x05','Max Current Month',0,100.0,'A', 11],
            ['\x37\x05','Max Current Year',0,100.0,'A', 11],
            ['\x38\x05','Max Current Total',0,100.0,'A', 11],

            ['\x34\x01','Min Voltage Day',0,1,'V~', 11],
            ['\x35\x01','Min Voltage Week',0,1,'V~', 11],
            ['\x36\x01','Min Voltage Month',0,1,'V~', 11],
            ['\x37\x01','Min Voltage Year',0,1,'V~', 11],
            ['\x38\x01','Min Voltage Total',0,1,'V~', 11],

            ['\x34\x02','Max Voltage Day',0,1,'V~', 11],
            ['\x35\x02','Max Voltage Week',0,1,'V~', 11],
            ['\x36\x02','Max Voltage Month',0,1,'V~', 11],
            ['\x37\x02','Max Voltage Year',0,1,'V~', 11],
            ['\x38\x02','Max Voltage Total',0,1,'V~', 11],

            ['\x34\x03','Min Frequency Day',0,100.0,'Hz', 11],
            ['\x35\x03','Min Frequency Week',0,100.0,'Hz', 11],
            ['\x36\x03','Min Frequency Month',0,100.0,'Hz', 11],
            ['\x37\x03','Min Frequency Year',0,100.0,'Hz', 11],
            ['\x38\x03','Min Frequency Total',0,100.0,'Hz', 11],

            ['\x34\x04','Max Frequency Day',0,100.0,'Hz', 11],
            ['\x35\x04','Max Frequency Week',0,100.0,'Hz', 11],
            ['\x36\x04','Max Frequency Month',0,100.0,'Hz', 11],
            ['\x37\x04','Max Frequency Year',0,100.0,'Hz', 11],
            ['\x38\x04','Max Frequency Total',0,100.0,'Hz', 11],

            ['\x34\x07','Min Reactive Power Day',4,1,'var', 11],
            ['\x35\x07','Min Reactive Power Week',4,1,'var', 11],
            ['\x36\x07','Min Reactive Power Month',4,1,'var', 11],
            ['\x37\x07','Min Reactive Power Year',4,1,'var', 11],
            ['\x38\x07','Min Reactive Power Total',4,1,'var', 11],

            ['\x34\x08','Max Reactive Power Day',4,1,'var', 11],
            ['\x35\x08','Max Reactive Power Week',4,1,'var', 11],
            ['\x36\x08','Max Reactive Power Month',4,1,'var', 11],
            ['\x37\x08','Max Reactive Power Year',4,1,'var', 11],
            ['\x38\x08','Max Reactive Power Total',4,1,'var', 11],


            ['\x1c\x01','DC Voltage',0,1,'V', 11],
            ['\x1c\x02','DC Current',0,10.0,'A', 11],
            ['\x1c\x03','Insulation Gnd-Plus',0,1,'kOhm', 11],
            ['\x1c\x04','Insulation Gnd-Minus',0,1,'kOhm', 11],
            ['\x1c\x05','DC Power',0,1,'W', 11],

            ['\x33\x01','AC Voltage',0,1,'V~', 11],
            ['\x33\x02','AC Frequency',0,100.0,'Hz', 11],
            ['\x33\x03','AC Current',0,10.0,'A', 11],
            ['\x33\x04','AC Power',0,1,'W', 11],
            ['\x33\x05','AC Reactive Power',4,1,'var', 11],
            ['\x33\x06','Power Factor',4,1000.0,'', 11],
            ['\x33\x07','DC Injection',4,1,'mA', 11],

            ['\x03\x01','Internal Ambient Temperature',0,1,'C', 11],
            ['\x03\x02','Heatsink Temperature',0,1,'C', 11]

            ]


