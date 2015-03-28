import struct,sys,time,serial,binascii
from crc import CRC16
from struct import *
from config import Configuration
class Inverter:

    inverterNum=0

    #Define known Commands in subclass
    cmds=[]

    #Constructor takes inverter number (incase you have more than 1)	
    def __init__(self,inverter,connection):
        self.inverterNum=inverter
        self.crcCalc = CRC16()
        self.connection = connection

    #private to do the binary packing of the protocol
    def __buildCmd(self, cmd):
        l = len(cmd)
        crc = self.crcCalc.calcString( struct.pack('BBB%ds'%l,5,self.inverterNum,l,cmd))
        lo = crc & (0xff)
        high = (crc>>8) & 0xff
        return struct.pack('BBBB%dsBBB' %len(cmd),2,5,self.inverterNum,len(cmd),cmd,lo,high,3);

    #retrieves the command object for the given human readable command
    def findCmdObj(self,strValue):
        for command in self.cmds:
            if command[1]==strValue:
                return command

    #Calls a command and returns the response
    def call(self,commandName):
        commandObj = self.findCmdObj(commandName)

        retryCount = 0
        succes = False
        while retryCount < 20 and not succes:
            if retryCount > 0:
                time.sleep(0.05 * retryCount)
                # reinit connection
                print "Retry count: " + str(retryCount) + " Reinitialize connection"
                self.connection.close()
                self.connection = serial.Serial('/dev/ttyUSB0',Configuration.serialBaud, timeout=Configuration.serialTimeoutSecs, parity=serial.PARITY_EVEN, rtscts=1, xonxoff=1)
            try:
                self.connection.write(self.__buildCmd(commandObj[0]))
                response = self.connection.read(commandObj[5])
                response_check_result = self.isValidResponse(response)
                if response_check_result == "N/A":
                    return "N/A"
                if response_check_result != True:
                    raise Exception("Invalid Response: " + str(response_check_result))
                return self.__unpackData(response, commandObj)
            except Exception as e:
                retryCount += 1
                print commandObj[1] + " command failed: " + str(e) + " RS485 id: " + str(self.inverterNum)

    #checks for a valid STX, ETX and CRC
    def isValidResponse(self,cmd):
        if len(cmd) == 0:
            return "Empty reply."
#        if len(cmd) != cmd[5]:
#            return "Len should be " + str(cmd[5]) + " was: " + str(len(cmd)) 
        if ord(cmd[1])== 0x15:
            return "N/A"
        elif cmd[:2] != binascii.unhexlify("0206"):
            return "First 2 bytes should be 0x0206. Was: 0x" + binascii.hexlify(cmd[:2])
        elif ord(cmd[-1:])!=0x03:
            return "Last byte should be 0x03. Was: 0x" + binascii.hexlify(cmd[-1:])
        cmdcontents = cmd[1:-3]
        crc = self.crcCalc.calcString(cmdcontents)
        lo = crc & (0xff)
        high = (crc>>8) & 0xff
        crcByte = len(cmd)-3
        if ord(cmd[crcByte])!=lo or ord(cmd[crcByte+1])!=high:   
            return "CRC failed"
        return True

    #Returns a raw value from a response
    def __unpackData(self,response, commandObj):
        cmdcontents = response[1:-3]
        lendata = ord(cmdcontents[2])-2
        try:
            code, stringName,fmt,divisor,unit,size = commandObj
            try:
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
                return "Error parsing string, perhaps unknown instruction. " + cmdcontents[3:5] + "format: " + fmt
        except:
            print("Error unpacking response. cmdcontents: " + ":".join("{0:x}".format(ord(c)) for c in cmdcontents))


