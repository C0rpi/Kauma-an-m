import json
import base64
from hashlib import sha256
from sys import stderr

global reduction

def json_parser(input):
    data = json.loads(input)
    match data['action']:
        case 'bytenigma':
            be_input_validation(data)
            input = list(base64.b64decode(data['input']))
            rotors = data['rotors']
            global reduction
            reduction = len(rotors[0])-1
            output = bytenigma(input, rotors)
    return json.dumps({"output": output})

def be_input_validation(data):
    try:
        try:
            list(base64.b64decode(data['input']))
        except:
            stderr.write("error: b64decoding input")
        if len(data['rotors']) == 0:
            stderr.write("error: json contains no rotors")
    except:
        stderr.write("error: bytenigma general input validation failed, trying to continue anyhow :)")

#group of manually created tests to check if results are still providing the same output
def run_tests():
    #one try except suffices, because we are expecting all to pass anyways
    try:
        with open("test1.json") as file : data = file.read()
        result = json.loads(data)['result']
        assert json.loads(json_parser(data))['output'] == result 

        with open("test2.json") as file : data = file.read() 
        result = json.loads(data)['result'] 
        assert json.loads(json_parser(data))['output'] == result 

    except:
        stderr.write("error running custom tests")


#writes the result back to input, very nice
def bytenigma(input : list, rotors : list):
    try:
        global reduction
    except:
        global reduction
        reduction = 255

    for i in range(0,len(input)):

        for rotor in rotors:
            input[i] = forwards_pass(rotor,input[i])  
        input[i] = bitwise_complement(input[i])

        for rotor in reversed(rotors):
            input[i] = backwards_pass(rotor,input[i])
        rotors = rotation(rotors)

    input = bytes(input)
    return input

def forwards_pass(rotor,input):
    return rotor[input]

def backwards_pass(rotor,input):
    return rotor.index(input) #certainly not the fastest but surely the easiest solution

def rotation(rotors):
    for rotor in rotors:
        rotor.append(rotor.pop(0))
        if rotor[-1] ==0:
            continue
        break
    return rotors

def bitwise_complement(input):
    try: 
        global reduction
        return reduction -input
    except:
        return 255-input



if __name__ == "__main__":



    #run_tests()

    with open('test1.json') as f: input = json.loads(f.read())
    global reduction
    reduction = len(input['rotors'][0])-1
    print(str(sha256(bytenigma(list(b'\0'*2**20), input['rotors'])).hexdigest()),'ascii')



    #out = json_parser(input)
    #print()
    #r = input['rotors']
    #out = bytenigma(list(b'\0'*2**20),rotors = r)
    #print(return_output(out))