from sauceclient import SauceClient


class SauceLabs:

    def update_test_info(j, b, p):
        sc = SauceClient('user', 'key')
        sc.jobs.update_job(job_id=j, build=b, passed=p)
