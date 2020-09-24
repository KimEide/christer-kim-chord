import hashlib

def id_from_name(name, m):
	return hash_name(name) % m

def hash_name(name):
	m = hashlib.sha1()
	m.update(name.encode('utf-8'))
	return int(m.hexdigest(), 16)

def print_all():
	for i in range(64):
		print("port{}, hash{}".format(8000+i, id_from_name("localhost:"+str(8000+i), 16)))

def find_placement(all_neighbors, id,  M):
	size = len(all_neighbors)
	if size == 1:
		return all_neighbors[0], all_neighbors[0]
	elif size >= 2:
		for i in range(len(all_neighbors)):
			a = id_from_name(all_neighbors[i], M)
			b = id
			c = id_from_name(all_neighbors[(i+1)%M], M)

			if is_bewteen(a, b, c, M):
				print(a, c)
				return all_neighbors[i], all_neighbors[(i+1)%M]
	
	else:
		print("unexpected error, size < 1")
		quit()

def is_bewteen(a, b, c, m):
	buffer = []
	
	gap = (c-a)
	if gap < 0:
		c = 16+c

	while(a < c):
		a += 1
		buffer.append(a % m)
				
	if b in buffer:
		return True

	return False


# neighbors = ["localhost:8001", "localhost:8002", "localhost:8016", "localhost:8009", "localhost:8003"]

# place = find_placement(neighbors, 11, 16)

# print(place)
node1="compute-8-12"
node2="compute-6-16"
node3="compute-3-25"
node4="compute-3-10"
node5="compute-2-2"
print("node {} has hash {}".format(node1, id_from_name(node1, 16)))
print("node {} has hash {}".format(node2, id_from_name(node2, 16)))
print("node {} has hash {}".format(node3, id_from_name(node3, 16)))
print("node {} has hash {}".format(node4, id_from_name(node4, 16)))
print("node {} has hash {}".format(node5, id_from_name(node5, 16)))


