import pygame as pg, random
from lib.colors import *

class Board():
  def __init__(self, rect_width, font, border_size = 2, status_height = 30, tile_color = None, font_color = None):
    # we have nine cells, 0 - 8 which make up the board
    # 0 1 2
    # 3 4 5
    # 6 7 8
    # many of the objects in this class use lists or tuples whose indices represent the cell number from the above grid
    self.rect_width = rect_width
    self.font = font
    self.font_color = font_color or BLACK
    self.border_size = border_size
    self.status_height = status_height
    self.tile_color = tile_color or MED_GRAY
    self.screen_size = (rect_width * 3 + border_size * 4, rect_width * 3 + border_size * 4 + status_height)
    self.positions = list(range(9))
    self.shuffle_positions()
    # These control where clicks can do something
    # the index is the rect number of the blank tile
    # the element is a list of rect numbers that are adjacent to that blank tile
    self.__adjacent_rects = ((1,3), (0,2,4), (1,5), (0, 4, 6), (1, 3, 5, 7), (2, 4, 8), (3, 7), (4, 6, 8), (5, 7))
    self.__build_rects()
    self.__build_fonts()
    self.__build_font_origins()

  def __build_rects(self):
    self.rects = []
    self.surfs = []
    y_origins = (self.status_height + self.border_size,
                self.status_height + 2 * self.border_size + self.rect_width,
                self.status_height + 3 * self.border_size + 2 * self.rect_width,
                )
    x_origins = (self.border_size, 2 * self.border_size + self.rect_width, 3 * self.border_size + 2 * self.rect_width)
    for y in y_origins:
      for x in x_origins:
        r = pg.Rect(x, y, self.rect_width, self.rect_width)
        r_surf =  pg.Surface((r.w, r.h))
        r_surf.fill(color = self.tile_color)
        self.rects.append(r)
        self.surfs.append(r_surf)

  def __build_fonts(self):
    self.font_surfs = []
    for x in range(9):
      # we're never gonna use surfs[0] with "0", but it just keeps things tidy to have index = actual digit
      s = self.font.render(str(x), True, self.font_color)
      self.font_surfs.append(s)

  def __build_font_origins(self):
    if not self.rects:
      self.__build_rects()
    self.font_origins = []
    for idx in range(len(self.rects)):
      font_rect = self.font_surfs[idx].get_rect()
      self.font_origins.append( (self.rects[idx].x + (self.rects[idx].width - font_rect.width) // 2,
                           self.rects[idx].y + (self.rects[idx].height - font_rect.height) // 2,))

  def swap_with_zero(self, num):
    zero_pos = self.positions.index(0)
    num_pos = self.positions.index(num)
    self.positions[zero_pos] = num
    self.positions[num_pos] = 0

  def click(self, click_pos):
    # this method is called for every mouse click it determines whether or not a tile should be moved
    # if a tile should be moved, it is moved and a 1 is returned
    # 0 is returned if a tile is not moved
    # TODO play sound and increment moves in calling code this object just handles code
    for x in range(len(self.rects)):
      if self.rects[x].collidepoint(click_pos):
        if x in self.__adjacent_rects[self.positions.index(0)]:
          # we have a click in a cell adjacent to the blank cell
          # so swap the num in the positions list at this index with 0 in the positions list
          self.swap_with_zero(self.positions[x])
          return 1
        # we found the rect but it wasn't adjacent
        return 0
    # click was not in a monitored cell (it was in a border or in the status Rect)
    return 0

  def shuffle_positions(self):
    random.shuffle(self.positions)

  def is_game_won(self):
    # The position of the blank tile is disregarded when evaluating the tile sequence
    l = self.positions.copy()
    l.remove(0)
    for idx in range(1, len(l)):
      if l[idx -1] > l[idx]:
        return False
    return True

  def cheat(self):
    # three moves away from a win
    self.positions = [1, 2, 3, 4, 6, 8, 7, 5, 0]

  def blit(self, screen):
    for idx in range (len(self.positions)):
      if self.positions[idx] != 0:
        screen.blit(self.surfs[idx], (self.rects[idx].x, self.rects[idx].y))
        screen.blit(self.font_surfs[self.positions[idx]], self.font_origins[idx])