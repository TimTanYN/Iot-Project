import time
import grovepi
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


sensor = 2
led = 4


grovepi.pinMode(sensor, "INPUT")
grovepi.pinMode(led, "OUTPUT")
now = datetime.now()
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
timestamp = int(time.time())
data = {
"Time": f"{date_time_str}",
"From": "Bed"
}
tag = f"{timestamp}_{date_time_str}_Bed"
db.child("summary").child(tag).set(data)

while True:
    try:
        
        myData = db.child("IOTASS").get().val()
        this = myData["Touch"]
        mit = myData["Mit"]
        value = grovepi.digitalRead(sensor)
        print(this);
        
        while mit == 0 or mit == '0':
        
            while value == 1:
                data ={"Touch": 1,
                       "Mit": 0,
                       "Status":"On"
                       }
                db.child("IOTASS").set(data)
                break
            while value == 0:
                data ={"Touch": 0,
                       "Mit": 0,
                       "Status":"Off"
                       }
                db.child("IOTASS").set(data)
                break
        
            break
        
        while mit == 1 or mit == '1':
            
            data ={"Touch": 1,
                   "Mit": 1,
                   "Status":"On"
                    }
            db.child("IOTASS").set(data)
            db.child("IoTAssignment").update({"Condition":"0"})
            break
        
        while this == 1 or this == '1':
            grovepi.digitalWrite(led, 1)
            print("LED ON")
            db.child("IoTAssignment").update({"Condition":"0"})
            break
            
        while this == 0 or this == '0':
            grovepi.digitalWrite(led, 0)
            print("LED off")
            break
            
    except KeyboardInterrupt:
        break
    except IOError:
        print("Error")