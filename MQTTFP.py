import sys
import uuid
import paho.mqtt.client as mqtt
import json
import sqlite3

mqtt_user_name ='oauth2-user'
mqtt_password  ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJuczAxIiwic3ViIjoiMjUxNCIsInVzZXJfbmFtZSI6ImFib3VoYXRhYkB5YWhvby5jb20iLCJzY29wZSI6WyJyZWFkLW9ubHkiXSwiZXhwIjoxNjIwNDA5MTE4LCJhdXRob3JpdGllcyI6WyJST0xFX1VTRVIiXSwianRpIjoiZjA0MzIzN2ItZDg3Ny00ZDNjLWExZmYtYWY0NWE3MmJiMDE5IiwiY2xpZW50X2lkIjoicmVhZC1vbmx5In0.u7LcGXSm_cGKWPec7bJOK_7f0fFCe7SLyjcwAx8dbRk' 
user_id        ='2514'
device_id      ='TO136-0202100001000901'
TopicPrefix    ='/v1/users/{user_id}/in/devices/{device_id}/datasources/'.format(user_id=user_id,device_id=device_id)
TopicList      =['ACCELERATION_NORM','WORLD_ACCELERATION_NORM','GYROSCOPE_NORM','ROTATION','HUMIDITY_TEMPERATURE','PRESSURE','HUMIDITY','PROXIMITY','VISIBLE_SPECTRUM_LIGHTNESS','IR_SPECTRUM_LIGHTNESS','MAGNETIC_FIELD_NORM','SOUND_LEVEL']
ca_cert_path   ='/home/pi/Desktop/cacert.crt'

# Setup Database
conn = sqlite3.connect('/home/pi/Desktop/FP.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Data(timestamp INTEGER, topic TEXT, scalar INTEGER)")

# Calculate Altitude from Temprature and Pressure
def Alt(x):
    return int(((int(sys.argv[1])/x)**0.190223-1)*(int(sys.argv[2])*280.4137+128897.8))
    
# Connect and subscribe to topics
def on_connect(client, userdata, flags, rc):
    print('Connected with result code {code}'.format(code=rc))
    for T in TopicList:
        client.subscribe(TopicPrefix+T)
        
# Save data
def on_message(client, userdata, msg):
    for x in json.loads(msg.payload.decode('utf-8')):
        #c.execute("INSERT INTO Data VALUES (?,?,?)",(x['timestamp'],msg.topic.replace(TopicPrefix,''),Alt(round(x['scalar']))))
        #conn.commit()
        if msg.topic.replace(TopicPrefix,'') == 'PRESSURE':
            print(Alt(round(x['scalar'])))
            c.execute("INSERT INTO Data VALUES (?,'ALTITUDE',?)",(x['timestamp'],Alt(round(x['scalar']))))
            conn.commit()
        else: #msg.topic.replace(TopicPrefix,'') =='HUMIDITY_TEMPERATURE':
            # Overwrite NOAA's Temprature since we are no longer on the ground
            T=round(x['scalar'])*9/5+32

client = mqtt.Client(client_id=str(uuid.uuid4()), transport='websockets')
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs=ca_cert_path)
client.username_pw_set(mqtt_user_name, mqtt_password)
client.connect('ns01-wss.brainium.com', 443)
client.loop_forever()
