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

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.run()


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #no functionality, useful for debugging if the server crashes
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    data = data.decode('ascii')
                    out = self.recv_input(data)
                    if not data:
                        break
                    conn.sendall(bytes(out))
            


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
        for i in range(0, int.from_bytes(self.feld,'little')):#TODO i>n(q)
            if i>len(self.q)-1:
                break
            try: 
                x = bxor(self.q[i],self.c)
                unpadder.update(x)
                unpadder.finalize()
                unpadder = PKCS7(128).unpadder()
                b.append(b"1")

            except ValueError as e:
                stderr.write(e)
                b.append(b"0")
                continue
        return(b"".join(b))
    

                
def bxor(ba,bb):
    return bytes(x ^ y for (x, y) in zip(ba, bb)) 


if __name__ == "__main__":
    s = Server("127.0.0.1",18732)
