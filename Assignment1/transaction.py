class Transaction:
  """Details of the transaction"""
  
  # Static tid
  tid = 0
  def __init__(self, id_x, id_y, amount):
    Transaction.tid += 1
    self.id_x = id_x
    self.id_y = id_y
    self.amount = amount
    self.tid = Transaction.tid


# For testing
if __name__ == '__main__':
  a = Transaction(0, 0, 0)
  b = Transaction(0, 0, 1)
  c = Transaction(0, 0, 2)
  print a.tid
  print b.tid
  print c.tid
  print Transaction.tid