from params import Parameters

from copy import deepcopy

class BlockChain:
	""" Defines a chain of blocks """
	
  def __init__(self, gen_block):
		init_balance = dict()
    for i in range(Parameters.num_peers):
      pid = "P_" + str(i)
      init_balance[pid] = Parameters.start_balance

    self._all_blocks = {gen_block.id : gen_block}
    self._all_leaves = {gen_block.id : gen_block}
    self._current_chain_last_block = gen_block.id
    self._balances = {gen_block.id : deepcopy(init_balance)}
    
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
    # check if prev blk of block is main chain or not
    if block.previous == self.current_chain_last_block.id:

  def add_transaction(self, t):
    if t.id in self._current_transactions:
      return False
    self._current_transactions[t.id] = t

  def generate_block(self):
    curr_balance = deepcopy(self._balances[self._current_chain_last_block])
    
    pass

# for testing
if __name__ == '__main__':
  