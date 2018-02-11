from params import Parameters

class BlockChain:
	""" Defines a chain of blocks """
	
  def __init__(self, gen_block):
		init_balance = dict()
    for i in range(Parameters.num_peers):
      pid = "P_" + str(i)
      init_balance[pid] = Parameters.start_balance

    self.all_blocks = {gen_block.id : gen_block}
    self.all_leaf = {gen_block.id : gen_block}
    self.current_chain_last_block = gen_block
    self.balances = {gen_block.id : init_balance}

  def update_balance(self, balances, block):

  def add_block(self, block):
    # check if prev blk of block is main chain or not
    if block.previous == self.current_chain_last_block.id:
