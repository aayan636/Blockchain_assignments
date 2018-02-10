from params import Parameters
from transaction import Transaction
from message import Message

import threading
import thread
import time
import numpy as np
import Queue
from collections import defaultdict

class Peer (threading.Thread):
  """Peer class"""
  
  def __init__(self, pid, is_slow):
    threading.Thread.__init__(self)
    self.pid = pid
    # TODO : Required is_slow?
    self.is_slow = is_slow
    self.balance = Parameters.start_balance

    self._semaphore = threading.Semaphore(0)
    self._queue = Queue.Queue()
    self._received_objs = defaultdict(set) # obj id to set of senders
    self._connected_peers_ptrs = {}
    self._connected_peers = {}
    
  def add_connected_peer(self, peer_id, peer_obj, receiver_func_ptr):
    self._connected_peers_ptrs[peer_id] = receiver_func_ptr
    self._connected_peers[peer_id] = peer_obj
    
  def gen_transaction(self):
    i=0
    while i<1:
      i+=1
      waiting_time = np.random.exponential(Parameters.txn_gen_mean)
      time.sleep(waiting_time)
      # TODO : Set proper transaction
      t = Transaction(1,1,0)
      msg = Message(t, self.pid, False)
      self._queue.put(msg)
      self._semaphore.release()
      print "Transaction generated ", t.id, " by peer ", self.pid

  def receive_message(self, message):
    # TODO : Add received message to _received_objs
    self._queue.put(message)
    self._semaphore.release()

  def get_delay(self, is_slow, is_block):
    # TODO. based on slow, fast type of self, receiver & on message content type
    return 5

  def process_message(self, message):
    # add to received objects
    msg_set = self._received_objs[message.content.id]
    msg_set.add(message.sender)                       # IS THIS A GOOD IDEA ? (JUST ONE MESSAGE OBJECT)

    print "Transaction processed", message.content.id, " by peer ", self.pid

    # send to connected peers, with conditions
    for p in self._connected_peers_ptrs:
      if p not in msg_set:
        # send to this!
        p_recv_ptr = self._connected_peers_ptrs[p]
        p_is_slow = self.is_slow and self._connected_peers[p].is_slow
        delay = self.get_delay(p_is_slow, message.is_block)
        message.send(p_recv_ptr, delay)

  def run(self):
    print "Starting Peer ", self.pid
    thread.start_new_thread(self.gen_transaction, ())
    while True:
      self._semaphore.acquire()
      self.process_message(self._queue.get())


# For testing
if __name__ == '__main__':
  a = Peer(1, False)
  a.start()
  time.sleep(100)