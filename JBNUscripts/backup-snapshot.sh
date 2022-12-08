#!/usr/bin/env bash
#
# OpneStack의 프로젝트들에 존재하는 인스턴스의 스냅샷을 백업서버에 전송한다.


PATH_TO_JOBLIST=queue
PATH_TO_SNAPSHOT_DIR=/var/lib/glance/images
#openstack server list -c "ID" --all-projects --host main02 | grep "[a-z0-9]" | sed 's/|\| //g' >> $PATH_TO_JOBLIST

while [[ -n $(cat $PATH_TO_JOBLIST) ]]; do
        # 백업할 인스턴스 id
        instance_id=$(head -n 1 $PATH_TO_JOBLIST)
        # 백업할 인스턴스 이름
        instance_name=$(openstack server show $instance_id | grep " name " | awk -F '|' '{print $3}' | sed 's/ //g')
        echo $instance_name
        # 백업할 스냅샷 이름 정하기
        timestamp=$(date "+%Y%m%d")
        snapshot_name="${instance_name}__${instance_id}__${timestamp}"
        echo $snapshot_name
        # matadata 저장
        mkdir -p /home/ubuntu/backup/${instance_name}__${instance_id}
        openstack server show $instance_id > /home/ubuntu/backup/${instance_name}__${instance_id}/info
        # 스냅샷 생성
        snapshot_id=$(openstack server image create --name $snapshot_name $instance_id | grep " id" | awk -F '|' '{print $3}' | sed 's/ //g')
        echo $snapshot_id
        # 스냅샷 생성 될까지 기다림
        while [ $(openstack image show $snapshot_id | grep status | awk '{print $4}') != "active" ]; do
                echo "Waiting..."
                sleep 5
        done
        ls -al $PATH_TO_SNAPSHOT_DIR/$snapshot_id
        # 스냅샷 폴더로 이동
        cp -r $PATH_TO_SNAPSHOT_DIR/$snapshot_id /home/ubuntu/backup/${instance_name}__${instance_id}/${timestamp}__${snapshot_id}
        # 스냅샷 삭제
        openstack image delete $snapshot_id
        # 작업 리스트에서 삭제
        sed -i '1d' $PATH_TO_JOBLIST
done
