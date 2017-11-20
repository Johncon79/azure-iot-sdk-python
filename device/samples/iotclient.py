
import random
import time
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue


#Enter your own credentials!!

# String containing Hostname, Device Id & Device Key in the format
CONNECTION_STRING = "HostName=IOTLabb1.azure-devices.net;DeviceId=Recon;SharedAccessKey="
# choose HTTP, AMQP or MQTT as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
AVG_WIND_SPEED = 10.0
SEND_CALLBACKS = 0
METHOD_CONTEXT = 0
RECEIVE_CONTEXT = 0
METHOD_CALLBACKS = 0
RECEIVE_CALLBACKS = 0

MSG_TXT = "{\"deviceId\": \"MyFirstPythonDevice\",\"windSpeed\": %.2f}"

def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    print ( "    message_id: %s" % message.message_id )
    print ( "    correlation_id: %s" % message.correlation_id )
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_CALLBACKS )

def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    # set the time until a message times out
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    client.set_option("logtrace", 0)
    client.set_device_method_callback(device_method_callback, METHOD_CONTEXT) #Anger vilken metod som anropas för att ta emot Method
    client.set_message_callback(receive_message_callback, RECEIVE_CONTEXT) #Anger vilken medotd för hantering av meddelanden
    return client


def device_method_callback(method_name, payload, user_context): #Hanterar mogganing av Method samt payload
    method=""
    global METHOD_CALLBACKS
    
    print ( "\nMethod callback called with:\nmethodName = %s\npayload = %s\ncontext = %s" % (method_name, payload, user_context) )
    METHOD_CALLBACKS += 1
    print ( "Total calls confirmed: %d\n" % METHOD_CALLBACKS )
    if method_name == "Start":
        print("Starting Service")
    elif method_name == "Stop":
        print("Stopping Service")
    device_method_return_value = DeviceMethodReturnValue()
    device_method_return_value.response = "{ \"Response\": \"This is the response from the device\" }"
    device_method_return_value.status = 200
    return device_method_return_value

def receive_message_callback(message, counter): #Hanterar mottagning av meddelanden till enhet
    global RECEIVE_CALLBACKS
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    print ( "Received Message [%d]:" % counter )
    print ( "    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    counter += 1
    RECEIVE_CALLBACKS += 1
    print ( "    Total calls received: %d" % RECEIVE_CALLBACKS )
    return IoTHubMessageDispositionResult.ACCEPTED



def iothub_client_telemetry_sample_run(): #Main funktion skickar meddelanden 

    try:
        client = iothub_client_init()
        print ( "IoT Device Simulator, press Ctrl-C to exit" )

        
        message_counter = 0
        inp = 0
        while inp != 4:
            print("Press 1 to send a mesage to IOT Hub (Simulated message")
            
            msg_txt_formatted = MSG_TXT % (AVG_WIND_SPEED + (random.random() * 4 + 2))
            # messages can be encoded as string or bytearray

            if (message_counter & 1) == 1:
                message = IoTHubMessage(bytearray(msg_txt_formatted, 'utf8'))
            else:
                message = IoTHubMessage(msg_txt_formatted)
            # optional: assign ids
            message.message_id = "message_%d" % message_counter
            message.correlation_id = "correlation_%d" % message_counter
            # optional: assign properties
            prop_map = message.properties()
            prop_text = "PropMsg_%d" % message_counter
            prop_map.add("Property", prop_text)
            inp = int(input())
            if inp == 1:
                client.send_event_async(message, send_confirmation_callback, message_counter)
                print ( "IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % message_counter )

            #status = client.get_send_status()
            #print ( "Send status: %s" % status )
            #time.sleep(5) # 5 sekunder delay i loopen

            #status = client.get_send_status()
            #print ( "Send status: %s" % status )

            message_counter += 1
            #break # Ta bort för att fortsätta i en loop

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
if __name__ == '__main__':
    print ( "Simulating a device using the Azure IoT Hub Device SDK for Python" )
    print ( "    Protocol %s" % PROTOCOL )
    print ( "    Connection string=%s" % CONNECTION_STRING )

    iothub_client_telemetry_sample_run()  #Function to call efter import