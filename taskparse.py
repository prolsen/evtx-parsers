'''
The MIT License (MIT)

Copyright (c) 2014 Patrick Olsen

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
'''
import re, csv, sys, os
import argparse
from lxml import etree
from lxml.etree import XMLSyntaxError
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view

def to_lxml(record_xml):
    '''Record'''
    return etree.fromstring("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>%s" %
                            record_xml.replace("xmlns=\"http://schemas.microsoft.com/win/2004/08/events/event\"", ""))

def getZero(xml):
    return to_lxml(xml).xpath("/Event/EventData/Data[@Name]")[0].text
def getOne(xml):
    return to_lxml(xml).xpath("/Event/EventData/Data[@Name]")[1].text
def getTwo(xml):
    return to_lxml(xml).xpath("/Event/EventData/Data[@Name]")[2].text
def getThree(xml):
    return to_lxml(xml).xpath("/Event/EventData/Data[@Name]")[3].text

def get_Tasks(evtx):
    '''
    Returns tasks.
    '''
    task_list = []    
    for xml, record in evtx_file_xml_view(evtx.get_file_header()):
        try:
            record_id = to_lxml(xml).xpath("/Event/System/EventRecordID")[0].text
            event_id = to_lxml(xml).xpath("/Event/System/Task")[0].text
            ctime = to_lxml(xml).xpath("/Event/System/TimeCreated")[0].get("SystemTime")
            task_action = to_lxml(xml).xpath("/Event/EventData")[0].get("Name")
            if to_lxml(xml).xpath("/Event/System/Correlation")[0].get("ActivityID"):
                correlation_activity = to_lxml(xml).xpath("/Event/System/Correlation")[0].get("ActivityID")
            else:
                correlation_activity = "None"
            #EventID: 100
            if task_action == "TaskStartEvent":
                task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), getTwo(xml), correlation_activity])
            #EventID: 101
            #elif task_action == "TaskStartFailedEvent":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), "None", correlation_activity])
            #EventID: 102
            #elif task_action == "TaskSuccessEvent":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), getTwo(xml), correlation_activity])
            #EventID: 103
            #elif task_action == "TaskFailureEvent":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getTwo(xml), getOne(xml), correlation_activity])
            #EventID: 106
            elif task_action == "TaskRegisteredEvent":
                task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), "None", correlation_activity])
            #EventID: 107
            #elif task_action == "TimeTriggerEvent":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), "None", getOne(xml), correlation_activity])
            #EventID: 108
            #elif task_action == "EventTriggerEvent":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), "None", getOne(xml), correlation_activity])
            #EventID: 110
            #elif task_action == "TaskRunEvent":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getTwo(xml), getOne(xml), correlation_activity])
            #EventID: 111
            #elif task_action == "TaskTerminationEvent":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), "None", getOne(xml), correlation_activity])
            #EventID: 117
            #elif task_action == "IdleTrigger":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), "None", getOne(xml), correlation_activity])
            #EventID: 118
            #elif task_action == "BootTrigger":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), "None", getOne(xml), correlation_activity])
            #EventID: 119
            #elif task_action == "LogonTrigger":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), getTwo(xml), correlation_activity])
            #EventID: 129
            elif task_action == "CreatedTaskProcess":
                task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), "None", correlation_activity])
            #EventID: 135
            #elif task_action == "TaskNoStartWithoutIdle":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), "None", "None", correlation_activity])
            #EventID: 140
            elif task_action == "TaskUpdated":
                task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), "None", correlation_activity])
            #EventID: 141
            elif task_action == "TaskDeleted":
                task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), "None", correlation_activity])
            #EventID: 200
            elif task_action == "ActionStart":
                task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), getTwo(xml), correlation_activity])
            #EventID: 201
            elif task_action == "ActionSuccess":
                task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getTwo(xml), getOne(xml), correlation_activity])
            #EventID: 202
            elif task_action == "ActionFailure":
                task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getTwo(xml), getOne(xml), correlation_activity])
            #EventID: 301
            #elif task_action == "TaskEngineExitEvent":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), "None", "None", correlation_activity])
            #EventID: 310
            #elif task_action == "TaskEngineProcessStarted":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getOne(xml), "None", correlation_activity])
            #EventID: 314
            #elif task_action == "TaskEngineIdle":
            #    task_list.append([record_id, ctime, event_id, task_action, "None", getZero(xml), "None", correlation_activity])
            #EventID: 317
            #elif task_action == "TaskEngineProcessMainStarted":
            #    task_list.append([record_id, ctime, event_id, task_action, "None", getZero(xml), "None", correlation_activity])
            #EventID: 318
            #elif task_action == "TaskEngineProcessMainShutdown":
            #    task_list.append([record_id, ctime, event_id, task_action, "None", getZero(xml), "None", correlation_activity])
            #EventID: 319
            #elif task_action == "TaskEngineProcessReceivedStartTask":
            #    task_list.append([record_id, ctime, event_id, task_action, getOne(xml), getZero(xml), "None", correlation_activity])
            #EventID: 320
            #elif task_action == "TaskEngineProcessReceivedStopTask":
            #    task_list.append([record_id, ctime, event_id, task_action, "None", getZero(xml), getOne(xml), correlation_activity])
            #EventID: 322
            #elif task_action == "NewInstanceIgnored":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), "None", getOne(xml), correlation_activity])
            #EventID: 328
            #elif task_action == "StoppingOnIdleEnd":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), "None", getOne(xml), correlation_activity])
            #EventID: 330
            #elif task_action == "StoppedOnRequest":
            #    task_list.append([record_id, ctime, event_id, task_action, getZero(xml), getTwo(xml), getOne(xml), correlation_activity])
            else:
                continue
                        
        except (etree.XMLSyntaxError, IndexError) as e:
            continue

    return task_list

def outputResults(task_results):
    task_writer = csv.writer(sys.stdout)
    task_writer.writerow(['Time', 'EID', 'Action', 'Data1', 'Data2', 'InstanceID', 'Correlation'])
    for task in task_results:
        fixed_time = str(task[1]).replace(" ", "T").partition(".")[0] + "Z"
        task_writer.writerow([fixed_time, task[2], task[3], task[4], task[5], task[6], task[7]])

def main():
    parser = argparse.ArgumentParser(description='Parse Task Scheduler EVTX logs.')
    parser.add_argument('-p', '--path', help='Path to Task Scheduler EVTX file(s).')
    args = parser.parse_args()
    if args.path:
        input_path = args.path
    else:
        print "You need to specify a path to your EVTX file(s)."

    for root, subdirs, files in os.walk(input_path):
        for file_names in files:
            if re.search(".*taskscheduler.*\.evtx$", file_names.lower()):
                with Evtx(os.path.abspath(input_path + file_names)) as evtx:
                    task_results = get_Tasks(evtx)
                    outputResults(task_results)

if __name__ == "__main__":
    main()