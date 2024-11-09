import pygame as pg

class SoundPlayer:
  def __init__(self, volume = 0.4, start_muted = False):
    pg.mixer.init()
    self.click = pg.mixer.Sound("click.wav")
    self.restart = pg.mixer.Sound("restart.wav")
    self.high_score = pg.mixer.Sound("high_score.wav")
    self.win = pg.mixer.Sound("win.wav")
    self.time_expired = pg.mixer.Sound("timeout.wav")
    self.vol_level = volume
    self.muted = start_muted
    pg.mixer.music.load("background_music.wav")
    pg.mixer.music.set_volume(self.vol_level)

  def bg_start(self):
    if not self.muted:
      pg.mixer.music.play(-1)

  def bg_stop(self):
    pg.mixer.music.stop()

  def play(self, sound_name):
    match sound_name.lower():
      case "click":
        self.click.play()
      case "restart":
        self.restart.play()
      case "restart":
        self.high_score.play()
      case "win":
        self.win.play()
      case "time_expired":
        self.time_expired.play()
      case "_":
        print(f"{sound_name} is not a valid sound")

  def mute(self):
    if self.muted:
      if self.vol_level < 0.1:
        self.vol_level = 0.1
        pg.mixer.music.set_volume(self.vol_level)
      pg.mixer.music.play(-1)
    else:
      pg.mixer.music.stop()
    self.muted = not self.muted

  def volume_up(self):
    if self.muted:
      # just unmute if volume was muted and up volume is pressed
      self.mute()
      return
    self.vol_level = min([1.0, self.vol_level + 0.1])
    pg.mixer.music.set_volume(self.vol_level)

  def volume_down(self):
    if self.muted:
      # we're not going to adjust volume when sound is muted
      return
    self.vol_level = max([0.0, self.vol_level - 0.1])
    pg.mixer.music.set_volume(self.vol_level)
