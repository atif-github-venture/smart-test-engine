import json

from engine.globalinfo import GlobalInfo
from engine.heart import Heart
from util.webdriver import Driver


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
            'Steps': rsteps
        }
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

    def run_test(self):
        step = []
        steps = self.test['Steps']
        for i in range(len(steps)):
            stepstatus = Heart().execute_step(steps[i]['identifier'], steps[i]['action'], steps[i]['data'])
            rstep = {
                'identifier': steps[i]['identifier'],
                'action': steps[i]['action'],
                'data': steps[i]['data'],
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
