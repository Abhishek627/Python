import logging

'''
Python code to use as a base class for working with redis cluster
'''


log = logging.getLogger(__name__)


class RedisCache(object):
    def __init__(self, redis_hosts, redis_port):
        self._conn = None
        self.redis_hosts = redis_hosts.split(",")
        self.port = redis_port

    def connection(self):
        startup_nodes = list()
        for item in self.redis_hosts:
            pair = dict()
            pair['host'], pair['port'] = item.split(':')
            startup_nodes.append(pair)
        if len(startup_nodes) > 1:
            import rediscluster
            self._conn = rediscluster.StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True,
                                                         retry_on_timeout=True)

        elif len(startup_nodes) == 1:
            import redis
            self._conn = redis.StrictRedis(host=startup_nodes[0]['host'], port=startup_nodes[0]['port'],
                                           retry_on_timeout=True)

        else:
            self._conn = None
        return self._conn

    def conn(self):
        if not self._conn:
            self._conn = self.connection()
        return self._conn

    def getkey(self, key):
        try:
            return self.conn().get(key)
        except Exception as e:
            log.error("Failed to get redis key {} with error {}".format(key, str(e)))

    def setkey(self, key, value, timer=None):
        try:
            return self.conn().set(key, value, timer)
        except Exception as e:
            log.error("Failed to set redis key {} with error {}".format(key, str(e)))

    def setTTL(self, key, time):
        try:
            return self.conn().expire(key, time)
        except Exception as e:
            log.error("Failed to set ttl for key {} with error {}".format(key, str(e)))

    def format_key(self, key):
        return key + "::agentCache"

    def increment_key(self, key):
        return self.conn().incr(key)
