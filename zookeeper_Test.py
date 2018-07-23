from kazoo.client import KazooClient

'''
Gets child nodes from zookeeper node
'''

zk = KazooClient(hosts='{zk_server_ip}:2181')
zk.start()
data= zk.get_children('/sample_child')
print "Number of devices in zookeeper" ,len(data)





