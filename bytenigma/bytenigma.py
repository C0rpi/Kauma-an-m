from sys import stderr
from base64 import b64decode
from base64 import b64encode

def be_input_validation(data):
    try:
        try:
            list(b64decode(data['input']))
        except:
            stderr.write("error: b64decoding input")
        if len(data['rotors']) == 0:
            stderr.write("error: json contains no rotors")
    except:
        stderr.write("error: bytenigma general input validation failed, trying to continue anyhow :)")

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

def bitwise_complement(input,reduction):
    return reduction-input

#writes the result back to input, very nice
def bytenigma(input : list, rotors : list, reduction):
    for i in range(0,len(input)):

        for rotor in rotors:
            input[i] = forwards_pass(rotor,input[i])  
        input[i] = bitwise_complement(input[i],reduction)

        for rotor in reversed(rotors):
            input[i] = backwards_pass(rotor,input[i])
        rotors = rotation(rotors)

    input = bytes(input)
    input = str(b64encode(input),'ascii')
    return input

