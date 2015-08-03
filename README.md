# hort
HTTP Object Retrieval Test (hort)

Use this program to run repeated timed retrievals of an HTTP object
(resource), with results written to file for analysis over time.

Usage:
 hort -u URL [options]

Example usage:
    python hort.py -u http://sv1.example.com/static/index.html -i 2 -n

Options:
 -h, --help          display this help and exit

 -u, --URL           URL of object to retrieve (can include port number)

 -m, --max-run-time  Maximum time to run for before exiting

                       (default is infinite)

 -n, --no-keepalive  use separate TCP session per request

                       (default is reuse TCP session)

 -i, --interval      interval between requests in seconds

                       (default is 1)

 -v, --version       output version information and exit

 Results are written in following CSV format:
 timestamp,elapsed_time_measured_by_requests_module,
    elapsed_time_measured_by_hort
