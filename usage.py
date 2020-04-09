import sys

def usage(error=None):
    if error != None:
        print(f'Error: {error}')

    print(
f'''Usage: {sys.argv[0]} <options> [FILE]...

Options:
  -b        Save base64-encoded pcap file in GeoJSON output
                (NOTE: This will bloat the JSON and isn't recommended)
  -o <file> Save resulting GeoJSON to file
  -h        Print this message
  -p        Make JSON more pretty(less dense)
''')

