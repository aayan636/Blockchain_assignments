from simulator import Simulator
import signal, os
import time

_copies_written = 0
s = Simulator()

def start_simulation():
	global s
	s.start_peers()
	time.sleep(10)
	while True:
		s.showtree()

def handler(signum, frame):
	global _copies_written, s
	_copies_written += 1
	for peer in s.nodes:
		text_file = open("outputs/Output_" + str(_copies_written) + "_" + peer.pid + ".txt", "w")
		text_file.write(peer.write_to_file())
		text_file.close()
	print "SNAPSHOTTED COPY " + str(_copies_written)


def main():
	signal.signal(signal.SIGQUIT, handler)
	start_simulation()

if __name__ == '__main__':
	main()