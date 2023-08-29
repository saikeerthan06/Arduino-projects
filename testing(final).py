import sys
import time
#from AADFramework.ArduinoComponents import ServoMotor, DigitalInput, DigitalOutput, ControlBoard, InputMonitor
#from AADFramework.ArduinoComponents import menuGenerator
import SMS_sending as SS

#Instantiating the controller
controller = ControlBoard('COM4')

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




def EZ_lock():
    owner_password = SS.sending_sms()
    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        password = str(input("Please enter the OTP given to you: "))
        counter = 1

        if owner_password == password:  #person enters password
             #Buzzer On -> indicates door is opening
            print("EZ-Lock is opening...")
            buzzer.turnOn()
            time.sleep(1) #buzzer buzzes for one second
            #Server Motor runs --> Box Opens
            xMotor.threadTurnTo(180, 100) #lid opens
            buzzer.turnOff()
            while True:
            #IR sensors constantly check whether blocked or not
                while irSensor.getCountValue() >= 1:
                    print("Turning on LED")
                    redLED.turnOn()
                    time.sleep(1)
                    #when the button is pushed then close the lid
                    if counter == 1:
                        while button.getCountValue() >= 1:
                            print("EZ-Lock is closing...")
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
                        counter += 1
                        break

        else:
            print(f"Wrong Password! You have {max_attempts - attempt} attempt(s) left")
            if attempt < max_attempts:
                a_input = input("Would you like to try again(y/n)?: ").lower()

                if (a_input == 'y') or (a_input == 'yes'):
                    EZ_lock()

                elif (a_input == 'n') or (a_input == 'no'):
                    print("Owner has been notified of this activity!")
                    SS.sus_inform(SS.get_time_of_day, SS.location)
                    sys.exit()
            else:
                print("Sorry! You have reached maximum number of attempts! Please contact the owner!")
                print("Owner has been notified of this activity!")
                SS.sus_inform(SS.get_time_of_day, SS.location)


def second_time(get_time_of_day, location):
    while True:
        retry = input("Would you like to add any other items?(y/n): ").lower()

        if (retry == 'y') or (retry == 'yes'):
            EZ_lock()

        elif (retry == 'n') or (retry == 'no'):
            print("Thank you for using EZ_lock! The owner is notified!")
            print(f"{get_time_of_day()} and {location()}")
            SS.confirm_message(get_time_of_day(), location())
            SS.get_time_of_day()
            sys.exit()

if __name__ == "__main__":
    EZ_lock()
    second_time(SS.get_time_of_day, SS.location)

