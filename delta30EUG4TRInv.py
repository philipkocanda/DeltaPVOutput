import crc,struct,sys
from crc import CRC16
from struct import *
class DeltaInverter:

    inverterNum=0;

    	#Known Commands
	                 ##StrValue, Format, divisor, units
    
    cmds = {
            '\x00\x09': ('Serial',-1,0,''),
            '\x00\x08': ('Inverter Type',-1,0,''),
            '\x00\x0a': ('Revision',-1,0,''),
            '\x00\x07': ('Date Code',-1,0,''),
            '\x00\x04': ('Calibration Date',11,0,''),
            '\x00\x05': ('Calibration Time',12,0,''),
            '\x00\x06': ('Tester ID',0,1,''),
            '\x00\x40': ('System Controller version',10,0,''),
            '\x00\x50': ('IT Grid Monitor version',10,0,''),
            '\x00\x43': ('DC Controller version',10,0,''),
            '\x00\x3f': ('AC Controller version',10,0,''),
            '\x00\xc2': ('Backlight status',0,0,''),
            '\x00\xc1': ('Contrast',0,1,''),
            '\x00\x20': ('Date',13,0,''),
            '\x00\x21': ('Time',12,0,''),
            '\x00\x00': ('Grid',1,0,''),
            '\x12\x0b': ('Feed in Tariff',2,100.0,''),
            '\x15\x01': ('Energy Day',3,1,'Wh'),
            '\x16\x01': ('Energy Week',3,1,'Wh'),
            '\x17\x01': ('Energy Month',3,1,'Wh'),
            '\x18\x01': ('Energy Year',3,1,'Wh'),
            '\x19\x01': ('Energy Total',3,1,'Wh'),
            '\x15\x03': ('Revenue Day',3,100.0,'Wh'),
            '\x16\x03': ('Revenue Week',3,100.0,'Wh'),
            '\x17\x03': ('Revenue Month',3,100.0,'Wh'),
            '\x18\x03': ('Revenue Year',3,100.0,'Wh'),
            '\x19\x03': ('Revenue Total',3,100.0,'Wh'),

            '\x34\x06': ('Max Active Power Day',0,1,'W'),
            '\x35\x06': ('Max Active Power Week',0,1,'W'),
            '\x36\x06': ('Max Active Power Month',0,1,'W'),
            '\x37\x06': ('Max Active Power Year',0,1,'W'),
            '\x38\x06': ('Max Active Power Total',0,1,'W'),

            '\x34\x05': ('Max Current Day',0,100.0,'A'),
            '\x35\x05': ('Max Current Week',0,100.0,'A'),
            '\x36\x05': ('Max Current Month',0,100.0,'A'),
            '\x37\x05': ('Max Current Year',0,100.0,'A'),
            '\x38\x05': ('Max Current Total',0,100.0,'A'),

            '\x34\x01': ('Min Voltage Day',0,1,'V~'),
            '\x35\x01': ('Min Voltage Week',0,1,'V~'),
            '\x36\x01': ('Min Voltage Month',0,1,'V~'),
            '\x37\x01': ('Min Voltage Year',0,1,'V~'),
            '\x38\x01': ('Min Voltage Total',0,1,'V~'),

            '\x34\x02': ('Max Voltage Day',0,1,'V~'),
            '\x35\x02': ('Max Voltage Week',0,1,'V~'),
            '\x36\x02': ('Max Voltage Month',0,1,'V~'),
            '\x37\x02': ('Max Voltage Year',0,1,'V~'),
            '\x38\x02': ('Max Voltage Total',0,1,'V~'),

            '\x34\x03': ('Min Frequency Day',0,100.0,'Hz'),
            '\x35\x03': ('Min Frequency Week',0,100.0,'Hz'),
            '\x36\x03': ('Min Frequency Month',0,100.0,'Hz'),
            '\x37\x03': ('Min Frequency Year',0,100.0,'Hz'),
            '\x38\x03': ('Min Frequency Total',0,100.0,'Hz'),

            '\x34\x04': ('Max Frequency Day',0,100.0,'Hz'),
            '\x35\x04': ('Max Frequency Week',0,100.0,'Hz'),
            '\x36\x04': ('Max Frequency Month',0,100.0,'Hz'),
            '\x37\x04': ('Max Frequency Year',0,100.0,'Hz'),
            '\x38\x04': ('Max Frequency Total',0,100.0,'Hz'),

            '\x34\x07': ('Min Reactive Power Day',4,1,'var'),
            '\x35\x07': ('Min Reactive Power Week',4,1,'var'),
            '\x36\x07': ('Min Reactive Power Month',4,1,'var'),
            '\x37\x07': ('Min Reactive Power Year',4,1,'var'),
            '\x38\x07': ('Min Reactive Power Total',4,1,'var'),

            '\x34\x08': ('Max Reactive Power Day',4,1,'var'),
            '\x35\x08': ('Max Reactive Power Week',4,1,'var'),
            '\x36\x08': ('Max Reactive Power Month',4,1,'var'),
            '\x37\x08': ('Max Reactive Power Year',4,1,'var'),
            '\x38\x08': ('Max Reactive Power Total',4,1,'var'),


            '\x1c\x01': ('DC Voltage',0,1,'V'),
            '\x1c\x02': ('DC Current',0,10.0,'A'),
            '\x1c\x03': ('Insulation Gnd-Plus',0,1,'kOhm'),
            '\x1c\x04': ('Insulation Gnd-Minus',0,1,'kOhm'),
            '\x1c\x05': ('DC Power',0,1,'W'),

            '\x33\x01': ('AC Voltage',0,1,'V~'),
            '\x33\x02': ('AC Frequency',0,100.0,'Hz'),
            '\x33\x03': ('AC Current',0,10.0,'A'),
            '\x33\x04': ('AC Power',0,1,'W'),
            '\x33\x05': ('AC Reactive Power',4,1,'var'),
            '\x33\x06': ('Power Factor',4,1000.0,''),
            '\x33\x07': ('DC Injection',4,1,'mA'),

            '\x03\x01': ('Internal Ambient Temperature',0,1,'C'),
            '\x03\x02': ('Heatsink Temperature',0,1,'C'),

            };


    #Constructor takes inverter number (incase you have more than 1)	
    def __init__(self,inverter=1):
        self.inverterNum=inverter
        self.crcCalc = CRC16()

    #private to do the binary packing of the protocol
    def __buildCmd(self, cmd):
        l = len(cmd)
        crc = self.crcCalc.calcString( struct.pack('BBB%ds'%l,5,self.inverterNum,l,cmd))
        lo = crc & (0xff);
        high = (crc>>8) & 0xff;
        return struct.pack('BBBB%dsBBB' %len(cmd),2,5,self.inverterNum,len(cmd),cmd,lo,high,3);        

    #retrieves the instruction for the given human readable command
    def __findCmd(self,strValue):
        for k,v in self.cmds.iteritems():
            if(v[0]==strValue):
                return k
    #unpacks the given command into an {Instruction} {Value} {Units} string    
    def __unpackFormatted(self,cmd):
        if not self.isValidResponse(cmd):
            return "Invalid Response"
        cmdcontents = cmd[1:-3]
        lendata = ord(cmdcontents[2])-2
        try:
            stringName,fmt,divisor,unit = self.cmds[cmdcontents[3:5]] 
            if fmt==0: ##General Numbers
                resp,invNum,size,instruction,value = struct.unpack('>BBB2sH',cmdcontents)
                value = value / divisor
            elif fmt==1: ##ascii string
                resp,invNum,size,instruction,value = struct.unpack('>BBB2s%ds' %lendata,cmdcontents)
            elif fmt==9: ##Model
                resp,invNum,size,instruction,typeof,model,value = struct.unpack('>BBB2sBB%ds' % (lendata-2),cmdcontents)
                return self.cmds[instruction][0]+": Type:" + str(typeof) + " Model:"  +value
            elif fmt==10: ##FWVersion #
                resp,invNum,size,instruction,ver,major,minor = struct.unpack('>BBB2sBBB',cmdcontents)
                return self.cmds[instruction][0]+": " + str(ver) +"." + str(major)+ "."+ str(minor)
            elif fmt==11: ## Date #
                resp,invNum,size,instruction,day,month,year = struct.unpack('>BBB2sBBB',cmdcontents)
                return self.cmds[instruction][0]+": " + str(day) +"/" + str(month)+ "-20"+ str(year)
            elif fmt==12: ## Time #
                resp,invNum,size,instruction,ver,major,minor = struct.unpack('>BBB2sBBB',cmdcontents)
                return self.cmds[instruction][0]+": " + str(ver) +":" + str(major)+ ":"+ str(minor)
            else:
                resp,invNum,size,instruction,value = struct.unpack('>BBB2s%ds' % lendata,cmdcontents)
            return self.cmds[instruction][0] + ": " + str(value) + " "+unit
        except:
            return "Error parsing string, perhaps unknown instruction"
    
    #Returns the packed command to be sent over serail, 
    #Command includes STX, inverter number, CRC, ETX    
    def getCmdStringFor(self,cmd):
        return self.__buildCmd(self.__findCmd(cmd))

    #Returns a formatted human readble form of a response
    def getFormattedResponse(self,cmd):
        return self.__unpackFormatted(cmd)

    #Returns a raw value from a response
    def getValueFromResponse(self,cmd):
        return self.__unpackData(cmd)
 
    #prints out hex values of a command string and the related instruction
    def debugRequestString(self,cmdString):
            cmd = cmdString[4:6]
            strCmd = self.cmds[cmd][0]
            inverter = ord(cmdString[2])
            print "%s on inverter %d:" % (strCmd,inverter)
            for ch in cmdString:
                sys.stdout.write("%02X " % ord(ch))
            print ""

    #checks for a valid STX, ETX and CRC
    def isValidResponse(self,cmd):
        if ord(cmd[1])== 0x15:
            return "N/A"
        elif ord(cmd[1])<> 0x06 or ord(cmd[0])!=0x02 or ord(cmd[len(cmd)-1])!=0x03:
            return "Invalid Response"
        cmdcontents = cmd[1:-3]
        crc = self.crcCalc.calcString(cmdcontents)
        lo = crc & (0xff)
        high = (crc>>8) & 0xff
        crcByte = len(cmd)-3
        if ord(cmd[crcByte])!=lo or ord(cmd[crcByte+1])!=high:   
            return "Invalid Response"
        return True

    #Returns a raw value from a response
    def __unpackData(self,cmd):
        if self.isValidResponse(cmd) != True:
            return self.isValidResponse(cmd)
        cmdcontents = cmd[1:-3]
        lendata = ord(cmdcontents[2])-2
        try:
            stringName,fmt,divisor,unit = self.cmds[cmdcontents[3:5]]
            if fmt==0: ##General Numbers
                resp,invNum,size,instruction,value = struct.unpack('>BBB2sH',cmdcontents)
                value = value / divisor
            elif fmt==2: ##Int Numbers
#                print ":".join("{0:x}".format(ord(c)) for c in cmdcontents)
                resp,invNum,size,instruction,value = struct.unpack('>BBB2sI',cmdcontents)
                value = value / divisor
            elif fmt==3: ##Long Numbers
             #   print ":".join("{0:x}".format(ord(c)) for c in cmdcontents)
                resp,invNum,size,instruction,value = struct.unpack('>BBB2sQ',cmdcontents)
                value = value / divisor
            elif fmt==4: ##Signed Numbers
                resp,invNum,size,instruction,value = struct.unpack('>BBB2sh',cmdcontents)
                value = value / divisor
            elif fmt==1: ##ascii string
                resp,invNum,size,instruction,value = struct.unpack('>BBB2s%ds' %lendata,cmdcontents)
            elif fmt==9: ##Model
                resp,invNum,size,instruction,typeof,model,value = struct.unpack('>BBB2sBB%ds' % (lendata-2),cmdcontents)
                return ": Type:" + str(typeof) + " Model:"  +value
            elif fmt==10: ##FWVersion #
                resp,invNum,size,instruction,ver,major,minor = struct.unpack('>BBB2sBBB',cmdcontents)
                return str(ver) +"." + str(major)+ "."+ str(minor)
            elif fmt==11: ## Date #
                #print ":".join("{0:x}".format(ord(c)) for c in cmdcontents)
                resp,invNum,size,instruction,day,month,year = struct.unpack('>BBB2sBBB',cmdcontents)
                return str(day) +"/" + str(month)+ "-20"+ str(year)
            elif fmt==13: ## Date 2 #
                resp,invNum,size,instruction,day,month,year = struct.unpack('>BBB3sBBB',cmdcontents)
                return str(day) +"/" + str(month)+ "-20"+ str(year)
            elif fmt==12: ## Time #
                # print ":".join("{0:x}".format(ord(c)) for c in cmdcontents)
                resp,invNum,size,instruction,ver,major,minor = struct.unpack('>BBB2sBBB',cmdcontents)
                return str(ver) +":" + str(major)+ ":"+ str(minor)
            else:
                resp,invNum,size,instruction,value = struct.unpack('>BBB2s%ds' % lendata,cmdcontents)
            return str(value)
        except:
            print ":".join("{0:x}".format(ord(c)) for c in cmdcontents)
            return "Error parsing string, perhaps unknown instruction"


