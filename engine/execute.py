import json
import os
import time
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
        from time import gmtime, strftime
        execution_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        start_time = gmtime()
        if any("#web" in s for s in self.test['tags']):
            rsteps = self.run_ui_test()
            end_time = gmtime()
            time_diff = time.mktime(end_time) - time.mktime(start_time)
            mictest = {
                'testname': self.test['testname'],
                'status': self.status,
                'execution_time': execution_time,
                'start_time': strftime("%Y-%m-%d %H:%M:%S", start_time),
                'end_time': strftime("%Y-%m-%d %H:%M:%S", end_time),
                'duration': time_diff,
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
                SauceLabs.update_test_info(self.session_id, self.buildnumber(), self.status)
            print(json.dumps(mictest))
        else:
            raise Exception('\nOops!!! Framework not configured to run for following tag/s -> ' + self.test['tags'])
        print('************************')
        # self.g = None


    # def set_test_information(self):
    #     self.g.set_filter(GlobalInfo, self.filter)
    #     self.g.set_buildnumber(self.buildnumber)
    #     self.g.set_additionaltags(self.additionaltags)
    #     self.g.set_runconfiguration(self.runconfiguration)
    #     self.g.set_project(self.project)
    #     self.g.set_datanamespace(self.datanamespace)
    #     self.g.set_testname(self.test['testname'])
    #     self.g.set_testtags(self.test['tags'])

    # def start_macrotest(self):
    #     microtestlist = self.test['MicroTest']
    #     mactest = []
    #     # list of micro test
    #     for i in range(len(microtestlist)):
    #         # Inside individual micro test
    #         steps = microtestlist[i]['Steps']
    #         # If a single step in a micro test fails, break the entire macro test
    #         if self.status is False:
    #             break
    #         else:
    #             rsteps = self.run_micro_test_steps(steps)
    #             mictest = {
    #                 'microtestname' : microtestlist[i]['microtestname'],
    #                 'Steps': rsteps
    #             }
    #             mactest.append(mictest)
    #     print('************************')
    #     print(json.dumps(mactest))

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
                # Heart.quit_driver(None)
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
