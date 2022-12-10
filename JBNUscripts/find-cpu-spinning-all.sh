#!/bin/bash
servers="com01 com02 com03 gpu01 gpu02"
result=""
for server in $servers
do

	temp=`sshpass -p 0slab ssh $server -tt -p 3932 < ~/find-cpu-spinning-single-node.sh | sed -n '/^'$server'/p'`
	result="$result$temp"

done
TZ=Asia/Seoul date
printf "%-10s\t%-10s\t%-17s\t%-36s\t%-30s\t%-20s\t%s\n" "HOSTNAME" "%CPU" "NAME" "UUID" "NOVA:NAME" "USER" "PROJECT"
echo "$result"
