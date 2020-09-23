import argparse

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


parser = arg_parser()
args = parser.parse_args()
print(args)