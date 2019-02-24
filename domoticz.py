import urllib2
import base64
from config import Configuration

class Domoticz:
    def dzRequest(self, url):
        print(url)
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (Configuration.dzUsername, Configuration.dzPassword)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request)
        return response.read()

    def updateElectricityMeter(self, idx, power):
        self.dzRequest(
            "http://" + Configuration.dzServer +
            "/json.htm?type=command&param=udevice&idx=%d" % idx +
            ("&nvalue=0&svalue=%d" % power) + ";1000" +
            "&passcode=" + Configuration.dzPasscode
        )

    def updateDeviceValue(self, idx, value):
        self.dzRequest(
            "http://" + Configuration.dzServer +
            "/json.htm?type=command&param=udevice&idx=%d" % idx +
            ("&nvalue=0&svalue=%f" % value) +
            "&passcode=" + Configuration.dzPasscode
        )

# Running this file will test drive the Domoticz integration:
if __name__ == '__main__':
    dz = Domoticz()
    dz.updateElectricityMeter(Configuration.dzEnergyMeterDeviceId, 80.5)
    dz.updateDeviceValue(Configuration.dzDcCurrentDeviceId, 12)
    dz.updateDeviceValue(Configuration.dzDcVoltageDeviceId, 420)
    dz.updateDeviceValue(Configuration.dzAcVoltageDeviceId, 234)
    dz.updateDeviceValue(Configuration.dzAcCurrentDeviceId, 16)
    dz.updateDeviceValue(Configuration.dzAcFrequencyDeviceId, 50.01)
    dz.updateDeviceValue(Configuration.dzInverterTemperatureDeviceId, 45.5)
