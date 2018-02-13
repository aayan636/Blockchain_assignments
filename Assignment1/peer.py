from params import Parameters
from message import Message
from blockchain import BlockChain
from transaction import Transaction

import time
import thread
import threading
import random
import Queue
from collections import defaultdict


class Peer (threading.Thread):
  """Peer class"""
  
  def __init__(self, pid, get_delay, gen_block):
    threading.Thread.__init__(self)
    self.pid = pid
    self._get_delay = get_delay
    self._connected_peers_ptrs = {}

    self._semaphore = threading.Semaphore(0)
    self._queue = Queue.Queue()
    self._recvd_or_sent = defaultdict(set) # obj id to set of senders

    # Block
    self._blockchain = BlockChain(gen_block, self.pid)
    self._block_timer = None
    # the random no denotes the computation power of the peer. lower the random no, higher the comp. power.
    self._block_gen_mean = Parameters.block_gen_mean * (random.uniform(0.5, 1.0))

    
  def add_connected_peer(self, peer_id, receiver_func_ptr):
    self._connected_peers_ptrs[peer_id] = receiver_func_ptr
    

  def gen_transaction(self):
    """
      Generates transactions after expovariant intervals
      Spawned as a new thread
    """
    while True:
      waiting_time = random.expovariate(1.0 / Parameters.txn_gen_mean)
      # Sleep for waiting_time
      time.sleep(waiting_time)

      # Sanity check
      if Parameters.num_peers < 1:
        print "Too few peers"
        continue
      
      # Randomly generate receiver
      self_id_int = int(self.pid[2:])
      receiver = "P_" + str(random.choice(range(0, self_id_int) + range(self_id_int+1, Parameters.num_peers)))
      
      # create txn, message
      curr_balance = self._blockchain.get_current_balance()
      amt = random.randint(0, curr_balance)
      t = Transaction(self.pid, receiver, amt)
      msg = Message(t, self.pid, False)
      
      # Put message in queue to be processes
      self._queue.put(msg)
      self._semaphore.release()
      
      #print "Transaction generated ", t.id, " by peer ", self.pid


  def _gen_block(self):
    """gen_block helper"""
    block = self._blockchain.generate_block()
    msg = Message(block, self.pid, True)
    self._queue.put(msg)
    self._semaphore.release()
    print Parameters.a[self.pid] + "Block generated ", block.id, " by peer ", self.pid, " having ", len(block.transactions), " txns" + Parameters.a[MAX]
    self.gen_block()
  

  def gen_block(self):
    """
      Generates new block at expovarient intervals
      Creates timer for calling _gen_block
      Timer object can be cancelled on receiving a new block
      _gen_block again calls this function on successfully creating block
    """
    waiting_time = random.expovariate(1.0 / (self._block_gen_mean)) # Tk
    self._block_timer = threading.Timer(waiting_time, self._gen_block)
    self._block_timer.start()


  def receive_message(self, message):
    """Every connected peer has a ptr to this function"""
    self._queue.put(message)
    self._semaphore.release()

  def process_message(self, message):
    """Process message from queue"""

    # add to received objects
    msg_set = self._recvd_or_sent[message.content.id]
    msg_set.add(message.sender)
    new_message = Message(message.content, self.pid, message.is_block)

    # print "Processing message id {} by peer {} sent by {}".format(message.content.id, self.pid, message.sender)
    # Process as per type of message
    if not message.is_block:
      self._blockchain.add_transaction(message.content)
    else:
      if self._blockchain.add_block(message.content):
        self._block_timer.cancel()
        self.gen_block()
      self._blockchain.print_longest_chain()

    # send to connected peers, with conditions
    for p in self._connected_peers_ptrs:
      if p not in msg_set:
        # send to this!
        msg_set.add(p)
        p_recv_ptr = self._connected_peers_ptrs[p]
        delay = self._get_delay(self.pid, p, message.is_block)
        new_message.send(p_recv_ptr, delay)


  def run(self):
    """Thread run"""
    print "Starting Peer ", self.pid
    thread.start_new_thread(self.gen_transaction, ())
    self.gen_block()
    # Process messages from queue
    while True:
      self._semaphore.acquire()
      self.process_message(self._queue.get())


  def write_to_file(self):
    write_string = ""
    write_string += "Peer ID : " + self.pid + "\n"
    write_string += self._blockchain.write_to_file()
    print write_string
    return write_string


  def render(self):
    postfix = "(" + self.get_postorder_string() + ")" + self.pid
    return postfix

  # Render helper
  def get_postorder_string(self):
    b_chain = self._blockchain._all_blocks.values()
    tree = {}
    for b in b_chain:
      if b.previous not in tree:
        tree[b.previous] = []
      tree[b.previous].append(b.id)
    return self.get_postorder("B_1", tree)

  # Render helper
  def get_postorder(self, cur, tree):
    sub_ans = ""
    if cur in tree.keys():
      sub_ans = "("
      for i in tree[cur]:
        sub_ans += self.get_postorder(i, tree) + ","
      sub_ans = sub_ans[:-1]
      sub_ans += (")" + cur)
    else:
      sub_ans = cur
    return sub_ans



# For testing
from block import Block
if __name__ == '__main__':
  def get_delay():
    return 5
  init_balances = {}
  for i in xrange(Parameters.num_peers):
    init_balances["P_" + str(i)] = Parameters.start_balance
  gen_block = Block(-1, 0, init_balances, {}, {}, "None")

  a = Peer("P_1", get_delay, gen_block)
  a.start()
  time.sleep(100)