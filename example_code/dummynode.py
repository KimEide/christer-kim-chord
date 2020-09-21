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
		if address in server.finger_table and True in server.finger_table[address]:
			full_address = server.finger_table[address][0]
			response, status = self.get_value(full_address, path, method, value)
		else:
			response, status = self.get_value(neighbors[0], path, method, value)	

		return response, status

	def extract_key_from_path(self, path):
		return re.sub(r'/storage/?(\w+)', r'\1', path)

	def get_value(self, node, path, method, content):
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
		if contenttype == "text/plain":
			value = value.decode("utf-8")
			print("-------------------------", value)
		conn.close()
		return value, resp.status

	def do_PUT(self):
		content_length = int(self.headers.get('content-length', 0))

		key = self.extract_key_from_path(self.path)
		value = self.rfile.read(content_length)

		address = int(uuid.UUID(key)) % server.M
		
		if address <= server.id and address > server.predecessor:
			object_store[key] = value

			self.send_whole_response(200, "Value stored for " + key)
		
		elif server.id < server.predecessor and self.is_bewteen(server.id, server.predecessor, address):
			object_store[key] = value

			self.send_whole_response(200, "Value stored for " + key)
		else:
			response, status = self.find_successor(address, self.path, "PUT", value)
			self.send_whole_response(200, "Value stored for " + key)
		
	
	def do_GET(self):

		if self.path.startswith("/storage"):
			key = self.extract_key_from_path(self.path)
			
			address = int(uuid.UUID(key)) % server.M
			
			if address <= server.id and address > server.predecessor or address == server.id:
				if key in object_store:
					
					self.send_whole_response(200, object_store[key])
				else:
					self.send_whole_response(404, "No object with key '%s' on this node" % key)

			elif server.id < server.predecessor and self.is_bewteen(server.id, server.predecessor, address):
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

	def is_bewteen(self, id, predecessor, address):
		gap = (server.M + id) - predecessor 
		interval = predecessor + gap 
		
		count = predecessor
		buffer = []

		while(count < interval):
			count +=1
			buffer.append((count%server.M))
					
		if address in buffer:
			return True

		return False

def arg_parser():
	PORT_DEFAULT = 8000
	DIE_AFTER_SECONDS_DEFAULT = 20 * 60
	parser = argparse.ArgumentParser(prog="node", description="DHT Node")

	parser.add_argument("-p", "--port", type=int, default=PORT_DEFAULT,
			help="port number to listen on, default %d" % PORT_DEFAULT)

	parser.add_argument("--die-after-seconds", type=float,
			default=DIE_AFTER_SECONDS_DEFAULT,
			help="kill server after so many seconds have elapsed, " +
				"in case we forget or fail to kill it, " +
				"default %d (%d minutes)" % (DIE_AFTER_SECONDS_DEFAULT, DIE_AFTER_SECONDS_DEFAULT/60))

	parser.add_argument("neighbors", type=str, nargs="*",
			help="addresses (host:port) of neighbour nodes")

	return parser

class ThreadingHttpServer(HTTPServer, socketserver.ThreadingMixIn):
	def __init__(self, *args, **kwargs):    
		super(ThreadingHttpServer, self).__init__(*args, **kwargs)
		self.finger_table = {}
		self.M = 16 #must be an exponent of two, 2, 4, 8, 16, 32, 64 
		self.predecessor = None
		self.successor = None

	def innit_(self, args):
		"""
		initializes the different "static" values that must be true based on the information of the neighbours
		the fingertable is a dictionary where node identity 0-16 maps the address of each identitie successor
		key: address: False/True:
		example:
		{2: ('localhost:8002', True)}, if you call: finger_table[2] then it would return ('localhost', True)
		"""

		self.id = int(args.port) % self.M
		self.port = args.port

		#initializing the static variables of the finger table, each finger that is between the server and its neigbhor will map to the neighbor
		#we do this so we get fingers that map to the correct successor of the node, the rest of the fingers will be fixed later, but for now we init them as false, false
		gap = self.neigbhor_interval() #number of nodes between the server and its neihbor
		interval = self.id + gap	# the highest number the nodes can map to its neighbor
		

		for i in range(int(np.log2(self.M))):
			identity = (self.id + 2**i)
			if identity <= interval:
				self.finger_table[(identity % self.M)] = neighbors[0], True
			else:
				self.finger_table[(identity % self.M)] = False, False
			
			# print("serverid: {}, interval: {}, identity: {}, finger: {}".format(self.id , interval, (identity % self.M), self.finger_table[(identity % self.M)]))
	

	def neigbhor_interval(self):
		"""
		helperfunction to initialize the fingertable correctly based on the neighbors
		calculates the number of nodes that should be mapped to the neighbor and not the 
		fingers itself. server.id is 12 and the neighbor of 12 is 2, then there should be
		6 nodes that maps to node 2, because each of those "x" nodes, would have node 2 as their successor node. 
		"""
		successor_port = (neighbors[0].split(':'))
		predecessor_port = (neighbors[1].split(':'))
		
		self.successor = (int(successor_port[1]) % self.M)
		self.predecessor = (int(predecessor_port[1]) % self.M)

		if self.successor < self.id:
			interval = (self.M + self.successor) - self.id
		else:
			interval = self.successor - self.id

		return interval

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

	# Wait on server thread, until timeout has elapsed
	#
	# Note: The timeout parameter here is also important for catching OS
	# signals, so do not remove it.
	#
	# Having a timeout to check for keeps the waiting thread active enough to
	# check for signals too. Without it, the waiting thread will block so
	# completely that it won't respond to Ctrl-C or SIGTERM. You'll only be
	# able to kill it with kill -9.
	thread.join(args.die_after_seconds)
	if thread.is_alive():
		print("Reached %.3f second timeout. Asking server to shut down" % args.die_after_seconds)
		server.shutdown()

	print("Exited cleanly")

if __name__ == "__main__":

	parser = arg_parser()
	args = parser.parse_args()
	run_server(args)
