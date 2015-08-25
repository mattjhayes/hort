# hort
HTTP Object Retrieval Test (hort)

This program is used to regularly test retrieval times for an
HTTP object (resource) for purposes such as baselining network
performance and carrying out testing. Timed results are written to a
CSV format file, with timestamps, for later analysis.

Usage:
```
python hort.py -u URL [options]
```

Example usage:
```
python hort.py -u http://sv1.example.com/static/index.html -i 2 -n
```

Options:

```
 -h, --help            Display this help and exit
 -u, --URL             URL of object to retrieve (can include port)
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
```

 Results are written in following CSV format:
```
<timestamp>, <elapsed_time_measured_by_hort>, <HTTP_response_code>
```

Example output:
```
21:28:37,0.00408291816711,200
21:28:38,0.00426006317139,200
21:28:39,0.00414991378784,200
```

Example Key-Value Pair (KVP) output:
```
21:27:38,load_time=0.00442314147949,status=200
21:27:39,load_time=0.00450420379639,status=200
21:27:40,load_time=0.00425410270691,status=200
```
