Python EVTX Parser Scripts 
===========================
I'll be updating this with some of the single purpose Python scripts i've written to parse various items out of some of the Window's Evtx log files.

Powershell Script Parse (pscriptparse.py)
==========================================
You will need Powershell 3.0+ enabled, and have module logging turned on.

				pscriptparse.py -h
				usage: pscriptparse.py [-h] [-p PATH]

				Parse PS1 scripts out of Windows Powershell EVTX Logs.

				optional arguments:
				  -h, --help            show this help message and exit
				  -p PATH, --path PATH  Path to EVTX.

It will provide the run time, event id, script name and message output from Windows Powershell and Powershell Operational logs. It's an easy way to see unique scripts executed and also get a nice format for reviewing the data.

				python pscriptparse.py -p Desktop/
				Time,EventID,ScriptName,Message
				2015-03-22T15:05:59Z,8,C:\Users\Lab\Desktop\helloworld.ps1,"ParameterBinding(Write-Host): name=""Object""; value=""Hello World"""
				2015-03-22T15:05:59Z,8,C:\Users\Lab\Desktop\helloworld.ps1,"ParameterBinding(Write-Host): name=""Object""; value=""Hello World"""