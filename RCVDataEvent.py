import zmq
import numpy as np
from convertString import convertString
import json


def prettyJson(jsonStr, tab = ''):
    for key in jsonStr.keys():
        if type(jsonStr[key]) is dict:
            print(key + "\n", end='')
            prettyJson(jsonStr[key], tab + '\t')
        else:
            print(tab, key, ": ", convertString(jsonStr[key]))

def main():
    context = zmq.Context()

    #  Socket to listen to OE
    print("Connecting to Open Ephys...")
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5557")
    #Have to Set to the beginning for the envelope!
    socket.setsockopt(zmq.SUBSCRIBE, b'ttl') # can also subscribe to b'spike' and others. See OE documentation

    for request in range(10):
        print('waiting')

        #Get raw input from socket
        envelope, jsonStr = socket.recv_multipart()
        print(envelope)

        #Our actual json object (last part)
        jsonStr = json.loads(jsonStr);
        prettyJson(jsonStr)

        print('\n')

if __name__ == "__main__":
    main()

