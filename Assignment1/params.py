class Parameters:
  """All the required parameters"""
  num_peers = 10    # total number of peers
  z = 0.5           # percent of slow nodes
  txn_gen_mean = 5  # transaction generation time mean
  txn_gen_var = 5   # transaction generation time variance
  start_balance = 100 

  # Latency parameters
  p_min = 0.01
  p_max = 0.50
  m = 8 * (10**6)
  c_high = 100 * (10**6)
  c_low = 5 * (10**6)
  d = 96 * (10**3)