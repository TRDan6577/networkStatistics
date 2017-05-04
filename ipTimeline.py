"""
Purpose: Makes the timeline for IP specific information throughout the capture
Author: Tom Daniels <trd6577@g.rit.edu>
"""

import datetime  # Converts floating point number to timestamp
import json      # Parses json
import plotly    # Graphs the data
import sys       # Gets the args

IP=1
GEN_INFO = 0    # General information
PHYS = 1        # Physical layer information
DATA = 2        # Data link layer information
NET = 3         # Network layer information
TRANS = 4       # Transport layer information
SRC_IP = 12
DST_IP=14
LOWER_MULTICAST = 224  # First octect of the lowest multicast addresses
UPPER_MULTICAST = 240  # First octect of the highest multicast addresses
BROADCAST = 255
NUM_SECTIONS = 25  # We'll divide the timeline into 25 sections to analyze it
BYTES = ['Bytes Sent', 'Bytes Received', 'ICMP Bytes', 'ICMPv6 Bytes', 'TCP Bytes',
         'UDP Bytes', 'ARP Bytes']
PACKETS = ['Packets Sent', 'Packets Received', 'ICMP Packets', 'ICMPv6 Packets',
           'TCP Packets', 'UDP Packets', 'ARP Frames']

# Get the list of packets
f = open('jsonOut.json', 'rb')
jsonData = json.loads(f.read())
packets = jsonData['pdml']['packet']

# Get the IP address to analyze traffic for
ip = sys.argv[2]

# Set up the variables needed for the timeline
startTime = packets[0]['proto'][GEN_INFO]['field'][3]['@value']
endTime = packets[len(packets)-1]['proto'][GEN_INFO]['field'][3]['@value']
if(len(packets) < NUM_SECTIONS):
    NUM_SECTIONS = len(packets)
segmentTime = (endTime - startTime) / NUM_SECTIONS
timeLine = []
x_axis = []

# Populate each section in the timeline with a dictionary of each type of traffic
# and use this loop to create the x-axis of our graph
for i in range(0, NUM_SECTIONS):
    timeLine.append({
        'Bytes Sent': 0,
        'Bytes Received': 0,
        'Packets Sent': 0,
        'Packets Received': 0,
        'ICMP Packets': 0,
        'ICMP Bytes': 0,
        'ICMPv6 Packets': 0,
        'ICMPv6 Bytes': 0,
        'TCP Packets': 0,
        'TCP Bytes': 0,
        'UDP Packets': 0,
        'UDP Bytes': 0,
        'ARP Frames': 0,
        'ARP Bytes': 0,
        })
    x_axis.append(datetime.datetime.utcfromtimestamp(segmentTime*i+startTime))

# Look for that IP address in the list of packets
for packet in packets:
    packetTime = packet['proto'][GEN_INFO]['field'][3]['@value']
    # If the packet has the network layer and the network layer is using IPv4
    # then grab the source and destination IP address
    if(len(packet['proto']) > NET and packet['proto'][NET]['@name'] == 'ip'):
        src = packet['proto'][NET]['field'][SRC_IP]['@show'].encode('ascii')
        dst = packet['proto'][NET]['field'][DST_IP]['@show'].encode('ascii')

        # If the IP address we're searching for is the source, increment the
        # appropriate variables
        if(ip == src):
            timeLine[int((packetTime - startTime) // segmentTime)]['Packets Sent'] += 1
            timeLine[int((packetTime - startTime) // segmentTime)]['Bytes Sent'] += packet['proto'][GEN_INFO]['@size']

        # If the IP address we're searching for is the destination, increment
        # the appropriate variables
        if(ip == dst):
            timeLine[int((packetTime - startTime) // segmentTime)]['Packets Received'] += 1
            timeLine[int((packetTime - startTime) // segmentTime)]['Bytes Received'] += packet['proto'][GEN_INFO]['@size']
        
        if(ip == src or ip == dst):
            # If the packet is using TCP, take note of the TCP statistics
            if(len(packet['proto']) > TRANS and 
               packet['proto'][TRANS]['@name'] == 'tcp'):
                timeLine[int((packetTime - startTime) // segmentTime)]['TCP Packets'] += 1
                timeLine[int((packetTime - startTime) // segmentTime)]['TCP Bytes'] += packet['proto'][GEN_INFO]['@size']

            # If the packet is using UDP, take note of the UDP statistics
            if(len(packet['proto']) > TRANS and 
               packet['proto'][TRANS]['@name'] == 'udp'):
                timeLine[int((packetTime - startTime) // segmentTime)]['UDP Packets'] += 1
                timeLine[int((packetTime - startTime) // segmentTime)]['UDP Bytes'] += packet['proto'][GEN_INFO]['@size']

            # If the packet is using ICMP, take note of the ICMP statistics
            if(len(packet['proto']) > TRANS and 
               packet['proto'][TRANS]['@name'] == 'icmp'):
                timeLine[int((packetTime - startTime) // segmentTime)]['ICMP Packets'] += 1
                timeLine[int((packetTime - startTime) // segmentTime)]['ICMP Bytes'] += packet['proto'][GEN_INFO]['@size']

            # If the packet is using ICMPv6, take note of the ICMPv6 statistics
            if(len(packet['proto']) > TRANS and 
               packet['proto'][TRANS]['@name'] == 'icmpv6'):
                timeLine[int((packetTime - startTime) // segmentTime)]['ICMPv6 Packets'] += 1
                timeLine[int((packetTime - startTime) // segmentTime)]['ICMPv6 Bytes'] += packet['proto'][GEN_INFO]['@size']

    # If the frame is an ARP request/reply, determine if it is to or from the
    # IP address we're analyzing
    if(len(packet['proto']) > DATA and packet['proto'][NET]['@name'] == 'arp'):
        # The ARP frame was sent from the IP address we're analyzing
        if(packet['proto'][NET]['field'][6]['@show'] == ip):
            timeLine[int((packetTime - startTime) // segmentTime)]['Packets Sent'] += 1
            timeLine[int((packetTime - startTime) // segmentTime)]['Bytes Sent'] += packet['proto'][GEN_INFO]['@size']
            timeLine[int((packetTime - startTime) // segmentTime)]['ARP Frames'] += 1
            timeLine[int((packetTime - startTime) // segmentTime)]['ARP Bytes'] += packet['proto'][GEN_INFO]['@size']

        # The ARP frame was sent to the IP address we're analyzing
        if(packet['proto'][NET]['field'][8]['@show'] == ip):
            timeLine[int((packetTime - startTime) // segmentTime)]['Packets Received'] += 1
            timeLine[int((packetTime - startTime) // segmentTime)]['Bytes Received'] += packet['proto'][GEN_INFO]['@size']
            timeLine[int((packetTime - startTime) // segmentTime)]['ARP Frames'] += 1
            timeLine[int((packetTime - startTime) // segmentTime)]['ARP Bytes'] += packet['proto'][GEN_INFO]['@size']

# datetime.datetime.utcfromtimestamp(<timestamp>) gets the date

# Create the traces for the byte statistics
traces = []
for byteType in BYTES:
    y_axis = []
    for section in range(0, NUM_SECTIONS):
        y_axis.append(timeLine[section][byteType])
    traces.append(plotly.graph_objs.Scatter(x=x_axis, y=y_axis, name=byteType))


layout = {'title': sys.argv[2] + ' Byte Timeline', 'xaxis': {'title':'Time'}, 'yaxis': {'title': 'Number of Bytes'}}
plotly.offline.plot({'data':traces, 'layout':layout}, filename=sys.argv[1] + 
                    '/' + sys.argv[2] + '_timelineBytes.html')

# Create the traces for the packets statistics
traces = []
for packetType in PACKETS:
    y_axis = []
    for section in range(0, NUM_SECTIONS):
        y_axis.append(timeLine[section][packetType])
    traces.append(plotly.graph_objs.Scatter(x=x_axis, y=y_axis, name=packetType))

layout = {'title': sys.argv[2] + ' Packet Timeline', 'xaxis': {'title':'Time'}, 'yaxis': {'title': 'Number of Packets'}}
plotly.offline.plot({'data':traces, 'layout':layout}, filename=sys.argv[1] + 
                    '/' + sys.argv[2] + '_timelinePackets.html')
