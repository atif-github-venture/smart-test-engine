class GlobalInfo:
    def __init__(self, f, b, a, r, p, d, tn, tt):
        self.filter = f
        self.buildnumber = b
        self.additionaltags = a
        self.runconfiguration = r
        self.project = p
        self.datanamespace = d
        self.testname = tn
        self.testtags = tt

    def set_microtestname(self, m):
        self.microtestname = m