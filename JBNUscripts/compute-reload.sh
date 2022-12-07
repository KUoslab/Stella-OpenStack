#!/bin/bash
echo "systemctl stop nova-compute.service"
systemctl stop nova-compute.service
echo "systemctl stop neutron-linuxbridge-*"
systemctl stop neutron-linuxbridge-agent.service
systemctl stop neutron-linuxbridge-cleanup.service

sleep 2

echo "systemctl start nova-compute.service"
systemctl start nova-compute.service
echo "systemctl start neutron-linuxbridge-*"
systemctl start neutron-linuxbridge-agent.service
systemctl start neutron-linuxbridge-cleanup.service

sleep 1

systemctl status nova-compute.service
systemctl status neutron-linuxbridge-agent.service
systemctl status neutron-linuxbridge-cleanup.service
