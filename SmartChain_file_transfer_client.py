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
import time
import pickle

class Client():
	# Client class for file transfer HTTP server
	def __init__(self, ip, port):
		# Define ip and port and check if connection exists
		self.ip = ip
		self.port = port
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

#c = Client('IP Address', 9000)
#c.uploadFile('Test text', 'test.txt')
#c.requestDirList()
#c.requestFileContents('test.txt')
