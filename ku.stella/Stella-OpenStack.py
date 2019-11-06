import argparse
import logging
import os

# for API server
from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api

import connect_openstack

app = Flask(__name__)
api = Api(app)
#

"""

Stella-OpenStack Conment main file
                                         
- by jmlim@os.korea.ac.kr

"""
class VM_info:
    _list_vms = {}

    # _vm_name = " "
    # _instance_name = " "
    # _project_id = " "
    # _hypervisor_name = " "
    # _hypervisor_ip = " "

    def print_all(self):
        return self._list_vms

    def print_num(self):
        return len(self._list_vms) + 1

    def set_info(self, _vm_name, _instance_name, _project_id, _hypervisor_name, _hypervisor_ip, _sla_option,
                 _sla_value):
        # Key for VMs list
        num = len(self._list_vms)
        # Add to VMs list
        # self._list_vms[num] = [_vm_name, _instance_name, _project_id, _hypervisor_name, _hypervisor_ip]
        self._list_vms[num] = {'vm_name': _vm_name, 'instance_name': _instance_name, 'project_id': _project_id,
                               'hypervisor_name': _hypervisor_name, 'hypervisor_ip': _hypervisor_ip,
                               'SLA_Option': _sla_option, 'SLA_Value': _sla_value}
        # _tmp = [ _vm_name, _instance_name, _project_id, _hypervisor_name, _hypervisor_ip]
        # self._vm_info.append(_tmp)
        return len(self._list_vms)

    def print_SLA(self, _name):
        count = -1
        for tmp in self._list_vms:
            # print(self._list_vms[tmp])
            if _name in self._list_vms[tmp]["vm_name"]:
                count = tmp
                break
            else:
                print("N")
        # print SLA_option and SLA_Value
        # print(self._list_vms[tmp]["vm_name"])
        # print(self._list_vms[count]["SLA_Option"])
        # print(self._list_vms[count]["SLA_Value"])

        # return self._list_vms['vm_name']

    def get_instance_name_by_name(self, _name):
        count = -1
        for count in self._list_vms:
            # print(self._list_vms[tmp])
            # print(count)
            if _name in self._list_vms[count]["vm_name"]:
                _instance_name = self._list_vms[count]["instance_name"]
                count = count
                # print("break")
                break
        return _instance_name

    def get_sla_option_by_name(self, _name):
        count = -1
        for count in self._list_vms:
            # print(self._list_vms[tmp])
            # print(count)
            if _name in self._list_vms[count]["vm_name"]:
                _sla_option = self._list_vms[count]["SLA_Option"]
                count = count
                # print("break")
                break
        return _sla_option

    def get_sla_value_by_name(self, _name):
        count = -1
        for count in self._list_vms:
            # print(self._list_vms[tmp])
            # print(count)
            if _name in self._list_vms[count]["vm_name"]:
                _sla_value = self._list_vms[count]["SLA_Value"]
                count = count
                # print("break")
                break
        return _sla_value

    def set_SLA(self, _name, _SLA_Option, _SLA_Value):
        count = -1
        for count in self._list_vms:
            # print(self._list_vms[tmp])
            # print(count)
            if _name in self._list_vms[count]["vm_name"]:
                # print(self._list_vms[count]["vm_name"])
                count = count
                # print("break")
                break
        # print SLA_option and SLA_Value
        # print(self._list_vms[count]["vm_name"])
        self._list_vms[count].update(SLA_Option=_SLA_Option)
        # print(self._list_vms[count]["SLA_Option"])
        # self._list_vms[count]['SLA_Option']: _SLA_Option
        self._list_vms[count].update(SLA_Value=_SLA_Value)
        # print(self._list_vms[count]["SLA_Value"])

        return count


class hypervisor_info:
    _list_hypervisor = {}
    def print_all(self):
        return self._list_hypervisor

    def set_data(self, _name, _ip):
        self._list_hypervisor[_name] = {'IP': _ip, 'c_usage': 1000, 'n_maxcredit': 10000, 'b_bw': 400000}

    def get_data(self, _name):
        return self._list_hypervisor[_name]["IP"]

    def set_capacity(self, _name, _type, _value):
        self._list_hypervisor[_name].update(_type=_value)

    def get_capacity(self, _name, _type):
        return self._list_hypervisor[_name][_type]

    def get_weight(self, _name, _type):
        tmp = self.get_capacity(self, _name, _type)
        if _type == 'c_usage':
            cap = 1000
        elif _type == 'n_maxcredit':
            cap = 10000
        else:
            cap = 400000
        weight = ((cap - tmp)/cap)*100
        return weight

# global variables
hypervisors = hypervisor_info
vms = VM_info
list_hypervisor_name = []

class Stella_OpenStack(Resource):

    def __init__(self, log_file=None):
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger("Stella-OpenStack START")
        self.log_file = log_file

        if log_file:
            self.log_handler = logging.FileHandler(self.log_file)
            self.logger.addHandler(self.log_handler)

        self.__stop = False

        # self.signal(signal.SIGINT, self.stop)
        # self.signal(signal.SIGTERM, self.stop)

    def main(self):
        self.logger.info("STELLA: PID {0}".format(os.getpid()))

    def stop(self, signum, frame):
        self.__stop = True
        self.logger.info("STELLA: Signal {0}".format(signum))
        self.logger.info("STELLA: STOP")



# Stella-OpenStack API list
# /stella : Check status of Stella scheduler and Stella-OpenStack
# /stella/vms : Returns the list of VMs and information of each VMs
# /stella/vms/sla: Set SLA for VM. Use instance name in horizon as a Input
# /stella/hypervisor : Returns Hypervisor IP address
@app.route('/stella/', methods=['GET'])
def StellaAPI_Status():
    return "Stella-OpenStack is ON"

@app.route('/stella/vms', methods=['GET'])
def StellaAPI_listVMs():
    return jsonify(vms.print_all(vms))

@app.route('/stella/vms/filter', methods=['POST'])
def StellaAPI_Filter():
    if not request.json or not 'name' in request.json:
        abort(400)
    if not request.json or not 'SLA_Option' in request.json:
        abort(400)
    if not request.json or not 'SLA_Value' in request.json:
        abort(400)
    _available_hosts = {}
    # tmp = {host_name, weight}
    _name = request.json['name']
    _SLA_option = request.json['SLA_Option']
    _SLA_value = request.json['SLA_Value']

    count = 0
    for index in list_hypervisor_name:
        idle = hypervisors.get_capacity(hypervisors, index, _SLA_option)
        if int(_SLA_value) < idle:
            if _SLA_option == 'c_usage':
                w1 = hypervisors.get_weight(self, index, 'n_maxcredit')
                w2 = hypervisors.get_weight(self, index, 'b_bw')
            elif _SLA_option == 'n_maxcredit':
                w1 = hypervisors.get_weight(self, index, 'c_usage')
                w2 = hypervisors.get_weight(self, index, 'b_bw')
            else:
                w1 = hypervisors.get_weight(self, index, 'c_usage')
                w2 = hypervisors.get_weight(self, index, 'n_maxcredit')

            _available_hosts[count]={'host_name': index, 'weight': w1+w2}
            sorted(_available_hosts, key=lambda hosts: _available_hosts[2])
            print(hosts)
#            new_idle = idle - int(_SLA_value)
#            hypervisors.set_capacity(hypervisors, index, _SLA_option, new_idle)
#            print(hypervisors.print_all(hypervisors))





@app.route('/stella/vms/sla', methods=['POST'])
def StellaAPI_Set_SLA_VM():
    if not request.json or not 'name' in request.json:
        abort(400)
    if not request.json or not 'SLA_Option' in request.json:
        abort(400)
    if not request.json or not 'SLA_Value' in request.json:
        abort(400)

    _name = request.json['name']
    _SLA_option = request.json['SLA_Option']
    _SLA_value = request.json['SLA_Value']

    count = vms.set_SLA(vms, _name, _SLA_option, _SLA_value)
    instance_name = vms.get_instance_name_by_name(vms, _name)
    sla_option = vms.get_sla_option_by_name(vms, _name)
    sla_value = vms.get_sla_value_by_name(vms, _name)
    # print(instance_name)

    # get_ROOT privilege
    olduid = 0
    if os.geteuid() != 0:
        # running as normal user
        olduid = os.geteuid()
        print(olduid)
        os.seteuid(0)

    # execute SLA setting script
    cmd_str = './insert_sla.sh' + ' ' + instance_name + ' ' + sla_option + ' ' + sla_value
    print(cmd_str)
    os.system(cmd_str)

    # reset user privilege
    if olduid != 0:
        os.seteuid(olduid)

    if (count < 0):
        return jsonify({'message': 'error'})
    else:
        return jsonify(vms.print_all(vms))

@app.route('/stella/hypervisor', methods=['POST'])
def StellaAPI_SearchHypervisorsByName():
    if not request.json or not 'name' in request.json:
        abort(400)
    else:
        _name = request.json['name']
        hypervisors.get_data(hypervisors, _name)
        return jsonify({'hypervisor_ip': hypervisors.get_data(hypervisors, _name)})

#
# Stella-OpenStack API list end

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", help="log filename", default=None)
    parser.add_argument("--pid", help="pid filename", default='/tmp/stella.pid')
    args = parser.parse_args()

    # fork to make deamin process
    # pid = os.fork()
    # if pid > 0:
    # for parent process

    #    exit(0)

    # else:
    # For children process
    #    os.chdir('/')
    #    os.setsid()
    #    os.umask(0)

    #    pid = os.fork()
    #    if pid > 0:
    #        exit(0)

    #    else:
    #        sys.stdout.flush()
    #        sys.stderr.flush()

    #        si = open(os.devnull, 'r')
    #        so = open(os.devnull, 'a+')
    #        se = open(os.devnull, 'a+')

    #        os.dup2(si.fileno(), sys.stdin.fileno())
    #        os.dup2(so.fileno(), sys.stdout.fileno())
    #        os.dup2(se.fileno(), sys.stderr.fileno())

    #        with open(args.pid, "w") as pid_file:
    #            pid_file.write(str(os.getpid()))

    #        Stella = Stella_OpenStack(args.log)
    #        code = Stella.main()
    # exit(code)

    Stella = Stella_OpenStack(args.log)
    code = Stella.main()

    Stella.logger.info("STELLA: connect to Stella-cloud")
    conn = connect_openstack.Opts.create_connection_from_config()

    Stella.logger.info("STELLA: listing hypervisor")

#    list_hypervisor_name = []
    list_hypervisor_ip = []
    # list_hypervisor = {}

    for HYPERVISOR in conn.compute.hypervisors():
        list_hypervisor_name.append(HYPERVISOR.name)

    for HYPERVISOR in conn.compute.hypervisors(list_hypervisor_name):
        list_hypervisor_ip.append(HYPERVISOR.host_ip)

    # Make key-value storage for hypervisor
    # e.g. hypervisor name: hypervisor ip
    #hypervisors = hypervisor_info
    # print(hypervisors.print_num(hypervisors))
    count = 0
    for index in list_hypervisor_name:
    #    print(index)
        list_hypervisor = {list_hypervisor_name[count]: list_hypervisor_ip[count]}
        hypervisors.set_data(hypervisors, list_hypervisor_name[count], list_hypervisor_ip[count])
        count = count + 1
    # for debugging
        print(hypervisors.print_all(hypervisors))
    # print(hypervisors.print_num(hypervisors))

    # Storing VM information

    print("VM information")
    for VM in conn.compute.servers():
        # print("VM_NAME: " + VM.name)
        # print("INSTANCE_NAME: " + VM.instance_name)
        # print("PROJECT_ID: " + VM.project_id)
        # print("HYPERVISOR_HOST: " + VM.hypervisor_hostname)
        # print("HOST_ID: " + VM.host_id)
        # print(vms.print_num(vms))
        ip = hypervisors.get_data(hypervisors, VM.hypervisor_hostname)
        vms.set_info(vms, VM.name, VM.instance_name, VM.project_id, VM.hypervisor_hostname, ip, '-', '-')

    # vms.print_SLA(vms, "stella_test-3")
    # vms.set_SLA(vms, "stella_test-3", 'b_bw', '100000')

    # print(VM)

    # hypervisor_list_name = " "
    # hypervisor_list_ip = " "

    # Get hypervisor list AND ip address
    # for HYPERVISOR in conn.compute.hypervisors():
    #    tmp_hypervisor['name'] = HYPERVISOR.name
    #    hypervisor_list_name =
    #
    # for HYPERVISOR in conn.compute.hypervisors(hypervisor_list_name):
    #    hypervisor_list_ip = HYPERVISOR.host_ip

    # for Debugging

    # print(hypervisor_list_name)
    # print(hypervisor_list_ip)

    # print("VM information")
    # for VM in conn.compute.servers():
    #    print("VM_NAME: " + VM.name)
    #    print("INSTANCE_NAME: " + VM.instance_name)
    #    print("PROJECT_ID: " + VM.project_id)
    #    print("HYPERVISOR_HOST: " + VM.hypervisor_hostname)
    #    print("HOST_ID: " + VM.host_id)
    #    print(VM)

    # for HYPERVISOR in conn.compute.hypervisors("DevStack"):
    #    print(HYPERVISOR)

    # print("tenant information: ")
    # for HYPERVISOR in conn.identity.projects():
    #    print(HYPERVISOR)

    # VM_info = VM_info.set_info()
    # print(VM_info)

    # run API server
    app.run(host='0.0.0.0', port=5001, debug=True)
#    app.run(host='163.152.20.140')
