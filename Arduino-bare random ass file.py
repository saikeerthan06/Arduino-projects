import time
from AADFramework.ArduinoComponents import ServoMotor, DigitalInput, DigitalOutput, ControlBoard, InputMonitor
from AADFramework.ArduinoComponents import menuGenerator
import sys

import SMS_sending as SS

#Instantiating the controller
controller = ControlBoard('COM4')

#Instantiating the components
#buzzer = controller.buildDigitalOutput(10, 'Buzzer')
button = controller.buildDigitalInput(9, 'Button')
irSensor = controller.buildDigitalInput(6, 'irSensor')
xMotor = controller.buildServoMotor(8, 'xMotor')

#Setting default values to the servo motor
xMotor.homePos = 0
xMotor.minAngle = 0
xMotor.maxAngle = 180

redLED = controller.buildDigitalOutput(12, 'redLED')

monitor = controller.buildInputMonitor()

controller.start()
monitor.start()

def send_new_otp():
    owner_password = SS.sending_OTP()

    return owner_password


def EZ_Lock():
    max_attempts = 3
    owner_password = send_new_otp()
    counter = 1

    password = input("Please enter the OTP sent to you: ")

    for attempt in range(max_attempts):
    #Validation of Password
        if owner_password == password:  #person enters password
            #Buzzer On -> indicates door is opening
            print("EZ-Lock is opening...")
            #Server Motor runs --> Box Opens
            xMotor.threadTurnTo(180, 100) #lid opens

            #Infinte while loop -> to ensure the sensors are always working
            while True:
                #IR sensors constantly check whether blocked or not
                while irSensor.getCountValue() >= 1:
                    print("Parcel detected...")
                    redLED.turnOn()
                    #when the button is pushed then close the lid
                    if counter == 1:
                        while button.getCountValue() >= 1:
                            print("Button pressed...")
                            #buzzer.turnOn()
                            time.sleep(1)
                            print("EZ-Lock is closing...")
                            xMotor.threadTurnTo(0, 100)
                            #buzzer.turnOff()
                        break
                else:
                    #If the box is empty then off the light
                    print("Light Off")
                    redLED.turnOff()
                    print("Button Prep")
                    #If button is pushed then close the lid with the buzzer sound, counter == 1 ensures that the lid closes only
                    #once when the button is pushed.
                    while button.getCountValue() >= 1 and counter == 1:
                        print("Button is on")
                        #buzzer.turnOn()
                        time.sleep(1)
                        xMotor.threadTurnTo(0, 100)
                        #buzzer.turnOff()
                        counter  += 1
                        break
                break
        else:
            remaining_attempts = max_attempts - attempt

            if remaining_attempts == 0:
                print("Sorry! Maximum number of attempts reached, you are locked out!")
                print("Owner is notified!")
                SS.sus_inform()
                sys.exit()

            a_input = input(f"Incorrect Password! You have {remaining_attempts} attempt(s) left, do you want to try again? (yes/no): ")

            if (a_input == 'y') or (a_input == 'yes'):
                owner_password = send_new_otp()
                continue

            elif (a_input == 'n') or (a_input == 'no'):
                print("You are now locked out! Owner is notified of this activity! ")
                SS.sus_inform()
                sys.exit()

    second_time()


def second_time():

    if button.getCountValue() < 1:
        print("Please press button to close the EZ-Lock...")
        if button.getCountValue() >= 1:
            xMotor.threadTurnTo(0, 100)


    while True:
        q_input = input("Would you like to add any other items?: ")

        if q_input == 'yes' or q_input == 'y':
            EZ_Lock()

        elif q_input == 'n' or q_input == 'no':
            print("Thank you for using EZ-lock! Have a great day ahead!")
            SS.confirm_message()
            sys.exit()




if __name__ == "__main__":
    EZ_Lock()





#controller.shutdown()
