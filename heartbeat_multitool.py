#!/usr/bin/python
description="""implements multiple commands, busybox-style:
heartbeatd - runs a heartbeat daemon
heartbeat_check - checks (once) if a daemon is running on a host
heartbeat_monitor - heartbeat_check, repeatedly, with timestamps, etc"""

import argparse
import signal
import sys, os
import heartbeat_lib


def heartbeatd(port):
    d= heartbeat_lib.HeartbeatListener(args.port)
    d.start()
    def exit_handler(signal, frame):
        #d.stop()
        exit(0)
    wait_for_ctrl_c(exit_handler)

def heartbeat_check(host, port, timeout, repeat):
    state= heartbeat_lib.heartbeat_check(host, port, timeout, repeat)
    print "Online" if state else "Offline"
    exit( int(not state) )

def heartbeat_monitor(hosts, port, timeout, repeat):
    monitors= [heartbeat_lib.HeartbeatMonitor(host, port, timeout, repeat) for host in hosts]
    for monitor in monitors:
        monitor.start()
    
    def exit_handler(signal, frame):
        for monitor in monitors:
            monitor.stop()
        exit(0)
    wait_for_ctrl_c(exit_handler)
    


def wait_for_ctrl_c( callback ):
    signal.signal(signal.SIGINT, callback)
    signal.pause()


if __name__=="__main__":
    c= os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description=description)
    if c=="heartbeatd":
        parser.add_argument('-p', action="store", type=int, help="port", dest="port", default=heartbeat_lib.HEARTBEAT_LISTEN_PORT)
    else:
        parser.add_argument('-p', action="store", type=int, help="port", dest="port", default=heartbeat_lib.HEARTBEAT_CONNECT_PORT)
        parser.add_argument('-t', action="store", type=int, help= "timeout", dest="timeout", default=heartbeat_lib.HEARTBEAT_TIMEOUT)
        parser.add_argument('-r', action="store", type=int, help= "repeat", dest="repeat", default=heartbeat_lib.HEARTBEAT_REPEAT)
        if c=="heartbeat_check":
            parser.add_argument('host', action="store", type=str)
        elif c=="heartbeat_monitor":
            parser.add_argument('hosts', action="store", nargs="*", type=str, default=heartbeat_lib.HEARTBEAT_HOSTS)
            parser.add_argument('-l', action="store_const", help= "redirect output to logfile", dest="dologfile", const=True)
        else:
            print "Command not recognized:",c
            print description
            exit(1)
 
    args= parser.parse_args()

    if c=="heartbeatd":
        heartbeatd(args.port)
    elif c=="heartbeat_check":
        heartbeat_check(args.host, args.port, args.timeout, args.repeat)
    elif c=="heartbeat_monitor":
        heartbeat_monitor(args.hosts, args.port, args.timeout, args.repeat)
