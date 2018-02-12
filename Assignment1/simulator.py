from params import Parameters
from peer import Peer
from block import Block

import random, threading

class Simulator:
  """Simulator class"""
  
  def __init__(self):
    init_balances = {}
    for i in xrange(Parameters.num_peers):
      init_balances["P_" + str(i)] = Parameters.start_balance

    self.gen_block = Block("B_-1", 0, init_balances, {}, {})
    self.nodes = [Peer("P_" + str(i), self.get_delay, self.gen_block) for i in xrange(Parameters.num_peers)]
    self.node_is_slow = dict()
    self.network_graph = self.generate_graph()
    self.assign_neighbours()
    for i in xrange(Parameters.num_peers):
      pid = "P_" + str(i)
      self.node_is_slow[pid] = (random.random() < Parameters.z)
    # testing str of peers.
    t = threading.Timer(5, self.nodes[0].write_to_file) 
    t.start()
    # print "Testing nodes' get_delay ", self.nodes[0]._get_delay("P_0", "P_1", False)

  # change to make this customisable
  def generate_graph(self):
    temp_graph = [[] for i in xrange(Parameters.num_peers)]
    unconnected = set([i for i in xrange(Parameters.num_peers)])
    while len(unconnected) > 1:
    	node1 = random.sample(unconnected, 1)[0]
    	unconnected.remove(node1)
    	node2 = random.sample(unconnected, 1)[0]
    	temp_graph[node2].append(self.nodes[node1])
    	temp_graph[node1].append(self.nodes[node2])
    unconnected = set([i for i in xrange(Parameters.num_peers)])
    i = 0
    for i in xrange(Parameters.num_peers*(Parameters.num_neighbours/2-1)):
    	a = random.sample(unconnected, 1)[0]
    	b = random.sample(unconnected, 1)[0]
    	while b == a:
    		b = random.sample(unconnected, 1)[0]
    	temp_graph[a].append(self.nodes[b])
    	temp_graph[b].append(self.nodes[a])
    graph = {}
    for i in xrange(len(self.nodes)):
      graph["P_" + str(i)] = list(set(temp_graph[i]))
    return graph

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
    print "Printing network graph : "
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
