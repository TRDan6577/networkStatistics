"""
Purpose: Makes the charts for IP specific information
Author: Tom Daniels <trd6577@g.rit.edu>
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
ip = sys.argv[2]

# Initialize the pie chart variables to zero
bytesSent = 0
bytesReceived = 0
packetsSent = 0
packetsReceived = 0
icmpPackets = 0
icmpBytes = 0
icmpv6Packets = 0
icmpv6Bytes = 0
tcpPackets = 0
tcpBytes = 0
udpPackets = 0
udpBytes = 0
arpFrames = 0
arpBytes = 0

# Look for that IP address in the list of packets
for packet in packets:
    # If the packet has the network layer and the network layer is using IPv4
    # then grab the source and destination IP address
    if(len(packet['proto']) > NET and packet['proto'][NET]['@name'] == 'ip'):
        src = packet['proto'][NET]['field'][SRC_IP]['@show'].encode('ascii')
        dst = packet['proto'][NET]['field'][DST_IP]['@show'].encode('ascii')

        # If the IP address we're searching for is the source, increment the
        # appropriate variables
        if(ip == src):
            packetsSent += 1
            bytesSent += packet['proto'][GEN_INFO]['@size']

        # If the IP address we're searching for is the destination, increment
        # the appropriate variables
        if(ip == dst):
            packetsReceived += 1
            bytesReceived += packet['proto'][GEN_INFO]['@size']
        
        if(ip == src or ip == dst):
            # If the packet is using TCP, take note of the TCP statistics
            if(len(packet['proto']) > TRANS and 
               packet['proto'][TRANS]['@name'] == 'tcp'):
                tcpPackets += 1
                tcpBytes += packet['proto'][GEN_INFO]['@size']

            # If the packet is using UDP, take note of the UDP statistics
            if(len(packet['proto']) > TRANS and 
               packet['proto'][TRANS]['@name'] == 'udp'):
                udpPackets += 1
                udpBytes += packet['proto'][GEN_INFO]['@size']

            # If the packet is using ICMP, take note of the ICMP statistics
            if(len(packet['proto']) > TRANS and 
               packet['proto'][TRANS]['@name'] == 'icmp'):
                icmpPackets += 1
                icmpBytes += packet['proto'][GEN_INFO]['@size']

            # If the packet is using ICMPv6, take note of the ICMPv6 statistics
            if(len(packet['proto']) > TRANS and 
               packet['proto'][TRANS]['@name'] == 'icmpv6'):
                icmpv6Packets += 1
                icmpv6Bytes += packet['proto'][GEN_INFO]['@size']

    # If the frame is an ARP request/reply, determine if it is to or from the
    # IP address we're analyzing
    if(len(packet['proto']) > DATA and packet['proto'][NET]['@name'] == 'arp'):
        # The ARP frame was sent to the IP address we're analyzing
        if(packet['proto'][NET]['field'][6]['@show'] == ip):
            arpFrames += 1
            arpBytes += packet['proto'][GEN_INFO]['@size']
            packetsSent += 1
            bytesSent += packet['proto'][GEN_INFO]['@size']

        # The ARP frame was sent to the IP address we're analyzing
        if(packet['proto'][NET]['field'][8]['@show'] == ip):
            arpFrames += 1
            arpBytes += packet['proto'][GEN_INFO]['@size']
            packetsReceived += 1
            bytesReceived += packet['proto'][GEN_INFO]['@size']


# Create the pie charts using the data we've gathered
fig = {
    # Data Section
    "data": [{
    # Data for bytes sent and received
    "values": [bytesSent, bytesReceived],
    "labels": ["Sent", "Received"],
    "domain": {"x": [0, .49], "y": [0, .49]},
    "name": "Bytes Transferred",
    "hoverinfo": "label+name+value",
    "hole": .4,
    "type": "pie"},
    { # Data for packets sent and received
    "values": [packetsSent, packetsReceived],
    "labels": ["Sent", "Received"],
    "domain": {"x": [0, .49], "y": [.51, 1]},
    "name": "Packets Transferred",
    "hoverinfo": "label+name+value",
    "hole": .4,
    "type": "pie"},
    { # Data for protocol specific bytes
    "values": [icmpBytes, icmpv6Bytes, tcpBytes, udpBytes, arpBytes],
    "labels": ["ICMP", "ICMPv6", "TCP", "UDP", "ARP"],
    "domain": {"x": [.51, 1], "y": [0, .49]},
    "name": "Bytes",
    "hoverinfo": "label+name+value",
    "hole": .4,
    "type": "pie"},
    { # Data for protocol specific packets
    "values": [icmpPackets, icmpv6Packets, tcpPackets, udpPackets, arpFrames],
    "labels": ["ICMP", "ICMPv6", "TCP", "UDP", "ARP"],
    "domain": {"x": [.51, 1], "y": [.51, 1]},
    "name": "Packets",
    "hoverinfo": "label+name+value",
    "hole": .4,
    "type": "pie"}],

    # Page layout
    "layout": {
    "title": ("Information About " + str(ip)),
    "annotations": [
        {"font": {"size": 20}, "text": "Bytes", "showarrow": False, "x": .205, "y": .225},
        {"font": {"size": 20}, "text": "Packets", "showarrow": False, "x": .19, "y": .78},
        {"font": {"size": 20}, "text": "Protocol\nBytes", "showarrow": False, "x": .81, "y": .205},
        {"font": {"size": 20}, "text": "Protocol\nPackets", "showarrow": False, "x": .81, "y": .795}]}
    }


plotly.offline.plot(fig, filename=sys.argv[1] + '/' + sys.argv[2] + '.html')
