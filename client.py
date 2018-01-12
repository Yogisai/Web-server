import threading
from datetime import datetime
import http.client
import os


class Client():
    def __init__(self):
        self.host = ''
        self.port = 3347
        self.threads = []
        self.send_req()

    def send_req(self):
        workers = 1
        while workers <= 100:
            thr_multiple = Multiple(workers, self.port)
            thr_multiple.start()
            print("Thread" + str(workers))
            self.threads.append(thr_multiple)
            workers = workers + 1
            for elements in self.threads:
                elements.join()


class Multiple(threading.Thread):
    def __init__(self, count, port):
        threading.Thread.__init__(self)
        self.count = count
        self.port = port

    def run(self):
        start_time = datetime.now()
        print(str(start_time + "\n \n"))
        conn = http.client.HTTPConnection('localhost:3346')
        conn.request("GET", "/")
        end_time = datetime.now()
        print(str(end_time + "\n \n"))
        print("Time taken by thread to execute " + str(end_time - start_time))
        conn.close()
        #100 req -diff fies
        conn.request("GET", "/%d",self.count)


'''
Things you might need to do in the PA:
1) Handle HTTP Error codes
2) Demonize threads to improve performance or implement timeout and return logic. 
3) Read the PA for more information
'''

if __name__ == '__main__':
    server = Client()
