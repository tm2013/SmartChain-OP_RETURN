"""
Basic OP_RETURN data storage tool for SmartChain functions.
Author: Tim M. (TM2013)
Co-contributor: Bitkapp (aka alaniz)
Organization: Project Radon
Date: 2/17/2016

Requirements:
BitcoinRPC
An RPC-enabled client

Reminders:
The client must be unlocked
0.0011 coins are required per 39 bytes you would like to store
Data ID's are invalid until the transactions that created them contain at least two confirmations.
"""

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
import time
import math
from binascii import hexlify, unhexlify

# Debug settings
debug = True
if debug:
    logging.basicConfig()
    logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)


# RPC Configuration
rpc_user = "user"
rpc_pass = "pass"
rpc_port = "port"

class Document():
    def __init__(self, data):
        # RPC Connection
        self.rpc = AuthServiceProxy(("http://%s:%s@127.0.0.1:%s/") % (rpc_user, rpc_pass, rpc_port))
        self.data = data

    def store_data(self, change_address):
        # Check if there are inputs
        if not change_address:
            raise Exception("Please enter a change address!")
        if not self.data:
            raise Exception("Please enter data to store!")
        # Define satoshi
        self.SATOSHI = 0.0001
        # Test and mold the data
        if len(self.data) > 351:
            raise Exception("You shall not pass.")
        dataChunks = list(enumerate(self.data[0+i:39+i] for i in range(0, len(self.data), 39)))
        print dataChunks
        blockHeight = self.rpc.getblockcount()
        blockHeightID = str(int(blockHeight)+1)
        first_bytes = []
        first_bytes_str = ""
        # Create OP_RETURN transactions
        for i in dataChunks:
            si = list(i)
            si = str(si[0]+1)+si[1]
            # Split inputs to avoid burning many coins into the void
            self.split_inputs(math.ceil(float(len(self.data)/40)), change_address)
            time.sleep(5)
            # Get the inputs
            self.get_inputs()
            time.sleep(1)
            # Form and submit transactions
            first_bytes.append(self.create_transaction(self.txid, self.vout, self.input_address, change_address, self.change_amount, si)[:12])
        # Form the Data ID
        for s in first_bytes:
            first_bytes_str += s
        self.ID = blockHeightID + first_bytes_str
        print self.ID
        return self.ID

    # Create OP_RETURN raw function
    def create_transaction(self, txidin, vout, input, change, changeamt, data):
        tx = self.rpc.createrawtransaction([{"txid": txidin, "vout": vout}], {input: self.SATOSHI, change: changeamt})
        oldScriptPubKey = tx[len(tx)-60:len(tx)-8]
        newScriptPubKey = "6a" + hexlify(chr(len(data))) + hexlify(data)
        newScriptPubKey = hexlify(chr(len(unhexlify(newScriptPubKey)))) + newScriptPubKey
        if oldScriptPubKey not in tx:
            print tx
            raise Exception("Something broke!")
        tx = tx.replace(oldScriptPubKey, newScriptPubKey)
        print self.rpc.decoderawtransaction(tx)
        tx = self.rpc.signrawtransaction(tx)['hex']
        tx = self.rpc.sendrawtransaction(tx)
        return tx

    # Get split inputs raw function
    def get_inputs(self):
        # Get unspent transactions
        unspent = self.rpc.listunspent()
        # Put the unspent transactions to the test
        for tx in unspent:
            print float(tx["amount"])
            if float(tx["amount"]) == 0.001:
                self.txid = tx["txid"]
                self.vout = tx["vout"]
                self.input_address = tx["address"]
                self.input_amount = float(tx["amount"])
                self.change_amount = self.input_amount - 0.0003
                break
        else:
            raise Exception("No proper inputs!")

    def split_inputs(self, split_qty, input_address_split):
        if int(split_qty) != 0:
            for i in range(int(split_qty)):
                self.rpc.sendtoaddress(input_address_split, 0.001)
        else:
            self.rpc.sendtoaddress(input_address_split, 0.001)

class Search():
    def __init__(self):
        # RPC Connection
        self.rpc = AuthServiceProxy(("http://%s:%s@127.0.0.1:%s/") % (rpc_user, rpc_pass, rpc_port))

    # Gather the data stored from a specific data ID
    def get_data(self, data_ID):
        # Check if there are inputs
        if not data_ID or not len(data_ID) > 12:
            raise Exception("Please enter a valid data ID.")
        tx_qty = len(data_ID) - int(math.floor(len(data_ID)/12.0) * 12)
        tx_in_ID = data_ID[tx_qty:len(data_ID)]
        tx_in_ID = list(tx_in_ID[0+i:12+i] for i in range(0, len(tx_in_ID), 12))
        blockNumber = int(data_ID[0:tx_qty])
        return self.transaction_search(blockNumber, tx_in_ID)

    def transaction_search(self, number, txns):
        prev_block_data = self.rpc.getblockbynumber(int(number)-1)
        block_data = self.rpc.getblockbynumber(int(number))
        next_block_data = self.rpc.getblockbynumber(int(number)+1)
        transactions = []
        op_return_data = []
        processed_data = ""
        for s in txns:
            for tx in prev_block_data["tx"]:
                if s == tx[:12]:
                    transactions.append(tx)
            for tx in block_data["tx"]:
                if s == tx[:12]:
                    transactions.append(tx)
            for tx in next_block_data["tx"]:
                if s == tx[:12]:
                    transactions.append(tx)

        for txn in transactions:
            tx_data = self.rpc.gettransaction(txn)
            for data in tx_data["vout"]:
                op_return_data.append(unhexlify(data["scriptPubKey"]["asm"][10:]))
        op_return_data.sort()
        for s in op_return_data:
            processed_data = processed_data + s[1:len(s)+1]
        print processed_data
        return processed_data

#d = Document('Some data')
#d.store_data("Some Radium address")

#s = Search()
#s.get_data("Some data ID")

