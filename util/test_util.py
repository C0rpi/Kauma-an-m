import json
from .kauma_util import json_parser
from sys import stderr

#group of manually created tests to check if results are still providing the same output
def be_run_tests():
    #one try except suffices, because we are expecting all to pass anyways
    try:
        with open("./tests/test1.json") as file : data = file.read()
        result = json.loads(data)['result']
        assert json.loads(json_parser(data))['output'] == result 

        with open("./tests/test2.json") as file : data = file.read() 
        result = json.loads(data)['result'] 
        assert json.loads(json_parser(data))['output'] == result 

    except:
        stderr("error running custom tests")