import sys
import hashlib
import json

from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

import requests
from urllib.parse import urlparse


class Blockchain(object):
    dificulty_target = "0000"

    def hash_block(self, block):
        block_encoded = json.dumps(block, sort_keys=True).encode()
        print("block_encoded: ", block_encoded)
        return hashlib.sha256(block_encoded).hexdigest()
    

    #create genesis block
    def __init__(self):
        self.chain = []
        self.current_transactions = []
       
        genesis_hash = self.hash_block("genesis_block")

        self.append_block(
            hash_of_previous_block = genesis_hash,
            nonce = self.proof_of_work(0, genesis_hash, []),
        )

    def proof_of_work(self, index, hash_of_previous_block, transactions, nonce):
        nonce = 0
        while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:
            nonce += 1

        return nonce
    

    def valid_proof(self, index, hash_of_previous_block, transactions, nonce):
        content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()
        print("content: ", content)
        content_hash = hashlib.sha256(content).hexdigest()
        print("content_hash: ", content_hash)
        return content_hash[:len(self.dificulty_target)] == self.dificulty_target

