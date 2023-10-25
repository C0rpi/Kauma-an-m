from util.test_util import be_run_tests
from util.kauma_util import json_parser
from sys import argv
from sys import stderr
from sys import stdout
if __name__ == "__main__":
    
    if len(argv) ==2:
        output = json_parser(argv[1])
        stdout.write(output)

    else:
        stderr.write("wrong number of paramters, please input one json document")
    
