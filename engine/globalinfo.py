class GlobalInfo:
    __instance = None
    filter = None
    buildnumber = None
    additionaltags = None
    runconfiguration = None
    project = None
    datanamespace = None
    testname = None
    testtags = None
    sessionid = None

    @staticmethod
    def get_instance():
        if GlobalInfo.__instance is None:
            GlobalInfo()
        return GlobalInfo.__instance

    def __init__(self):
        GlobalInfo.__instance = self

    def set_filter(self, f):
        self.filter = f

    def get_filter(self):
        return self.filter

    def set_buildnumber(self, b):
        self.buildnumber = b

    def get_buildnumber(self):
        return self.buildnumber

    def set_additionaltags(self, a):
        self.additionaltags = a

    def get_additionaltags(self):
        return self.additionaltags

    def set_runconfiguration(self, r):
        self.runconfiguration = r

    def get_runconfiguration(self):
        return self.runconfiguration

    def set_project(self, p):
        self.project = p

    def get_project(self):
        return self.project

    def set_datanamespace(self, d):
        self.datanamespace = d

    def get_datanamespace(self):
        return self.datanamespace

    def set_testname(self, t):
        self.testname = t

    def get_testname(self):
        return self.testname

    def set_testtags(self, tt):
        self.testtags = tt

    def get_testtags(self):
        return self.testtags

    def set_sessionid(self, sid):
            self.sessionid = sid

    def get_sessionid(self):
        return self.sessionid

