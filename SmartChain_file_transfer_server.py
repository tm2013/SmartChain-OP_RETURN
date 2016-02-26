"""
Basic file transfer server for SmartChain functions.
Author: Tim M. (TM2013)
Co-Author: Bitkapp (aka alaniz)
Organization: Project Radon
Date: 2/19/2016

Requirements:
HTTP Connection
"""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import os
try:
  import cPickle as pickle
except:
  import pickle

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global running
        print self.client_address[0]
        if self.path == '/':
            self.list_files()
        elif self.path.startswith('/quit'):
            self.send_response(200)
            running = False
        else:
            self.send_file(self.path[1:])

    def do_POST(self):
        filename = self.path[1:] # Remove the / from the path
        filesize = int(self.headers['Content-Length'])
        contents = self.rfile.read(filesize)

        with open(os.getcwd()+'/data/'+filename, 'w') as f:
            f.write(contents.decode())

        self.send_response(200)

    def send_file(self, filename):
        # Check to see if file exists and is a file, not directory
        if os.path.isfile(os.getcwd()+'/data/'+filename):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()

            # Read and send the contents of the file
            with open(os.getcwd()+'/data/'+filename) as f:
                contents = f.read()
            self.wfile.write(contents)
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()

    def list_files(self):
        # List files in ./data directory
        file_list = os.listdir(os.getcwd()+'/data')
        if file_list:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            for filename in file_list:
                self.wfile.write('{}\n'.format(filename))
        else:
            # If no files are found send 404
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()

class Server():
    def __init__(self):
        # Check if ./data directory exists and start server
        if not os.path.isdir(os.getcwd()+'/data'):
            raise Exception('You must create a directory ./data to start server.')
        elif not os.path.isfile(os.getcwd()+'/data'+'/nodes.p'):
            nodes = {}
            pickle.dump(nodes, open( "data/nodes.p", "wb" ))
            if not os.path.isfile(os.getcwd()+'/data'+'/data.p'):
                data = {}
                pickle.dump(data, open( "data/data.p", "wb" ))
                self.startServer()
            else:
                self.startServer()
        elif not os.path.isfile(os.getcwd()+'/data'+'/data.p'):
            data = {}
            pickle.dump(data, open( "data/data.p", "wb" ))
            self.startServer()
        else:
            self.startServer()

    def startServer(self):
        running = True
        server = HTTPServer(('', 9000), Handler)
        print 'Server started on host:{}, port:{}'.format(*server.server_address)
        while running:
            server.handle_request()

s = Server()
