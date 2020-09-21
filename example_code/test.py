def is_bewteen(id, predecessor, address):
		gap = (16 + id) - predecessor 
		interval = predecessor + gap 
		
		count = predecessor
		buffer = []

		while(count < interval):
			count +=1
			buffer.append((count%16))
					
		if address in buffer:
			return True

		return False 

print(is_bewteen(2, 12, 0))
print(is_bewteen(2, 12, 2))
print(is_bewteen(2, 12, 15))
print(is_bewteen(2, 12, 12))
print(is_bewteen(2, 12, 3))




