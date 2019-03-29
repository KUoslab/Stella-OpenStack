Prerequisites
-------------

Before you install and configure the ku.stella service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``ku.stella`` database:

     .. code-block:: none

        CREATE DATABASE ku.stella;

   * Grant proper access to the ``ku.stella`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON ku.stella.* TO 'ku.stella'@'localhost' \
          IDENTIFIED BY 'KU.STELLA_DBPASS';
        GRANT ALL PRIVILEGES ON ku.stella.* TO 'ku.stella'@'%' \
          IDENTIFIED BY 'KU.STELLA_DBPASS';

     Replace ``KU.STELLA_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``ku.stella`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt ku.stella

   * Add the ``admin`` role to the ``ku.stella`` user:

     .. code-block:: console

        $ openstack role add --project service --user ku.stella admin

   * Create the ku.stella service entities:

     .. code-block:: console

        $ openstack service create --name ku.stella --description "ku.stella" ku.stella

#. Create the ku.stella service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        ku.stella public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        ku.stella internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        ku.stella admin http://controller:XXXX/vY/%\(tenant_id\)s
