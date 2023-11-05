from cryptography.hazmat.primitives.padding import PKCS7
import base64
import json
import socket
from sys import stderr
class Server:
    feld : bytes
    q : list 
    c : str
    host : str  = "127.0.0.1" #TODO hostname auslesen
    port : int = 18733

    step : int = 1

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.run()
        self.step = 1


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #no functionality, useful for debugging if the server crashes
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                input = b''
                while True:
                    match self.step:
                        case 1:
                            input = input + (conn.recv(24)) #24 because 16 bytes b64 encoded and padded = 24 bytes transfered
                            if len(input) == 24:
                                self.c = input
                                input = b''
                                self.step = 2
                        case 2:
                            input = input + (conn.recv(2))
                            print(input)
                            print(len(input))
                            if len(input) == 2:
                                self.feld = int.from_bytes(input,'little')
                                if self.feld == 0:
                                    conn.sendall(b'0')
                                    break
                                input = b''
                                self.q = [[] for i in range(self.feld)]
                                self.step = 3
                        case 3:
                            input = input + (conn.recv(16*self.feld))
                            if len(input) == 16*self.feld:
                                for i in range(self.feld):
                                    self.q[i] = input[i*16:(i+1)*16]
                                input = b''
                                ret = self.check_pad()
                                conn.sendall(ret)
                                self.step = 2
                                self.q = []

            


    #TODO exception handling
    def recv_input(self, input : str):
        input = json.loads(input)
        if "ciphertext" in input:
            self.c = base64.b64decode(input['ciphertext'])
        if "feld" in input:
            self.feld = input['feld'].encode()
        if "q" in input:
            self.q = input['q']
            if type(self.q) == list:
                self.q = [i.encode() for i in self.q ]
            else:
                self.q = [self.q.encode()]
            return self.check_pad()
    

    def check_pad(self):
        b = []
        unpadder = PKCS7(128).unpadder()
        for i in range(0, self.feld):#TODO i>n(q)
            if i>len(self.q)-1:
                break
            x = bxor(self.q[i],self.c) 
            try: 
                unpadder.update(x)
                unpadder.finalize()
                unpadder = PKCS7(128).unpadder()
                b.append(b"1")
                print(x)

            except ValueError:
                b.append(b"0")
                continue
        return(b"".join(b))
    

                
def bxor(ba,bb):
    return bytes(x ^ y for (x, y) in zip(ba, bb)) 


if __name__ == "__main__":
    s = Server("127.0.0.1",18732)
