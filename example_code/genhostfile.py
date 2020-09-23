import numpy as np
import uuid 
import hashlib
import sys

def mergeSort(arr): 
	"""mergesort from geeksforgeeks"""
	if len(arr) >1: 
		mid = len(arr)//2 
		L = arr[:mid] 
		R = arr[mid:] 

		mergeSort(L)
		mergeSort(R) 

		i = j = k = 0
		while i < len(L) and j < len(R): 
			if int(L[i].split(":")[0]) < int(R[j].split(":")[0]): 
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

def make_names_to_array(filename):
	node_names = np.genfromtxt(filename, dtype=str, delimiter="\n")
	return node_names

def hash_each(nodes, m):
	hashes = []

	for i in range(len(nodes)):
		a = hashlib.sha1()
		a.update(nodes[i].encode('utf-8'))
		b = a.hexdigest()
		
		b = str(int(b, 16) % m)
		c = nodes[i]

		hashes.append(b + ":" + nodes[i])
		
	return hashes

def remove_duplicates(nodes, size):
	done = False
	
	i = 0
	j = 0	

	while(i < size):
		j = 0	
		while(j < size):
			if(i >= size):
				i = 0
			if i == j:
				j += 1
				continue
			print(i, j)
			a = int(nodes[i].split(":")[0])
			b = int(nodes[j].split(":")[0])
 
			if a == b:
				nodes.pop(j)
				size -= 1
				print("size:", size)
	
			j += 1
		i += 1

	return nodes

def make_pretty(nodes):	
	sorted_pretty = mergeSort(nodes.copy())

	for i in range(len(nodes)):
		nodes[i] = nodes[i].split(":")[1]
		sorted_pretty[i] = sorted_pretty[i].split(":")[1]

	return sorted_pretty, nodes

def write_to_file(filename, nodes):

	f = open(filename, "w")

	for i in range(len(nodes)):
		f.write(nodes[i])
		f.write("\n")
	
	f.close()

def run(args):
	try:
		if np.ceil(np.log2(args)) != np.floor(np.log2(args)):
			print("number must be a power of two!")
			quit()
	except:
		print("number must be a power of two!")
		quit()

	nodes = make_names_to_array("compute.txt")

	hash_nodes = hash_each(nodes, args)

	no_duplicate = remove_duplicates(hash_nodes, len(nodes))

	sorted_result, random_result = make_pretty(no_duplicate)

	write_to_file("hostfile-sorted.txt", sorted_result)
	write_to_file("hostfile-random.txt", random_result)


run(int(sys.argv[1]))






