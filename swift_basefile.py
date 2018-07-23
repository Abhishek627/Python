import os
import traceback
import copy
from urlparse import urlparse
from swiftclient.client import Connection
from swiftclient.utils import generate_temp_url
import requests
import logging
import urllib

RETRY_CNT = 5
CONN_TIMEOUT = 30

'''
Able to upload, download and delete file from swiftclient using openstack python swiftclient library
https://github.com/openstack/python-swiftclient

'''


class SwiftFileServer(object):
    """ Swift File server """

    def __init__(self, region_name):
        # self.cfg = cfg.CONF
        self.region_name = region_name
        # self.authurl = self.cfg.FileSvc.authurl
        # self.auth_version = self.cfg.FileSvc.auth_version
        # self.user = self.cfg.FileSvc.user
        # self.key = self.cfg.FileSvc.key
        # self.tenant_name = self.cfg.FileSvc.tenant_name
        # self.container_name = self.cfg.FileSvc.container_name
        # self.temp_url_key = self.cfg.FileSvc.temp_url_key
        # self.temp_url_key_2 = self.cfg.FileSvc.temp_url_key_2
        # self.chosen_temp_url_key = self.cfg.FileSvc.chosen_temp_url_key
        # self.authurl='http://10.204.248.50:35357/v2.0'
        self.authurl = 'http://10.204.248.228:35357/v2.0'
        self.auth_version='2.0'
        self.user='admin'
        self.key='passw0rd'
        self.tenant_name='admin'
        self.temp_url_key= 'mykey'
        self.temp_url_key_2='mykey2'
        self.chosen_temp_url_key= 'temp_url_key'
        self.container_name= 'mycontainer'
        self.storageurl = None
        self.swift_conn = None

    def connect_to_swift(self):
        """ return connect to swift fileserver """
        for i in range(RETRY_CNT):
            i += 1
            try:
                self.__init_swift_fileserver()
                break
            except Exception as err:
                print('[Try %d/%d ]: Connecting swift fileserver failed. %s %s',
                            i, RETRY_CNT, err, traceback.format_exc())
                if i == RETRY_CNT:
                    raise

    def __init_swift_fileserver(self):
        try:
            options = {
                'authurl': self.authurl,
                'user': self.user,
                'key': self.key,
                'auth_version': self.auth_version,
                'tenant_name': self.tenant_name,
                'insecure': True,
                'timeout': CONN_TIMEOUT,
                'os_options': {'region_name': self.region_name}}


            headers = {'Temp-URL-Key': self.temp_url_key,
                       'Temp-URL-Key-2': self.temp_url_key_2
                       }

            print_opts = copy.deepcopy(options)
            print_opts['key'] = '<password stripped>'
            self.swift_conn = Connection(**options)
            self.swift_conn.post_account(headers)
            self.swift_conn.put_container(self.container_name)
            self.storageurl = self.swift_conn.get_auth()[0]
            print ('swift-file-server: Connected. options %s storageurl %s',
                     print_opts, self.storageurl)
        except Exception as err:
            print('swift-file-server: Connect FAILED %s options %s',
                     err, print_opts)
            raise

    def upload_file(self, fpath, fname=None,expires=3600):
        """ upload the file in 'filepath' on to the file server  and return a
        temporary url for the users to download """
        if not self.swift_conn:
            self.connect_to_swift()
        if fname is None:
            fname = os.path.basename(fpath)
        finp = open(fpath, 'rb')
        try:
            self.swift_conn.put_object(
                container=self.container_name, obj=fname, contents=finp)
            print ('swift-file-server: Uploading file %s ... [OK]', fname)
        except Exception as err:
            logging.error(
                'swift-file-server: Unable to upload the file %s:  %s', fname, err)
            raise

        # return self.get_temp_download_url(fname,expires)

    def get_temp_download_url(self, fname, expires):
        """ return the temporary download url """
        file_uri = '%s/%s/%s' % (self.storageurl, self.container_name, fname)
        file_path = urlparse(file_uri).path
        key = getattr(self, self.chosen_temp_url_key)
        try:
            temp_url = generate_temp_url(file_path, expires, key, 'GET')
        except Exception as err:
            logging.error(
                'swift-file-server: Generating temp url for %s failed %s', fname, err)
            raise

        download_url = self.storageurl.replace(
            urlparse(self.storageurl).path, temp_url)
        print(
            'swift-file-server: Temporary download URL for file %s: %s', fname, download_url)
        return download_url

    def delete_file(self, fpath):
        """ Delete the file from the file server """
        fname = os.path.basename(fpath)
        try:
            self.swift_conn.delete_object(
                container=self.container_name, obj=fname)
            print('swift-file-server: Deleting file %s ... [OK]', fname)
        except Exception as err:
            print(
                'swift-file-server: Deleting file %s ... [FAIL]: %s %s (IGNORED) ', fname, err, traceback.format_exc())

    def getObjectContent(self, filename):
        return self.swift_conn.get_object(container=self.container_name, obj=filename)

import time
base_class=SwiftFileServer('central')
base_class.connect_to_swift()
# upload=base_class.upload_file(fpath='/Users/shabhishek/custom-function-0.1.tar.gz',fname='custom-function-0.1.tar.gz')
# print upload
download=base_class.get_temp_download_url(fname='oc-device.json',expires=3600)
# print download
# a=time.time()
# aa,bb=urllib.urlretrieve(download,filename="/Users/shabhishek/Desktop/test/test.tar.gz")
# print bb
# with open('/Users/shabhishek/Desktop/oc-device_latest1.json','w') as f:
#     f.write(data)
# print "Done"
# base_class.delete_file(fpath='oc-device_junos_dep_map.json')
