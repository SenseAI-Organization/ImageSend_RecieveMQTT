import os
import json
import base64
import ssl
import time
import random
import csv
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTT_ERR_SUCCESS
from datetime import datetime

###Variables Importadas InOva
establecimiento = "Sense AI"
propietario = "Daniel Escobar"

TOPIC_ALIAS_MAX = 0

def check_and_save_image(part_number, total_parts, image_data, filepath):
    # Check if the current part is the last part
    print("Saving part" + str(part_number) + "...")
    if part_number >= (total_parts - 3):
        # Check if all parts are received
        if all(image_data): 
            # Reconstruct the image and save it
            image = b''.join(image_data)

            # Create subfolder if it doesn't exist
            directory = os.path.dirname(filepath)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(filepath, 'wb') as f:
                f.write(image)
            print('Image received and saved')

            # Save image_data to a CSV file ///COMENTAR O ELIMINAR
            with open(filepath + '.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(image_data)
            # FIN COMENTAR O ELIMINAR

            # Reset image_data for next image
            image_data = [None] * total_parts
            filepath = None
        else:
            # Find and print the missing parts
            missing_parts = [i+1 for i, part in enumerate(image_data) if part is None]
            print(f"Missing parts: {missing_parts}")
    return image_data, filepath
 
def on_connect(client, userdata, flags, rc, properties=None):
    global TOPIC_ALIAS_MAX
    print(f"Connected to endpoint {mqtt_server} with result code {rc}")
    print(f"Userdata: {userdata}, flags: {flags}, properties: {properties}")
    if properties:
        TOPIC_ALIAS_MAX = properties.TopicAliasMaximum
        print(f"Topic alias maximum: {TOPIC_ALIAS_MAX}")
    client.is_connected = True
    print(f'Subscribing to topic: {topic}')
    client.subscribe(topic, qos=0, options=None, properties=None)

def on_disconnect(client, userdata, rc, properties=None):
    print("Disconnected with result code", rc)

def on_log(client, userdata, level, buf):
    print(f"Log: {buf}")

def on_message(client, userdata, msg):
    global image_data
    global filepath
    try:
        data = json.loads(msg.payload.decode())
        part_number, total_parts = map(int, data['devInfo']['part'].split('/'))
        base64_data = data['data']

        # If this is the first part, initialize image_data with the correct size
        if part_number == 1:
            image_data = [None] * total_parts
            serial_number = data['devInfo']['S']
            output_folder = serial_number
            batch_number = data['devInfo']['Batch']
            foto_number = data['devInfo']['foto']
            # Construct the filename
            filename = f"{serial_number}-{batch_number}-{foto_number}.jpg"
            filepath = os.path.join(output_folder, filename)
            print(f"Receiving image {filename} in {total_parts} parts")

        # Decode base64 image data
        image_part = base64.b64decode(base64_data)

        # Store image data in the appropriate part of the image_data list
        image_data[part_number - 1] = image_part # /000111/000111-1-1.txt

        image_data, filepath = check_and_save_image(part_number, total_parts, image_data, filepath)

    except Exception as e:
        print(f"Error processing message: {e}")


#Script  config
folder_path = "Fotos"
topic = "alpha"
variables_topic = "pub"
mqtt_server = "a320jkm5cscowr-ats.iot.us-west-2.amazonaws.com"
mqtt_port = 8883  # Default MQTT over TLS port

# Set TLS context with certificate and key files
root_ca_path = os.path.join("Certificados", "AmazonRootCA1.pem")  # Use either AmazonRootCA1.pem or AmazonRootCA3.pem
cert_path = os.path.join("Certificados", "device001-certificate.pem.crt")
key_path = os.path.join("Certificados", "device001-private.pem.key")

# Initialize MQTT client with TLS/SSL encryption
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
client.tls_set(root_ca_path, certfile=cert_path, keyfile=key_path, cert_reqs=ssl.CERT_REQUIRED)

# Set callback functions
client.on_publish = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_log = on_log

# Connect to AWS IoT Core broker
rc = client.connect(mqtt_server, 8883, 60)

# Subscribe to the topic for image data
client.subscribe(f"{topic}/{variables_topic}")

# Loop to keep the client running
client.loop_forever()

if rc != MQTT_ERR_SUCCESS:
    print(f"Failed to connect to broker with result code: {rc}")
else:
    time.sleep(5)  # Wait for the client to establish the connection

print("Is connected:", client.is_connected())