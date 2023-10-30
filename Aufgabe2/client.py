import socket

HOST = "127.0.0.1"  
PORT = 18732
input = """
{
"ciphertext" : "MDAwMDAwMDAwMDAwMDAwMQ==",
"q" : "0000000000000000",
"feld" : "0001"
}"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) #create_connection ist besser 
    s.sendall(bytes(input,'ascii'))
    data = s.recv(1024)
    print(data)
