#!/bin/bash

INSTALL_DIR=/usr/local/bin/
SERVICES_DIR=/etc/init.d/



if [[ `id -u` != 0 ]]
    then    
    echo "must be run as root"
    exit 0
fi

whereis nc | grep bsd > /dev/null
if [[ $? != 0 ]]
    then
    echo "you don't seem to have openBSD's netcat. GNU netcat will not do, sorry"
    exit 0
fi


cp heartbeatd heartbeat_check heartbeat_monitor heartbeat_md $INSTALL_DIR
cp init.d/heartbeat init.d/heartbeat_monitor $SERVICES_DIR

echo "install completed"
echo "copied files to:"
echo "    " $INSTALL_DIR
echo "    " $SERVICES_DIR
