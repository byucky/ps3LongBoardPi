import pygame
import time
import os
#import pigpio
import time
import sys
import threading
import subprocess
from pprint import pprint

pathToController = '/dev/input/js0'

INPUTS = {
    "THROTTLE_AXIS" : 1,
    "THROTTLE_ENABLE": 8,
    "POWER_OFF": 13,
    "CRUISE" : 10, 
}

is_debug = "debug" in sys.argv

power_off = 0
powerdown = ["sudo", "shutdown", "now"]

def PowerOffPi():
    elapsed_time = 0
    while(elapsed_time < 5):
        time.sleep(1)
        if power_off is 1:
            elapsed_time += 1
        else:
            elapsed_time = 0
    subprocess.call(powerdown)

class Skateboard():

    def __init__(self):
        self.powerThread = threading.Thread(target=PowerOffPi)
        self.powerThread.start()
        self.j = pygame.joystick.Joystick(0)
        self.j.init()
        print(self.j)
        self.buttons = {
            'axis' : 0,
            'enable': 0,
            'power_off': 0
        }

    def getInput(self):

        changes = {}

        # get input from controllers
        events = pygame.event.get()
        if events is not None:
            for event in events:
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == INPUTS["THROTTLE_AXIS"]:
                        changes["axis"] = event.value
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == INPUTS["THROTTLE_ENABLE"]:
                        changes["enable"] = 1
                    if event.button == INPUTS["POWER_OFF"]:
                        changes['power_off'] = 1
                if event.type == pygame.JOYBUTTONUP:
                    if event.button == INPUTS["THROTTLE_ENABLE"]:
                        changes["enable"] = 0
                    if event.button == INPUTS["POWER_OFF"]:
                        changes['power_off'] = 0

        return changes

    def update(self, changes):
        #update state based on gathered input
        if "axis" in changes:
            # self.buttons['axis'] = changes['axis']
            self.updateSpeed(changes['axis'])
        if "enable" in changes:
            self.buttons['enable'] = changes['enable']
        if "power" in changes:
            self.buttons['power_off'] = changes['power_off']
            self.adjustPowerOff()
            
    def adjustPowerOff():
        if self.buttons['power_off'] is 1:
            power_off = 1
        elif self.buttons['power_off'] is 0:
            power_off = 0

    def updateSpeed(self, newSpeed):
        return True
    
    def OutputButtonValues(self, changes):
        pprint(changes)

    def mainloop(self):
        while(True):
            changes = self.getInput()
            self.update(changes)
            if(is_debug):
                self.OutputButtonValues(changes)
            time.sleep(0.1)


def main():
    pygame.init()
    os.putenv('SDL_VIDEODRIVER','fbcon')
    pygame.display.init()	

    time.sleep(5.0)

    skate = Skateboard()
    skate.mainloop()
    

if __name__ == "__main__":
	main()