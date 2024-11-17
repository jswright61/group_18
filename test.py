# Class: CSE 1321
# Section: W02
# Term: Fall 2024
# Instructor: Nick Murphy
# Group 18
# Members: Ernie Fichtel, Sequoya Jackson, Oneeb Khan, Jonathan Parson, Scott Wright
# Group Project



import pygame as pg, sys, random, pdb
from lib.colors import *
from lib.timer import Timer
from lib.high_score import HighScore
from lib.board import Board
from lib.sound_player import SoundPlayer
from lib.button import Button
from lib.text_writer import TextWriter
from pygame.locals import *
import os.path




pg.init()
pg.display.set_caption("testing")
tile_font = pg.font.Font(None, 32)
board = Board(98, tile_font)
# screen size = (302, 332) with 98 size tile
resolution = board.screen_size
screen = pg.display.set_mode(resolution)
screen.fill(color = BLACK)

def process_special_keys(key, modifiers, timer):
  if key == pg.K_ESCAPE:
    sys.exit(0)
  # if key == pg.K_u:
  #   sound_player.volume_up()
  # if key == pg.K_d:
  #   sound_player.volume_down()
  # if key == pg.K_m and modifiers & pg.KMOD_CTRL:
  #   # m plus CTRL key
  #   sound_player.mute()
  # if "cheat" in cl_args and key == pg.K_c and modifiers & pg.KMOD_CTRL:
  #   # c plus CTRL only in cheat mode
  #     board.cheat()
  # if "cheat" in cl_args and key == pg.K_e and modifiers & pg.KMOD_CTRL:
  #   # e plus CTRL only in cheat mode
  #   timer.reset(allowed_secs - 5)
  # if "debug" in cl_args and key == pg.K_p:
    # breakpoint()

def show_screen():
  while True:
    for event in pg.event.get():
      if event.type == QUIT:
        sys.exit(0)
      if event.type == pg.MOUSEBUTTONDOWN:
        click_pos = pg.mouse.get_pos()
        print(click_pos)
        # print(bb.was_clicked(click_pos))
        pg.event.clear()
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_p:
          screen.fill(BLACK)
          breakpoint()
          pg.display.flip()
    clock.tick(60)

clock = pg.time.Clock()
lines = [["now is the time", RED], ["for all good men", WHITE], ["To come to the aid", MED_GRAY], ["Of his country", WHITE]]
c_text = TextWriter(lines, 302, font_size = 20, font_name = None, vertical_gutter = 10)

show_screen()

# Game Over