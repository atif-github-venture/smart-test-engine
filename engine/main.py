import getopt
import sys
from engine.threadcontrol import ThreadControl


def main(argv):
    filter = None
    buildnumber = None
    threads = None
    additionaltags = None
    runconfiguration = None
    project = None
    datanamespace = None

    try:
        opts, args = getopt.getopt(argv, "f:b:t:a:r:p:d:",
                                   ["filter=", "buildnumber=", "threads=", "additionaltags=", "runconfiguration=",
                                    "project=", "datanamespace"])
    except getopt.GetoptError:
        print(
            'main.py -f <filter1,filter2> -b <buildnumber> -t <threads> -a <#additional,#tags,#to,#report> -r <run configuration> -p <project> -d <datanamespace>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(
                'main.py -f <filter1,filter2> -b <buildnumber> -t <threads> -a <#additional,#tags,#to,#report> -r <run configuration> -p <project> -d <datanamespace>')
            sys.exit()
        elif opt in ("-f", "--filter"):
            filter = arg
        elif opt in ("-b", "--buildnumber"):
            buildnumber = arg
        elif opt in ("-t", "--threads"):
            threads = arg
        elif opt in ("-a", "--additionaltags"):
            additionaltags = arg
        elif opt in ("-r", "--runconfiguration"):
            runconfiguration = arg
        elif opt in ("-p", "--project"):
            project = arg
        elif opt in ("-d", "--datanamespace"):
            datanamespace = arg
    arglist = [filter, buildnumber, threads, runconfiguration, project, datanamespace]
    if None in arglist:
        raise Exception('Correct the arguments, item missing!!!')
    tc = ThreadControl(filter, buildnumber, threads, additionaltags, runconfiguration, project, datanamespace)
    tc.execute()


if __name__ == '__main__':
    main(sys.argv[1:])
