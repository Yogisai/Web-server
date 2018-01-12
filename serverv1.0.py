import socket
import threading
import sys
import re
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Server():
    def __init__(self,port,timer,homedir): 
        self.host = '' 
        self.port = port
        self.time= timer
        self.homedir = homedir
        self.threads=[]
        self.create_socket()
    def create_socket(self):
        try:
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#create an INET, STREAMing socket
            sock.bind((self.host,self.port))#bind the socket to a host, and a port
            sock.listen(250)#queue up as many as 250 connect requests
            logger.info('Serving HTTP on port %s ...', str(self.port))
            self.sock=sock
            self.accept_req()#call accept_req()
        except socket.error as message: 
            if sock: 
                sock.close() 
            logger.info("Could not open socket: %s", str(message) )
            sys.exit(1) 
    def accept_req(self):
        while 1:
            try:
                conn,addr=self.sock.accept()#accept Request
                if conn:
                    thr_multiple=Multiple(conn,addr,homedir,self.time)
                    thr_multiple.start()
                    self.threads.append(thr_multiple)
                for elements in self.threads: 
                    elements.join()
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)

class Multiple(threading.Thread):
    def __init__(self,conn,addr,homedir,time):
        threading.Thread.__init__(self)
        logger.info("client connected at %s",conn)
        self.conn = conn
        self.addr = addr 
        self.size = 65535
        self.time = time
        self.homedir = homedir

    def run(self):
        request = self.conn.recv(65535)
        if request:
            try:
                fh = open("ws.conf", "r")
                request2 = request.decode()
                request3 = request2.split("\n")
                #print(request3)
                request4 = request3[0].split()
                #print(request4)
                if request4[0] == "GET":
                    flag = 0
                    cntType = ""
                    filename = request4[1]
                    if filename != "/" and filename != "/inside":
                        extn = filename.split(".")
                        print(extn[1])
                        for line in fh:
                            if(line[:11] == "ContentType"):
                                print("2")
                                for word in line.split():
                                    if word[1:] == extn[1]:
                                        cntType = line
                                        flag = 1
                                        header = (request4[2] + "200 OK\n")
                                        break
                                #if(flag == 1):
                                 #   break
                        path = self.homedir + filename
                        if flag == 0:
                            header = (request4[2] + " 501 Not Implemented\n")
                            cntType = "Content-Type .html text/html"
                            http_response = ("<html><body>501 Not Implemented 501: " + filename + " </body></html>").encode()
                        
                        elif not(os.path.isfile(path)):
                            header = (request4[2] + " 404 Not Found\n")
                            cntType = "Content-Type .html text/html"
                            http_response =("<html><body>404 Not Found Reason URL does not exist: " + path + " </body></html>").encode()
                        else:
                            fh = open(path, "rb")
                            http_response = fh.read()
                            header = (request4[2] + " 200 OK\n")
                    elif filename == "/" or "/inside":
                        try:
                            extn2 = "index.html"
                            path = self.homedir + "/" + extn2
                            cntType = "Content-Type .html text/html"
                            fh = open(path, "rb")
                            http_response = fh.read()
                            header = (request4[2] + " 200 OK\n")
                        except:
                            header = (request4[2] + " 400 Not Found\n")
                            cntType = "Content-Type .html text/html"
                            http_response = ("<html><body>404 Not Found Reason URL does not exist: " + path + " </body></html>").encode()
                    else:
                        header = (request4[2] + "500 Internal Server Error:cannot allocate memory\n")
                        self.conn.send(header.encode())
                        self.conn.close()
                        return
                    print("5")
                    cnt = cntType.split()
                    header2 = (cnt[0] + ": " + cnt[2] + "\n")
                    self.conn.send(header.encode())
                    self.conn.send(header2.encode())
                    self.conn.send(b'\n')
                    self.conn.send(http_response)
                    self.conn.close()
                elif request4[0] == "POST":
                    flag = 0
                    pflag = 0
                    cntType = ""
                    filename = request4[1]
                    if filename != "/" and filename != "/inside":
                        extn = filename.split(".")
                        print(extn[1])
                        for line in fh:
                            if(line[:11] == "ContentType"):
                                print("2")
                                for word in line.split():
                                    if word[1:] == extn[1]:
                                        cntType = line
                                        flag = 1
                                        header = (request4[2] + "200 OK\n")
                                        break
                            if len(line.strip()) == 0:
                                pflag = 1
                            if pflag == 1:
                                postdata.append(line)
                                #if(flag == 1):
                                 #   break
                        path = self.homedir + filename
                        postdatasize = len(postdata)
                        if flag == 0:
                            header = (request4[2] + " 501 Not Implemented\n")
                            cntType = "Content-Type .html text/html"
                            http_response = ("<html><body>501 Not Implemented 501: " + filename + " </body></html>").encode()
                        
                        elif not(os.path.isfile(path)):
                            header = (request4[2] + " 404 Not Found\n")
                            cntType = "Content-Type .html text/html"
                            http_response =("<html><body>404 Not Found Reason URL does not exist: " + path + " </body></html>").encode()
                        else:
                            fh = open(path, "rb")
                            contents = fh.read()
                            data = ''.join(postdata)
                            encdata = ("<html><body><pre>" + data + "</body></html>").encode()
                            http_response = encdata + contents
                            header = (request4[2] + " 200 OK\n")
                    elif filename == "/" or "/inside":
                        try:
                            extn2 = "index.html"
                            path = self.homedir + "/" + extn2
                            cntType = "Content-Type .html text/html"
                            fh = open(path, "rb")
                            contents = fh.read()
                            data = ''.join(postdata)
                            encdata = ("<html><body><pre>" + data + "</body></html>").encode()
                            http_response =  encdata + contents
                            header = (request4[2] + " 200 OK\n")
                        except:
                            header = (request4[2] + " 400 Not Found\n")
                            cntType = "Content-Type .html text/html"
                            http_response = ("<html><body>404 Not Found Reason URL does not exist: " + path + " </body></html>").encode()
                    else:
                        header = (request4[2] + "500 Internal Server Error:cannot allocate memory\n")
                        self.conn.send(header.encode())
                        self.conn.close()
                        return
                    print("5")
                    cnt = cntType.split()
                    header2 = (cnt[0] + ": " + cnt[2] + "\n")
                    self.conn.send(header.encode())
                    self.conn.send(header2.encode())
                    self.conn.send(b'\n')
                    self.conn.send(http_response)
                    self.conn.close()
                else:
                    http_response=("<html><body>400 Bad Request Reason:Invalid Method: " + request4[1] + " </body></html>" )
                    self.conn.send(http_response.encode())
                    self.conn.close()
            except Exception as e:
                print(e)
    #def conClose(self):
        
                
if __name__ == '__main__':
    extn = "root"
    homedir = os.getcwd() + "/" + extn
    try:
        fh = open("ws.conf","r")
        for line in fh:
            try:
                port = re.search(r'(ListenPort)\s(.*)',line)
                if (port.group(2) != "None"):
                    break
            except:
                continue
        for line in fh:
            try:
                AliveTimer = re.search(r'(KeepaliveTime)\s(.*)',line)
                if (AliveTimer.group(2) != "None"):
                    break
            except:
                continue
    except:
        logger.info("ws.conf file not found")
        sys.exit(0)
    if (int(port.group(2))<=65535 and int(port.group(2))>1023):
        server=Server(int(port.group(2)), int(AliveTimer.group(2)), homedir)
    else:
        logger.info("Port number not accepted")
        sys.exit(1)
