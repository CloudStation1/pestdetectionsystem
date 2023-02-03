#!/bin/bash

#(cd minio; sh deploy.sh)
#sleep 180
#(cd mosquitto; sh deploy.sh)
#sleep 180
(cd mqttreceiver; sh deploy.sh)
sleep 120
(cd notifier; sh deploy.sh)
sleep 120
(cd webapp; sh deploy.sh)
