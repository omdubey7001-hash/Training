#!/bin/bash

URL="http://localhost:3000/ping"
LOG_FILE="./logs/health.log"

while true
do
  STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL)

  if [ "$STATUS_CODE" != "200" ]; then
    echo "$(date) - Server DOWN - Status: $STATUS_CODE" >> $LOG_FILE
  fi

  sleep 10
done

