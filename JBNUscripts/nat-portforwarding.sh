#!/bin/bash

# iptables 로 ssh, http 를 NAT 설정하는 스크립트
# ssh  == (Public IP):19xxx -> 192.168.0.xxx:7777
# http == (Public IP):18xxx -> 192.168.0.xxx:80 (TCP and UDP)
# 위와 같이 포트 번호를 기준으로 내부 인스턴스로 NAT
# 자세한 설명은 readme.md 를 참고하세요.


# ip netns 로 확인: 최근에 만들어진 라우터가 id 가 더 높음
# ip netns <router name> ifconfig <- 여기서 두 번째 NIC 확인해야함
router=""
#nic="qr-0cf50ae1-50"
nic=""  # 외부 IP가 할당된 인터페이스

ssh_public_port_prefix="19"    # ssh  19xxx -> 7777
http_public_port_prefix="18"   # http 18xxx -> 80
https_public_port_prefix="17"   # http 18xxx -> 80
node_public_port_prefix="13"   # nodejs devel 13xxx -> 3000
http8080_public_port_prefix="10"   # http 10xxx -> 8080

ssh_inner_port="7777"
http_inner_port="80"
https_inner_port="443"
node_inner_port="3000"
http8080_inner_port="8080"


inner_net_prefix="10.0.0."

echo "J-cloud NAT 설정 스크립트입니다."
echo "편의를 위해 스크립트 내에 IP 와 라우터 이름을 하드코딩해 놓았습니다."
echo "스크립트 유출에 주의해주세요."
echo ""
echo "ssh  == (Public IP):${ssh_public_port_prefix}xxx -> ${inner_net_prefix}xxx:${ssh_inner_port}"
echo "http == (Public IP):${http_public_port_prefix}xxx -> ${inner_net_prefix}xxx:${http_inner_port}"
echo ""

#ssh $username@$controller_ip -p $controller_ssh_port /bin/bash -s ${router} ${option} ${os2019_nic} ${ssh_public_port_prefix} ${inner_net_prefix} ${ssh_inner_port} ${http_public_port_prefix} ${http_inner_port}

i=3

while [ $i -lt 255 ]; do
        sudo ip netns exec $router iptables -t nat -A PREROUTING -i $nic -p tcp --dport $ssh_public_port_prefix$(printf '%03d' $i) -j DNAT --to $inner_net_prefix$(printf '%d' $i):$ssh_inner_port
        sudo ip netns exec $router iptables -t nat -A PREROUTING -i $nic -p tcp --dport $http_public_port_prefix$(printf '%03d' $i) -j DNAT --to $inner_net_prefix$(printf '%d' $i):$http_inner_port
        sudo ip netns exec $router iptables -t nat -A PREROUTING -i $nic -p udp --dport $http_public_port_prefix$(printf '%03d' $i) -j DNAT --to $inner_net_prefix$(printf '%d' $i):$http_inner_port
        sudo ip netns exec $router iptables -t nat -A PREROUTING -i $nic -p tcp --dport $https_public_port_prefix$(printf '%03d' $i) -j DNAT --to $inner_net_prefix$(printf '%d' $i):$https_inner_port
        sudo ip netns exec $router iptables -t nat -A PREROUTING -i $nic -p udp --dport $https_public_port_prefix$(printf '%03d' $i) -j DNAT --to $inner_net_prefix$(printf '%d' $i):$https_inner_port
        sudo ip netns exec $router iptables -t nat -A PREROUTING -i $nic -p tcp --dport $node_public_port_prefix$(printf '%03d' $i) -j DNAT --to $inner_net_prefix$(printf '%d' $i):$node_inner_port
        sudo ip netns exec $router iptables -t nat -A PREROUTING -i $nic -p udp --dport $node_public_port_prefix$(printf '%03d' $i) -j DNAT --to $inner_net_prefix$(printf '%d' $i):$node_inner_port
        sudo ip netns exec $router iptables -t nat -A PREROUTING -i $nic -p tcp --dport $http8080_public_port_prefix$(printf '%03d' $i) -j DNAT --to $inner_net_prefix$(printf '%d' $i):$http8080_inner_port
        sudo ip netns exec $router iptables -t nat -A PREROUTING -i $nic -p udp --dport $http8080_public_port_prefix$(printf '%03d' $i) -j DNAT --to $inner_net_prefix$(printf '%d' $i):$http8080_inner_port


        echo "$inner_net_prefix$(printf '%d' $i) 의 DNAT 설정이 ${text}되었습니다."
        ((i++))
done
sudo ip netns exec $router iptables -t nat -A POSTROUTING -o $nic -j MASQUERADE

echo "모든 설정이 완료되었습니다."
