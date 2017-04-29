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

# Initialize the pie chart variables to zero
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

# For each frame, note the statistics
for packet in packets:
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

    # If the frame is an ARP request/reply
    if(len(packet['proto']) > DATA and packet['proto'][NET]['@name'] == 'arp'):
            arpFrames += 1
            arpBytes += packet['proto'][GEN_INFO]['@size']

# Create the pie charts using the data we've gathered
fig = {
    # Data Section
    "data": [
    { # Data for protocol specific bytes
    "values": [icmpBytes, icmpv6Bytes, tcpBytes, udpBytes, arpBytes],
    "labels": ["ICMP", "ICMPv6", "TCP", "UDP", "ARP"],
    "domain": {"x": [0, .49]},
    "name": "Bytes",
    "hoverinfo": "label+name+value",
    "hole": .4,
    "type": "pie"},
    { # Data for protocol specific packets
    "values": [icmpPackets, icmpv6Packets, tcpPackets, udpPackets, arpFrames],
    "labels": ["ICMP", "ICMPv6", "TCP", "UDP", "ARP"],
    "domain": {"x": [.51, 1]},
    "name": "Packets",
    "hoverinfo": "label+name+value",
    "hole": .4,
    "type": "pie"}],

    # Page layout
    "layout": {
    "title": ("Information About Your pcap"),
    "annotations": [
        {"font": {"size": 20}, "text": "Protocol\nBytes", "showarrow": False, "x": .2},
        {"font": {"size": 20}, "text": "Protocol\nPackets", "showarrow": False, "x": .8}]}
    }


plotly.offline.plot(fig, filename=sys.argv[1] + '/allIpInfo.html')
