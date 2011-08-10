#!/usr/bin/python
from heartbeat_lib import heartbeat_check, HEARTBEAT_CONNECT_PORT, HEARTBEAT_TIMEOUT, HEARTBEAT_REPEAT
import argparse

parser = argparse.ArgumentParser(description=heartbeat_check.__doc__)
parser.add_argument('-p', action="store", type=int, help="port", dest="port", default=HEARTBEAT_CONNECT_PORT)
parser.add_argument('-t', action="store", type=int, help= "timeout", dest="timeout", default=HEARTBEAT_TIMEOUT)
parser.add_argument('-r', action="store", type=int, help= "repeat", dest="repeat", default=HEARTBEAT_REPEAT)


if __name__=="__main__":
    parser.add_argument('host', action="store", type=str)
    args= parser.parse_args()
    h,p,t,r= args.host, args.port, args.timeout, args.repeat
    result= heartbeat_check(h,p,t,r)
    print result
    exit(int(not result))

