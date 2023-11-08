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

    def __init__(self, host, port, c, iv) -> None:
        self.host = host
        self.port = port
        self.c = c
        self.iv = iv
        self.q = b''

    def run(self) -> bytes:
        self.feld = int.to_bytes(256,2,'little')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port)) #create_connection ist besser #create once and PRAY

            s.sendall(self.c)
            for j in range(16,0,-1):
                #set padding values, length
                pad = int.to_bytes(16-j+1)
                pad_count = 16-j+1
                qbytes = self.generate_bytes(j,pad,pad_count) #i love this 
                s.sendall(self.feld)
                s.sendall(self.q)   
                data = s.recv(256)  
                #find the correct padding
                for i,v in enumerate(data):
                    if v == 1:
                        #set the byte value the server found to be acceptable padding
                        add = int.to_bytes((qbytes[i][j-1]))
                        #if first byte, do cross check
                        if j == 16:
                            verifier = qbytes[i][:j-2]+ int.to_bytes(qbytes[i][j-1] ^ 0xff) + add + qbytes[i][j:]
                            s.sendall(b'\1\0')
                            s.send(verifier)
                            b = s.recv(1)
                            #if not valid: continue with next iteration, dont set dc
                            if not b == b'\1':
                                continue                        
                        self.dc = self.dc[:j-1] + bxor(add,pad) + self.dc[j:]
                        break
            ret = str(base64.b64encode(bxor(self.iv,self.dc)),'ascii')
            print(f"check: {base64.b64decode(ret)}")
            return(ret)
        
    #generates the bytes that will be send to the server and return the 256*16byte values as a list
    def generate_bytes(self,j,pad,pad_count):
        self.q = b''
        qbytes = [int.to_bytes(i,j) + bxor(self.dc,b'\0'*j + pad*(pad_count))[j:] for i in range(256)]
        for i in qbytes:
            self.q = self.q + i
        return qbytes

def bxor(ba : bytes,bb : bytes):
    return bytes(x ^ y for (x, y) in zip(ba, bb))     

c = Client("localhost",18732,base64.b64decode("RW1lcnNvbiBCcmFkeSACbw=="),base64.b64decode("AAAAAAAAAAAAAAAAAAAAAA=="))
print(c.run())