===============================
ku.stella
===============================

Stella Cloud project

This page is Stella-OpenStack code repository.
Stella-OpenStack support Stella VM scheduler to set performance SLA in OpenStack IaaS clouds. 
Visit our project page for detailed information about Stella project.

* Documentation: https://stella.korea.ac.kr
* Source
        OpenStack repo: https://git.openstack.org/cgit/openstack/ku.stella
        GitHub repo: https://github.com/KUoslab/Stella-OpenStack
* Bugs
        Email: starlab@os.korea.ac.kr
        Lanchpad: https://bugs.launchpad.net/KU.stella


--------

* Stella-OpenStack APIs

Stella-OpenStack APIs(a.k.s Stella APIs) provide access Stella-OpenStack functions.
Stella APIs support RestAPI(http based APIs).
The list of Stella APIs is below. 

1. /stella: 
        Check the status of Stella scheduler(xGoS) and Stella-OpenStack.
2. /stella/vms: 
        Returns the list of VMs and information of each VMs.
3. /stella/vms/sla:
        Set SLA for VM. Use instance name in horizon as a Input
4. /stella/hypervisor:
        Returns the IP address of the hypervisor host.
        'hypervisor_name' field is essential.
