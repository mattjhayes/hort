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

#*** General imports:
import socket
import datetime
import time
import os

#*** For parsing JSON responses:
import json

#*** Import sys and getopt for command line argument parsing:
import sys, getopt

def main(argv):
    """
    Main function of hort
    """
    version = "0.1.4"
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
    elapsed_time = 0
    kvp = 0
    log_object_data = 0
    parse_json = 0
    #*** What to record if connection fails:
    arbitrary_timeout = 99
    arbitrary_status = "failure"
    arbitrary_content_len = 0
    verify = True


    #*** Get the hostname for use in filenames etc:
    hostname = socket.gethostname()

    #*** Start by parsing command line parameters:
    try:
        opts, args = getopt.getopt(argv, "hu:m:ni:p:w:Wb:jekcxz:v",
                                ["help",
                                "url=",
                                "max-run-time=",
                                "no-keepalive",
                                "interval=",
                                "proxy=",
                                "output-file=",
                                "output-path=",
                                "no-header-row",
                                "elapsed-time",
                                "kvp",
                                "log-object-data",
                                "parse-json",
                                "verify=",
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
        elif opt in ("-e", "--elapsed-time"):
            elapsed_time = 1
        elif opt in ("-c", "--log-object-data"):
            log_object_data = 1
        elif opt in ("-x", "--parse-json"):
            parse_json = 1
        elif opt in ("-z", "--verify"):
            if arg == 'True':
                verify = True
            elif arg == 'False':
                verify = False
            else:
                verify = arg
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
        header_csv = "time,"
        if elapsed_time:
            header_csv += "GET_elapsed-time,"
        header_csv += hostname + session + "-retrieval-time," + \
                        "\"" + hostname + session + "-" + url + \
                        "-status-code\",content-length\n"

        with open(output_file, 'a') as the_file:
            the_file.write(header_csv)

    if not header_row:
        print "Not writing a header row to CSV"

    #*** Set up an HTTP/1.1 session:
    s = requests.session()

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
        http_proxy = "http://" + proxy
        https_proxy = "https://" + proxy
        proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy
            }
    else:
        proxyDict = {}

    #*** Use for base for calculating total elapsed time:
    base_start_time = time.time()

    #*** Start the loop:
    while not finished:
        timenow = datetime.datetime.now()
        timestamp = timenow.strftime("%H:%M:%S")
        start_time = time.time()
        #*** Make the HTTP GET request:
        failure = 0
        try:
            r = s.get(url, headers=headers, proxies=proxyDict,
                                 verify=verify)
        except:
            failure = 1
        end_time = time.time()
        total_time = end_time - start_time
        if not failure:
            retrieval_time = str(total_time)
            status_code = str(r.status_code)
            content_len = str(r.headers.get('content-length'))
            object_data = unicode(r.text)
        else:
            #*** Results that reflect a connection failure:
            retrieval_time = str(arbitrary_timeout)
            status_code = str(arbitrary_status)
            content_len = str(arbitrary_content_len)
            object_data = ""
        #*** Put the stats into a nice string for printing and
        #***  writing to file:
        if parse_json:
            object_data = convert_json_to_csv(object_data, kvp)
        #*** Assemble the result string:
        if not kvp:
            result = str(timestamp) + ","
            if elapsed_time:
                result += str(start_time - base_start_time) \
                        + ","
            result += retrieval_time + "," +  status_code \
                                  + "," + content_len
            if log_object_data:
                result += "," + object_data
        else:
            result = str(timestamp) + ","
            if elapsed_time:
                result += "GET_elapsed_time=" + \
                str(start_time - base_start_time) + ","
            result += "load_time=" + retrieval_time \
                                  + ",status=" + status_code \
                                  + ",size=" + content_len
            if log_object_data and not parse_json:
                result += ",object_data=" + object_data
            elif log_object_data:
                result += "," + object_data
        #*** Print result string to screen:
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

def convert_json_to_csv(json_data, kvp):
    """
    Convert simple flat JSON into CSV
    Pass kvp as True if you want key-value pairs
    """
    #*** Convert JSON object data into CSV:
    json_object = json.loads(json_data)
    csv_data = ""
    for x, y in json_object.items():
        if not kvp:
            csv_data += str(y) + ","
        else:
            csv_data += str(x) + "=" + str(y) + ","
    return csv_data

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
 -h  --help            Display this help and exit
 -u  --url             URL of object to retrieve (can include port)
 -m  --max-run-time    Maximum time to run for before exiting
                         (default is infinite)
 -n  --no-keepalive    Use separate TCP session per request
                         (default is reuse TCP session)
 -i  --interval        Interval between requests in seconds
                         (default is 1)
 -p  --proxy           Use a proxy, format is NAME:PORT
 -w  --output-file     Specify an output filename
 -W                    Output results to default filename
                         default format is:
                         hort-HOSTNAME-YYYYMMDD-HHMMSS.csv
 -b  --output-path     Specify path to output file directory
 -j  --no-header-row   Suppress writing header row into CSV
 -e  --elapsed-time    Log the elapsed time when the GET request was
                        sent (not elapsed time when result was returned)
 -k  --kvp             Write output data as key=value pairs
 -c  --log-object-data Write the HTTP object data into the output file
 -x  --parse-json      Enable this if you want to log results from an
                         API that are in JSON. Will only work if JSON is
                         simple, flat and not jagged.
 -z  --verify          Control SSL verification. Default is True
                         Specify False to skip SSL cert verification
                         Specify path to certfile to use own trusted
                           certificates
 -v, --version         Output version information and exit

 Results are written in following CSV format:
   <timestamp>, <object_retrieval_time>, <HTTP_response_code>,
      <object_size>[,<other_optional_values>]
 """
    return()

if __name__ == "__main__":
    #*** Run the main function with command line
    #***  arguments from position 1
    main(sys.argv[1:])
