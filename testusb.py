import usb
import time


while(True):
    s = ""
    connected = False
    busses = usb.busses()
    for bus in busses:
        devices = bus.devices
        for dev in devices:
            if dev.idVendor == 1356:
                connected = True 
    print(connected)    
    time.sleep(3)