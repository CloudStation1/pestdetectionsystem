#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}going to undeploy webapp, sleeping for 5 sec..press Ctrl+C to cancel${NC}"
sleep 5
(cd webapp; sh ./undeploy.sh)

echo -e "${RED}going to undeploy notifier, sleeping for 5 sec..press Ctrl+C to cancel${NC}"
sleep 5
(cd notifier; sh ./undeploy.sh)

echo -e "${RED}going to undeploy mqttreceiver, sleeping for 5 sec..press Ctrl+C to cancel${NC}"
sleep 5
(cd mqttreceiver; sh ./undeploy.sh)

echo -e "${RED}going to undeploy mqtt server, sleeping for 5 sec..press Ctrl+C to cancel${NC}"
sleep 5
(cd mosquitto; sh ./undeploy.sh)

echo -e "${RED}going to undeploy minio, sleeping for 5 sec..press Ctrl+C to cancel${NC}"
sleep 5
(cd minio; sh ./undeploy.sh)
