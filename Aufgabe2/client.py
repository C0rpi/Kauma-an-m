import socket
import base64

HOST = "127.0.0.1"  
PORT = 18732
inp = """
{
"ciphertext" : "MDAwMDAwMDAwMDAwMDAwMQ==",
"q" : "0000000000000000",
"feld" : "0001"
}"""

c = "fJxLd1A3aY8YVk2Ge0akWQ=="
qbytes = [int.to_bytes(i,16) for i in range(0xff) ]
q = b''
for i in qbytes:
    q = q+ i
feld = int.to_bytes(0xff,2,'little')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) #create_connection ist besser 
    s.sendall(bytes(c,'ascii'))
    s.sendall(feld)
    s.sendall(q)
    data = s.recv(1024)
    s.close()
            
