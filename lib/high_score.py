class HighScore:
  def __init__(self, f_name = "high_score.txt"):
    self.f_name = f_name
    self.__high_score = None

  def high_score(self):
    if self.__high_score is not None:
      return self.__high_score
    else:
      try:
        f = open(self.f_name, "r")
        self.__high_score = int(f.read())
        f.close()
      except (FileNotFoundError, ValueError) as e:
        # if the file doesn't exist, or it's contents cannot be cast to an int, just set hs = 0
        self.__high_score = 0
    return self.__high_score

  def check_high_score(self, cur_score):
    prev_hs = self.high_score()
    if cur_score > self.high_score():
      self.write_high_score(cur_score)
      verb = "beat"
      color = (0, 255, 0) # green
    elif cur_score == self.high_score():
      verb = "tied"
      color = (255, 255, 0) #yellow
    else:
      verb = "failed to beat"
      color = (255, 0, 0) # red
    return [prev_hs, verb, color]

  def write_high_score(self, hi_score):
    f = open(self.f_name, "w")
    f.write(str(hi_score))
    f.close()
    self.__high_score = hi_score
    return hi_score
