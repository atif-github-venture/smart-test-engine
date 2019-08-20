import os

from util.api import Api


def get_filtered_tests(f, p, path):
    Api('api.test.path', f, p, path).getcall_tests()


def get_run_configuration(rc, p, path):
    Api('api.test-config.path', rc, p, path).getcall_run_conf()


def get_data_namespace(d, p, path):
    Api('api.data-setup.path', d, p, path).getcall_data_namespace()

def get_data_for_execution(self):
    path = (
        os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                     'temp', 'test.json'))
    from util.folder import ensure_dir
    ensure_dir(path)
    get_filtered_tests(self.filter, self.project, path)
    path = (
        os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                     'temp', 'config.json'))
    get_run_configuration(self.runconfiguration, self.project, path)
    path = (
        os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                     'temp', 'data.json'))
    get_data_namespace(self.datanamespace, self.project, path)


def call_for_execution(f, b, a, r, p, d):
    path = (
        os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                     'temp', 'test.json'))
    from util.json import read_json_data
    test_to_execute = read_json_data(path)
    # json_object = json.loads(json_raw[0])
    for i in range(len(read_json_data(path))):
        from engine.execute import Execute
        e = Execute(test_to_execute[i], f, b, a, r, p, d)
        e.start_test()


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
        call_for_execution(self.filter, self.buildnumber, self.additionaltags, self.runconfiguration, self.project,
                           self.datanamespace)
