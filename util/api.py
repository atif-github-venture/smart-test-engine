import configparser
import os
import requests
import urllib3


class Api:
    def __init__(self, servicename, f, p):
        self.servicename = servicename
        self.filter = f
        self.project = p

    def getcall_macro_tests(self):
        config = configparser.RawConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                                 'resources', 'configfile.properties'))
        urllib3.disable_warnings()
        uri = 'http://' + config.get('API', 'api.base-uri') + config.get('API', self.servicename)
        PARAMS = {'tags': self.filter.split(',')}
        headers = {'content-type': 'application/json', 'project': self.project}
        r = requests.get(url=uri, params=PARAMS, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            print(data)

    def getcall_run_conf(self):
        config = configparser.RawConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                                 'resources', 'configfile.properties'))
        urllib3.disable_warnings()
        uri = 'http://' + config.get('API', 'api.base-uri') + config.get('API', self.servicename)
        PARAMS = {'testconfiguration': self.filter}
        headers = {"content-type": "application/json", "project": self.project}
        r = requests.get(url=uri, params=PARAMS, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            print(data)
        else:
            print(r.status_code)

    def getcall_data_namespace(self):
        config = configparser.RawConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                                 'resources', 'configfile.properties'))
        urllib3.disable_warnings()
        uri = 'http://' + config.get('API', 'api.base-uri') + config.get('API', self.servicename)
        # PARAMS = {'name': self.filter}
        PARAMS={}
        headers = {"content-type": "application/json", "project": self.project}
        r = requests.get(url=uri, params=PARAMS, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            print(data)
        else:
            print(r.status_code)
