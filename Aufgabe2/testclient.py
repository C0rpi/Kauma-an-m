import socket
import base64
from cryptography.hazmat.primitives.padding import PKCS7
import json

class Client:
    host :str  
    port : int
    c : str
    q : bytes
    iv : bytes
    dc = b'\0'*16

    def __init__(self, host, port, c, iv) -> None:
        self.host = host
        self.port = port
        self.c = c
        self.iv = iv
        self.q = b''

    def run(self):
        self.feld = int.to_bytes(0xff,2,'little')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port)) #create_connection ist besser #create once and PRAY

            s.sendall(self.c)
            for j in range(16,0,-1):
                pad = int.to_bytes(16-j+1)
                pad_count = 16-j+1
                self.q = b''
                qbytes = [int.to_bytes(i,j) + bxor(self.dc,b'\0'*j + pad*(pad_count))[j:] for i in range(0xff+1)] #i love this 
                for i in qbytes[:-1]:
                    self.q = self.q + i
                s.sendall(self.feld)
                s.sendall(self.q)   
                data = s.recv(256)
                #ich hasse dass das notwendig ist
                s.sendall(int.to_bytes(1,2,'little'))
                s.sendall(qbytes[-1])   
                data = data+ s.recv(1)
                for i,v in enumerate(data):
                    if v == 1:
                        add = int.to_bytes((qbytes[i][j-1]))
                        if j == 16: #verify solution for first byte
                            s.sendall(b'\1\0')
                            verifier = qbytes[i][:j-2]+ int.to_bytes(qbytes[i][j-1] ^ 0xff) + add + qbytes[i][j:]
                            s.send(verifier)
                            b = s.recv(1)
                            if b ==b'\1':
                                self.dc = self.dc[:j-1] + bxor(add,pad) + self.dc[j:]
                                break
                            else:
                                continue
                        else:
                            self.dc = self.dc[:j-1] + bxor(add,pad) + self.dc[j:]
                            break
            ret = bxor(self.iv,self.dc)
            return(ret)


def bxor(ba : bytes,bb : bytes):
    return bytes(x ^ y for (x, y) in zip(ba, bb))     

def verify_padding(input):
    unpadder = PKCS7(128).unpadder()
    try: 
        unpadder.update(input)
        unpadder.finalize()
        unpadder = PKCS7(128).unpadder()
        return True        
    except ValueError:
        return False

with open("Aufgabe2/ct1.json") as f: input = json.loads(f.read())
for i in input['pairs']:
    iv = i['iv']
    ct_l = i['ct']
    res = b''

    for ct in ct_l:
        client = Client("141.72.5.194",18732, bytes.fromhex(ct), bytes.fromhex(iv))
        res = res + client.run()
        iv = ct
    print(f"\n\n\nresult: {res.decode('utf-8')}") 