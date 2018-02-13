class Parameters:
  """All the required parameters"""
  
  num_peers = 5    # total number of peers
  z = 1.5           # fraction of slow nodes
  start_balance = 100 

  # Transaction parameters
  txn_gen_mean = 5  # transaction generation time mean
  txn_per_block = 10

  # Block prams
  block_gen_mean = 15 # Tk mean
  block_generation_fee = 50
  
  # Temporary
  num_neighbours = 2

  # Latency parameters
  p_min = 0.01
  p_max = 0.50
  m = 8.0 * (10**6)
  c_high = 100.0 * (10**6)
  c_low = 5.0 * (10**6)
  d = 96.0 * (10**3)

  # Print statements
  a = {}
  MAX = "END"
  a["P_0"] = '\033[95m'
  a["P_1"] = '\033[94m'
  a["P_2"] = '\033[93m'
  a["P_3"] = '\033[92m'
  a["P_4"] = '\033[91m'
  a["END"] = '\033[0m'