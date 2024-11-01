import time
class Timer:
  def __init__(self):
    self.start_time = time.time()

  def elapsed(self, compare_time = None, milliseconds = False):
    compare_time = compare_time or time.time()
    elapsed = compare_time - self.start_time
    if milliseconds:
      return int(elapsed * 1000)
    else:
      return int(elapsed)

  def reset(self, offset = 0):
    self.start_time = time.time() - offset
