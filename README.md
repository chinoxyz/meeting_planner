# Meeting Planner

System for employees to submit booking requests for meetings in a meeting. It process batches of booking requests.
It process input as text.

* The first line of the input text represents the company office hours, in 24 hour
clock format
* The remainder of the input represents individual booking requests. Each
booking request is in the following format:
    
    [request submission time, in the format YYYY-MM-DD HH:MM:SS] [ARCH:employee id]
    [meeting start time, in the format YYYY-MM-DD HH:MM] [ARCH:meeting duration in hours]

Requirements to run:
    
    virtualenv env -p python3 # To create environment with python3
    pip install -r requirements.txt

How to run it:
    
    python script.py < input.txt

Example input:

    0900 1730
    2015-08-17 10:17:06 EMP001
    2015-08-21 09:00 2
    2015-08-16 12:34:56 EMP002
    2015-08-21 09:00 2
    2015-08-16 09:28:23 EMP003
    2015-08-22 14:00 2
    2015-08-17 11:23:45 EMP004
    2015-08-22 16:00 1
    2015-08-15 17:29:12 EMP005
    2015-08-21 16:00 3

Example output:
    
    2015-08-2109:00 11:00 EMP002
    2015-08-22
    14:00 16:00 EMP003
    16:00 17:00 EMP004


To run the tests:

    nosetests .
   

