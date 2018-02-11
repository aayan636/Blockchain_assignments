from params import Parameters
from transaction import Transaction
from message import Message

import threading
import thread
import time
import random
import Queue
from collections import defaultdict

class Peer (threading.Thread):
  """Peer class"""
  
  def __init__(self, pid, get_delay):
    threading.Thread.__init__(self)
    self.pid = pid
    self.balance = Parameters.start_balance

    self._get_delay = get_delay
    self._semaphore = threading.Semaphore(0)
    self._queue = Queue.Queue()
    self._recvd_or_sent = defaultdict(set) # obj id to set of senders
    self._connected_peers_ptrs = {}
    
  def add_connected_peer(self, peer_id, receiver_func_ptr):
    self._connected_peers_ptrs[peer_id] = receiver_func_ptr
    
  def gen_transaction(self):
    i=0
    if self.pid == "P0":
      while i<1:
        i+=1
        waiting_time = random.expovariate(1.0 / Parameters.txn_gen_mean)
        time.sleep(waiting_time)
        # TODO : Set proper transaction
        t = Transaction(1,1,0)
        msg = Message(t, self.pid, False)
        self._queue.put(msg)
        self._semaphore.release()
        print "Transaction generated ", t.id, " by peer ", self.pid

  def receive_message(self, message):
    self._queue.put(message)
    self._semaphore.release()

  def process_message(self, message):
    # add to received objects
    msg_set = self._recvd_or_sent[message.content.id]
    msg_set.add(message.sender)
    new_message = Message(message.content, self.pid, message.is_block)

    print "Transaction processed", message.content.id, " by peer ", self.pid, " sent by ", message.sender
    # TODO : call add_block if its a block.
    # send to connected peers, with conditions
    for p in self._connected_peers_ptrs:
      if p not in msg_set:
        # send to this!
        msg_set.add(p)
        p_recv_ptr = self._connected_peers_ptrs[p]
        delay = self._get_delay(self.pid, p, message.is_block)
        new_message.send(p_recv_ptr, delay)

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