import pygame as pg
from lib.colors import *

class Button:
  def __init__(self, text, font_size, font_name = None, font_color = BLACK, origin = (0, 0), width = -1,
               pad = (10, 2), bg_color = RED):
    self.bg_color = bg_color
    self.font = pg.font.Font(font_name, font_size)
    self.surf = self.font.render(text, True, font_color)
    self.font_rect = self.surf.get_rect()
    self.create_rect(width, pad, origin)
    # print(f"{text} font_rect {self.font_rect.width} x {self.font_rect.height}")
    # print(f"{text} font_rect {self.rect.width} x {self.rect.height}")

  def render(self, draw_surface):
    pg.draw.rect(draw_surface, self.bg_color, self.rect)
    draw_surface.blit(self.surf, (self.rect.x + self.offset_x, self.rect.y + self.offset_y))

  def set_origin(self, origin):
    self.rect.update(origin, (self.rect.width, self.rect.height))

  def was_clicked(self, click_pos):
    return self.rect.collidepoint(click_pos)

  def create_rect(self, width, pad, origin):
    self.offset_y = pad[1]
    if width == -1:
      self.offset_x = pad[0]
    else:
      self.offset_x = max([0, (width - self.font_rect.width) // 2])
    self.rect = pg.Rect(origin[0],
                          origin[1],
                          width,
                          self.font_rect.height + 2 * self.offset_y)