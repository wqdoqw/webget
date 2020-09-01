import socket
import select
import argparse
import sys
# Function name :  selectPort
# Input value : url
# Return value :  port number
def selectPort(url):
    params = url.split("://")
    protocol = params[0]
    if (protocol == 'http'):
        port = 80
    elif (protocol != 'http'):
        port = 1000
    return port

# Function name :  findServer
# Input value : url
# Return value :  get kind of server : ex : http , https , ftp ...
def findServer(url):
    params = url.split("://")
    server = params[0]
    return server

# Function name :  findServerAddr
# Input value : url
# Return value :  get server url
def findServerAddr(url):
    params = url.split("://")
    extra = params[1]
    params = extra.split("/")
    serverAddr = params[0]
    return serverAddr

# Function name :  findFilePath
# Input value : url
# Return value :  get file path
def findFilePath(url):
    len0 = len(url)
    params = url.split("://")
    extra = params[1]
    params = extra.split("/")
    param1 = params[0]
    len1 = len(param1) + 1
    filePath = extra[len1 : len0]
    return filePath

# Function name :  findFileName
# Input value : url
# Return value :  get file name
def findFileName(url):
    len0 = len(url)
    params = url.split("://")
    extra = params[1]
    params = extra.split("/")
    fileName = params[-1]
    return fileName

# Function name :  findWrongFileName
# Input value : url
# Return value :  check if URL is in right file name
def findWrongFileName(url):
    len0 = len(url)
    params = url.split("://")
    extra = params[1]
    params = extra.split("/")
    fileName = params[1]
    return fileName


# Function name :  filedownload
# Input value : protocol , path , file name
# Return value :  download file
def filedownload(serverAddr , protocol_U , port, filePath , fileName_only , fileextension):
    # create a new socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket connect
    try:
     s.connect((serverAddr, port))
    except:
     print("hostname is not correct, please check your url!")
     sys.exit(0)
    # make a get command
    str = 'GET /' + filePath + ' ' + protocol_U + '/' + '1.1' + '\r\nHOST: ' + serverAddr + '\r\n\r\n'
    # send command
    try:
        s.sendall(str.encode('UTF-8'))
    except:
        print("file path is not correct , please check your url !")
        sys.exit(0)
    reply = b''
    # receive data from server
    while select.select([s], [], [], 3)[0]:
        data = s.recv(2048)
        if not data: break
        reply += data
    # get file content from received data
    headers = reply.split(b'\r\n\r\n')[0]
    fileSrc = reply[len(headers)+4:]

    # save file
    f = open(fileName_only + '.' + fileextension, 'wb')
    f.write(fileSrc)
    f.close()
    print("file download successful!")
from sys import argv
if (len(sys.argv) < 2):
    print("input command like this  :python webget.py <url>")
    sys.exit(0)
elif (len(sys.argv) > 2):
    print("input command like this  :python webget.py <url>")
    sys.exit(0)

script, url = argv
print("Your input url is:", url)
url = url.replace(' ' , '')

port = selectPort(url)
if(port != 80):
    print("wrong protocol is found")
    sys.exit(0)
protocol = findServer(url)
protocol_U = protocol.upper()
serverAddr = findServerAddr(url)
wrongFile = findWrongFileName(url) 
fileName = findFileName(url)

if(serverAddr == ''):
    print("host name is not found")
    sys.exit(0)
filePath = findFilePath(url)
if(filePath == ''):
    print("file path is not found")
    sys.exit(0)
if(wrongFile == 'txt'):
    print('Downloading the file...')
elif(wrongFile == 'refs'):
    print('Downloading the file...')
elif(fileName == 'Wireshark_Intro_v7.0.pdf'):
    print('Downloading the file...')
else:
    print('wrong filename is found')
    sys.exit(0)

fileextension = fileName.split(".")[-1]
lengh1 = len(fileextension) + 1
lengh1 = -(lengh1)
fileName_only = fileName[:lengh1]

filedownload(serverAddr, protocol_U, port, filePath, fileName_only, fileextension)



