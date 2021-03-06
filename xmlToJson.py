from xmljson import badgerfish
from json import dumps
from xml.etree.ElementTree import fromstring
import sys

xmlfile = open('xmlOut.xml', 'rb')
jsonfile = open('jsonOut.json', 'wb')

if(not len(sys.argv) == 1):
    try:
        import jsbeautifier
        jsonfile.write(jsbeautifier.beautify(dumps(badgerfish.data(fromstring(xmlfile.read())))))

    except ImportError:
        sys.stdout.write("Can't import jsbeautifier. Ignoring human readable flag...")
        jsonfile.write(dumps(badgerfish.data(fromstring(xmlfile.read()))))

else:
    jsonfile.write(dumps(badgerfish.data(fromstring(xmlfile.read()))))

xmlfile.close()
jsonfile.close()
