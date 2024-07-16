import time
from grovepi import *
from grove_rgb_lcd import *
from pyrebase import pyrebase
from datetime import datetime

config = {
   "apiKey": "AIzaSyAAIFFX8ukW1TCdmzE6-Z_iMBNOfrWcV6I",
   "authDomain": "project1-d4377.firebaseapp.com",
   "databaseURL": "https://project1-d4377-default-rtdb.firebaseio.com",
   "storageBucket": "project1-d4377.appspot.com"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

blue_temp = 20
red_temp = 30

# Connect the Grove Light Sensor to A0 and the Grove Buzzer to D2
light_sensor = 0
buzzer = 2

# Set pin mode for the buzzer
pinMode(buzzer, "OUTPUT")

# Set the threshold for the light sensor to trigger the buzzer
light_threshold = 100000
now = datetime.now()
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
timestamp = int(time.time())
data = {
"Time": f"{date_time_str}",
"From": "Curtain"
}
tag = f"{timestamp}_{date_time_str}_Curtain"
db.child("summary").child(tag).set(data)

while True:
    try:
        # Read the value from the light sensor
        light_value = analogRead(light_sensor)

        # If the light value is greater than the threshold, activate the buzzer
        if light_value > light_threshold:
            digitalWrite(buzzer, 1)
            result = db.child("Curtain").update({"Brightness":str(light_value)})
            result2 = db.child("Curtain").update({"Condition":"Close"})
            print("Light Value: ", light_value)
            print("Curtain is close.")
        else:
            digitalWrite(buzzer, 0)
            result = db.child("Curtain").update({"Brightness":str(light_value)})
            result2 = db.child("Curtain").update({"Condition":"Open"})
            print("Light Value: ", light_value)
            print("Curtain is open.")
        
        myData = db.child("IoTAssignment").get().val()
        condition = myData["Condition"]
        status = db.child("iot").get().val()
        value = status["true"]

        
        time.sleep(0.5)
        
        if int(condition) == 0 or condition == '0' or int(value) == 0 :
            setRGB(0, 0, 255)
        elif int(condition) == 1 or condition == '1':
            setRGB(255, 165, 0)
        
    except KeyboardInterrupt:
        # Turn off the buzzer if the user interrupts the program
        digitalWrite(buzzer, 0)
        break
    except IOError:
        print("Error")