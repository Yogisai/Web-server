The server is run on the command promt without any arguments.
Port number is set by changing the port number in the ws.conf file.
The server will implement 2 methods

1.Get:
The server will read the request sent by the client i.e. the browser.
Depending on whether the file exists in the root directory or the extension exists in ws.conf file,the error is thrown to the client according to the given format in the question.
If no error exists, the server reads the request and sends the required file in binary format.
A header is sent before the actual file is sent for the client to recognize and to expect what it is recieveing next.
Multi threading is implemented in the accept_req function under the class server.
The server will accept further requests sent by the client read in the html file if any and responds to them too in a similar fashion.
If no file name is given, a default html file is shown.
All the information is sent to the client in binary format.


2.Post
Post does a similar job as get. 
All the data sent in the request after the empty line is read and copied into a list which is then prepended with the required information before the file is sent.
Logging is used in place of print.
regular expressions are used for cutting the required information from the ws.conf file

A client file is made.
This file sends requests to the server in 2 ways. One requesting the same file a 100 times and other 100 different files. This basically tests the multithreading approach on the server.