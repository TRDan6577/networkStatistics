"""
Purpose: Makes the charts for IP specific information
"""

import json
import plotly
import sys

IP=1
GEN_INFO = 0    # General information
PHYS = 1        # Physical layer information
DATA = 2        # Data link layer information
NET = 3         # Network layer information
TRANS = 4       # Transport layer information
SRC_IP = 12
DST_IP=14
LOWER_MULTICAST = 224 # First octect of the lowest multicast addresses
UPPER_MULTICAST = 240 # First octect of the highest multicast addresses
BROADCAST = 255


# Get the list of packets
f = open('jsonOut.json', 'rb')
jsonData = json.loads(f.read())
packets = jsonData['pdml']['packet']

# Get the IP address to analyze traffic for
ip = sys.argv[IP]
bytesSent = 0
bytesReceived = 0
packetsSent = 0
packetsReceived = 0

# Look for that IP address in the list of packets
for packet in packets:
    if(len(packet['proto']) > NET and packet['proto'][NET]['@name'] == 'ip'):
        src = packet['proto'][NET]['field'][SRC_IP]['@show'].encode('ascii')
        dst = packet['proto'][NET]['field'][DST_IP]['@show'].encode('ascii')

        if(ip == src):
            packetsSent += 1
            bytesSent += packet['proto'][GEN_INFO]['@size']

        if(ip == dst):
            packetsReceived += 1
            bytesReceived += packet['proto'][GEN_INFO]['@size']

plotly.offline.plot(plotly.graph_objs.Pie(labels=['Bytes Sent', 'Bytes Received'], values=[bytesSent, bytesReceived]))

"""
fig = {"data": [{
    "values": [bytesSent, bytesReceived],
    "labels": ["Sent", "Received"],
    "domain": {"x": [0, .4]},
    "name": "Bytes Transferred",
    "hoverinfo":"label+percent+name",
    "hole":.4,
    "type":"pie"}],
    "layout": {
        "title": ("Information About " + str(ip))}}


plotly.offline.plot(fig)

    This gets you a list of protocols

    if(packet['proto'][len(packet['proto'])-1]['@name'] is not 'fake-field-wrapper'):
        print(packet['proto'][len(packet['proto'])-1]['@name'])
    else:
        print(packet['proto'][len(packet['proto'])-2]['@name'])
"""


