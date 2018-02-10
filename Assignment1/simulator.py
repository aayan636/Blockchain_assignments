from params import Parameters
from peer import Peer;

class Simulator:
  """Simulator class"""
  
  def __init__(self, param):
    self.param = param
    self.nodes = [Peer("P" + str(i), False) for i in xrange(Parameters.num_peers)]
    self.network_graph = self.generate_graph()
    self.assign_neighbours()

  # change to make this customisable
  def generate_graph(self):
  	a = {}
  	for i in xrange(len(self.nodes)):
  		neighbours = [self.nodes[j] for j in xrange(max(i-Parameters.num_neighbours,0), i)]
  		neighbours = neighbours + [self.nodes[j] for j in xrange(i+1, min(1+i+Parameters.num_neighbours, Parameters.num_peers))]
  		a["P" + str(i)] = neighbours
  	return a

  def assign_neighbours(self):
  	for i in xrange(len(self.nodes)):
  		cur_neighbours = self.network_graph["P" + str(i)]
  		for j in cur_neighbours:
  			self.nodes[i].add_connected_peer(j.pid, j, j.receive_message)

  def start_peers(self):
  	for i in self.nodes:
  		i.start()

  # debugging
  def print_network_graph(self):
  	for i in xrange(len(self.network_graph)):
  		print i
  		for j in self.network_graph["P" + str(i)]:
  			print j.pid, 
  		print "\n"

# For testing
if __name__ == '__main__':
  s = Simulator("blah")
  s.print_network_graph()
  s.start_peers()
