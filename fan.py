from time import *
from grovepi import *
from grove_rgb_lcd import *
from pyrebase import pyrebase
from datetime import datetime

config = {
   "apiKey": "AIzaSyAAIFFX8ukW1TCdmzE6-Z_iMBNOfrWcV6I",
   "authDomain": "project1-d4377.firebaseapp.com",
   "databaseURL": "https://project1-d4377-default-rtdb.firebaseio.com",
   "storageBucket": "project1-d4377.appspot.com"
  };

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

dhtsensor = 7

blue_temp = 20
green_temp = 25
red_temp = 30

pinMode(dhtsensor, "INPUT")
now = datetime.now()
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
timestamp = int(time.time())
data2 = {
"Time": f"{date_time_str}",
"From": "Fan"
}
tag = f"{timestamp}_{date_time_str}_Fan"
db.child("summary").child(tag).set(data2)

while True:
    try:
        status2 = db.child("iot").get().val()
        value = status2["true"]
        
        sleep(0.5)
        [temp, hum] = dht(dhtsensor, 0)
        data = {"Temperature":str(temp),
                "Humidity":str(hum)}
        
        db.child("Fan").update(data)
        t = str(temp)
        
        myData = db.child("Fan").get().val()
        status = myData["Status"]
        Fan= db.child("Fan").get().val()
        mode = myData["Mode"]
       
        if int(status) == 0 or int(value) == 0:
            Fan1= db.child("Fan").get().val()
            device = myData["Device"]
            print(device)
            if int(device) == 0:
                if temp < blue_temp:
                    setRGB(0, 0, 255)
                elif temp < green_temp:
                    setRGB(0, 255, 0)
                    print("Temp = ", temp, '\u00b0C', " Fan speed = 1 ")
                    setText("Temp = " + t + '\337' + "C   Fan speed = 1 ")
                elif temp < red_temp:
                    setRGB(255, 165, 0)
                    print("Temp = ", temp, '\u00b0C', " Fan speed = 2 ")
                    setText("Temp = " + t + '\337' + "C   Fan speed = 2 ")
                else:
                    setRGB(255, 0, 0)
                    print("Temp = ", temp, '\u00b0C', " Fan speed = 3 ")
                    setText("Temp = " + t + '\337' + "C   Fan speed = 3 ")
            else:
                if int(mode) == 2:
                    setRGB(0, 255, 0)
                    setText("Fan speed = 1")
                    print("Fan speed = 1")
                elif int(mode) == 3:
                    setRGB(255, 165, 0)
                    setText("Fan speed = 2")
                    print("Fan speed = 2")
                elif int(mode) == 4:
                    setRGB(255, 0, 0)
                    setText("Fan speed = 3")
                    print("Fan speed = 3")
        elif int(status) == 1:
            setRGB(0, 0, 0)
            setText("Fan Off")
            print("Fan Off")
            time.sleep(1.5)
       
    except KeyboardInterrupt:
        setText("Program Exited")
        break