from elasticsearch import Elasticsearch, client
from elasticsearch import helpers
from datetime import datetime, timedelta
import json
import random
import os

random.seed(7)

'''
Description: Python code to create random data in specified format and populate that data in elasticsearch with bulk api. Tested with es version> 6.


'''


# CREATING DATA OBJECT
'''
POST RPM_DATA/INTERFACE/{{INTERFACE_NUMBER}}
{
 "@timestamp:"2017-12-09 00:00:30",
 "resource_type":"interface",
 "connected: 'link-1',
 "probe-type":"sample",
 "loss-percent": 10,
 "Jitter" : 100 ,
 "avg-delay": 1

}
'''


def create_data_object_interface(num_interfaces, num_links, time_range):
    # Generating sample data
    for time_val in date_range_variable(time_range):
        for j in range(num_interfaces):
            sample_data = {
                "@timestamp": time_val,
                "resource_type": "interface",
                "resource_name": "ge-0/0/" + str(j),
                "connected": 'link-' + str(random.randint(1, num_links)),
                "probe_type": "sample",
                "loss_percent": random.randint(1, 70),
                "jitter": random.randint(10, 200),
                "avg_delay": random.randint(10, 200)
            }
            yield sample_data


def create_data_object_links(num_interfaces, num_links, time_range):
    for time_val in date_range_variable(time_range):
        for j in range(num_links):
            sample_data = {
                "@timestamp": time_val,
                "resource_type": "link",
                "resource_name": "link-" + str(j),
                "connected": 'device-' + str(random.randint(1, num_interfaces)),
                "probe_type": "sample",
                "loss_percent": random.randint(1, 70),
                "jitter": random.randint(10, 200),
                "avg_delay": random.randint(10, 200)
            }
            yield sample_data


def create_es_instance(ip_port):
    es = Elasticsearch(ip_port)
    return es


# CREATING TEMPLATE
def create_es_template(es, template_name, template_file_path):
    es_indices = client.IndicesClient(es)
    with open(template_file_path, 'r') as f:
        template_body = json.loads(f.read())
    es_indices.put_template(name=template_name, body=template_body)


def create_es_indices_bulk(es, data_list):
    '''
    For creating elastic search indices in bulk
    :param es:
    :param data_list:
    :return:
    '''
    print helpers.bulk(es, data_list)


def create_es_indices_bulk_parallel(es, data_list, thread_cnt):
    '''
    For creating elastic search indices in bulk ( Works with parallel threading, thus faster than es_indices_bulk)
    :param es:
    :param data_list:
    :param thread_cnt:
    :return:
    '''
    for success, info in helpers.parallel_bulk(es, data_list, thread_count=thread_cnt, chunk_size=1000000,
                                               request_timeout=30):
        if not success:
            print('A document failed:', info)


def search_es(es, index, type, search_query):
    '''
    For searching and getting data from ES instance
    :param es:
    :param index:
    :param type:
    :param search_query:
    :return:
    '''
    print json.dumps(es.search(index=index, doc_type=type, body={"query": search_query}), indent=2)


def format_time(input_time):
    allowed_format = "%d/%m/%Y %H:%M:%S.%f"
    return datetime.strptime(input_time, allowed_format)


## generate a time range with 3 in interval
def date_range_variable(time_range):
    start_time = time_range[0]
    end_time = time_range[1]
    delta = timedelta(seconds=180)
    while start_time <= end_time:
        yield start_time
        start_time += delta


def pre_process():
    start_time = raw_input("Enter the start time in dd/mm/yyyy H:M:S.ms format: ")
    end_time = raw_input("Enter the end time in dd/mm/yyyy H:M:S.ms format: ")
    es_server = raw_input("Enter the elasticsearch server and port in http://<server-ip>:<server-port> format: ")
    start_time = format_time(start_time)
    end_time = format_time(end_time)
    return es_server, (start_time, end_time)


def generate_data_for_tenant(tenant_name, time_range, es):
    start_time = datetime.now()
    index_prefix = "site-rpm-data"
    # create indexes with a fixed prefix, for easy of application of templates
    es_index_list = []
    for i in range(10):
        es_index_list.append(index_prefix + "-" + tenant_name + "-" + str(i))

    total_entry = 0
    for es_index in es_index_list:
        es_data = []
        for data in create_data_object_interface( num_interfaces=10, num_links=10, time_range=time_range):
            sample_entry = {
                "_op_type": "index",
                "_index": es_index,
                "_type": "device",
                "_source": data
            }
            es_data.append(sample_entry)
        total_entry += len(es_data)

        for data in create_data_object_links( num_interfaces=10, num_links=10, time_range=time_range):
            sample_entry = {
                "_op_type": "index",
                "_index": es_index,
                "_type": "device",
                "_source": data
            }
            es_data.append(sample_entry)
        total_entry += len(es_data)
        create_es_indices_bulk_parallel(es, es_data, thread_cnt=8)
    print "Number of entries added for tenant " + tenant_name + " : ", total_entry
    print "Time taken for indexing for tenant (hh:mm:ss.ms) " + tenant_name + " : ", datetime.now() - start_time


if __name__ == '__main__':
    es_server, time_range = pre_process()
    es = create_es_instance([es_server])
    create_es_template(es, template_name='site_template',
                       template_file_path=os.path.join(os.path.dirname(__file__), '../data/site_template.json'))
    generate_data_for_tenant("airtel", time_range, es)
    generate_data_for_tenant("vodafone", time_range, es)
    generate_data_for_tenant("idea", time_range, es)
