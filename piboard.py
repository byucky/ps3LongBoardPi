import pygame
import time
import os
import time
import sys
import threading
import subprocess
import re
from pprint import pprint

is_debug = "debug" in sys.argv
notPi = "--not_pi" in sys.argv

if not notPi:
    import pigpio
    pi = pigpio.pi()
else:
    import fakePiGpio
    pi = fakePiGpio

controllerId = 1356
pathToController = '/dev/input/js0'

INPUTS = {
    "THROTTLE_AXIS" : 1,
    "THROTTLE_ENABLE": 8,
    "POWER_OFF": 13,
    "CRUISE" : 10, 
}


motor = 18

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

    min_speed = 1720
    max_speed = 1100

    def __init__(self):
        pi.set_PWM_frequency(motor, 50)
        self.speed = 1500
        self.__speed = 1500
        self.j = None
        self.power_off_timer = 0
        self.powerThread = threading.Thread(target=PowerOffPi)
        self.powerThread.start()
        self.buttons = {
            'axis' : 0,
            'enable': 0,
            'power_off': 0
        }
    
    @property
    def speed(self):
        return self.__speed
    
    @speed.setter
    def speed(self, value):
        print(value)
        value = max(min(value, Skateboard.min_speed), Skateboard.max_speed)
        print(value)
        pi.set_servo_pulsewidth(motor, value)		
        self.__speed = value

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
        if "power_off" in changes:
            self.buttons['power_off'] = changes['power_off']

    def removeController(self):
        self.j = None

    def initController(self):
        print('connecting controller')
        tries = 0
        while(tries < 6):
            if(pygame.joystick.get_count() < 1):
                pygame.joystick.quit()
                pygame.joystick.init()
            else:
                self.j = pygame.joystick.Joystick(0)
                self.j.init()
                break
            time.sleep(0.5)
        print('connected')


    def isControllerPresent(self):
        regex = r"\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}"
        proc = subprocess.Popen(['hcitool', 'con'], stdout=subprocess.PIPE)
        text = proc.stdout.read()

        try:
            found = re.search(regex, text).group(0)
            if(found == "00:07:04:EF:27:55"):
                return True
            else:
                return False
        except AttributeError:
            return False

    def updateSpeed(self, newSpeed):
        print('update speed')
        self.speed = 1500 + (500 * newSpeed)
    
    def OutputButtonValues(self, changes):
        pprint(changes)

    def mainloop(self):
        while(True):
            if not self.isControllerPresent():
                self.removeController()
            else:
                if self.j is None:
                    self.initController()

                changes = self.getInput()
                self.update(changes)
                self.PowerOffPi()
                if(is_debug):
                    self.OutputButtonValues(changes)
            time.sleep(0.1)

    def PowerOffPi(self):
        if self.buttons['power_off'] is 1:
            self.power_off_timer += .1
        else:
            self.power_off_timer = 0
        
        if self.power_off_timer >= 5:
            print('powering down')
            subprocess.call(powerdown)


def main():	
    pygame.init()
    os.putenv('SDL_VIDEODRIVER','fbcon')
    pygame.display.init()
    time.sleep(3.0)

    skate = Skateboard()
    skate.mainloop()
    

if __name__ == "__main__":
	main()