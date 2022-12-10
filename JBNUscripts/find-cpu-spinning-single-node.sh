#!/bin/bash

stty cols 300
top=`top -bcn 1`

result=$(echo "$top"  | egrep "((\s[0-9][0-9][0-9][0-9]\s\s)|(\s[0-9][0-9][0-9]\.[0-9]\s))"  | grep /usr/bin/qemu-system-x86_64  | awk -v OFS=',' '{print $9 ,  substr($14, 7, 17)}')
hostname=$(hostname)
for row in $result
do
        cpu_usage=$(echo $row | awk -F, '{print $1}')
        instance=$(echo $row | awk -F, '{print $2}')
        uuid=$(virsh dumpxml $instance | grep "<uuid>" | awk '{print substr($1, 7, 36)}')
        name=$(virsh dumpxml $instance | grep nova:name | sed 's/<nova:name>\|<\/nova:name>\| //g')
        user=$(virsh dumpxml $instance | grep nova:user | awk '{ print substr($2, 41) }' | sed 's/<\/nova:user>//g')
        project=$(virsh dumpxml $instance | grep nova:project | awk '{ print substr($2, 41) }' | sed 's/<\/nova:project>//g')
        printf "%-10s\t%-10s\t%-17s\t%-36s\t%-30s\t%-20s\t%s\n" $hostname $cpu_usage $instance $uuid $name $user $project
done
logout
