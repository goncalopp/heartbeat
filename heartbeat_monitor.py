#!/usr/bin/python
from heartbeat_lib import HeartbeatMonitor, HEARTBEAT_HOSTS
from heartbeat_check import parser as check_parser
import argparse
import signal
import time

parser = argparse.ArgumentParser(parents=[check_parser], conflict_handler='resolve', description="Monitors one or more hosts for heartbeat until SIGINT is received")
parser.add_argument('hosts', action="store", nargs="*", type=str, default=HEARTBEAT_HOSTS)

if __name__=="__main__":
    args= parser.parse_args()
    p,t,r= args.port, args.timeout, args.repeat
    hosts= args.hosts

    monitors= [HeartbeatMonitor(host, p,t,r) for host in hosts]
    map(HeartbeatMonitor.start, monitors)

    def ctrl_c_handler(signal, frame):
            map(HeartbeatMonitor.stop, monitors)
            exit(0)
            
    signal.signal(signal.SIGINT, ctrl_c_handler)
    signal.pause()  #wait for ctrl-c
