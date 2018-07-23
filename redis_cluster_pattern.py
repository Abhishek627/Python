import redis
import ast

'''
Gets data from keys having a pattern from redis
'''

def get_redis_keys(conn, pattern):
    for key in conn.scan_iter(pattern):
        yield conn.get(key)


if __name__ == '__main__':
    redis_conn = redis.StrictRedis(host='{redis_host_ip}', port=6379, db=0)
    result = 0
    for item in get_redis_keys(redis_conn, pattern='*::sample'):
        val = ast.literal_eval(item)['skip_count']
        result += val

    print result
