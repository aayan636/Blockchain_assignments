from params import Parameters

from copy import deepcopy

import threading
import thread
import time

class BlockChain:
	""" Defines a chain of blocks """
	
  def __init__(self, gen_block, tk, receiver_func_ptr):
    self._all_blocks = {gen_block.id : gen_block}
    self._all_leaves = set() # set of all block ids.
    self._all_leaves.add(gen_block.id)
    self._current_chain_last_block = gen_block.id
    self._tk = tk
    self._lock = threading.Lock(blocking = False)
    self._receiver_func_ptr = receiver_func_ptr
    self._foreign_node_added = False

    self._current_transactions = dict()

  def update_balance(self, balances, block):
    # TODO : We need to also check double transactions (t.id)
    curr_balance = deepcopy(balances)
    for t in block.transactions.values():
      curr_balance[t.id_x] -= t.amount
      curr_balance[t.id_y] += t.amount
      if curr_balance[t.id_x] < 0:
        return (False, balances)
    return (True, curr_balance)

  def add_block(self, block):
    # This lock competes with add_block and solve_problem
    if self._lock.acquire() == True:
      # check if prev blk of block is main chain or not
      if block.previous not in self._all_blocks:
        print "Error : received ablock whose previous is not available in this peer."
        self._lock.release()
        return False

      self._foreign_node_added = True
      
      self._all_blocks[block.id] = block
      # update leaves :
      if block.previous in self._all_leaves:
        self._all_leaves.remove(block.previous)
      self._all_leaves.add(block.id)

      # update main chain:
      if block.length > self._all_blocks[self._current_chain_last_block].length:
        self._current_chain_last_block = block.id

      self._lock.release()
      return True
    else:
      return False

  def add_transaction(self, t):
    if t.id in self._current_transactions:
      return False
    self._current_transactions[t.id] = t
    if len(self._current_transactions) >= Parameters.txn_per_block:
      thread.start_new_thread(self.solve_problem, ())
    return True

  def solve_problem(self):
    time.sleep(self._tk)
    if self._lock.acquire() == True:
      if self._foreign_node_added == False:
        self._receiver_func_ptr(generate_block())
        self._lock.release()
      else:
        # UDAO EVERYTHING?
        pass
    else:
      # ERASE ANYTHING??? KOI AUR BLOCK AA KE BAITH GAYA
      pass

  def generate_block(self):
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

    self._current_transactions.clear()
    new_block = Block(prev_block.id, prev_block.length, new_balances, new_txns, new_all_txns)

    self._all_blocks[new_block.id] = new_block

    self._all_leaves.remove(self._current_chain_last_block)
    self._all_leaves.add(new_block.id)
    
    self._current_chain_last_block = new_block.id
    return new_block

# for testing
if __name__ == '__main__':
  print "x"