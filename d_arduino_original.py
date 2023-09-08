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

redLED = controller.buildDigitalOutput(5, 'redLED')

monitor = controller.buildInputMonitor()

controller.start()
monitor.start()



#def send_new_otp():
   # owner_password = SS.sending_OTP()

    #return owner_password

def validate_password():
    owner_password = SS.sending_OTP()
    password = input("Please enter the OTP given to you: ")

    if owner_password == password:
        EZ_lock()


def EZ_lock():
    counter = 1
    #Validation of Password
    #Buzzer On -> indicates door is opening
    print("EZ-Lock is opening...")
    #buzzer.turnOn()
    time.sleep(3)
    #Server Motor runs --> Box Opens
    xMotor.threadTurnTo(180, 100) #lid opens
    #buzzer.turnOff()

    #Infinte while loop -> to ensure the sensors are always working
    while True:
        ir_val = irSensor.getCountValue()
        time.sleep(1)

        if ir_val >= 1:
            print("Parcel detected...")
            redLED.turnOn()
            time.sleep(1)
        #IR sensors constantly check whether blocked or not
                                                                #while irSensor.getCountValue() >= 1:
                                                                    #print("Turning on LED")
                                                                    #redLED.turnOn()
                                                                      # time.sleep(1)
            #when the button is pushed then close the lid
            button_val = button.getCountValue()
            time.sleep(1)
            if button_val == 1:
                print("EZ-Lock is closing...")
                #buzzer.turnOn()
                #time.sleep()
                xMotor.threadTurnTo(0, 100)
                #buzzer.turnOff()
                break
        else:
            #If the box is empty then off the light
            print("EZ-Lock is empty...")
            redLED.turnOff()
            #If button is pushed then close the lid with the buzzer sound, counter == 1 ensures that the lid closes only
            #once when the button is pushed.
            while button.getCountValue() >= 1 and counter == 1:
                print("EZ-Lock is Closing...")
                #buzzer.turnOn()
                time.sleep(1)
                xMotor.threadTurnTo(0, 100)
                #buzzer.turnOff()
                counter  += 1
                break

def second_time():

    s_ask = input("Would you like to place any other items?: ")

    if s_ask == 'y' or s_ask == 'yes':
        main()
    elif s_ask == 'n' or s_ask == 'no':
        print("Thank you for using EZ-Lock! Have a nice day ahead! ")
        SS.confirm_message()
        sys.exit(1)
def main():

     #counter = 1
    ir_val = 0
    max_attempts = 3
    owner_password = SS.sending_OTP()

    for attempt in range(max_attempts):

        if owner_password == password:
            EZ_lock()
            break

        else:
            remaining_attempts = max_attempts - attempt

            if remaining_attempts == 0:
                print(f'You have exceeded the number of attempts, you are locked out! Owner is notified!')
                SS.sus_inform()
                sys.exit(1)

            else:
                if 0 < remaining_attempts < 3:
                    a_input = input(f"You have {remaining_attempts} left, would you like to try again? ")

                    if a_input == 'yes' or a_input == 'y':
                        continue
                        #validate_password()

                    elif a_input == 'no' or a_input == 'n':
                        print("You are locked out! Owner is notified of this suspicious activity! ")
                        SS.sus_inform()
                        sys.exit(1)

    ir_val = irSensor.getCountValue()

    if ir_val >= 1:
        second_time()
    else:
        sys.exit(1)
        pass


if __name__ == "__main__":
    main()







#controller.shutdown()
