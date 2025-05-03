import paho.mqtt.publish as publish
import psutil
import string

# The ThingSpeak Channel ID.
# Replace <YOUR-CHANNEL-ID> with your channel ID.
channel_ID = "<YOUR-CHANNEL-ID>"

# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt3.thingspeak.com"

# Your MQTT credentials for the device
mqtt_client_ID = "<YOUR-CLIENT-ID>"
mqtt_username  = "<YOUR-USERNAME>"
mqtt_password  = "<YOUR-MQTT-PASSWORD>"

t_transport = "websockets"
t_port = 80

# Create the topic string.
topic = "channels/" + channel_ID + "/publish"

while (True):

    # get the system performance data over 20 seconds.
    cpu_percent = psutil.cpu_percent(interval=20)
    ram_percent = psutil.virtual_memory().percent

    # build the payload string.
    payload = "field1=" + str(cpu_percent) + "&field2=" + str(ram_percent)

    # attempt to publish this data to the topic.
    try:
        print ("Writing Payload = ", payload," to host: ", mqtt_host, " clientID= ", mqtt_client_ID, " User ", mqtt_username, " PWD ", mqtt_password)
        publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})
    # except (keyboardInterrupt)
    #     break
    except Exception as e:
        print (e)