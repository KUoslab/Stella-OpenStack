#!/bin/bash
# 지금까지 194.163.182.183, 51.89.217.80, 186.195.132.204 185.167.96.138 178.154.224.45  155.159.120.74 차단됨
ip="43.131.43.132" # 여기에 차단할 IP 주소 넣고 실행
routers=$(sudo ip netns list | grep router | awk '{ print $1 }')
for router in $routers
do
	sudo ip netns exec $router iptables -I FORWARD  1 -s $ip -d 0.0.0.0/0 -j DROP
	sudo ip netns exec $router iptables -L

done
