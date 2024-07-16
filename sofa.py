import time
import pyrebase
from grove_rgb_lcd import *
from grovepi import *
from datetime import datetime

config = {
   "apiKey": "AIzaSyAAIFFX8ukW1TCdmzE6-Z_iMBNOfrWcV6I",
   "authDomain": "project1-d4377.firebaseapp.com",
   "databaseURL": "https://project1-d4377-default-rtdb.firebaseio.com",
   "storageBucket": "project1-d4377.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
key = 'sensor'
last_value = 1
rotary_sensor =0
pinMode(rotary_sensor,"INPUT")
now = datetime.now()
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
timestamp = int(time.time())
data = {
"Time": f"{date_time_str}",
"From": "Sofa"
}
tag = f"{timestamp}_{date_time_str}_Sofa"
db.child("summary").child(tag).set(data)

while True:
    status = db.child("iot").get().val()
    value = status["true"]
    if int(value) != last_value:
        print(last_value)
        print("New value detected: {}".format(value))
        rotary_value = analogRead(rotary_sensor)

        # Map the rotary value (0-1023) to the color range (0-255)
        green = int(rotary_value * 255 / 1023)
        red = 0
        blue = 255-green

        setRGB(red, green, blue)
        
        db.child('angle').update({'Green':green ,'Blue':blue})
        mode = db.child("iot").get().val()
        val = mode["Mode"]
        if int(val) == 1:
            timestamp = int(time.time())
            if int(green)<= 255 and int(green) >= 200 and int(blue)<=55:
                db.child('iot').update({'mode': 1})
                setText("Mode 1")
                data = {
                    "Mode": "1",
                    "Time": f"{date_time_str}",
                    "From": "Sensor"
                        }
                tag = f"{timestamp}_{date_time_str}_Sensor"
                db.child("record").child(tag).set(data)
            elif int(green) >= 150 and int(green)<=199 and int(blue) >=56 and int(blue) <= 106:
                db.child('iot').update({'mode':2})
                setText("Mode 2")
                timestamp = int(time.time())
                data = {
                    "Mode": "2",
                    "Time": f"{date_time_str}",
                    "From": "Sensor"
                        }
               
                tag = f"{timestamp}_{date_time_str}_Sensor"
                db.child("record").child(tag).set(data)
            elif int(green) >= 100 and int(green)<=149 and int(blue) >=107 and int(blue) <= 157:
                db.child('iot').update({'mode':3})
                setText("Mode 3")
                timestamp = int(time.time())
                data = {
                    "Mode": "3",
                    "Time": f"{date_time_str}",
                    "From": "Sensor"
                        }
               
                tag = f"{timestamp}_{date_time_str}_Sensor"
                db.child("record").child(tag).set(data)
            elif int(green) >= 50 and int(green)<=99 and int(blue) >=158 and int(blue) <= 208:
                db.child('iot').update({'mode':4})
                setText("Mode 4")
                timestamp = int(time.time())
                data = {
                    "Mode": "4",
                    "Time": f"{date_time_str}",
                    "From": "Sensor"
                        }
               
                tag = f"{timestamp}_{date_time_str}_Sensor"
                db.child("record").child(tag).set(data)
            else:
                db.child('iot').update({'mode':5})
                setText("Mode 5")
                timestamp = int(time.time())
                data = {
                    "Mode": "5",
                    "Time": f"{date_time_str}",
                    "From": "Sensor"
                        }
               
                tag = f"{timestamp}_{date_time_str}_Sensor"
                db.child("record").child(tag).set(data)
        else:
            modes = db.child("IOT_Control_4Load").get().val()
            values = modes["Green"]
            setText(f" App\nMode: {values}")
            timestamp = int(time.time())
            data = {
                    "Mode": f"{values}",
                    "Time": f"{date_time_str}",
                    "From": "App"
                        }
               
            tag = f"{timestamp}_{date_time_str}_App"
            db.child("record").child(tag).set(data)
        
        time.sleep(0.5)
    else:
        setRGB(255,0,0)
        setText("OFF")
        time.sleep(1.5)