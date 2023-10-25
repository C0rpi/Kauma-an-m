import json
from bytenigma.bytenigma import be_input_validation
from bytenigma.bytenigma import bytenigma
import base64
from sys import stderr

def json_parser(json_path):


    try:
        with open(json_path) as file: input = file.read()
        data = json.loads(input)
    except ValueError as error:
        stderr.write(error)
        stderr.write("Error opening the file by relativ and absolute path, aborting")
        raise 

    match data['action']:
        case 'bytenigma':
            be_input_validation(data) 
            input = list(base64.b64decode(data['input']))
            rotors = data['rotors']
            output = bytenigma(input, rotors, len(rotors[0])-1)
            
    return json.dumps({"output": output})