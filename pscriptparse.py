'''
The MIT License (MIT)

Copyright (c) 2015 Patrick Olsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Author: Patrick Olsen

Thanks to Willi Ballenthin for https://github.com/williballenthin/python-evtx
'''
import re, csv, sys, os
import argparse
from lxml import etree
from lxml.etree import XMLSyntaxError
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view

script_re = re.compile("ScriptName\=(?P<scriptname>.*\.ps1)")

def to_lxml(record_xml):
    return etree.fromstring("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>%s" %
                            record_xml.replace("xmlns=\"http://schemas.microsoft.com/win/2004/08/events/event\"", ""))

def get_Scripts(evtx):
    '''
    Returns powershell scripts that were run on the system by parsing the Windows Powershell Logs.
    '''
    ps_scripts_ran = []
    
    for xml, record in evtx_file_xml_view(evtx.get_file_header()):
        try:
            for entry in to_lxml(xml):
                record_id = entry.xpath("/Event/System/EventRecordID")[0].text
                ctime = entry.xpath("/Event/System/TimeCreated")[0].get("SystemTime")
                event_id = to_lxml(xml).xpath("/Event/System/Task")[0].text

                try:
                    script_name = script_re.search(str(to_lxml(xml).xpath("/Event/EventData/Data/string")[1].text)).group("scriptname")
                    message = str(to_lxml(xml).xpath("/Event/EventData/Data/string")[2].text).strip()
                    ps_scripts_ran.append([record_id, str(ctime).replace(" ", "T") + "Z", event_id, script_name, message])

                except (IndexError, AttributeError) as e:
                    continue

        except etree.XMLSyntaxError as e:
            continue

    return ps_scripts_ran

def processData(script_data):
    entry_writer = csv.writer(sys.stdout)
    entry_writer.writerow(['Time', 'EventID', 'ScriptName', 'Message'])
    for entries in script_data:
        entry_writer.writerow([entries[1], entries[2], entries[3], entries[4]])    

def main():
    parser = argparse.ArgumentParser(description='Parse PS1 scripts out of Windows Powershell EVTX Logs.')
    parser.add_argument('-p', '--path', help='Path to EVTX.')
    args = parser.parse_args()
    if args.path:
        input_path = args.path
    else:
        print "You need to specify a path to your Windows Powershell EVTX file."

    for root, subdirs, files in os.walk(input_path):
        for file_names in files:
            if re.search(".*powershell\.evtx$", file_names.lower()):
                with Evtx(os.path.abspath(input_path + file_names)) as evtx:
                    script_data = get_Scripts(evtx)
                    processData(script_data)

if __name__ == "__main__":
    main()