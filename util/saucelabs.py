from sauceclient import SauceClient


class SauceLabs:

    def update_test_info(j, b, p):
        sc = SauceClient('fatebamboo', '9099ed6e-b6ab-42d0-a2d1-76fe26985c74')
        sc.jobs.update_job(job_id=j, build=b, passed=p)
