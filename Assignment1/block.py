import threading

class Block:
  """ Details of a block, stores a dictionary of all txns """
  _id = 0
  _lock = threading.Lock()
  _made_by = {}
  def __init__(self, previous_blk_id, previous_blk_len, balances, transactions, all_transactions, creator_pid):
    Block._lock.acquire()
    Block._id += 1
    self.id = "B_" + str(Block._id)
    self.creator_pid = creator_pid
    Block._lock.release()
    self.previous = previous_blk_id
    self.length = previous_blk_len + 1
    self.balances = balances
    self.transactions = transactions
    self.all_transactions = all_transactions
    Block._made_by[self.id] = creator_pid

from copy import deepcopy
if __name__ == '__main__':
  b = Block(1,1,1,1,1)
  b1 = b
  b2 = deepcopy(b1)
  print b.id
  print b1.id
  print b2.id
