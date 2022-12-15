# Bibliotecas utilizadas
from paho.mqtt import client as mqtt_client
import time
import keyboard
import json
import serial.tools.list_ports
import serial

# Variveis utilizadas
i = 0
broker = "mqtt.tago.io"
port = 1883
topic = "tago/data/post"
topicCommand = "temp/receive"
jsonMsg = {
    "variable": "realTemp",
    "value": 0,
    "unit": "°C"
}
msgSend = ""
strMsg = []
packet = ""
temperatura = 0


# Função de conexão com MQTT
def connect_mqtt() -> mqtt_client:
    # Função que confirma a conexão com o MQTT
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            connected = True
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("armReceive")
    client.on_connect = on_connect
    client.username_pw_set("Default","338d6620-7ca9-4b41-843f-f74c16f2305e")
    client.connect(broker, port)
    
    return client

# Função para inscrição nos topicos
def subscribe(client: mqtt_client):
    # Função para exibição de conteúdo recebido
    def on_message(client, userdata, msg):
        recado = msg.payload.decode("utf-8")
        
        temperatura = int(recado)
        # print("Mudando a temperatura para: ")
        print(temperatura)
        
        serialInst.write(bytes(str(temperatura),'Ansi'))
    
    client.subscribe(topicCommand) # Subscribe to Both topics
    client.on_message = on_message #Callback to function on_message

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
#Opening COM PORT
serialInst.baudrate = 115200
serialInst.port = portVar
serialInst.open()

client = connect_mqtt()
client.loop_start()
time.sleep(1)
subscribe(client)
# Connect and subscribe to MQTT


while True:
    i = i + 1
    
    if serialInst.in_waiting: #Verficia se a algo para ser recebido via serial
        #   Lê e trata o conteúdo da serial
        packet = serialInst.readline()
        strMsg = (packet.decode('utf-8')).split()
        
        # Exibe o conteudo da serial para verificação "humana" e o envia ao dashboard
        manda = strMsg[0]
        print(strMsg[0])
        jsonMsg["value"] = float(manda)
        msgSend = json.dumps(jsonMsg)
        client.publish(topic,msgSend)