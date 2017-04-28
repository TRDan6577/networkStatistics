# Stastical Network Analysis in Python (SNAP)

## What does it do?
SNAP provides a statistical insight into your network through colorful graphs that make everyone
from C-level executives to your very own grandma impressed with you. Capture traffic from
your network using your favorite sniffer (make sure the file is in .pcap or .pcapng format)
and feed it to SNAP. SNAP then presents you with a list of options for you to extract and
export stastical goodies out of your .pcap. Choose as many options as you want!

## Installation
*Prerequisites* - You must have the following packages installed:
* [xmljson](https://pypi.python.org/pypi/xmljson) - python package that converts xml to json
* [igraph](http://igraph.org/redirect.html) - python package with fantastic graphing capabilities
* [plotly](https://plot.ly/python/) - python package that takes advantage of igraph and adds
even more graphing/statistical capabilities
* [tshark](https://www.wireshark.org/docs/man-pages/tshark.html) - network protocol analyzer

*Optional Packages* - You don't have to install these, but if you like taking up hard drive
space with programs you'll only use a couple times, then by golly install these bad boys:
* [jsbeautifier](https://pypi.python.org/pypi/jsbeautifier) - a python package that makes json
great again by converting unintelligible json files into ones readable by humans

Other than the prerequisites, download SNAP by using 
`git clone https://github.com/TRDan6577/networkStatistics.git`

### Reading installation instructions is lame and boring. Gimme the copy-pasta and leave the thinking to our robot overlords
`sudo pip install xmljson plotly igraph jsbeautifier && sudo apt-get install tshark && 
git clone https://github.com/TRDan6577/networkStatistics.git`

## How do I amaze others with this program?
Usage is simple: `./visualize <pacp file>`

## What do the different options mean?
`1. Force graph of IP interactions` : This option creates nodes on a graph where each node is
a computer on the network and each edge connecting them indicates a transaction between computers.
The resulting graph is interactive. Hovering over a node gives you its IP address, the left mouse
button allows you to spin the graph, and the right mouse button allows you to move the graph.
![alt tag](https://raw.githubusercontent.com/TRDan6577/networkStatistics/master/exampleOutput/forcegraph1.JPG)
![alt tag](https://raw.githubusercontent.com/TRDan6577/networkStatistics/master/exampleOutput/forcegraph2.JPG)

`2. IP specific information (types of traffic, how much traffic, etc)` : This option shows the
statistical properties of a particular host on the network. Information provided includes:
amount of traffic sent and received, and types and amounts of traffic processed by the host 
(expressed in both bytes and number of packets). Currently, the types of traffic supported are
ICMP, ICMPv6, ARP, TCP, and UDP.
![alt tag](https://raw.githubusercontent.com/TRDan6577/networkStatistics/master/exampleOutput/ipinfo.JPG)

## Drawbacks
At this time, we have not found a good program that converts XML to JSON. Our current solution
does not play well with large XML files. This means that the pcap file that generates the XML
can not be large. The maximum pcap file size is dependant on the hardware you have available,
but as an example, a 700MB pcap file resulted in an XML file larger than 100GB. Any future
work done here should change start by changing the way we read the file (read the raw pcap
rather than converting it to a different file type)

## Contributors
Tom Daniels,
Kaitlin Keenan, and
Corinne Smith
