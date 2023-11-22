import socket
import base64
from cryptography.hazmat.primitives.padding import PKCS7

class Client:
    host :str  
    port : int
    c : str
    q : bytes
    iv : bytes
    dc = b'\0'*16
    s : socket

    def __init__(self, host, port, c, iv) -> None:
        self.host = host
        self.port = port
        self.c = c
        self.iv = iv
        self.q = b''

    def run(self) -> str:
        self.feld = int.to_bytes(256,2,'little')
        print(self.host)
        with socket.create_connection((self.host,self.port)) as self.s:
            self.s.sendall(self.c)
            for j in range(16,0,-1):

                #set padding values, length, generate qbytes and send the bytes to the server
                
                pad = (16-j+1).to_bytes(1,'big') #python3.10 is deprecated why use it??
                pad_count = 16-j+1
                qbytes = self.generate_bytes(j,pad,pad_count)
                self.s.sendall(self.feld + self.q)
                data = self.s.recv(256)  

                #find the correct padding in the server response
                for i,v in enumerate(data):
                    if v == 1:
                        #set the byte value the server found to be acceptable padding
                        add = int.to_bytes((qbytes[i][j-1]))        

                        #if first byte, do cross check
                        if j == 16:
                            chance = data.find(1)
                            if not chance == -1: 
                                add = self.verify_first_bytes(chance, qbytes,add,i)
                        self.dc = self.dc[:j-1] + bxor(add,pad) + self.dc[j:]
                        break
            ret = bxor(self.iv,self.dc)
            return ret 
        
    #generates the bytes that will be send to the server and return the 256*16byte values as a list
    def generate_bytes(self,j,pad,pad_count) -> list:
        self.q = b''
        qbytes = [int.to_bytes(i,j) + bxor(self.dc,b'\0'*j + pad*(pad_count))[j:] for i in range(256)]
        for i in qbytes:
            self.q = self.q + i
        return qbytes
    
    def verify_first_bytes(self, chance : int, qbytes : list, add : list, i : int, j = 16):
        try:
            verifier = qbytes[i][:j-2]+ int.to_bytes(qbytes[i][j-1] ^ 0xff) + add + qbytes[i][j:]
            self.s.sendall(b'\1\0' + verifier)
            b = self.s.recv(1)
            print(b)
            if not b == b'\1':
                return int.to_bytes((qbytes[chance][j-1])) 
            return add
        except ValueError:
            print(f"add: {add}")
            return add

def bxor(ba : bytes,bb : bytes) -> bytes:
    return bytes(x ^ y for (x, y) in zip(ba, bb))     