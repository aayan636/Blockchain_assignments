import time
import thread

class Message:
  def __init__(self, content, sender, is_block):
    self.content = content
    self.sender = sender
    self.is_block = is_block

  def send(self, receiver_func_ptr, sleep_time):
    """Send message to receiver_func_ptr"""    
    def send_fn():
      time.sleep(sleep_time)
      receiver_func_ptr(self)
    
    thread.start_new_thread(send_fn, ())


# Testing
if __name__ == '__main__':
  m1 = Message("yo", 1234)
  m1.send("", 1)
  m1.send("", 2)
  time.sleep(100)