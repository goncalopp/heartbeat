import socket
import datetime
import time
import threading
import sys
from configobj import ConfigObj
from validate import Validator


HEARTBEAT_CONFIG_FILE= "/etc/heartbeat.conf"

def read_configuration():
    heartbeat_config = ConfigObj(HEARTBEAT_CONFIG_FILE, configspec='heartbeat_config_validator')
    validator= Validator()
    if not True==heartbeat_config.validate(validator):
        print "Error validating configuration file"
        sys.exit(1)
    globals().update(
            {
        'HEARTBEAT_LISTEN_PORT':    heartbeat_config['listen_port'],
        'HEARTBEAT_CONNECT_PORT':   heartbeat_config['connect_port'],
        'HEARTBEAT_TIMEOUT':        heartbeat_config['timeout'],
        'HEARTBEAT_REPEAT':         heartbeat_config['repeat'],
        'HEARTBEAT_HOSTS':          heartbeat_config['hosts'],
        'HEARTBEAT_LOGFILE':        heartbeat_config['logfile'],
            })

read_configuration()


def heartbeat_check(host, port= HEARTBEAT_CONNECT_PORT, timeout= HEARTBEAT_TIMEOUT, repeat= HEARTBEAT_REPEAT, sleep=False):
    '''Checks for a heartbeat on HOST:PORT.
    Tries to contact REPEAT times, waiting TIMEOUT on each.
    Returns False if all fail, True otherwise.
    If SLEEP is set, the method always returns after REPEAT*TIMEOUT seconds.
   '''
    if sleep:
        start= datetime.datetime.now()

    state= False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    for i in range(repeat):
        try:
            s.connect((host, port))
            state=True
        except:
            pass
    
    if sleep:
        delta= datetime.datetime.now() - start
        elapsed= delta.seconds + (delta.microseconds / 1E6)
        lacking= repeat*timeout - elapsed - 0.004
        if lacking > 0:
            time.sleep(lacking)

    return state
    
class HeartbeatListener(threading.Thread):
    '''runs a heartbeat listener on PORT'''
    def __init__(self, port=HEARTBEAT_LISTEN_PORT):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.port= port
        self.running=False

    def run(self):
        self.socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.socket.listen(1)
        while(True):
            try:
                conn, addr = self.socket.accept()
                conn.close()
            except:
                pass
        print "exiting..."

    def start(self):
        self.running=True
        self.stopsignal=False
        threading.Thread.start(self)

    def stop(self):
        self.stopsignal=True
        self.join()
        self.running=False


def now_unix():
    return time.mktime( datetime.datetime.now().timetuple() )


class HeartbeatMonitor(threading.Thread):
    def __init__(self, host, port=HEARTBEAT_CONNECT_PORT, timeout=HEARTBEAT_TIMEOUT, repeat=HEARTBEAT_REPEAT):
        threading.Thread.__init__(self)
        self.host, self.port, self.timeout, self.repeat= host, port, timeout, repeat
        self.state= 'different'
        self.stopsignal= False
        self.running= False
        
    def _log_start(self):
        print "{time}\t{host}\tMonitoring running".format(time= now_unix(), host=self.host)

    def _log_stop(self  ):
        print "{time}\t{host}\tMonitoring stopped".format(time= now_unix(), host=self.host)
  

    def _log_changestate(self, newstate):
        state_str= int(newstate)
        print "{time}\t{host}\t{state}".format(time=now_unix(), host=self.host, state=state_str)

    def run(self):
        while True:
            if self.stopsignal==True:
                break
            new_state= heartbeat_check(self.host, self.port, self.timeout, sleep=True)
            if new_state!=self.state:
                self._log_changestate(new_state)
                self.state= new_state
    
    def start(self):
        if self.running:
            #already running
            raise Exception("Already running")
        self.stopsignal=False
        self._log_start()
        self.running= True
        threading.Thread.start(self)

    def stop(self):
        if not self.running:
            #not running
            raise Exception("Not running")
        self._log_stop()
        self.stopsignal= True
        self.join()
        self.running=False




