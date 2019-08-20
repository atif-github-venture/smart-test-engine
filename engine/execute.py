import json
import os
from engine.globalinfo import GlobalInfo
from engine.heart import Heart
from util.api import Api
from util.saucelabs import SauceLabs


class Execute:

    def __init__(self, test, f, b, a, r, p, d):
        self.test = test
        self.filter = f
        self.buildnumber = b
        self.additionaltags = a
        self.runconfiguration = r
        self.project = p
        self.datanamespace = d
        self.status = True

    def start_test(self):
        self.set_test_information()
        rsteps = self.run_test()
        mictest = {
            'testname': self.test['testname'],
            'status': self.status,
            'Steps': rsteps
        }
        g = GlobalInfo.get_instance()
        SauceLabs.update_test_info(g.get_sessionid(), g.get_buildnumber(), self.status)
        print('************************')
        print(json.dumps(mictest))

    def set_test_information(self):
        g = GlobalInfo.get_instance()
        g.set_filter(self.filter)
        g.set_buildnumber(self.buildnumber)
        g.set_additionaltags(self.additionaltags)
        g.set_runconfiguration(self.runconfiguration)
        g.set_datanamespace(self.datanamespace)
        g.set_testname(self.test['testname'])
        g.set_testtags(self.test['tags'])

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

    def run_test(self):
        step = []
        steps = self.test['Steps']
        for i in range(len(steps)):
            identifier = self.get_repository_details(steps[i]['identifier'])
            data = self.get_data(steps[i]['data']) if steps[i]['data'] != '' else None
            stepstatus = Heart().execute_step(identifier, steps[i]['action'], data)
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
                Heart.quit_driver(None)
                break
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
