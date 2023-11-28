import json
from Aufgabe1.bytenigma.bytenigma import be_input_validation
from Aufgabe1.bytenigma.bytenigma import bytenigma
from Aufgabe2.client import Client
import base64
from Aufgabe3.aes import AES128GCM
from Aufgabe3.poly import Poly
from Aufgabe3.CZPoly import CZPoly
from Aufgabe3.Cantor import Cantor
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
            output = base64.b64encode(bytenigma(input, rotors, len(rotors[0])-1)).decode('ascii')
            return json.dumps({"output": output})        
        case 'padding-oracle-attack':
            #no more input validation (currently)
            hostname = data['hostname']
            port = data['port']
            iv = base64.b64decode(data['iv'])
            ct = base64.b64decode(data['ciphertext'])
            client = Client(hostname,port,ct,iv)
            output = str(base64.b64encode(client.run()),'ascii')
            return json.dumps({"plaintext": output})
        
        case 'gcm-encrypt':
            key =  Poly(base64.b64decode(data['key']))
            nonce =  Poly(base64.b64decode(data['nonce']))
            associated_data =  base64.b64decode(data['associated_data'])
            ptb = (base64.b64decode(data['plaintext']))



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
            ct_out = bytearray(b''.join([i.poly2block() for i in cts]))
            for i in ct_out[::-1]:
                if i == 0:
                    ct_out = ct_out[:-1] 
                else: 
                    break
            ct_out = base64.b64encode(ct_out).decode('ascii')
            at_out = base64.b64encode(at.poly2block()).decode('ascii')
            y0_out = base64.b64encode(y0.poly2block()).decode('ascii')
            h_out = base64.b64encode(h.poly2block()).decode('ascii')
            output = json.dumps({"ciphertext": ct_out, "auth_tag" : at_out, "Y0": y0_out,"H":h_out})
            return output
        
        case 'gcm-block2poly':
            b = data['block']
            output = Poly(b)
            return json.dumps({"exponents": output})
        case 'gcm-poly2block':
            e = data['exponents']
            output = base64.b64encode(Poly(e).poly2block())
            return json.dumps({"block": output})
        case 'gcm-clmul':
            a = Poly(base64.b64decode(data['a']))
            b = Poly(base64.b64decode(data['b']))
            output = base64.b64encode((a*b).poly2block())
            return json.dumps({"a_times_b": output})
        
        case 'gcm-poly-add':
            a = CZPoly([base64.b64decode(i) for i in data['a']])
            b = CZPoly([base64.b64decode(i) for i in data['b']])
            out = (a+b).poly2block()
            output = list()
            for i in out:
                output.append(str(base64.b64encode(i),'ascii'))
            return str(json.dumps({"result": output}))
        case 'gcm-poly-mul':
            a = CZPoly([base64.b64decode(i) for i in data['a']])
            b = CZPoly([base64.b64decode(i) for i in data['b']])
            out = (a*b).poly2block()
            output = list()
            for i in out:
                output.append(str(base64.b64encode(i),'ascii'))
            return json.dumps({"result": output})
        case 'gcm-poly-gcd':
            a = CZPoly([base64.b64decode(i) for i in data['a']])
            b = CZPoly([base64.b64decode(i) for i in data['b']])
            out = (a.gcd(b)).poly2block()
            output = list()
            for i in out:
                output.append(str(base64.b64encode(i),'ascii'))
            return json.dumps({"result": output})
        case 'gcm-poly-div':
            a = CZPoly([base64.b64decode(i) for i in data['a']])
            b = CZPoly([base64.b64decode(i) for i in data['b']])
            out = (a/b).poly2block()
            output = list()
            for i in out:
                output.append(str(base64.b64encode(i),'ascii'))
            return json.dumps({"result": output})
        case 'gcm-poly-mod':
            a = CZPoly([base64.b64decode(i) for i in data['a']])
            b = CZPoly([base64.b64decode(i) for i in data['b']])
            out = (a%b).poly2block()
            output = list()
            for i in out:
                output.append(str(base64.b64encode(i),'ascii'))
            return json.dumps({"result": output})
        case 'gcm-poly-pow':
            base = CZPoly([base64.b64decode(i) for i in data['base']])
            exp = data['exponent']
            out = (base**exp).poly2block()
            output = list()
            for i in out:
                output.append(str(base64.b64encode(i),'ascii'))
            return json.dumps({"result": output})
        case 'gcm-poly-powmod':
            base = CZPoly([base64.b64decode(i) for i in data['base']])
            exp = data['exponent']
            mod = CZPoly([base64.b64decode(i) for i in data['modulo']])
            out = (base.powmod(exp,mod)).poly2block()
            output = list()
            for i in out:
                output.append(str(base64.b64encode(i),'ascii'))
            return json.dumps({"result": output})
        
        case 'gcm-recover':
            nonce = base64.b64decode(data['nonce'])
            msg_in = [data['msg1'],data['msg2'],data['msg3'],data['msg4']]
            ct,ad,at = [],[],[]
            for i in msg_in:
                for k,v in i.items():
                    if k == "ciphertext":
                        ct.append(base64.b64decode(v))
                    if k == "associated_data":
                        ad.append(base64.b64decode(v))
                    if k == "auth_tag":
                        at.append(base64.b64decode(v))
            c = Cantor(nonce,ct,ad,at)
            out = c.run()
            