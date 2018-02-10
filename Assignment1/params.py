class Parameters:
  """All the required parameters"""
  num_peers = 6    # total number of peers
  z = 0.5           # percent of slow nodes
  txn_gen_mean = 1  # transaction generation time mean
  start_balance = 100 

  # Temporary
  num_neighbours = 3

  # Latency parameters
  p_min = 0.01
  p_max = 0.50
  m = 8 * (10**6)
  c_high = 100 * (10**6)
  c_low = 5 * (10**6)
  d = 96 * (10**3)