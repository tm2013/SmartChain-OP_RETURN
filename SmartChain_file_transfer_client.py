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
from hashlib import sha256
from simplecrypt import encrypt, decrypt
from binascii import hexlify, unhexlify
from random import randint
import SmartChain_OP_RETURN

class Client():
    # Client class for file transfer HTTP server
    def __init__(self, IP='127.0.0.1', PORT=9000):
        self.authentication_key = False
        # Define ip and port and check if connection exists
        self.ip = IP
        self.port = PORT
        try:
            urllib2.urlopen(self.make_url(self.ip, self.port, '/'))
        except urllib2.URLError:
            raise Exception('Could not connect to server.')

    def make_url(self, server, port, path, scheme='http'):
        # Parse URL
        netloc = '{}:{}'.format(server, port)
        url = urlparse.urlunsplit((scheme, netloc, path, '', ''))
        return url

    def requestDirList(self, PRINT=False):
        # Request directory listing
        url = self.make_url(self.ip, self.port, '/')
        file_list = urllib2.urlopen(url).read()
        files = []
        if PRINT:
            print 'Files from server:'
            for filename in file_list.splitlines():
                files.append(filename)
                print '- {}'.format(filename)
        return files

    def requestFileContents(self, filename, decrypted=True):
        # Request contents of a file
        url = self.make_url(self.ip, self.port, filename)
        contents = urllib2.urlopen(url).read()
        if decrypted:
            contents = decrypt(self.authentication_key, unhexlify(contents))
            f = open(filename, 'wb')
            f.write(contents)
            f.close()
        else:
            print contents

    def uploadFile(self, filepath):
        # Upload file to server
        if not self.authentication_key:
            raise Exception("You are not identified, please log in.")
        shredded_contents = self.shred_file(self.authentication_key, filepath)
        url = self.make_url(self.ip, self.port, os.path.basename(filepath))
        f = urllib2.urlopen(url, data=shredded_contents)

    def authenticateAs(self, secret_key, pin):
        if not type(pin) == int or len(str(pin)) > 4:
            raise Exception("The PIN you provided is not a vaild number, please try again.")
        for i in range(pin):
            authentication_key = sha256(secret_key).hexdigest()
        self.authentication_key = str(authentication_key)
        return self.authentication_key

    def shred_file(self, authkey, file_path):
        with open(str(file_path), 'rb') as f:
            content = f.read()
        file_data = encrypt(authkey, content)
        file_data = str(hexlify(file_data))
        return file_data

    def newStorageContract(self, changeAddress, extIP, extPORT, filepath, duration, pricePerServer):
        title = hexlify(str(randint(100000,1000000)))
        #SmartChain_OP_RETURN.Document("ICC"+extIP+":"+str(extPORT)+title).store_data(changeAddress)
        contractData = '{"file":%s,"size":%d,"duration":%d,"price":%d}' % (os.path.basename(filepath), os.path.getsize(filepath), duration, float(pricePerServer))
        url = self.make_url(self.ip, self.port, title+".txt")
        f = urllib2.urlopen(url, data=contractData)

# Start the client

#c = Client()
# Authenticate yourself as an entity using a passcode and a PIN number

#c.authenticateAs("", 0000)
# Upload a file. You are required to be authenticated if you wish to modify data on a server.

#c.uploadFile(r'')
# Standard request

#c.requestDirList()
# Request (download) the contents of the file that you stored.
# If you enter the False flag, it will return the encrypted data, rather than the decrypted data.

#c.requestFileContents('')
#Client().newStorageContract("VKEWRJvYBtjqarXuAhYaKFjvUMc2PugNMf", "173.170.69.31", 9000, "test.txt", 100, 1)
Client().requestDirList()
