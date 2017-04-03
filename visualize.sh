#!/bin/bash
# Author: Tom Daniels <trd6577@g.rit.edu>
# Purpose: This file is the main running file for the visualization software

# Check to make sure there was exactly one argument
if ! [ -n "$1" ]; then
    echo 'Usage: ./visualize.sh pcapfile'
    exit
fi

# Convert pcap to XML
printf 'Converting your pcap file to a XML file...'
tshark -r "$1" -T pdml > xmlOut.xml
echo 'done'
echo

# Determine if the JSON file should be beautified
result='a'
while [ "$(echo $result | tr [:upper:] [:lower:])" != "n" -a "$(echo $result | tr [:upper:] [:lower:])" != 'y' ]; do
    printf "Would you like the resulting JSON file to be human-readable?"
    read -p " Please note this will take a lot of time and resouces [y/n]: " result
done

# Convert the XML to JSON
printf 'Converting xmlOut.xml to jsonOut.json...'
if [ "$(echo $result | tr [:upper:] [:lower:])" == 'y' ]; then
    python xmlToJson.py beautify
else
    python xmlToJson.py
fi
echo 'done'

fileDir="$(date)"
fileDir=${fileDir//" "/"."}

# Make the directory to keep all of the files during this session
mkdir $fileDir

menuChoice=1
while [ $menuChoice -ne 0 ]; do
    clear

    # Print the menu
    echo 'Menu:
    
1. Force graph of IP interactions
2. IP specific information (types of traffic, how much traffic, etc)
3. General Information (For all IP address: types of traffic, how much traffic, etc)
0. Exit

'

    # Get option
    read -p "Please enter an option: " menuChoice

    # Do nothing
    if [ "$menuChoice" == '' ]; then
        menuChoice=1
        continue
    fi

    # Create forceGraph.html
    if [ $menuChoice -eq 1 ]; then
        # Check to see if we already make a force graph. If so, don't waste
        # resources doing it again
        if [ ! -f "$fileDir/forceGraph.html" ]; then
            python networkNodes.py $fileDir #> /dev/null 2>&1
        else
            printf "Force graph already generated. Open forceGraph.html in "
            echo "$fileDir to view it"
        fi
    fi
done
