#!/bin/bash

init() {
  mkdir -p logs
  if [ ! -f logs/prev_head ]; # initialize if this is the 1st poll
  then
    git rev-parse main > logs/prev_head
  fi
}

run() {
  echo "Starting $PROGRAM Process "
  nohup python3 $PROGRAM >> logs/nohup.out &
}

kill() {
  echo "Killing $PROGRAM process"
  pkill -f $PROGRAM
  ps ax | grep $PROGRAM
}

fetch() {
  git fetch  > logs/build_log.txt 2>&1
  if [ $? -eq 0 ]
  then
    echo "Fetch from git done";
    git merge FETCH_HEAD >> logs/build_log.txt 2>&1 ;
    git rev-parse main > logs/latest_head
  fi
}

PROGRAM=$1
: ${1?"Usage: $0 Must pass program to run as first argument"}
trap kill EXIT
init
kill
run
while true
do
  echo "Fetching..."
  fetch
  if ! diff logs/latest_head logs/prev_head > /dev/null ;
    then
      echo "Merge via git done";
      cat logs/latest_head > logs/prev_head

      kill
      run
  fi
  echo "Sleeping...";
  sleep 3
done

