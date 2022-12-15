from paho.mqtt import client as mqtt_client
import json
import time
import serial.tools.list_ports
import keyboard
#libs

broker = "mqtt.tago.io"
port = 1883
topic = "tago/data/post" # topic to send information for visualization and plot on graphical design
topicInfo = "comando/temp" #topic for triggering the action of command
#MQTT Connection Infos

strMsg = []
packet = ""

jsonMsg = {
    "variable": "tempcomando",
    "value": 0,
    "unit": "°C"
}
#My json Info Msg

#variables

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            connected = True
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("armCommand")
    client.on_connect = on_connect
    client.username_pw_set("Default","05cc4aa7-c3e0-4731-b011-79644ac97149")
    client.connect(broker, port)
    
    return client
#connect function

ports = serial.tools.list_ports.comports()

serialInst = serial.Serial()

portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val = input ('Select Port: COM')

print(val)

for x in range(0,len(portList)):
    if portList[x].startswith("COM"+str(val)):
        portVar = "COM"+str(val)
        print(portList[x])
serialInst.baudrate = 115200
serialInst.port = portVar
serialInst.open()
#Opening COM PORT

client = connect_mqtt()
client.loop_start()
#connecting to MQTT Device

while True:
    
    if serialInst.in_waiting:
        packet = serialInst.readline()
        strMsg = (packet.decode('utf-8')).split()
        manda = strMsg[0]
        print(strMsg[0])

        jsonMsg["value"] = int(manda)
        msgSend = json.dumps(jsonMsg)
        #receiving and exctrating relevant information from Serial COM Port

        client.publish(topicInfo, msgSend)
        client.publish(topic, msgSend)
        #Publishing the command temperature to monitoring and graphic topic

    if keyboard.is_pressed('t'):
        newTemp = str(input('Digite a Nova Temperatura: '))
        serialInst.write(bytes(newTemp,'Ansi'))
        #Changing temperature Routine