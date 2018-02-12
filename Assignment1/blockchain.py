from params import Parameters
from block import Block

import threading
import time
from copy import deepcopy
from collections import defaultdict

class BlockChain:
  """ Defines a chain of blocks """
  def __init__(self, gen_block, pid):
    self._pid = pid
    self._all_blocks = {gen_block.id : gen_block}
    self._all_blocks_times = {gen_block.id : time.time()}
    self._all_leaves = set() # set of all block ids.
    self._all_leaves.add(gen_block.id)

    # peer's longest chain :
    self._current_chain_last_block = gen_block.id
    
    # current, local txns set
    self._current_transactions = dict()
    self._current_changes = 0

    # Orphaned blocks previous index -> set of blocks
    self._orphaned_blocks = defaultdict(set)

    self._lock = threading.Lock()

  def add_block(self, block):
    if block.id in self._all_blocks:
      print "Error : Block id {} received multiple times".format(block.id)
      return False

    # check if prev blk of block is main chain or not
    if block.previous not in self._all_blocks:
      self._orphaned_blocks[block.previous].add(block)
      print "Semi Error : Block id {} previous not in peer".format(block.id)
      return True

    self._lock.acquire()
    self._all_blocks[block.id] = block
    self._all_blocks_times[block.id] = time.time()
    # update leaves
    if block.previous in self._all_leaves:
      self._all_leaves.remove(block.previous)
    self._all_leaves.add(block.id)

    # update main chain:
    if block.length > self._all_blocks[self._current_chain_last_block].length:
      self._current_chain_last_block = block.id

    for b in self._orphaned_blocks[block.id]:
      self._lock.release()
      self.add_block(b)
      self._lock.acquire()

    self._orphaned_blocks[block.id].clear()

    self._lock.release()
    return True

  def add_transaction(self, t):
    if t.id in self._current_transactions:
      return False
    self._lock.acquire()
    self._current_transactions[t.id] = t
    self._lock.release()
    return True

  def get_current_balance(self):
    # might be invalid due to no lock, but fine with generating invalid txns.
    curr_block = self._all_blocks[self._current_chain_last_block]
    # current block balance
    curr_balance = curr_block.balances[self._pid]
    # add all valid current txns
    for txn in self._current_transactions.values():
      if txn.id in curr_block.all_transactions:
        continue
      if txn.id_x == self._pid:
        if curr_balance < txn.amount:
          continue
        curr_balance -= txn.amount
    return curr_balance

  def generate_block(self):
    self._lock.acquire()
    prev_block = self._all_blocks[self._current_chain_last_block]
    prev_all_txns = prev_block.all_transactions
    prev_balances = prev_block.balances

    new_all_txns = deepcopy(prev_all_txns)
    new_txns = dict()
    new_balances = deepcopy(prev_balances)
    for txn in self._current_transactions.values():
      if txn.id in prev_all_txns:
        continue
      if new_balances[txn.id_x] < txn.amount:
        continue
      new_balances[txn.id_x] -= txn.amount
      new_balances[txn.id_y] += txn.amount
      new_all_txns[txn.id] = txn
      new_txns[txn.id] = txn

    new_balances[self._pid] += Parameters.block_generation_fee

    self._current_transactions.clear()
    new_block = Block(prev_block.id, prev_block.length, new_balances, new_txns, new_all_txns)
    # this block will be added to the peer's block tree when its added to queue, and add_block is called by peer class.
    # self._all_blocks[new_block.id] = new_block
    # self._all_blocks_times[new_block.id] = time.time()
    # self._all_leaves.remove(self._current_chain_last_block)
    # self._all_leaves.add(new_block.id)
    # self._current_chain_last_block = new_block.id
    self._lock.release()
    return new_block

  def write_to_file(self):
    write_str = ""
    for block_id in self._all_blocks.keys():
      write_str += "Block id : " + block_id + ", Previous Ptr : " + self._all_blocks[block_id].previous + ", Time added to tree : " + str(self._all_blocks_times[block_id] - self._all_blocks_times["B_1"]) + "\n"
    return write_str

# for testing
if __name__ == '__main__':
  print "x"