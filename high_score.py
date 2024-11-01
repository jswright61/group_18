class HighScore:
  def __init__(self, f_name = "high_score.txt"):
    self.f_name = f_name

  def high_score(self):
    if self.high_score is not None:
      return self.high_score
    else:
      try:
        f = open(self.f_name, "r")
        self.high_score = int(f.read())
        f.close()
      except (FileNotFoundError, ValueError) as e:
        # if the file doesn't exist, or it's contents cannot be cast to an int, just set hs = 0
        self.high_score = 0
    return self.high_score

  def check_high_score(self, cur_score):
    new_hs = False
    if cur_score > self.high_score():
      self.high_score = cur_score
      self.write_high_score()
      verb = "beat"
      color = (0, 255, 0) # green
      new_hs = True
    elif cur_score == self.high_score:
      verb = "tied"
      color = (255, 255, 0) #yellow
    else:
      verb = "failed to beat"
      color = (255, 0, 0) # red
    return [self.high_score, verb, color, new_hs]

  def write_high_score(self):
    f = open(self.f_name, "w")
    f.write(str(self.high_score))
    f.close()
