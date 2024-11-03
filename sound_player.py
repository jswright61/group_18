import pygame as pg

class SoundPlayer:
  def __init__(self, initial_volume = 0.6):
    pg.mixer.init()
    self.click = pg.mixer.Sound("click.wav")
    self.restart = pg.mixer.Sound("restart.wav")
    self.high_score = pg.mixer.Sound("high_score.wav")
    self.win = pg.mixer.Sound("win.wav")
    self.time_expired = pg.mixer.Sound("timeout.wav")
    pg.mixer.music.load("background_music.wav")
    pg.mixer.music.set_volume(initial_volume)  # Adjust volume

  def bg_start(self):
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
    pg.mixer.music.set_volume(0)

  def volume_up(self):
    volume = pg.mixer.music.get_volume()
    if volume < 1.0:
      volume += 0.1
      pg.mixer.music.set_volume(min([1.0, volume]))

  def volume_down(self):
    volume = pg.mixer.music.get_volume()
    if volume > 0.0:
      volume -= 0.1
      pg.mixer.music.set_volume(max([0.0, volume]))
