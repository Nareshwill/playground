#!/bin/sh

#stats=$(docker stats --no-stream --format '{{ json . }}')
#statsTableFormat=`docker stats --no-stream --format "table {{.MemPerc}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.Name}}"`
#echo $stats
#echo $statsTableFormat


# To find out the actual cpu utilization percentage.
# You can set NanoCPUs. 1000000000 units would equal 1 core.
nanoCPUUnit=1000000000

# To get the instance id
# instanceId=$(wget -q -O - http://169.254.169.254/latest/meta-data/instance-id)

# Instance Id
instanceId="i-instance"
while :
do
  containers=$(printf "%s|" `docker container ls -q --no-trunc`)

  while [[ $containers ]]; do
    if [[ $containers = *'|'* ]]; then
      first=${containers%%'|'*}
      rest=${containers#*'|'}
    else
      first=$containers
      rest=''
    fi
    if [ $first ]
    then
      echo "Container ID: $first"
      TIMESTAMP=`date +"%s.%3N"`
      stats=$(docker stats $first --no-stream --format '{{ json . }}')
      status=$(docker ps --filter ID=$first --format '{{ json . }}')
      NanoCpu=$(docker inspect $first --format "{{json (index .HostConfig ).NanoCpus}}")
      if [[ $NanoCpu -gt 0 ]]
      then
        echo "The value of NanoCpu $NanoCpu"
        NoCpuCore=$(expr $NanoCpu / $nanoCPUUnit)
        CPUPERC=$(echo "$stats" | jq -r '.CPUPerc')
        cpuInfo=$(bc -l <<< $(echo $CPUPERC | sed "s/%//g"))
        ActCPUPerc="$(echo $cpuInfo / $NoCpuCore | bc)"
        CPUPERC=""
        CPUPERC+=$ActCPUPerc
        CPUPERC+="%"
      else
        echo "The value is less than or equal to zero"
        echo "NanoCpu $NanoCpu"
        CPUPERC=$(echo "$stats" | jq -r '.CPUPerc')
      fi
      BLOCKIO=$(echo "$stats" | jq -r '.BlockIO')
#      CPUPERC=$(echo "$stats" | jq -r '.CPUPerc')
      MEMPERC=$(echo "$stats" | jq -r '.MemPerc')
      MEMUSAGE=$(echo "$stats" | jq -r '.MemUsage')
      NAME=$(echo "$stats" | jq -r '.Name')
      CREATEDAT=$(echo "$status" | jq -r '.CreatedAt')
      IMAGE=$(echo "$status" | jq -r '.Image')
      PORTS=$(echo "$status" | jq -r '.Ports')
      RUNNINGFOR=$(echo "$status" | jq -r '.RunningFor')
      SIZE=$(echo "$status" | jq -r '.Size')
      STATE=$(echo "$status" | jq -r '.State')
      STATUS=$(echo "$status" | jq -r '.Status')
      # Logs the Info
      echo "BlockIO: $BLOCKIO"
      echo "CPUPerc: $CPUPERC"
      echo "MemPerc: $MEMPERC"
      echo "MemUsage: $MEMUSAGE"
      echo "Name: $NAME"
      echo "CreatedAt: $CREATEDAT"
      echo "Image: $IMAGE"
      echo "Ports: $PORTS"
      echo "RunningFor: $RUNNINGFOR"
      echo "Size: $SIZE"
      echo "State: $STATE"
      echo "Status: $STATUS"
      # Formatting the information into json object
      BODY='{
        "container_id": "'"$first"'",
        "block_io": "'"$BLOCKIO"'",
        "cpu_perc": "'"$CPUPERC"'",
        "mem_perc": "'"$MEMPERC"'",
        "mem_usage": "'"$MEMUSAGE"'",
        "container_name": "'"$NAME"'",
        "container_created_at": "'"$CREATEDAT"'",
        "image": "'"$IMAGE"'",
        "ports": "'"$PORTS"'",
        "running_for": "'"$RUNNINGFOR"'",
        "size": "'"$SIZE"'",
        "state": "'"$STATE"'",
        "status": "'"$STATUS"'",
        "timestamp": "'"$TIMESTAMP"'",
	      "instance_id": "'"$instanceId"'"
      }'
      # Making a request to the server
      curl --data "$BODY" \
          --header 'content-type: application/json' \
          http://localhost:5000/log/docker_info
      containers=$rest
      else
        echo "No Containers are running"
        sleep 2
    fi
  done
  sleep 1
done
