from params import Parameters
from peer import *;

class Simulator:
  """Simulator class"""
  
  def __init__(self, param):
    self.param = param
    self.nodes = [Peer(i, False) for i in xrange(Parameters.num_peers)]
    self.network_graph = self.generate_graph()

  # change to make this customisable
  def generate_graph(self):
  	a = []
  	for i in xrange(len(self.nodes)):
  		neighbours = [self.nodes[j] for j in xrange(max(i-Parameters.num_neighbours,0), i)]
  		neighbours = neighbours + [self.nodes[j] for j in xrange(i+1, min(i+Parameters.num_neighbours, Parameters.num_peers))]
  		a.append(neighbours)
  	return a

  def start_peers(self):
  	for i in self.nodes:
  		i.start()

  # debugging
  def print_network_graph(self):
  	for i in xrange(len(self.network_graph)):
  		print i
  		for j in self.network_graph[i]:
  			print j.pid, 
  		print "\n"

# For testing
if __name__ == '__main__':
  s = Simulator("blah")
  s.print_network_graph()
  s.start_peers()
