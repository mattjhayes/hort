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

import socket
import datetime
import time
import os

#*** Import sys and getopt for command line argument parsing:
import sys, getopt

def main(argv):
    """
    Main function of hort
    """
    version = "0.1.2"
    keepalive = True
    interval = 1
    proxy = 0
    url = ""
    max_run_time = 0
    finished = 0
    output_file = 0
    output_file_enabled = 0
    output_path = 0
    header_row = 1
    kvp = 0
    #*** What to record if connection fails:
    arbitrary_timeout = 99
    arbitrary_status = "failure"
    arbitrary_content_len = 0

    #*** Get the hostname for use in filenames etc:
    hostname = socket.gethostname()

    #*** Start by parsing command line parameters:
    try:
        opts, args = getopt.getopt(argv, "hu:m:ni:p:w:Wb:jkv",
                                ["help",
                                "url=",
                                "max-run-time=",
                                "no-keepalive",
                                "interval=",
                                "proxy=",
                                "output-file=",
                                "output-path=",
                                "no-header-row",
                                "kvp",
                                "version"])
    except getopt.GetoptError as err:
        print "hort: Error with options:", err
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-v", "--version"):
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
        elif opt in ("-p", "--proxy"):
            proxy = arg
        elif opt in ("-w", "--output-file"):
            output_file = arg
            output_file_enabled = 1
        elif opt == "-W":
            output_file = "hort-" + hostname + "-" + \
                             time.strftime("%Y%m%d-%H%M%S.csv")
            output_file_enabled = 1
        elif opt in ("-b", "--output-path"):
            output_path = arg
        elif opt in ("-j", "--no-header-row"):
            header_row = 0
        elif opt in ("-k", "--kvp"):
            kvp = 1

    if not url:
        #*** We weren't passed a URL so have to exit
        print "hort: Error, no URL passed. Exiting..."
        sys.exit()

    print "\nHTTP Object Retrieval Test (hort) version", version 
    print "URL is", url
    #*** Display output filename:
    if output_file_enabled:
        if output_path:
            output_file = os.path.join(output_path, output_file)
        print "Results filename is", output_file
    else:
        print "Not outputing results to file, as option not selected"

    if output_file_enabled and header_row:
        #*** Write a header row to CSV:
        if keepalive:
            session = "-cxn-keep-alive"
        else:
            session = "-cxn-close"
        header_csv = "time," + \
                        hostname + session + "-retrieval-time," + \
                        "\"" + hostname + session + "-" + url + \
                        "-status-code\",content-length\n"
        with open(output_file, 'a') as the_file:
            the_file.write(header_csv)

    if not header_row:
        print "Not writing a header row to CSV"

    #*** Set up an HTTP/1.1 session:
    s = requests.session()

    #*** Hack the HTTP adapter to set max retries to a larger value:
    a = requests.adapters.HTTPAdapter(max_retries=5)
    s.mount('http://', a)

    #*** Set HTTP Headers to either keep connection alive or close
    #***  based on preference:
    if keepalive:
        print "Setting headers to keep TCP session alive..."
        headers = {'Connection': 'keep-alive',
                   'Cache-Control': 'no-cache',
                   'Pragma': 'no-cache'}
    else:
        print "Setting headers to close TCP sessions..."
        headers = {'Connection': 'close',
                   'Cache-Control': 'no-cache',
                   'Pragma': 'no-cache'}

    #*** Use this if max_run_time is set:
    initial_time = time.time()

    #*** If using a proxy set the parameters:
    if proxy:
        http_proxy  = "http://" + proxy
        https_proxy = "https://" + proxy
        proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy 
            }
    else:
        proxyDict = {}

    #*** Start the loop:
    while not finished:
        timenow = datetime.datetime.now()
        timestamp = timenow.strftime("%H:%M:%S")
        start_time = time.time()
        #*** Make the HTTP GET request:
        failure = 0
        try:
            r = s.get(url, headers=headers, proxies=proxyDict)
        except:
            failure = 1
        end_time = time.time()
        total_time = end_time - start_time
        if not failure:
            retrieval_time = str(total_time)
            status_code = str(r.status_code)
            content_len = str(r.headers.get('content-length'))
        else:
            #*** Results that reflect a connection failure:
            retrieval_time = str(arbitrary_timeout)
            status_code = str(arbitrary_status)
            content_len = str(arbitrary_content_len)
        #*** Put the stats into a nice string for printing and
        #***  writing to file:
        if not kvp:
            result = str(timestamp) + "," +  retrieval_time\
                                  + "," +  status_code \
                                  + "," + content_len
                                  
        else:
            result = str(timestamp) + ",load_time=" + retrieval_time \
                                  + ",status=" + status_code \
                                  + ",size=" + content_len
        print result

        if output_file_enabled:
            #*** Write results to CSV file:
            with open(output_file, 'a') as the_file:
                the_file.write(result)
                the_file.write("\n")

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
  python hort.py -u http://sv1.example.com/static/index.html -i 2 -n -W

Options:
 -h, --help            Display this help and exit
 -u, --url             URL of object to retrieve (can include port)
 -m, --max-run-time    Maximum time to run for before exiting
                         (default is infinite)
 -n, --no-keepalive    Use separate TCP session per request
                         (default is reuse TCP session)
 -i, --interval        Interval between requests in seconds
                         (default is 1)
 -p, --proxy           Use a proxy, format is NAME:PORT
 -w, --output-file     Specify an output filename
 -W                    Output results to default filename
                         default format is:
                         hort-HOSTNAME-YYYYMMDD-HHMMSS.csv
 -b, --output-path     Specify path to output file directory
 -j  --no-header-row   Suppress writing header row into CSV
 -k  --kvp             Write output data as key=value pairs 
 -v, --version         Output version information and exit

 Results are written in following CSV format:
   <timestamp>, <elapsed_time_measured_by_hort>, <HTTP_response_code>
 """
    return()

if __name__ == "__main__":
    #*** Run the main function with command line
    #***  arguments from position 1
    main(sys.argv[1:])
