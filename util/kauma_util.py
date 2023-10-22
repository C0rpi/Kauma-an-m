import json
from bytenigma.bytenigma import be_input_validation
from bytenigma.bytenigma import bytenigma
import base64

def json_parser(input):
    data = json.loads(input)
    match data['action']:
        case 'bytenigma':
            be_input_validation(data) 
            input = list(base64.b64decode(data['input']))
            rotors = data['rotors']
            output = bytenigma(input, rotors, len(rotors[0])-1)
    return json.dumps({"output": output})