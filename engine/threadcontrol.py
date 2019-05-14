# do a web service call, save the json file in local
# find number of tests
#  spin multi thread and call execute class to run each test (pass test body as json)

# let the pool of containers grid

from util.api import Api


def get_filtered_tests(f, p):
    Api('api.macro-test.path', f, p).getcall_macro_tests()


def get_run_configuration(rc, p):
    Api('api.test-config.path', rc, p).getcall_run_conf()


def get_data_namespace(d, p):
    Api('api.data-setup.path', d, p).getcall_data_namespace()

def get_data_for_execution(self):
    get_filtered_tests(self.filter, self.project)
    get_run_configuration(self.runconfiguration, self.project)
    get_data_namespace(self.datanamespace, self.project)


class ThreadControl:
    def __init__(self, filter, buildnumber, threads, additionaltags, runconfiguration, project, datanamespace):
        self.filter = filter
        self.buildnumber = buildnumber
        self.threads = threads
        self.additionaltags = additionaltags
        self.runconfiguration = runconfiguration
        self.project = project
        self.datanamespace = datanamespace

    def execute(self):
        get_data_for_execution(self)
