
import os

from Handler import Handler
import MySQLdb

class HSMySQLHandler(Handler):
    """
    Implements the abstract Handler class, sending data to a mysql table
    """
    conn = None

    def __init__(self, config=None):
        """
        Create a new instance of the MySQLHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Options
        self.hostname = self.config['hostname']
        self.port = int(self.config['port'])
        self.username = self.config['username']
        self.password = self.config['password']
        self.database = self.config['database']
        self.table = self.config['table']
        self.col_time = self.config['col_time']
        self.col_metric = self.config['col_metric']
        self.col_value = self.config['col_value']
        self.col_rbd_name = self.config['col_rbd_name']

        # Connect
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(HSMySQLHandler, self).get_default_config_help()

        config.update({
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(HSMySQLHandler, self).get_default_config()

        config.update({
        })

        return config

    def __del__(self):
        """
        Destroy instance of the MySQLHandler class
        """
        self._close()

    def process(self, metric):
        """
        Process a metric
        """
        # Just send the data
        self._send(str(metric))

    def _get_rbd_list(self):
        rbd_conf_path = "/etc/rbc"
        files = os.listdir(rbd_conf_path)
        rbd_list = []
        for file in files:
            if os.path.isfile(rbd_conf_path + "/" + file):
                rbd = file.split(".")[0]
                rbd_list.append(rbd)
        return rbd_list

    def _send(self, data):
        """
        Insert the data
        """
        rbd_list = self._get_rbd_list()

        data = data.strip().split(' ')
        metric = data[0]
        new_metric = None
        rbd_name = None
        for rbd in rbd_list:
            if rbd in metric:
                new_metric = metric.split(rbd)[1].strip("_")
                rbd_name = rbd
                break
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO %s (%s, %s, %s, %s) VALUES(%%s, %%s, %%s, %%s)"
                           % (self.table, self.col_metric,
                              self.col_time, self.col_value, self.col_rbd_name),
                           (new_metric, data[2], data[1], rbd_name))
            cursor.close()
            self.conn.commit()
        except BaseException, e:
            # Log Error
            self.log.error("HSMySQLHandler: Failed sending data. %s.", e)
            # Attempt to restablish connection
            self._connect()

    def _connect(self):
        """
        Connect to the MySQL server
        """
        self._close()
        self.conn = MySQLdb.Connect(host=self.hostname,
                                    port=self.port,
                                    user=self.username,
                                    passwd=self.password,
                                    db=self.database)

    def _close(self):
        """
        Close the connection
        """
        if self.conn:
            self.conn.commit()
            self.conn.close()
