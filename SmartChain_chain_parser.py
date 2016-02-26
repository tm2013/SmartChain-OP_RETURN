"""
Basic chain parser tool for SmartChain functions.
Author: Tim M. (TM2013)
Co-Author: Bitkapp (aka alaniz)
Organization: Project Radon
Date: 2/17/2016

Requirements:
BitcoinRPC
An RPC-enabled client
"""

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
import time
try:
  import cPickle as pickle
except:
  import pickle

# Debug settings
debug = True
if debug:
    logging.basicConfig()
    logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

# RPC Configuration
rpc_user = "user"
rpc_pass = "pass"
rpc_port = "port"

class DataBase():
	def __init__(self):
		# Initialise database and RPC connection
		self.loadSync()
		self.rpc = AuthServiceProxy(("http://%s:%s@127.0.0.1:%s/") % (rpc_user, rpc_pass, rpc_port))

	def saveSync(self):
		# Dump database into a pickle
		pickle.dump(self.block_data, open('block_data.p','wb'))

	def loadSync(self):
		# Load database from pickle
		try:
			self.block_data = pickle.load(open('block_data.p','rb'))
		except IOError as e:
			# If no pickle exists initialise a new database
			self.block_data = {}

	def syncFromLastBlock(self):
		block_height = self.rpc.getblockcount()
		# Sync from last block of existing database
		try:
			if self.block_data:
				last_block = max(self.block_data.keys())
				for block in range(last_block+1, block_height):
					self.block_data[block] = self.rpc.getblockbynumber(block)["tx"]
			# Start new sync process if new database has been initialised
			else:
				for block in range(0, block_height):
					self.block_data[block] = self.rpc.getblockbynumber(block)["tx"]
		except KeyboardInterrupt as e:
			self.saveSync()

	def returnBlock(self, blocknumber):
		# Returns block data from database for a particular block
		try:
			block = self.block_data[blocknumber]
			return block
		except KeyError as e:
			raise KeyError('Local database is not synced to required block height.')

#d = DataBase()
#d.syncFromLastBlock()
#d.saveSync()