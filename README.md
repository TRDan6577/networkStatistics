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
