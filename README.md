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
```

 Results are written in following CSV format:
```
timestamp, elapsed_time_requests_module, elapsed_time_measured_by_hort
```
Example output:
```
20:41:05,0.031679,0.0661058425903
20:41:07,0.002359,0.00296592712402
20:41:09,0.004727,0.0057680606842
```
