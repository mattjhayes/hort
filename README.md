# hort
HTTP Object Retrieval Test (hort)

This program is used to regularly test retrieval times for an
HTTP object (resource) for purposes such as baselining network
performance and carrying out testing. It can also be used to
carry out regular retrieval of HTTP data (i.e. JSON API).
Timed results are written to a CSV format file.

Usage:
```
python hort.py -u URL [options]
```

Example usage (see below for more examples):
```
python hort.py -u http://sv1.example.com/static/index.html -i 2 -n
```

Options:

```
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
 -c  --log-object-data Write the HTTP object data into the output file
 -x, --parse-json      Enable this if you want to log results from an
                         API that are in JSON. Will only work if JSON is
                         simple, flat and not jagged.
 -z  --verify          Control SSL verification. Default is True
                         Specify False to skip SSL cert verification
                         Specify path to certfile to use own trusted
                           certificates
 -v, --version         Output version information and exit
```

 Results are written in following CSV format:
```
<timestamp>, <elapsed_time_measured_by_hort>, <HTTP_response_code>,<object_size>[,<other_optional_values>]
```

Simple Example:
```
hort.py --url http://sv1.example.com/static/index.html

HTTP Object Retrieval Test (hort) version 0.1.3
URL is http://sv1.example.com/static/index.html
Not outputing results to file, as option not selected
Setting headers to keep TCP session alive...
21:58:55,0.0243651866913,200,5757
21:58:56,0.00290298461914,200,5757
```

KVP Example:
```
hort.py --url http://sv1.example.com/static/index.html --kvp

HTTP Object Retrieval Test (hort) version 0.1.3
URL is http://sv1.example.com/static/index.html
Not outputing results to file, as option not selected
Setting headers to keep TCP session alive...
21:59:55,load_time=0.0494849681854,status=200,size=5757
21:59:57,load_time=0.00508594512939,status=200,size=5757
21:59:58,load_time=0.00422501564026,status=200,size=5757
```

Writing to File Example:
```
hort.py --url http://sv1.example.com/static/index.html --output-file test.csv --output-path /tmp/

HTTP Object Retrieval Test (hort) version 0.1.3
URL is http://sv1.example.com/static/index.html
Results filename is /tmp/test.csv
Setting headers to keep TCP session alive...
22:02:16,0.0237650871277,200,5757
22:02:17,0.00389218330383,200,5757
22:02:18,0.00473284721375,200,5757
```
And the resulting CSV file:
```
time,ct1-cxn-keep-alive-retrieval-time,"ct1-cxn-keep-alive-http://sv1.example.com/static/index.html-status-code",content-length
22:02:16,0.0237650871277,200,5757
22:02:17,0.00389218330383,200,5757
22:02:18,0.00473284721375,200,5757
```

JSON API Example:

```
hort.py --url http://api.example.com/measurement/eventrates/ --log-object-data --parse-json --kvp

HTTP Object Retrieval Test (hort) version 0.1.3
URL is http://api.example.com/measurement/eventrates/
Not outputing results to file, as option not selected
Setting headers to keep TCP session alive...
21:54:22,load_time=0.031307220459,status=200,size=39,packet_in=39.7,packet_out=39.7,
21:54:23,load_time=0.00234913825989,status=200,size=39,packet_in=43.5,packet_out=43.5,
21:54:24,load_time=0.00214815139771,status=200,size=41,packet_in=47.45,packet_out=47.45,
```
