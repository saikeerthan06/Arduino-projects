#sending SMS uing Twilio API

from twilio.rest import Client
import random
import datetime

import geocoder

#below function is to get the location of the arduino.
def location():
    g = geocoder.ip('me')
    return g.city, g.postal  # Get the city name from the geocoder result


#below function is to get the time of the day.
def get_time_of_day():
    current_hour_date = datetime.datetime.now()
    return current_hour_date.strftime("\n %B, %d, %Y %H:%M:%S")

#creating a function to randomise OTP
def generate_otp():
    otp = ""
    for i in range(5):
        otp += str(random.randint(0 ,9))

    return otp

#sending the OTP to the delivry person
def sending_OTP():

    account_sid = 'AC5d3a355c4c211259e28ee6947c1eaa8d'
    auth_token = 'a346d958eea4c16f7e4eac3a6fd61a9e'

    client = Client(account_sid, auth_token)

    otp = generate_otp()

    message = client.messages.create(
        from_= '+17657911854',
        body= f"OTP is {otp}" ,
        to= '+6581838924'


    )

    return otp

#below function is to send a confirmation message to the owner that the parcel has been delivered.
# In the confirmation message, the time, and the location is given, hence we are calling the previosuly defined functions(to retrieve location and time) into this function.
def confirm_message():

    account_sid = 'AC5d3a355c4c211259e28ee6947c1eaa8d'
    auth_token = 'a346d958eea4c16f7e4eac3a6fd61a9e'

    client = Client(account_sid, auth_token)

    time_of_day = get_time_of_day()

    # Get location information
    city, postal_code = location()

    # Create the message content
    message_content = f"Your Parcel has been delivered at {time_of_day} in {city}, Postal Code: {postal_code}"


    message = client.messages.create(
        from_= '+17657911854',
        body= f"{message_content}" ,
        to= '+6581838924'

    )


# This function is created to alert the owner if there is any suspicious activities regarding the box.
# THis function uses the function to retrieve the date, time and location.
def sus_inform(get_time_of_day, location):

    account_sid = 'AC5d3a355c4c211259e28ee6947c1eaa8d'
    auth_token = 'a346d958eea4c16f7e4eac3a6fd61a9e'

    client = Client(account_sid, auth_token)

    time_of_day = get_time_of_day()

    city, postal_code = location()

    message_content = f"There has been suspicious activity on your EZ-Lock at {time_of_day} in {city}, {postal_code}"

    message = client.messages.create(
        from_= '+17657911854',
        body= f"{message_content}" ,
        to= '+6581838924'

    )






#for testing of the functions:
if __name__ == "__main__":
    #confirm_message(get_time_of_day, location)
    sus_inform(get_time_of_day, location)

