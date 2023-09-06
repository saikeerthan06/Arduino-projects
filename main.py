from AADFramework.ArduinoComponents import ServoMotor, DigitalInput, DigitalOutput, ControlBoard, InputMonitor
from AADFramework.ArduinoComponents import menuGenerator
import sys
import SMS_sending as SS

controller = ControlBoard('COM4')

buzzer = controller.buildDigitalOutput(10, 'Buzzer')
button = controller.buildDigitalInput(9, 'Button')
irSensor = controller.buildDigitalInput(6, 'irSensor')
xMotor = controller.buildServoMotor(8, 'xMotor')
redLED = controller.buildDigitalOutput(2, 'redLED')

xMotor.homePos = 0
xMotor.minAngle = 0
xMotor.maxAngle = 180


counter = 1
monitor = controller.buildInputMonitor()
controller.start()
monitor.start()

def send_new_otp():
    owner_password = SS.sending_OTP()

    return owner_password


def EZ_Lock():
    counter = 1
    max_attempts = 3
    owner_password = send_new_otp()

    for attempt in range(max_attempts):
        password = input("Please enter the OTP sent to your phone number: ")

        if owner_password == password:
            print("wer")
            # EZ_Lock will open (Servo Motor will turn to open the lid)
            xMotor.threadTurnTo(180, 100)  # Code for the servoMotor to turn

            while irSensor.getCountValue() >= 1:
                redLED.turnOn()

            if counter == 1:
                while button.getCountValue() >= 1:
                     xMotor.threadTurnTo(0, 100)  # Lid closes once the button is pushed.
                break  # Exit the EZ_Lock function and go to the second_time function

            break  # Exit the EZ_Lock function and go to the second_time function

        else:
            remaining_attempts = max_attempts - 1 - attempt

            if remaining_attempts == 0:
                print("Maximum number of attempts have been reached! You are locked out! Owner is notified!")
                SS.sus_inform()
                sys.exit()

            a_input = input(f"Incorrect Password! You have {remaining_attempts} attempt(s) left. Would you like to try again? (yes/no): ")
            if (a_input == 'y') or (a_input == 'yes'):
                owner_password = send_new_otp()
                continue
            elif (a_input == 'n') or (a_input == 'no'):
                print("Owner has been notified of this suspicious activity!")
                SS.sus_inform()
                sys.exit()


    # Run the second_time function when the correct password is entered
    second_time()

def second_time():
    while True:
        q_input = input("Would you like to place any other item? ")
        if (q_input == 'y') or (q_input == 'yes'):
            EZ_Lock()

        elif (q_input == 'n') or (q_input == 'no'):
            print("Thank you for using EZ-Lock! Have a great day ahead!")
            SS.confirm_message()
            sys.exit()

if __name__ == "__main__":
    EZ_Lock()  # Start with the EZ_Lock function
