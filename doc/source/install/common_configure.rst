2. Edit the ``/etc/ku.stella/ku.stella.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://ku.stella:KU.STELLA_DBPASS@controller/ku.stella
