from engine.globalinfo import GlobalInfo
from engine.heart import Heart


class Execute:

    def __init__(self, test, f, b, a, r, p, d):
        self.test = test
        self.filter = f
        self.buildnumber = b
        self.additionaltags = a
        self.runconfiguration = r
        self.project = p
        self.datanamespace = d

    def start_test(self):
        self.set_test_information()
        self.start_macrotest()

    def set_test_information(self):
        testname = self.test['macrotestname']
        testtags = self.test['tags']
        g = GlobalInfo(self.filter, self.buildnumber, self.additionaltags, self.runconfiguration, self.project,
                       self.datanamespace, testname, testtags)

    def start_macrotest(self):
        microtestlist = self.test['MicroTest']

        # list of micro test
        for i in range(len(microtestlist)):
            # Inside individual micro test
            microtestname = microtestlist[i]['microtestname']
            steps = microtestlist[i]['Steps']
            self.runmicrotest(steps)

    def runmicrotest(self, steps):
        for i in range(len(steps)):
            Heart().execute_step(steps[i]['identifier'], steps[i]['action'], steps[i]['data'])