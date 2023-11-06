import json
from bytenigma.bytenigma import be_input_validation
from bytenigma.bytenigma import bytenigma
from Aufgabe2.client import Client
import base64
from sys import stderr


#central point which decides what action to perform based on the input
def json_parser(json_path):


    try:
        with open(json_path) as file: input = file.read()
        data = json.loads(input)
    except ValueError as error:
        stderr.write(error)
        stderr.write("Error opening the file by relativ and absolute path, aborting")
        raise 

    #decider
    match data['action']:
        case 'bytenigma':
            be_input_validation(data) 
            input = list(base64.b64decode(data['input']))
            rotors = data['rotors']
            output = bytenigma(input, rotors, len(rotors[0])-1)
            return json.dumps({"output": output})
        case 'padding-oracle-attack':
            #no more input validation (currently)
            hostname = data['hostname']
            port = data['port']
            iv = base64.b64decode(data['iv'])
            ct = base64.b64decode(data['ciphertext'])
            client = Client(hostname,port,ct,iv)
            output = client.run()
            print(output)
            return json.dumps({"plaintext": output})


            