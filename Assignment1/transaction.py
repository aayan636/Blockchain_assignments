import threading

class Transaction:
  """Details of the transaction"""
  
  # Static variables
  _id = 0
  _lock = threading.Lock()
  
  def __init__(self, id_x, id_y, amount):
    Transaction._lock.acquire()
    Transaction._id += 1
    self.id = "T_"+str(Transaction._id)
    Transaction._lock.release()
    
    self.id_x = id_x
    self.id_y = id_y
    self.amount = amount


# For testing
if __name__ == '__main__':
  a = Transaction(0, 0, 0)
  b = Transaction(0, 0, 1)
  c = Transaction(0, 0, 2)
  print a.id
  print b.id
  print c.id
  print Transaction.id