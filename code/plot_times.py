import numpy as np
import matplotlib.pyplot as plt 

def import_and_plot(filename):
    arr = np.genfromtxt(filename, delimiter=",", dtype=float, comments="#")
    
    t_put = []

    tries = np.delete(arr, [1,2,3,4], 1)
    nodes = np.delete(arr, [0,2,3,4], 1)
    simple = np.delete(arr, [0,1,3,4], 1)
    diff = np.delete(arr, [0,1,2,4], 1 )
    nonexistant = np.delete(arr, [0,1,2,3], 1)

    for i in range(len(simple)):
        t_put.append(tries[i] / ((simple[i]+diff[i])/2))

    plt.figure(1)
    plt.plot(nodes, simple, label="simple")
    plt.plot(nodes, diff, label="diff")
    plt.xlabel('Number of nodes')
    plt.ylabel('Time To Handle 1000 requests in seconds')
    
    plt.figure(2)
    plt.plot(nodes, t_put, label="Average Troughput")
    plt.xlabel('Number of nodes')
    plt.ylabel('Request Handled Per Second')
    
times = import_and_plot("times.txt")

#do_plot(times)
plt.legend(loc='center right')
	

plt.show()