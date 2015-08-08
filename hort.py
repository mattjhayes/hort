#!/usr/bin/python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
HTTP Object Retrieval Test (hort)
.
This code is used to test object retrieval times for
HTTP GET requests (all contained within a single
HTTP/1.1 TCP connection by default, although can
alter this behaviour)
.
Requests module does not do caching, so each GET
retrieves the object fresh
.
Do not use this code for production deployments - it
is proof of concept code and carries no warrantee
whatsoever. You have been warned.
"""

#*** Import library to do HTTP GET requests:
import requests
import datetime
import time

#*** Import sys and getopt for command line argument parsing:
import sys, getopt

def main(argv):
    """
    Main function of hort
    """
    version = 2.0
    keepalive = True
    interval = 1
    url = ""
    max_run_time = 0
    finished = 0
    output_file = 0

    #*** Start by parsing command line parameters:
    try:
        opts, args = getopt.getopt(argv, "hu:m:ni:w:v", ["help",
                                   "url=", "max-run-time=",
                                   "no-keepalive", "interval=",
                                   "output-file=", "version"])
    except getopt.GetoptError as err:
        print "hort: Error with options:", err
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt == '-V':
            print 'hort.py version', version
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-m", "--max-run-time"):
            max_run_time = float(arg)
        elif opt in ("-n", "--no-keepalive"):
            keepalive = False
        elif opt in ("-i", "--interval"):
            interval = float(arg)
        elif opt in ("-w", "--output-file"):
            output_file = arg

    if not url:
        #*** We weren't passed a URL so have to exit
        print "hort: Error, no URL passed. Exiting..."
        sys.exit()

    #*** Write results to a CSV file:
    if output_file:
        filename = output_file
    else:
        filename = time.strftime("%Y%m%d-%H%M%S.csv")
    print "results filename is", filename
    with open(filename, 'a') as the_file:
        the_file.write(url)
        the_file.write('\n')

    #*** Set up an HTTP/1.1 session:
    s = requests.session()

    #*** Hack the HTTP adapter to set max retries to a larger value:
    a = requests.adapters.HTTPAdapter(max_retries=5)
    s.mount('http://', a)

    #*** Set HTTP Headers to either keep connection alive or close
    #***  based on preference:
    if keepalive:
        print "Setting headers to keep TCP session alive..."
        headers = {'Connection': 'keep-alive'}
    else:
        print "Setting headers to close TCP sessions..."
        headers = {'Connection': 'close'}

    #*** Use this if max_run_time is set:
    initial_time = time.time()

    #*** Start the loop:
    while not finished:
        timenow = datetime.datetime.now()
        timestamp = timenow.strftime("%H:%M:%S")
        start_time = time.time()
        #*** Make the HTTP GET request:
        r = s.get(url, headers=headers)
        end_time = time.time()
        total_time = end_time - start_time
        #*** Put the stats into a nice string for printing and
        #***  writing to file:
        result = str(timestamp) + "," + str(r.elapsed.total_seconds()) \
                                  + "," + str(total_time) + "\n"
        print result
        with open(filename, 'a') as the_file:
            the_file.write(result)

        if max_run_time:
            if (start_time - initial_time) > max_run_time:
                break

        #*** Sleep for interval seconds:
        time.sleep(interval)

def print_help():
    """
    Print out the help instructions
    """
    print """
HTTP Object Retrieval Test (hort)
---------------------------------

Use this program to run repeated timed retrievals of an HTTP object
(resource), with results written to file for analysis over time.

Usage:
  python hort.py -u URL [options]

Example usage:
  python hort.py -u http://sv1.example.com/static/index.html -i 2 -n

Options:
 -h, --help          Display this help and exit
 -u, --URL           URL of object to retrieve (can include port number)
 -m, --max-run-time  Maximum time to run for before exiting
                       (default is infinite)
 -n, --no-keepalive  Use separate TCP session per request
                       (default is reuse TCP session)
 -i, --interval      Interval between requests in seconds
                       (default is 1)
 -w, --output-file   Specify an output filename
                       (default is format YYYYMMDD-HHMMSS.csv)
 -v, --version       Output version information and exit

 Results are written in following CSV format:
 <timestamp>,<elapsed_time_measured_by_requests_module>,
    <elapsed_time_measured_by_hort>
 """
    return()

if __name__ == "__main__":
    #*** Run the main function with command line
    #***  arguments from position 1
    main(sys.argv[1:])
