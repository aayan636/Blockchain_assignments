import threading
import time
#
import numpy as np
#
from params import Parameters

class Peer (threading.Thread):
  """Peer class"""
  # pid
  # is_slow
  # gen_transaction()
  
  def __init__(self, pid, is_slow):
    threading.Thread.__init__(self)
    self.pid = pid
    self.is_slow = is_slow

  def gen_transaction(self):
    while True:
      waiting_time = np.random.exponential(Parameters.transaction_generation_mean_time)
      time.sleep(waiting_time)
      print "Txn generated ", self.pid

  def run(self):
    print "Starting Peer ", self.pid
    self.gen_transaction()
    print "Exiting Peer ", self.pid


# For testing
if __name__ == '__main__':
  a = Peer(1, False)
  a.start()
  b = Peer(2, False)
  b.start()
  c = Peer(3, False)
  c.start()