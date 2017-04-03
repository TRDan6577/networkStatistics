"""
TODO: Make nodes colorful based on the amount of traffic they send/receive (ie
a node that gets a lot of traffic is red and ones that barely have any are blue)
"""

import igraph
import json
import plotly
import plotly.graph_objs as pg
import sys

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

f = open('jsonOut.json', 'rb')
jsonData = json.loads(f.read())
packets = jsonData['pdml']['packet']

nodeID = {}  # Maps: Node -> ID
nodes = []   # List of nodes
mapping = {} # Maps: Node interation with Node -> # times
nodeNumber = 0

for packet in packets:
    if(len(packet['proto']) > NET and packet['proto'][NET]['@name'] == 'ip'):
        src = packet['proto'][NET]['field'][SRC_IP]['@show'].encode('ascii')
        dst = packet['proto'][NET]['field'][DST_IP]['@show'].encode('ascii')

        # If either address is multi/broadcast address, ignore it
        if(LOWER_MULTICAST <= int(src.split('.')[0]) < UPPER_MULTICAST or
           LOWER_MULTICAST <= int(dst.split('.')[0]) < UPPER_MULTICAST or
           int(dst.split('.')[3]) == 255):
            continue

        # Add the address(es) to our database if they're not in them
        if(not(nodeID.has_key(src))):
            nodes.append(src)
            nodeID[src] = nodeNumber
            nodeNumber = nodeNumber + 1
        if(not(nodeID.has_key(dst))):
            nodes.append(dst)
            nodeID[dst] = nodeNumber
            nodeNumber = nodeNumber + 1

        # Replace string IP addresses with numbers
        src = str(nodeID[src])
        dst = str(nodeID[dst])

        # Add the mapping to the dictionary
        if(mapping.has_key(src + ':' + dst)):
            mapping[src + ':' + dst] = mapping[src + ':' + dst] + 1
        elif(mapping.has_key(dst + ':' + src)):
            mapping[dst + ':' + src] = mapping[dst + ':' + src] + 1
        else:
            mapping[src + ':' + dst] = 1

edges = [(int(key.split(':')[0]), int(key.split(':')[1])) for key in mapping.keys()]

graph = igraph.Graph(edges, directed=False)

layout = graph.layout('kk', dim=3)

length = len(nodes)
Xn = [layout[i][0] for i in range(length)]
Yn = [layout[i][1] for i in range(length)]
Zn = [layout[i][2] for i in range(length)]

Xe = []
Ye = []
Ze = []
for e in edges:
    Xe+=[layout[e[0]][0], layout[e[1]][0], None]
    Ye+=[layout[e[0]][1], layout[e[1]][1], None]
    Ze+=[layout[e[0]][2], layout[e[1]][2], None]

trace1 = pg.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines',
                      line=pg.Line(color='rgb(125,125,125)', width=1),
                      hoverinfo='none')

trace2 = pg.Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers',
                      name='IP Addresses',
                      marker=pg.Marker(symbol='dot',size=6,
                                       line=pg.Line(color='rgb(50,50,50)', width=0.5)),
                      text=nodes, hoverinfo='text')

axis = dict(showbackground=False, showline=False, zeroline=False, showgrid=False,
           showticklabels=False, title='')

trueLayout = pg.Layout(title='test', width=1000, height=1000, showlegend=False,
                       scene=pg.Scene(xaxis=pg.XAxis(axis),
                                      yaxis=pg.YAxis(axis),
                                      zaxis=pg.ZAxis(axis)),
                       margin=pg.Margin(t=100), hovermode='closest')

plotly.offline.plot(pg.Figure(data=pg.Data([trace1, trace2]), layout=trueLayout),
                    filename=sys.argv[1] + '/' + 'forceGraph.html')
