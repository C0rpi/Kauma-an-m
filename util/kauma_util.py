import json
from Aufgabe1.bytenigma.bytenigma import be_input_validation
from Aufgabe1.bytenigma.bytenigma import bytenigma
from Aufgabe2.client import Client
import base64
from Aufgabe3.aes import AES128GCM
from Aufgabe3.poly import Poly
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
            output = str(base64.b64encode(bytenigma(input, rotors, len(rotors[0])-1)))
            return json.dumps({"output": output})        
        case 'padding-oracle-attack':
            #no more input validation (currently)
            hostname = data['hostname']
            port = data['port']
            iv = base64.b64decode(data['iv'])
            ct = base64.b64decode(data['ciphertext'])
            client = Client(hostname,port,ct,iv)
            output = str(base64.b64encode(client.run()),'ascii')
            print(output)
            return json.dumps({"plaintext": output})
        case 'gcm-encrypt':
            key =  Poly(base64.b64decode(data['key']))
            nonce =  Poly(base64.b64decode(data['nonce']))
            associated_data =  base64.b64decode(data['associated_data'])
            ptb = (base64.b64decode(data['plaintext']))



            print(len(ptb))

            adt = list()
            if not adt == "" or not associated_data == []:
                for i in range(0,len(associated_data),16):
                    adt.append(Poly(associated_data[i:i+16]))
            else:
                adt.append(Poly([]))
            pt = list()
            if not ptb == []:
                for i in range(0,len(ptb),16):
                    pt.append(Poly(ptb[i:i+16]))
            else:
                pt.append(Poly(adt))
            cipher = AES128GCM(key,nonce,adt,pt)            
            cts,at,y0,h = cipher.encrypt()
            ct_out = base64.b64encode(b''.join([i.poly2block() for i in cts])).decode('ascii')
            at_out = base64.b64encode(at.poly2block()).decode('ascii')
            y0_out = base64.b64encode(y0.poly2block()).decode('ascii')
            h_out = base64.b64encode(h.poly2block()).decode('ascii')
            output = json.dumps({"ciphertext": ct_out, "auth_tag" : at_out, "Y0": y0_out,"H":h_out})
            return output
            ##testing
            with open("Aufgabe3/nist_vectors/nist_4.out.json") as f: validator = json.loads(f.read())
            res = json.loads(output)
            for k,v in res.items():
                try:
                    assert v == validator[k]
                except:
                    stderr.write(f"failed for: {k}")
                    stderr.write(f"res: {res[k]}\nval: {validator[k]}")
            return output