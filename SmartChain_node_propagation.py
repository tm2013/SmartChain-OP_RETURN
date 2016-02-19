"""
Basic node propagation service for SmartChain functions.
Author: Tim M. (TM2013)
Co-Author: Bitkapp (aka alaniz)
Organization: Project Radon
Date: 2/19/2016

Requirements:
HTTP Connection
BitcoinRPC
An RPC-enabled client
"""

from SmartChain_file_transfer_client import Client
from SmartChain_OP_RETURN import Search

SEED_NODE_ID = ''


class Propagator():
	def __init__(self):
		self.search = Search()

	def findSeedNodes(self):
		seed_node_list = self.search.get_data(SEED_NODE_ID)
		# Format DATA
		return seed_node_list

	def findNodeList(self, search_id):
		# Return a general nodes list from a search_id
		node_list = self.search.get_data(search_id)
		# Format Data
		return node_list

	def connectToNode(self, ip, port):
		try:
			client = Client(ip, port)
		except Exception as e:
			client = None
		return client

	def findConnectedNodes(self, nodes):
		clients = []
		for node in nodes:
			client = self.connectToNode(node[0], node[1])
			if client:
				clients.append(client)
		return clients

	def findBestNode(self, nodes):
		connected_nodes = self.findConnectedNodes(nodes)
		dir_heights = {}
		for node in connected_nodes:
			dir_heights[node.ip+':'+str(node.port)] = len(node.requestDirList())
		height = max(dir_heights.values())
		best_node = dict(zip(i.values(),i.keys()))[height].split(':')
		best_node_ip, best_node_port = best_node[0], best_node[1]
		return best_node_ip, best_node_port

	def syncNode(self):
		pass
		# This will be main loop calling for nodes lists and download files from nodes

		# Big while sort of loop with while connected: Download stuff from best node
		# and if disconnected look for another best node and continue

