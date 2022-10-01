logfilname="docker.log"
echo "Started Logging"
#docker stats --no-stream | cat >> $logfilname
#CPU=$(docker stats --no-stream --format "table {{.CPUPerc}}")
#DATE=`date`
#echo $DATE  $CPU >> cpu_log.txt
docker stats --no-stream --format "{{ json . }}" >> $logfilname