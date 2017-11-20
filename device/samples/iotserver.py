
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import sys
import iothub_service_client
from iothub_service_client import IoTHubDeviceMethod, IoTHubError
from iothub_service_client_args import get_iothub_opt, OptionError

# String containing Hostname, SharedAccessKeyName & SharedAccessKey in the format:
# "HostName=<host_name>;SharedAccessKeyName=<SharedAccessKeyName>;SharedAccessKey=<SharedAccessKey>"
CONNECTION_STRING = "HostName=IOTLabb1.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey="
DEVICE_ID = "Recon"

METHOD_NAME = ""
METHOD_PAYLOAD = ""
TIMEOUT = 60


def iothub_devicemethod_sample_run():

    try:
        print("Send Method to IOT Device, input Start or Stop: ")
        print("Press 1 to Start the service or 2 to stop it: ")
        while True:

            inp = int((input()))
            if inp == 1:
                METHOD_NAME="Start"
                METHOD_PAYLOAD = "{\"StartService\":\"42\"}"
            elif inp == 2:
                METHOD_NAME="Stop"
                METHOD_PAYLOAD = "{\"StopService\":\"42\"}"
            iothub_device_method = IoTHubDeviceMethod(CONNECTION_STRING)

            response = iothub_device_method.invoke(DEVICE_ID, METHOD_NAME, METHOD_PAYLOAD, TIMEOUT)

            print ( "" )
            print ( "Device Method called" )
            print ( "Device Method name       : {0}".format(METHOD_NAME) )
            print ( "Device Method payload    : {0}".format(METHOD_PAYLOAD) )
            print ( "" )
            print ( "Response status          : {0}".format(response.status) )
            print ( "Response payload         : {0}".format(response.payload) )

        
        try:
            # Try Python 2.xx first
            raw_input("Press Enter to continue...\n")
        except:
            pass
            # Use Python 3.xx in the case of exception
            input("Press Enter to continue...\n")

    except IoTHubError as iothub_error:
        print ( "" )
        print ( "Unexpected error {0}".format(iothub_error) )
        return
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )


def usage():
    print ( "Usage: iothub_devicemethod_sample.py -c <connectionstring> -d <device_id>" )
    print ( "    connectionstring: <HostName=<host_name>;SharedAccessKeyName=<SharedAccessKeyName>;SharedAccessKey=<SharedAccessKey>>" )
    print ( "    deviceid        : <Existing device ID to call a method on>" )


if __name__ == '__main__':
    print ( "" )
    print ( "Python {0}".format(sys.version) )
    print ( "IoT Hub Service Client for Python" )
    print ( "" )

    try:
        (CONNECTION_STRING, DEVICE_ID) = get_iothub_opt(sys.argv[1:], CONNECTION_STRING, DEVICE_ID)
    except OptionError as option_error:
        print ( option_error )
        usage()
        sys.exit(1)

    print ( "Starting the IoT Hub Service Client DeviceMethod Python sample..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )

    iothub_devicemethod_sample_run()