.. _verify:

Verify operation
~~~~~~~~~~~~~~~~

Verify operation of the ku.stella service.

.. note::

   Perform these commands on the controller node.

#. Source the ``admin`` project credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. List service components to verify successful launch and registration
   of each process:

   .. code-block:: console

      $ openstack ku.stella service list
