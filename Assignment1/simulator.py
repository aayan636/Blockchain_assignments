from params import Parameters
from peer import Peer

import random

class Simulator:
  """Simulator class"""
  
  def __init__(self):
    self.nodes = [Peer("P_" + str(i), self.get_delay) for i in xrange(Parameters.num_peers)]
    self.node_is_slow = dict()
    self.network_graph = self.generate_graph()
    self.assign_neighbours()
    for i in xrange(Parameters.num_peers):
      pid = "P_" + str(i)
      self.node_is_slow[pid] = (random.random() < Parameters.z)

  # change to make this customisable
  def generate_graph(self):
  	a = {}
  	for i in xrange(len(self.nodes)):
  		neighbours = [self.nodes[j] for j in xrange(max(i-Parameters.num_neighbours,0), i)]
  		neighbours = neighbours + [self.nodes[j] for j in xrange(i+1, min(1+i+Parameters.num_neighbours, Parameters.num_peers))]
  		a["P_" + str(i)] = neighbours
  	return a

  def assign_neighbours(self):
  	for i in xrange(len(self.nodes)):
  		cur_neighbours = self.network_graph["P_" + str(i)]
  		for j in cur_neighbours:
  			self.nodes[i].add_connected_peer(j.pid, j.receive_message)

  def start_peers(self):
  	for i in self.nodes:
  		i.start()

  # debugging
  def print_network_graph(self):
  	for i in xrange(len(self.network_graph)):
  		print i
  		for j in self.network_graph["P_" + str(i)]:
  			print j.pid, 
  		print "\n"

  def get_delay(self, pid1, pid2, is_block):
    is_slow = self.node_is_slow[pid1] or self.node_is_slow[pid2]
    p = random.uniform(Parameters.p_min, Parameters.p_max)
    c = Parameters.c_low if is_slow else Parameters.c_high
    m = Parameters.m if is_block else 0
    d = random.expovariate(c / Parameters.d)
    return (p + m/c + d)

# For testing
if __name__ == '__main__':
  s = Simulator()
  s.print_network_graph()
  s.start_peers()
