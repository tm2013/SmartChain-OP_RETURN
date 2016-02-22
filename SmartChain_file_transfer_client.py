"""
Basic file transfer client for SmartChain functions.
Author: Tim M. (TM2013)
Co-Author: Bitkapp (aka alaniz)
Organization: Project Radon
Date: 2/19/2016

Requirements:
HTTP Connection
"""

import urllib2
import urlparse
import os
import time
import pickle
from hashlib import sha256
from simplecrypt import encrypt, decrypt
from binascii import hexlify, unhexlify

class Client():
    # Client class for file transfer HTTP server
    def __init__(self):
        # Define ip and port and check if connection exists
        if not os.path.isfile(os.getcwd()+'/nodes.p'):
            nodes = ["localhost", {
                "127.0.0.1":9000
            }]
            pickle.dump(nodes, open("nodes.p", "wb"))

        if pickle.load(open("nodes.p", "rb"))[0] != "localhost":
            raise Exception("Your node list is not configured correctly, and could possibly be malicious.")
        else:
            SEED_NODES = pickle.load(open( "nodes.p", "rb" ))[1]
        for key in SEED_NODES:
            self.ip = key
            self.port = SEED_NODES[key]
        try:
            urllib2.urlopen(self.make_url(self.ip, self.port, '/'))
        except urllib2.URLError:
            raise Exception('Could not connect to server.')

    def make_url(self, server, port, path, scheme='http'):
        # Parse URL
        netloc = '{}:{}'.format(server, port)
        url = urlparse.urlunsplit((scheme, netloc, path, '', ''))
        return url

    def requestDirList(self):
        # Request directory listing
        url = self.make_url(self.ip, self.port, '/')
        file_list = urllib2.urlopen(url).read()
        files = []
        print 'Files from server:'
        for filename in file_list.splitlines():
            files.append(filename)
            print '- {}'.format(filename)
        return files

    def requestFileContents(self, filename):
        # Request contents of a file
        url = self.make_url(self.ip, self.port, filename)
        contents = urllib2.urlopen(url).read()
        print 'Contents:'
        print contents

    def uploadFile(self, contents, filename):
        # Upload file to server
        url = self.make_url(self.ip, self.port, filename)
        f = urllib2.urlopen(url, data=contents)

    def authenticateAs(self, secret_key, pin):
        if not type(pin) == int:
            raise Exception("The PIN you provided is not a vaild number, please try again.")
        for i in range(pin):
            authentication_key = sha256(secret_key)
        authentication_key = str(authentication_key)
        return authentication_key

    def shred_file(self, authkey, splitBytes=10, file_path):
        with open(str(file_path), 'rb') as f:
            content = f.read()
        content = hexlify(content)
        file_data = encrypt(authkey, content)
        file_data = list(file_data[0+i:splitBytes+i] for i in range(0, len(file_data), splitBytes))
        return file_data


# c = Client()
# c.uploadFile('Test text', 'test.txt')
# c.requestDirList()
# c.requestFileContents('test.txt')
# key = c.authenticateAs("hello world", 10)
# c.shred_file(key, 100, 'README.md')
