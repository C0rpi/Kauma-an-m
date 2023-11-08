from cryptography.hazmat.primitives.padding import PKCS7
import socket
class Server:
    feld : bytes
    q : list 
    c : str
    host : str  = "127.0.0.1"
    port : int = 18733

    step : int = 1

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.run()
        self.step = 1
        self.running = True

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #no functionality, useful for debugging if the server crashes
            s.bind((self.host, self.port))
            while True:
                s.listen()
                print("waiting for connection")
                conn, addr = s.accept()
                self.running = True
                with conn:
                    print(f"Connected by {addr}")
                    input = b''
                    while self.running:

                        if self.is_socket_closed(conn):
                            self.step = 1
                            input = b''    
                            self.c = b''
                            self.q = b''
                            self.feld = 0
                            self.running = False
                            conn.close()
                            break
                        #follow the protocol:
                        match self.step:
                            case 1:
                                input = input + (conn.recv(16))
                                if len(input) == 16:
                                    self.c = input
                                    input = b''
                                    self.step = 2
                            case 2:
                                input = input + (conn.recv(2))
                                if len(input) == 2:
                                    self.feld = int.from_bytes(input,'little')
                                    if self.feld == 0:
                                        conn.sendall(b'ENDEGELAENDE')#breaks connection if 0 q blocks announced
                                        self.running = False
                                        break
                                    input = b''
                                    self.q = [[] for i in range(self.feld)]
                                    self.step = 3
                            case 3:
                                input = input + (conn.recv(16*self.feld))
                                print(f"input: {len(input)} 16*self.feld: {16*self.feld}")
                                if len(input) == 16*self.feld:
                                    for i in range(self.feld):
                                        self.q[i] = input[i*16:(i+1)*16]
                                    input = b''
                                    ret = self.check_pad()

                                    #return response, jumpt to step 2 and wait for next inputs
                                    conn.sendall(ret)
                                    self.step = 2
                                    self.q = []
    #hello stackoverflow
    #checks if client connection is still alive
    #reads the bytes from input buffer without removing them from the buffer
    def is_socket_closed(self, conn: socket.socket) -> bool:
        try:
            data = conn.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False
        except ConnectionResetError:
            return True
        except Exception as e:
            print(str(e))
        return False


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
                b.append(b"\1")

            except ValueError:
                b.append(b"\0")
                continue
        return(b"".join(b))
    

                
def bxor(ba : bytes, bb : bytes):
    return bytes(x ^ y for (x, y) in zip(ba, bb)) 


if __name__ == "__main__":
    s = Server("127.0.0.1",18732)
