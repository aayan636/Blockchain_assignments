class Parameters:
  """All the required parameters"""
  num_peers = 3    # total number of peers
  z = 1.5           # fraction of slow nodes

  txn_gen_mean = 1  # transaction generation time mean
  
  start_balance = 100 
  block_generation_fee = 50
  
  # Block generation params :
  block_gen_mean = 1 # Tk mean
  
  # Temporary
  num_neighbours = 2

  # Latency parameters
  p_min = 0.01
  p_max = 0.50
  m = 8.0 * (10**6)
  c_high = 100.0 * (10**6)
  c_low = 5.0 * (10**6)
  d = 96.0 * (10**3)