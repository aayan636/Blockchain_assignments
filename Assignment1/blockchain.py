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
    if block.previous in self._all_blocks:
      (is_valid, new_balances) = self.update_balance(self._balances[block.previous], block)
      if not is_valid:
        print "Block not valid"
        return False
      self._all_blocks[block.id] = block
      # update leaves :
      del self._all_leaves[block.previous]
      self._all_leaves[block.id] = block
      # update balances :
      del self._balances[block.previous]
      self._balances[block.id] = new_balances
      # update main chain:
      if block.length > self._current_chain_last_block.length:
        self._current_chain_last_block = block
        self._current_balance = deepcopy(new_balances)
        self._current_transactions = ??
    else:
      print "Error : received ablock whose previous is not available in this peer."
      return False

  def add_transaction(self, t):
    if t.id in self._current_transactions:
      return False
    self._current_transactions[t.id] = t

  def generate_block(self):
    curr_balance = deepcopy(self._balances[self._current_chain_last_block])
    pass

# for testing
if __name__ == '__main__':
  print "x"