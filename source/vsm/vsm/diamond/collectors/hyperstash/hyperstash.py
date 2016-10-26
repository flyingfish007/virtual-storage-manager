
import os

import diamond.collector

import redis

class HyperstashCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(HyperstashCollector,
                            self).get_default_config_help()
        config_help.update({
            'test': 'Test test',
            'redis_host': 'The host to connect redis',
            'redis_port': 'The port of redis',
            'redis_db': 'The db of redis to fetch data',
            'hyperstash_metrics': 'The monitoring metrics of hyperstash'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """

        config = super(HyperstashCollector, self).get_default_config()
        config.update({
            'test': '',
            'redis_host': 'localhost',
            'redis_port': 6379,
            'redis_db': 0,
            'hyperstash_metrics': 'free_cache_ratio,used_cache_ratio,dirty_cache_ratio'
        })
        return config

    def _get_rbd_list(self):
        rbd_conf_path = "/etc/rbc"
        files = os.listdir(rbd_conf_path)
        rbd_list = []
        for file in files:
            if os.path.isfile(rbd_conf_path + "/" + file):
                rbd = file.split(".")[0]
                rbd_list.append(rbd)
        return rbd_list

    def collect(self):
        rbd_list = self._get_rbd_list()

        r = redis.StrictRedis(host=self.config('redis_host'),
                              port=int(self.config('redis_port')),
                              db=int(self.config('redis_db')))
        hyperstash_metrics = self.config['hyperstash_metrics']
        hyperstash_metrics_list = hyperstash_metrics.split(',')
        for rbd in rbd_list:
            for metric in hyperstash_metrics_list:
                metric = metric.strip(" ")
                new_metric = rbd + "_" + metric
                m_value = r.get(new_metric)
                self.publish(metric, m_value)
