import argparse

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


parser = arg_parser()
args = parser.parse_args()
print(args)
l = []
print(type(args.join), type(l), type(args.neighbors))