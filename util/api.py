import configparser
import os
import requests
import urllib3

from util.json import write_json


class Api:

    def __init__(self, servicename, f, p, save_to_file_path):
        self.servicename = servicename
        self.filter = f
        self.project = p
        self.temppath = save_to_file_path

    def getcall_tests(self):
        pass
        # config = configparser.RawConfigParser()
        # config.read(os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
        #                          'resources', 'configfile.properties'))
        # urllib3.disable_warnings()
        # uri = 'http://' + config.get('API', 'api.base-uri') + config.get('API', self.servicename)
        # PARAMS = {'tags': self.filter.split(',')}
        # headers = {'content-type': 'application/json', 'project': self.project}
        # r = requests.get(url=uri, params=PARAMS, headers=headers, verify=False)
        # if r.status_code == 200:
        #     data = r.json()
        #     print(data)
        #     write_json(data, self.temppath)

    def getcall_run_conf(self):
        pass
        # config = configparser.RawConfigParser()
        # config.read(os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
        #                          'resources', 'configfile.properties'))
        # urllib3.disable_warnings()
        # uri = 'http://' + config.get('API', 'api.base-uri') + config.get('API', self.servicename)
        # PARAMS = {'testconfig': self.filter}
        # headers = {"content-type": "application/json", "project": self.project}
        # r = requests.get(url=uri, params=PARAMS, headers=headers, verify=False)
        # if r.status_code == 200:
        #     data = r.json()
        #     print(data)
        #     write_json(data, self.temppath)
        # else:
        #     print(r.status_code)

    def getcall_data_namespace(self):
        pass
        # config = configparser.RawConfigParser()
        # config.read(os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
        #                          'resources', 'configfile.properties'))
        # urllib3.disable_warnings()
        # uri = 'http://' + config.get('API', 'api.base-uri') + config.get('API', self.servicename)
        # # PARAMS = {'name': self.filter}
        # PARAMS = {}
        # headers = {"content-type": "application/json", "project": self.project}
        # r = requests.get(url=uri, params=PARAMS, headers=headers, verify=False)
        # if r.status_code == 200:
        #     data = r.json()
        #     print(data)
        #     write_json(data, self.temppath)
        # else:
        #     print(r.status_code)

    def getcall_repository(self):
        pass
        # config = configparser.RawConfigParser()
        # config.read(os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
        #                          'resources', 'configfile.properties'))
        # urllib3.disable_warnings()
        # uri = 'http://' + config.get('API', 'api.base-uri') + config.get('API', self.servicename)
        # PARAMS = {'identifier': self.filter}
        # headers = {'content-type': 'application/json', 'project': self.project}
        # r = requests.get(url=uri, params=PARAMS, headers=headers, verify=False)
        # if r.status_code == 200:
        #     return r.json()[0]['property']
        # else:
        #     return None