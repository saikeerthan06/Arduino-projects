import time
from AADFramework.ArduinoComponents import ServoMotor, DigitalInput, DigitalOutput, ControlBoard, InputMonitor
from AADFramework.ArduinoComponents import menuGenerator
import sys
#Instantiating the controller
controller = ControlBoard('COM3')

#Instantiating the components
buzzer = controller.buildDigitalOutput(10, 'Buzzer')
button = controller.buildDigitalInput(9, 'Button')
irSensor = controller.buildDigitalInput(6, 'irSensor')
xMotor = controller.buildServoMotor(8, 'xMotor')

#Setting default values to the servo motor
xMotor.homePos = 0
xMotor.minAngle = 0
xMotor.maxAngle = 180

redLED = controller.buildDigitalOutput(2, 'redLED')

monitor = controller.buildInputMonitor()

controller.start()
monitor.start()

owner_password = "Hello"
password = str(input("Please enter the password given to you: "))
counter = 1

#Validation of Password
if owner_password == password:  #person enters password
    #Buzzer On -> indicates door is opening
    print("Buzzer on")
    buzzer.turnOn()
    time.sleep(1)
    #Server Motor runs --> Box Opens
    xMotor.threadTurnTo(180, 100) #lid opens
    buzzer.turnOff()

    #Infinte while loop -> to ensure the sensors are always working
    while True:
        #IR sensors constantly check whether blocked or not
        while irSensor.getCountValue() >= 1:
            print("Turning on LED")
            redLED.turnOn()
            time.sleep(1)
            #when the button is pushed then close the lid
            if counter == 1:
                while button.getCountValue() >= 1:
                    print("Button is on")
                    buzzer.turnOn()
                    time.sleep(1)
                    xMotor.threadTurnTo(0, 100)
                    buzzer.turnOff()
        else:
            #If the box is empty then off the light
            print("Light Off")
            redLED.turnOff()
            print("Button Prep")
            #If button is pushed then close the lid with the buzzer sound, counter == 1 ensures that the lid closes only
            #once when the button is pushed.
            while button.getCountValue() >= 1 and counter == 1:
                print("Button is on")
                buzzer.turnOn()
                time.sleep(1)
                xMotor.threadTurnTo(0, 100)
                buzzer.turnOff()
                counter  += 1
                break
else:
    print("Wrong Password! You have been locked out!")









#controller.shutdown()
