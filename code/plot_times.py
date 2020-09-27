import numpy as np
import matplotlib.pyplot as plt 

def import_and_plot(filename):
    arr = np.genfromtxt(filename, delimiter=",", dtype=float, comments="#")
    
    tries = np.delete(arr, [1,2,3,4], 1)
    nodes = np.delete(arr, [0,2,3,4], 1)
    simple = np.delete(arr, [0,1,3,4], 1)
    diff = np.delete(arr, [0,1,2,4], 1 )
    nonexistant = np.delete(arr, [0,1,2,3], 1)

    plt.plot(nodes, simple, label="simple")
    plt.plot(nodes, diff, label="diff")
    plt.plot(nodes, nonexistant, label="nonexistant")

times = import_and_plot("times.txt")

#do_plot(times)
plt.legend(loc='center right')
	
plt.xlabel('Number of nodes')
plt.ylabel('Time To Handle 1000 requests in seconds')

plt.show()