class Block:
""" Details of a block, stores a dictionary of all txns """
	id = 0
	def __init__(self, previous_blk_id, previous_blk_len, ):
    init_balance = dict()
    for i in range(Parameters.num_peers):
      pid = "P_" + str(i)
      init_balance[pid] = Parameters.start_balance
		Block.id += 1
		self.id = "B_" + str(Block.id)
    self.previous = previous_blk_id
    self.length = previous_blk_len + 1
    self.transactions = dict()    
    self.balances = init_balance
    self.all_transactions = dict()

  def add_transaction(self, t):
    if t.id not in self.transactions:
      self.transactions[t.id] = t

  def is_txn_present(self, tid):
    return (tid in self.transactions)