import requests
import json
import datetime
import time

'''
Uses exposed rabbitmqctl api to get data about queues
'''

rabbit_url = 'rabbit_server_ip'
rabbit_username= 'rabbit_user'
rabbit_password = 'rabbit_pass'
queue_name = 'queue_name'
time_to_run = '1'  # In sec

url = 'http://{}:{}@{}:15672/api/queues/%2f/{}'.format(rabbit_username,rabbit_password, rabbit_url, queue_name)
flag = False
start_time = time.time()
entry = list()
while not flag:
    result = requests.get(url)
    if result.status_code == 200:
        data = json.loads(result.text)
        message_ready = data['messages_ready']
        message_unack = data['messages_unacknowledged']
        message_stat = data['message_stats']
        message_enter_rate = message_stat['publish_details']['rate']
        curr_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        entry.append({'Time': curr_time, 'message_in_ready_state': message_ready, 'message_unacked': message_unack,
                      'message_enter_rate': message_enter_rate})
        if int(time.time() - start_time) > 0.5 * 60:
            flag = True
        time.sleep(2)

print entry
