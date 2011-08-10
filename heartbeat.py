#!/usr/bin/python
from heartbeat_lib import HeartbeatListener, HEARTBEAT_LISTEN_PORT
import argparse
import signal
import time

parser = argparse.ArgumentParser(description=HeartbeatListener.__doc__)
parser.add_argument('-p', action="store", type=int, help="port", dest="port", default=HEARTBEAT_LISTEN_PORT)

if __name__=="__main__":    
    args= parser.parse_args()
    d= HeartbeatListener(args.port)
    d.start()
    while True:
        time.sleep(10)
