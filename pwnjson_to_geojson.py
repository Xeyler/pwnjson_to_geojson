#!/bin/python

import json
import sys
import os
import dateutil.parser
import base64

from usage import usage
from json_template import get_geojson_template, get_feature_template

if __name__ == '__main__':
    #
    # Process arguments and remove them from the list as they're processed
    #
    if '-h' in sys.argv:
        usage()
        exit(0)

    should_include_pcap = False

    if '-b' in sys.argv:
        sys.argv.remove('-b')
        should_include_pcap = True

    savefile = None

    if '-o' in sys.argv:
        arg_index = sys.argv.index('-o')
        sys.argv.remove('-o')
        savefile = sys.argv.pop(arg_index)

    json_indent = None

    if '-p' in sys.argv:
        sys.argv.remove('-p')
        json_indent = 4

    if len(sys.argv) < 2:
        usage("At least one pwnagotchi gps file is required!")
        exit(1)

    #
    # Set up JSON and process files
    #
    geojson_result = get_geojson_template()

    for file in sys.argv[1:]:
        with open(file, 'r') as gps_file:
            gps_json = json.load(gps_file)

            filename = os.path.split(file)[-1]
            
            feature = get_feature_template()

            # Does the GeoJSON format care what the id is or does it simply
            # have to be unique? Let's just set it to the filename which
            # should(heh) be unique.
            feature['id'] = str.split(filename, '.')[0]
            feature['geometry']['coordinates'] = [
                    gps_json['Longitude'],
                    gps_json['Latitude'],
                    gps_json['Altitude']
                ]

            # BSSIDs are always 12 characters, so we can splice the filename
            # along one point to get the SSID and BSSID separately
            feature['properties']['ssid'] = filename.split('.')[0][:-13]
            feature['properties']['bssid'] = filename.split('.')[0][-12:]
            # Because our goal is to vizualize the data, why not make the date
            # more readable as well?
            feature['properties']['time'] = dateutil.parser.parse(
                    gps_json['Updated']).strftime('%A, %B %d, %Y %I:%M:%S %p')
            feature['properties']['quality'] = gps_json['FixQuality']

            if should_include_pcap:
                with open(f'{file.split(".")[0]}.pcap', 'rb') as pcap_file:
                    pcap_b64 = base64.b64encode(pcap_file.read())
                    feature['properties']['pcap'] = pcap_b64.decode('utf-8')

            geojson_result['features'].append(feature)

    #
    # Output result either to file or stdout
    #
    if savefile != None:
        with open(savefile, 'w') as outfile:
            json.dump(geojson_result, outfile, indent=json_indent)
    else:
        json.dump(geojson_result, sys.stdout, indent=json_indent)
