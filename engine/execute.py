import json
import os
import sys
import time

from engine.heart import Heart
from util.api import Api
from util.saucelabs import SauceLabs


def spin_cloud_machine_for_execution(machine_name, token):
    path = (
        os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                     'resources', 'smart-digital.sh'))
    import subprocess
    ip = None
    cmd = path + " " + machine_name + " " + token
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        str = line.decode('utf-8')
        if 'ip:: ' in line.decode('utf-8'):
            ip = (str.splitlines()[0].split('ip:: ')[1]).strip()
        print(line),
    retval = p.wait()
    p.communicate()
    p.wait()
    print('The cloud platform is ready for execution!!!')
    print('IP obtained -> ' + ip)
    print('Waiting Selenium Server to load')
    import requests
    code = 0
    counter = 0
    while code != 200:
        try:
            code = requests.get('http://' + ip + ':4444/grid/api/hub').status_code
            print('Polling for selenium grid\'s health -> request status code: ')
            print(code)
            counter += 1
            time.sleep(1)
            if counter > 50:
                break
        except Exception as e:
            print(e)
            counter += 1
            time.sleep(1)
            if counter > 50:
                break
    if code != 200:
        destroy_cloud_instance(machine_name)
    return ip


# def spin_cloud_machine(machine_name):
#     from resources import digitalocean
#     droplet = digitalocean.Droplet(token="ca4fe5b59b62d1770e2f73e9f8c30e66778870373161f9d228fc188fd1941343",
#                                    name=machine_name,
#                                    region='nyc1',  # New York 2
#                                    image='ubuntu-14-04-x64',  # Ubuntu 14.04 x64
#                                    size_slug='512mb',  # 512MB
#                                    disk='1gb',
#                                    backups=True)
#     droplet.create()
#     condition = True
#     while condition:
#         actions = droplet.get_actions()
#         for action in actions:
#             action.load()
#             # Once it shows complete, droplet is up and running
#             print(action.status)
#             if action.status == 'completed':
#                 condition = False

# import json
# import requests
# api_token = 'ca4fe5b59b62d1770e2f73e9f8c30e66778870373161f9d228fc188fd1941343'
# api_url_base = 'https://api.digitalocean.com/v2/'
# headers = {'Content-Type': 'application/json',
#            'Authorization': 'Bearer {0}'.format(api_token)}
# api_url = '{0}account'.format(api_url_base)
#
# response = requests.get(api_url, headers=headers)
#
# if response.status_code == 200:
#     return json.loads(response.content.decode('utf-8'))
# else:
#     return None


def destroy_cloud_instance(machine_name):
    import subprocess
    p = subprocess.Popen(args=['docker-machine rm ' + machine_name + ' -y'], shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    p.wait()
    p.communicate()
    print('Deleted the cloud image and selenium grid -> ' + machine_name)


class Execute:
    session_id = None
    machine_name = None

    def __init__(self, test, f, b, a, r, p, d, t, tok):
        self.test = test
        self.filter = f
        self.buildnumber = b
        self.additionaltags = a
        self.runconfiguration = r
        self.project = p
        self.datanamespace = d
        self.type = t
        self.status = True
        self.token = tok

    def start_test(self):
        from datetime import datetime, timezone
        execution_time = datetime.now(timezone.utc)
        start_time = datetime.now(timezone.utc)
        if any("#web" in s for s in self.test['tags']):
            from util.common import to_hypen_lowercase
            ip = None
            if self.type == 'digitalocean':
                self.machine_name = to_hypen_lowercase(self.test['testname'])
                ip = spin_cloud_machine_for_execution(self.machine_name, self.token)
                if ip is None:
                    raise Exception('Exiting tests since could machine instantiation failed :(:(:(')
            rsteps = self.run_ui_test(ip)
            end_time = datetime.now(timezone.utc)
            time_diff = end_time - start_time
            mictest = {
                'testname': self.test['testname'],
                'status': self.status,
                'execution_time': execution_time.isoformat(),
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration': time_diff.seconds,
                'Steps': rsteps,
                'test_build_info': {
                    'filter': self.filter,
                    'buildnumber': self.buildnumber,
                    'additionaltags': self.additionaltags,
                    'runconfiguration': self.runconfiguration,
                    'project': self.project,
                    'datanamespace': self.datanamespace,
                    'testtags': self.test['tags']
                }
            }
            if self.type == 'sauce':
                SauceLabs.update_test_info(self.session_id, self.buildnumber, self.status)
            from util.elasticsearch import ElasticSearch as es
            es().post_to_elasticsearch('localhost', 9200, self.project, json.dumps(mictest))
            print(json.dumps(mictest))
            destroy_cloud_instance(self.machine_name)
        else:
            raise Exception('\nOops!!! Framework not configured to run for following tag/s -> ' + self.test['tags'])
        print('************************')

    def get_repository_details(self, d):
        return Api('api.repository.path', d, self.project, "").getcall_repository()

    def run_ui_test(self, ip):
        print('run_ui_test')
        step = []
        steps = self.test['steps']
        from util.webdriver import Driver
        d = Driver().setUp(self.test['testname'], self.type, ip)
        print('Driver is created :):):)')
        if d is None:
            if ip is not None:
                destroy_cloud_instance(self.machine_name)
            raise Exception('Initiate driver failed!!!')
        self.session_id = d.session_id
        for i in range(len(steps)):
            identifier = self.get_repository_details(steps[i]['identifier'])
            data = self.get_data(steps[i]['data']) if steps[i]['data'] != '' else None
            stepstatus = Heart().execute_step(d, identifier, steps[i]['action'], data)
            rstep = {
                'identifier': steps[i]['identifier'],
                'action': steps[i]['action'],
                'data': data,
                'status': stepstatus,
            }
            if stepstatus is True:
                rstep['status'] = stepstatus
                step.append(rstep)
            else:
                rstep['status'] = stepstatus[0]
                rstep['error'] = stepstatus[1]
                step.append(rstep)
                self.status = False
                break
        d = None
        return step

    def get_data(self, search):
        path = (
            os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                         'temp', 'data.json'))

        from util.json import read_json_data
        data = read_json_data(path)
        valuetoreturn = None
        for x in data:
            valuetoreturn = x['key']
            if valuetoreturn == search:
                valuetoreturn = x['value']
                break
        return valuetoreturn
