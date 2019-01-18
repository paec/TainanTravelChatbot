import socket
import sys
import struct


def askForService(token,data):
    # HOST, PORT 記得修改
    global HOST
    global PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    received = ""
    try:
        sock.connect((HOST, PORT))
        msg = bytes(token+"@@@"+data, "utf-8")
        msg = struct.pack(">I", len(msg)) + msg
        sock.sendall(msg)
        received = str(sock.recv(8192), "utf-8")
    finally:
        sock.close()
        return received
    ### Don't touch

def process(token,data):
    # 可在此做預處理

    result = askForService(token,data)
    # 可在此做後處理

    WSResult = []
    response = result

    if(response is not None or response != ''):
        response = response.split()
        for resp in response:
            resp = resp.strip()
            resp = resp[0:len(resp)-1]
            temp = resp.split('(')
            word = temp[0]
            pos = temp[1]
            WSResult.append((word,pos))

    return WSResult

def segresult(data):

    global HOST
    global PORT
    HOST, PORT = "140.116.245.151", 9996

    token = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOiIwIiwic3ViIjoiIiwiZXhwIjoxNTU0MDg2OTkwLCJhdWQiOiJ3bW1rcy5jc2llLmVkdS50dyIsImlhdCI6MTUzODUzNDk5MCwic2VydmljZV9pZCI6IjEiLCJpZCI6NTMsImlzcyI6IkpXVCIsIm5iZiI6MTUzODUzNDk5MCwidmVyIjowLjEsInVzZXJfaWQiOiIyOCJ9.OzoVfvfV6jl2Nd5HtQrM9wxkp6pMj6VwhOhfBY_uwF6NAI2MBeSs9_IUDDogY_jMI0Cg_BSO3r2q-c-ClwfPS5mvsCeaN9s5i9DUQ5kShpMjTdrdSUVcukFslaEImxq2DPvJz3l8PLhnsh5ypnqG2UBCnzsCM9Y3KJfMj_4SGeY"

    while True:

        try:

            tokenlist = process(token,data)
            resultlist = list()

            for tok in tokenlist:
                resultlist.append(tok[0])

            return str(resultlist)
            
        except EOFError:
            break

# if __name__ == '__main__':
#     segresult("123")