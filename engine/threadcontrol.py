import os
import threading
import concurrent.futures
import time
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool, cpu_count
from itertools import repeat
from threading import Thread
from util.api import Api
from queue import Queue


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


def thread_initiate(t, f, b, a, r, p, d, ty):
    # lock.acquire()
    from engine.execute import Execute
    Execute(t, f, b, a, r, p, d, ty).start_test()
    # lock.release()


def call_for_execution(f, b, a, r, p, d, ty):
    from time import strftime, gmtime
    st_time = gmtime()
    path = (
        os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                     'temp', 'test.json'))
    from util.json import read_json_data
    test_to_execute = read_json_data(path)
    # json_object = json.loads(json_raw[0])

    # #simple threading
    # threads = []
    # # lock = threading.Lock()
    # for i, browser in enumerate(test_to_execute):
    #     thread = threading.Thread(target=thread_initiate, args=[ test_to_execute[i], f, b, a, r, p, d, ty])
    #     threads.append(thread)
    #     thread.start()
    # for thread in threads:
    #     thread.join()

    # ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(test_to_execute)) as executor:
        future_to_url = {executor.submit(thread_initiate, t, f, b, a, r, p, d, ty): t for t in test_to_execute}

        for future in concurrent.futures.as_completed(future_to_url):
            t = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (t, exc))

    # single execution
    # for i in range(len(read_json_data(path))):
    #         from engine.execute import Execute
    #         Execute(test_to_execute[i], f, b, a, r, p, d, ty).start_test()
    en_time = gmtime()
    print('total execution time: ' + str(time.mktime(en_time) - time.mktime(st_time)))


class ThreadControl:
    def __init__(self, filter, buildnumber, threads, additionaltags, runconfiguration, project, datanamespace, type):
        self.filter = filter
        self.buildnumber = buildnumber
        self.threads = threads
        self.additionaltags = additionaltags
        self.runconfiguration = runconfiguration
        self.project = project
        self.datanamespace = datanamespace
        self.type = type

    def execute(self):
        get_data_for_execution(self)
        call_for_execution(self.filter, self.buildnumber, self.additionaltags, self.runconfiguration, self.project,
                           self.datanamespace, self.type)

# class GetterPool(object):
#     def __init__(self, maxgetters=8):
#         self.getters = []
#         self.queue = Queue()
#         for _n in range(maxgetters):
#             getter = Getter(use_phantom=False)
#             self.queue.put(getter)
#             self.getters.append(getter)
#
#     def run_in_free_getter(self, url):
#         #print("get free getter")
#         getter = self.queue.get()
#         #print("got getter %d" % getter.instance)
#         thread = threading.Thread(target=partial(self.get_thread, getter, url))
#         thread.start()
#
#
#     def get_thread(self, getter, url):
#         active_urls.add(url)
#         try:
#             html = getter.get_url(url)
#         except Exception as exc:
#             print("getter %d failed for %s with %s" %
#                   (getter.instance, url, exc))
#         # print("got an html string with %d characters" % len(html))
#         active_urls.remove(url)
#         self.queue.put(getter)
#
#     def print_stats(self):
#         #for getter in self.getters:
#         #    print("getter %d needed %.2fs to create driver and %.2fs to get %d urls" %
#         #        (getter.instance, getter.t_mkdriver, getter.t_get_sum, getter.get_count))
#         print("timedout urls")
#         for url in timedout_urls:
#             print("    ", url)
#         print("\n\n")
#         print("active_urls")
#         for url in active_urls:
#             print("    ", url)
#         print("\n\n")
#
#     def wait_for_all_threads(self):
#         for n in range(len(self.getters)):
#             getter = self.queue.get()
#             print("getter %d finished" %  getter.instance)
