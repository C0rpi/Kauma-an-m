import json
import base64


def json_parser(input):
    l = json.loads(input)
    match l['action']:
        case 'bytenigma':
            return bytenigma(l)
        
def return_output(output):
    return json.dumps({"output": output})


def bytenigma(l):
    input = base64.b64decode(l['input'])
    input_l = list(input)
    rotors = l['rotors']
    out = pass_values(rotors,input_l)
    out = ''.join(chr(i) for i in out)
    out = base64.b64encode(out.encode())
    return 0

def pass_values(rotors,input):
    output = list()
    for i in range(0,len(input)):        
        for index, rotor in enumerate(rotors):
            input[i] = forwards_pass(rotor,input[i])  
        input[i] = bitwise_complement(input[i])
        for rotor in reversed(rotors):
            input[i] = backwards_pass(rotor,input[i])
        rotors = rotation(rotors)
        output.append(input[i])
    return output


def forwards_pass(rotor,input):
    return rotor[input]

def backwards_pass(rotor,input):
    return rotor.index(input)

#done
def rotation(rotors):
    l = list(rotors)
    for index, rotor in enumerate(rotors):
        l[index] = rotor[1:] + [rotor[0]]
        if l[index][-1] ==0:
            continue
        else:
            break
    return l

def bitwise_complement(input):
    return 255-input




with open('test1.json') as f: input = f.read()
out = json_parser(input)
print(return_output(out))