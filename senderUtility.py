import os
import json
import base64
import ssl
import time
import random
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTT_ERR_SUCCESS
from datetime import datetime

TOPIC_ALIAS_MAX = 0

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

def on_message(client, userdata, msg):
    print(f"Received message: topic: {msg.topic}, payload: {msg.payload.decode()}")

def publish_image(client, folder_path, filename, topic, variables_topic, foto_number):
    try:
        print(f"Publishing image: {filename}")
        file_path = os.path.join(folder_path, filename)
        serial_number, batch_number, foto_number = extract_values_from_filename(filename, foto_number)
        print(f"Serial number: {serial_number}, Batch number: {batch_number}, Foto number: {foto_number}")

        with open(file_path, "rb") as file:
            file_size = os.path.getsize(file_path)
            print(f"Image size: {file_size} bytes")

            chunk_size = 1024*2  # Adjust chunk size as needed
            total_parts = (file_size + chunk_size - 1) // chunk_size

            for i in range(total_parts):
                part_number = i + 1
                part_string = f"{part_number}/{total_parts}"
                print(f"Processing part {part_string}")

                # Read chunk from file
                buffer = file.read(chunk_size)
                bytes_read = len(buffer)
                print(f"Read {bytes_read} bytes from file")

                if bytes_read > 0:
                    # Encode image chunk to base64
                    base64_data = base64.b64encode(buffer).decode('utf-8')

                    # Create JSON document
                    json_document = {
                        "devInfo": {
                            "S": serial_number,
                            "Batch": batch_number,
                            "foto": foto_number,
                            "part": part_string
                        },
                        "data": base64_data
                    }

                    # Publish via MQTT
                    full_topic = f"{topic}/{variables_topic}"
                    client.publish(full_topic, json.dumps(json_document))
                    print(f"Published part {part_string} to MQTT topic {full_topic}")
                    time.sleep(0.25)

    except Exception as e:
        print(f"Error publishing image: {e}")

def extract_values_from_filename(filename, foto_number):
    parts = filename.split("_")
    if len(parts) == 3:
        serial_number, batch_number, foto_number = parts[0], int(parts[1]), int(parts[2].split(".")[0])
        return serial_number, batch_number, foto_number
    else:
        print(f"Invalid filename format: {filename}")
        return None, None, None
    
def on_publish(client, userdata, mid):
    print("Message published")

def on_disconnect(client, userdata, rc, properties=None):
    print("Disconnected with result code", rc)

def on_log(client, userdata, level, buf):
    print(f"Log: {buf}")

#Script 
folder_path = "Fotos"
topic = "alpha"
variables_topic = "pub"
mqtt_server = "a320jkm5cscowr-ats.iot.us-west-2.amazonaws.com"
mqtt_port = 8883  # Default MQTT over TLS port
initial_foto_number = 1  # Initial foto number

# Initialize MQTT client with TLS/SSL encryption
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)

# Set TLS context with certificate and key files
root_ca_path = os.path.join("Certificados", "AmazonRootCA1.pem")  # Use either AmazonRootCA1.pem or AmazonRootCA3.pem
cert_path = os.path.join("Certificados", "device001-certificate.pem.crt")
key_path = os.path.join("Certificados", "device001-private.pem.key")
client.tls_set(root_ca_path, certfile=cert_path, keyfile=key_path, cert_reqs=ssl.CERT_REQUIRED)

# Set callback functions
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.on_log = on_log

# Connect to AWS IoT Core broker
rc = client.connect(mqtt_server, 8883, 60)

# Loop to keep the client running
client.loop_start()

if rc != MQTT_ERR_SUCCESS:
    print(f"Failed to connect to broker with result code: {rc}")
else:
    time.sleep(5)  # Wait for the client to establish the connection

print("Is connected:", client.is_connected())

send_first_image_only = True

# Iterate over files in the folder
foto_number = initial_foto_number
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg"):
        if client.is_connected():
            publish_image(client, folder_path, filename, topic, variables_topic, foto_number)
            foto_number += 1
            time.sleep(10) # Wait between images
        else:
            print("MQTT client is not connected")
            break

        if send_first_image_only:
            break

# Disconnect MQTT client
client.disconnect()
