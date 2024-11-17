import pygame as pg, pdb
from lib.colors import *

class CenteredText:
  def __init__(self, text_lines, width, font_size = 20, font_name = None, vertical_gutter = 10):
    font = pg.font.Font(font_name, font_size)
    self.lines = []
    y_offset = 0
    for txt_ln in text_lines:
      y_offset += vertical_gutter
      surf = font.render(txt_ln[0], True, txt_ln[1])
      rect = surf.get_rect()
      x_offset = max([(width - rect.width) // 2, 0])
      self.lines.append([surf, x_offset, y_offset])
      y_offset += rect.height

  def render(self, draw_suface, start_x, start_y):
    for ln in self.lines:
      draw_suface.blit(ln[0], (ln[1] + start_x, ln[2] + start_y))
