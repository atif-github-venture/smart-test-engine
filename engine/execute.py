import json
import os
from engine.heart import Heart
from util.api import Api
from util.saucelabs import SauceLabs


class Execute:
    session_id = None

    def __init__(self, test, f, b, a, r, p, d, t):
        self.test = test
        self.filter = f
        self.buildnumber = b
        self.additionaltags = a
        self.runconfiguration = r
        self.project = p
        self.datanamespace = d
        self.type = t
        self.status = True

    def start_test(self):
        from datetime import datetime, timezone
        execution_time = datetime.now(timezone.utc)
        start_time = datetime.now(timezone.utc)
        if any("#web" in s for s in self.test['tags']):
            rsteps = self.run_ui_test()
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
        else:
            raise Exception('\nOops!!! Framework not configured to run for following tag/s -> ' + self.test['tags'])
        print('************************')

    def get_repository_details(self, d):
        return Api('api.repository.path', d, self.project, "").getcall_repository()

    def run_ui_test(self):
        step = []
        steps = self.test['Steps']
        from util.webdriver import Driver
        d = Driver().setUp(self.test['testname'], self.type)
        if d is None:
            raise Exception('Driver initiate failed!!!')
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
