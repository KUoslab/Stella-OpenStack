# This work is done by Operating System Lab

"""
This file defines wrapper to connect OpenStack cloud
assume that we use DevStack for configuration file

by jmlim@os.korea.ac.kr
"""

import argparse
import os
import sys

import openstack
from openstack import utils
from openstack.config import loader

# kwlee
#utils.enable_logging(True, stream=sys.stdout)

#: Defines the OpenStack Config loud key in your config file,
#: typically in $HOME/.config/openstack/clouds.yaml. That configuration
#: will determine where the examples will be run and what resource defaults
#: will be used to run the examples.
STELLA_CLOUD = os.getenv('OS_CLOUD', 'Stella')
config = loader.OpenStackConfig()
CLOUD = openstack.connect(cloud=STELLA_CLOUD)


class Opts(object):
    def __init__(self, cloud_name='Stella-DevStack', debug=False):
        # This function is for init OpenStack connection
        # I use DevStack and the configureation file is automaticly generated in /etc/openstack/clouds.yaml
        self.cloud = cloud_name
        self.debug = debug
        # use identity v3 API
        self.identity_api_version = '3'

    def _get_resource_value(resource_key, default):
        return config.get_extra_config('example').get(resource_key, default)

    SERVER_NAME = 'openstacksdk-example'
    IMAGE_NAME = _get_resource_value('image_name', 'cirros-0.3.5-x86_64-disk')
    FLAVOR_NAME = _get_resource_value('flavor_name', 'm1.small')
    NETWORK_NAME = _get_resource_value('network_name', 'private')
    KEYPAIR_NAME = _get_resource_value('keypair_name', 'openstacksdk-example')
    SSH_DIR = _get_resource_value(
        'ssh_dir', '{home}/.ssh'.format(home=os.path.expanduser("~")))
    PRIVATE_KEYPAIR_FILE = _get_resource_value(
        'private_keypair_file', '{ssh_dir}/id_rsa.{key}'.format(
            ssh_dir=SSH_DIR, key=KEYPAIR_NAME))

    EXAMPLE_IMAGE_NAME = 'openstacksdk-example-public-image'

    def create_connection_from_config():
        return openstack.connect(cloud=STELLA_CLOUD)

    def create_connection_from_args():
        parser = argparse.ArgumentParser()
        config = loader.OpenStackConfig()
        config.register_argparse_arguments(parser, sys.argv[1:])
        args = parser.parse_args()
        return openstack.connect(config=config.get_one(argparse=args))

    def create_connection(auth_url, region, project_name, username, password):
        return openstack.connect(
            auth_url=auth_url,
            project_name=project_name,
            username=username,
            password=password,
            region_name=region,
            app_name='Stella-OpenStack',
            app_version='0.1',
        )
