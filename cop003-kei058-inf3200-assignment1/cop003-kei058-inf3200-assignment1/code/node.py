#!/usr/bin/env python3
import argparse
import json
import re
import signal
import socket
import socketserver
import threading
import http.client
import uuid
import numpy as np
import hashlib
import argparse

from http.server import BaseHTTPRequestHandler,HTTPServer

object_store = {}
neighbors = []
request_buffer = []
	
class NodeHttpHandler(BaseHTTPRequestHandler):
	def send_whole_response(self, code, content, content_type="text/plain"):

		if isinstance(content, str):
			content = content.encode("utf-8")
			if not content_type:
				content_type = "text/plain"
			if content_type.startswith("text/"):
				content_type += "; charset=utf-8"
		elif isinstance(content, bytes):
			if not content_type:
				content_type = "application/octet-stream"
		elif isinstance(content, object):
			content = json.dumps(content, indent=2)
			content += "\n"
			content = content.encode("utf-8")
			content_type = "application/json"

		self.send_response(code)
		self.send_header('Content-type', content_type)
		self.send_header('Content-length',len(content))
		self.end_headers()
		self.wfile.write(content)

	def find_successor(self, address, path, method, value):
		"""
		forwards a request untill the successor of the address is found
		"""
		if address in server.finger_table and True in server.finger_table[address]:
			full_address = server.finger_table[address][0]
			response, status = self.get_value(full_address, path, method, value)
		else:
			response, status = self.get_value(neighbors[0], path, method, value)	

		return response, status

	def extract_key_from_path(self, path):
		return re.sub(r'/storage/?(\w+)', r'\1', path)

	def extract_node_from_path(self, path):
		"""
		helper function to extract the node identity from a path starting with /finger
		"""
		return path.split("/")[2]


	def get_value(self, node, path, method, content):
		"""
		used to forward request, borrowed from client.py in the handout, somewhat modified version of it.
		"""
		conn = http.client.HTTPConnection(node)
		if method == 'GET':
			conn.request(method, path)
		else: 
			conn.request(method, path, content)
		resp = conn.getresponse()
		headers = resp.getheaders()
		if resp.status != 200:
			value = None
		else:
			value = resp.read()
		contenttype = "text/plain"
		for h, hv in headers:
			if h=="Content-type":
				contenttype = hv
		conn.close()
		return value, resp.status
	
	def do_POST(self):
		"""
		Handler for post request
		"""
		#if it starts with successor, then the node who sent the message is the servers predecessor
		if self.path.startswith("/successor"):
			p = self.extract_node_from_path(self.path)

			neighbors[1] = p
			
			server.predecessor = id_from_name(p)
		
		#if it starts with predecessor, then the node who sent the message is the servers successor
		else:
			if self.path.startswith("/predecessor"):
				s = self.extract_node_from_path(self.path)

				neighbors[0] = s
				server.successor = id_from_name(s)

	def do_PUT(self):
		"""
		Handler for PUT request
		"""
		content_length = int(self.headers.get('content-length', 0))

		key = self.extract_key_from_path(self.path)
		value = self.rfile.read(content_length)

		address = int(uuid.UUID(key)) % server.M
		
		#edge case for when there are only one node in the circle
		if server.successor == server.id:
			object_store[key] = value

			self.send_whole_response(200, "Value stored for " + key)
		
		elif address <= server.id and address > server.predecessor:
			object_store[key] = value

			self.send_whole_response(200, "Value stored for " + key)
		
		elif server.id < server.predecessor and is_bewteen(server.predecessor, address, server.id):
			object_store[key] = value

			self.send_whole_response(200, "Value stored for " + key)
		else:
			response, status = self.find_successor(address, self.path, "PUT", value)
			self.send_whole_response(200, "Value stored for " + key)
		
	
	def do_GET(self):
		"""
		Handler for GET request
		"""
		if self.path.startswith("/storage"):
			key = self.extract_key_from_path(self.path)
			
			address = int(uuid.UUID(key)) % server.M

			#edge case for when there are only one node in the circle
			if server.successor == server.id:
				if key in object_store:
					
					self.send_whole_response(200, object_store[key])
				else:
					self.send_whole_response(404, "No object with key '%s' on this node" % key)
			
			elif address <= server.id and address > server.predecessor or address == server.id:
				if key in object_store:
					
					self.send_whole_response(200, object_store[key])
				else:
					self.send_whole_response(404, "No object with key '%s' on this node" % key)

			elif server.id < server.predecessor and is_bewteen(server.predecessor, address, server.id):
				if key in object_store:
					self.send_whole_response(200, object_store[key])
				else:
					self.send_whole_response(404, "No object with key '%s' on this node" % key)

			else:
				value, status = self.find_successor(address, self.path, "GET", None)
		
				if status != 200:
					self.send_whole_response(404, "No object with key '%s' on this node" % key)
				else:
					self.send_whole_response(200, value)

		elif self.path.startswith("/neighbors"):
			self.send_whole_response(200, neighbors)
		else:
			self.send_whole_response(404, "Unknown path: " + self.path)

class ThreadingHttpServer(HTTPServer, socketserver.ThreadingMixIn):
	def __init__(self, *args, **kwargs):    
		super(ThreadingHttpServer, self).__init__(*args, **kwargs)
		self.finger_table = {}
		self.M = 16 #must be an exponent of two, 2, 4, 8, 16, 32, 64 
		self.predecessor = None
		self.successor = None

	def innit_(self, args):
		"""
		initializes the server
		"""
		self.port = args.port
		
		if args.cluster == True:
			self.name = self.server_name.split('.')[0]
			self.address = self.name + ":" + str(self.port)
			self.id = id_from_name(self.name)
		else:
			self.name = "localhost:"+str(self.port)
			self.address = self.name
			self.id = id_from_name(self.name)


		#this will only happen when several instances of the api is run at the same time
		if neighbors[0] != None and neighbors[1] != None:
			self.successor = id_from_name(neighbors[0])
			self.predecessor = id_from_name(neighbors[1])

		#this means that a join opperation should be ran
		else:
			if args.join != None:
				nodes = list(walk(args.join))
				nodes = mergeSort(nodes)

				p, s = self.find_placement(nodes)
				
				neighbors[0] = s
				neighbors[1] = p

				self.successor = id_from_name(s)
				self.predecessor = id_from_name(p)

				notify_successor(neighbors[0], self.address)
				notify_predecessor(neighbors[1], self.address)
			else:
				neighbors[0] = self.address
				neighbors[1] = self.address
				
				self.successor = id_from_name(self.address)
				self.predecessor = id_from_name(self.address)

	def find_placement(self, all_neighbors):
		"""
		finds the nodes placement in the chord circle based on all nodes in the network
		"""
		size = len(all_neighbors)
		if size <= 1:
			return all_neighbors[0], all_neighbors[0]
		
		elif size >= 2:
			
			for i in range(size):
				a = id_from_name(all_neighbors[i])
				b = self.id
				c = id_from_name(all_neighbors[(i + 1) % size])

				if is_bewteen(a, b, c):
					return all_neighbors[i], all_neighbors[(i + 1) % size]
		
		else:
			print("unexpected error, size < 1")
			quit()

def mergeSort(arr): 
	""" Borrowed mergesort from geeksforgeeks.com """
	if len(arr) >1: 
		mid = len(arr)//2 
		L = arr[:mid] 
		R = arr[mid:] 

		mergeSort(L)
		mergeSort(R) 

		i = j = k = 0
		while i < len(L) and j < len(R): 
			if id_from_name(L[i]) < id_from_name(R[j]):
				arr[k] = L[i] 
				i+= 1
			else: 
				arr[k] = R[j] 
				j+= 1
			k+= 1
 
		while i < len(L): 
			arr[k] = L[i] 
			i+= 1
			k+= 1

		while j < len(R): 
			arr[k] = R[j] 
			j+= 1
			k+= 1 
	
	return arr

def id_from_name(name):
	"""
	returns the value of the hashed name mod M
	"""
	if name.startswith("localhost"):
		ids = hash_name(name) % server.M
	else:
		name = name.split(":")[0]
		ids = hash_name(name) % server.M
	
	return ids

def hash_name(name):
	"""
	hashes a name with sha1 hashfunction
	"""
	m = hashlib.sha1()
	m.update(name.encode('utf-8'))
	return int(m.hexdigest(), 16)

def is_bewteen(a, b, c):
	"""
	checks if the number b is in the intervall a-c
	"""
	buffer = []

	gap = (c-a)
	if gap < 0:
		c = server.M + c

	while(a < c):
		a += 1
		buffer.append(a % server.M)
				
	if b in buffer:
		return True

	return False

def walk(start_nodes):
	"""
	borrowed from the client.py in the handout
	"""

	to_visit = start_nodes
	visited = set()
	while to_visit:
		next_node = to_visit.pop()
		visited.add(next_node)
		neighbors = neighbours(next_node)
		for neighbor in neighbors:
			if neighbor not in visited:
				to_visit.append(neighbor)
	
	return visited

def neighbours(node):
	"""
	borrowed from the client.py in the handout
	"""

	conn = http.client.HTTPConnection(node)
	conn.request("GET", "/neighbors")
	resp = conn.getresponse()
	if resp.status != 200:
		neighbors = []
	else:
		body = resp.read()
		neighbors = json.loads(body)
	conn.close()
	return neighbors

def notify_successor(node, message):
	"""
	sends a post to a node to notify that it has gotten new predecessor
	"""
	conn = http.client.HTTPConnection(node)
	conn.request("POST", "/successor/"+str(message))
	conn.close()

def notify_predecessor(node, message):
	"""
	sends a post to a node to notify that it has gotten new successor
	"""
	conn = http.client.HTTPConnection(node)
	conn.request("POST", "/predecessor/"+str(message))
	conn.close()

def arg_parser():
	PORT_DEFAULT = 8000
	DIE_AFTER_SECONDS_DEFAULT = 20 * 60
	NEIGHBORS_DEFAULT = [None, None]
	JOIN_DEFAULT = None

	parser = argparse.ArgumentParser(prog="node", description="DHT Node")

	parser.add_argument("-p", "--port", type=int, default=PORT_DEFAULT,
			help="port number to listen on, default %d" % PORT_DEFAULT)

	parser.add_argument("--die-after-seconds", type=float,
			default=DIE_AFTER_SECONDS_DEFAULT,
			help="kill server after so many seconds have elapsed, " +
				"in case we forget or fail to kill it, " +
				"default %d (%d minutes)" % (DIE_AFTER_SECONDS_DEFAULT, DIE_AFTER_SECONDS_DEFAULT/60))

	parser.add_argument("neighbors", type=str, default=NEIGHBORS_DEFAULT, nargs="*",
			help="addresses (host:port) of neighbour nodes")
	
	#argument for joining, expected value should be along the lines of node:port
	parser.add_argument("-j", "--join", type=str, default=JOIN_DEFAULT, nargs="*",
			help="node:port to join, default %s" % JOIN_DEFAULT)
	
	#argumnet to know whether we are running on cluster or not
	parser.add_argument("-c", "--cluster", type=bool, default=False,
			help="node:port to join, default True")

	return parser

def run_server(args):
	global server
	global neighbors
	global request_buffer

	neighbors = args.neighbors

	server = ThreadingHttpServer(('', args.port), NodeHttpHandler)
	server.innit_(args)

	def server_main():
		print("Starting server on port {}. Neighbors: {}".format(args.port, args.neighbors))
		server.serve_forever()
		print("Server has shut down")

	def shutdown_server_on_signal(signum, frame):
		print("We get signal (%s). Asking server to shut down" % signum)
		server.shutdown()

	# Start server in a new thread, because server HTTPServer.serve_forever()
	# and HTTPServer.shutdown() must be called from separate threads
	thread = threading.Thread(target=server_main)
	thread.daemon = True
	thread.start()

	# Shut down on kill (SIGTERM) and Ctrl-C (SIGINT)
	signal.signal(signal.SIGTERM, shutdown_server_on_signal)
	signal.signal(signal.SIGINT, shutdown_server_on_signal)

	thread.join(args.die_after_seconds)
	if thread.is_alive():
		print("Reached %.3f second timeout. Asking server to shut down" % args.die_after_seconds)
		server.shutdown()

	print("Exited cleanly")

if __name__ == "__main__":

	parser = arg_parser()
	args = parser.parse_args()
	run_server(args)
