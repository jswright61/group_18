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
from pygame.locals import *
import os.path




pg.init()
pg.display.set_caption("SlideScape")
tile_font = pg.font.Font(None, 32)
status_font = pg.font.Font(None, 32)
end_screen_font = pg.font.Font(None, 32)
inst_screen_font = pg.font.Font(None, 20)
board = Board(98, tile_font) # screen size = (302, 332) with 98 size tile
exit_button = Button("Exit", 32, origin = (206, 5), pad = (10, 1), width = 90, bg_color = RED)

cl_args = list(map(lambda x: x.lower(), sys.argv[1:]))
sound_player = SoundPlayer(0.2, "mute" in cl_args)
allowed_secs = 300

screen = pg.display.set_mode(board.screen_size)


def get_x_coord(surf, screen_width = board.screen_size[0]):
  return (screen_width - surf.get_rect().width) // 2

def should_show_instructions():
  # the presence of a file named "skip_instructions.txt" in the same directory as the game file
  # will cause the instructions screen to be skipped and gameplay will begin immediately on launch
  # to create the file, issue the following command from your teminal in the same directory where your game exists:
  # touch skip_instructions.txt
  if "show_instructions" in cl_args:
    return True
  if os.path.isfile("skip_instructions.txt") or "skip_instructions" in cl_args:
    return False
  return True

def display_instructions_screen():
  screen.fill(color = BLACK)
  start_game_button = Button("Play Game", 32, origin = (91, 285), width = 120, bg_color = GREEN)
  inst_surf_1 = inst_screen_font.render(f"Arrange the tiles in ascending order.", True, WHITE)
  inst_surf_2 = inst_screen_font.render(f"Move a tile by clicking it. Only tiles next to", True, WHITE)
  inst_surf_3 = inst_screen_font.render(f"the blank space can move. A moved tile", True, WHITE)
  inst_surf_4 = inst_screen_font.render(f"swaps places with the blank space.", True, WHITE)
  inst_surf_5 = inst_screen_font.render(f"Image below shows tiles in winning position.", True, WHITE)
  game_won_img_surf = pg.transform.scale(pg.image.load("media/tile_game.jpg").convert_alpha(), (101, 111))
  screen.blit(inst_surf_1, (get_x_coord(inst_surf_1), 20))
  screen.blit(inst_surf_2, (get_x_coord(inst_surf_2), 50))
  screen.blit(inst_surf_3, (get_x_coord(inst_surf_3), 80))
  screen.blit(inst_surf_4, (get_x_coord(inst_surf_4), 110))
  screen.blit(inst_surf_5, (get_x_coord(inst_surf_5), 140))
  screen.blit(game_won_img_surf, (101, 160))
  start_game_button.render(screen)
  pg.display.flip()
  while True:
    # This shows the screen indefinitely while processing events
    # no need to blit the screen or flip display because it's static
    # the sound is off
    for event in pg.event.get():
      if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        sys.exit(0)
      if event.type == QUIT:
        sys.exit(0)
      if event.type == pg.MOUSEBUTTONDOWN:
        click_pos = pg.mouse.get_pos()
        if start_game_button.was_clicked(click_pos):
          random.shuffle(board.positions)
          play_game()
      pg.event.clear()
    clock.tick(60)

def display_main_screen(elapsed, move_count):
  screen.fill(BLACK)
  timer_surf = status_font.render(f"{str(allowed_secs - elapsed)}", True, WHITE)
  screen.blit(timer_surf, ((302 - timer_surf.get_width()) // 2, 5))

  moves_text = status_font.render(f"Moves: {move_count}", True, WHITE)
  screen.blit(moves_text, (10, 5))

  exit_button.render(screen)
  board.blit(screen)

  pg.display.flip()

def display_game_won_screen(score, move_count):
  sound_player.bg_stop()
  hi_score = HighScore()
  quit_button = Button("Quit", 32, origin = (21, 270), width = 120, pad = (10, 3))
  play_again_button = Button("Play Again", 32, origin = (161, 270), width = 120, bg_color = GREEN)
  screen.fill(color = BLACK)
  prev_hs, hs_verb, hs_text_color = hi_score.check_high_score(score)
  if score > prev_hs:
    sound_player.play("high_score")
  sound_player.play("win")
  if "debug" in cl_args:
    print(f"Your score of: {score} {hs_verb} the previous high score of {prev_hs}")
    print(f"Moves used: {move_count}")
  over_surf_1 = end_screen_font.render(f"Your score of:", True, WHITE)
  over_surf_2 = end_screen_font.render(f"{score} ", True, hs_text_color)
  over_surf_3 = end_screen_font.render(f"{hs_verb} the previous", True, hs_text_color)
  over_surf_4 = end_screen_font.render(f"high score of", True, WHITE)
  over_surf_5 = end_screen_font.render(f"{prev_hs}", True, WHITE)
  moves_surf = end_screen_font.render(f"Moves used: {move_count}", True, WHITE)
  screen.blit(over_surf_1, (get_x_coord(over_surf_1), 70))
  screen.blit(over_surf_2, (get_x_coord(over_surf_2), 100))
  screen.blit(over_surf_3, (get_x_coord(over_surf_3), 130))
  screen.blit(over_surf_4, (get_x_coord(over_surf_4), 160))
  screen.blit(over_surf_5, (get_x_coord(over_surf_5), 190))
  screen.blit(moves_surf, (get_x_coord(moves_surf), 220))
  quit_button.render(screen)
  play_again_button.render(screen)
  pg.display.flip()
  while True:
    # This shows the screen indefinitely while processing events
    # no need to blit the screen or flip display because it's static
    # the sound is off
    for event in pg.event.get():
      if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        sys.exit(0)
      if event.type == QUIT:
        sys.exit(0)
      if event.type == pg.MOUSEBUTTONDOWN:
        click_pos = pg.mouse.get_pos()
        if quit_button.was_clicked(click_pos):
          sys.exit(0)
        if play_again_button.was_clicked(click_pos):
          random.shuffle(board.positions)
          play_game()
          sound_player.play("restart")
      pg.event.clear()
    clock.tick(60)

def display_game_exit_screen(display_text, play_sound = False ):
  end_screen_font = pg.font.Font(None, 32)
  quit_button = Button("Quit", 32, origin = (21, 270), width = 120, pad = (10, 3))

  play_again_button = Button("Play Again", 32, origin = (161, 270), width = 120, bg_color = GREEN)
  sound_player.bg_stop()
  if play_sound:
    sound_player.play("time_expired")
  screen.fill(color = BLACK)
  over_surf_1 = end_screen_font.render(f"{display_text}", True, WHITE)
  screen.blit(over_surf_1, (get_x_coord(over_surf_1), 140))
  quit_button.render(screen)
  play_again_button.render(screen)
  pg.display.flip()
  while True:
    for event in pg.event.get():
      if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        sys.exit(0)
      if event.type == QUIT:
        sys.exit(0)
      if event.type == pg.MOUSEBUTTONDOWN:
        click_pos = pg.mouse.get_pos()
        if quit_button.was_clicked(click_pos):
          sys.exit(0)
        if play_again_button.was_clicked(click_pos):
          random.shuffle(board.positions)
          sound_player.play("restart")
          play_game()
      pg.event.clear()
    clock.tick(60)

def process_special_keys(key, modifiers, timer):
  if key == pg.K_ESCAPE:
    sys.exit(0)
  if key == pg.K_u:
    sound_player.volume_up()
  if key == pg.K_d:
    sound_player.volume_down()
  if key == pg.K_m and modifiers & pg.KMOD_CTRL:
    # m plus CTRL key
    sound_player.mute()
  if "cheat" in cl_args and key == pg.K_c and modifiers & pg.KMOD_CTRL:
    # c plus CTRL only in cheat mode
      board.cheat()
  if "cheat" in cl_args and key == pg.K_e and modifiers & pg.KMOD_CTRL:
    # e plus CTRL only in cheat mode
    timer.reset(allowed_secs - 5)
  if "debug" in cl_args and key == pg.K_p:
    breakpoint()

def play_game():
  sound_player.bg_start()
  move_count = 0
  timer = Timer()
  while True:
    display_main_screen(timer.elapsed(), move_count)
    for event in pg.event.get():
      if event.type == QUIT:
        sys.exit(0)
      if event.type == pg.MOUSEBUTTONDOWN:
        click_pos = pg.mouse.get_pos()
        if exit_button.was_clicked(click_pos):
          display_game_exit_screen("Game exited")
        else:
          if board.click(click_pos) == 1:
            move_count += 1
            sound_player.play("click")
        pg.event.clear()
      if event.type == pg.KEYDOWN:
        process_special_keys(event.key, pg.key.get_mods(), timer)
    if board.is_game_won():
      display_game_won_screen(allowed_secs - timer.elapsed(), move_count)
      break
    if allowed_secs - timer.elapsed() < 1:
      display_game_exit_screen("Time expired", True)
      break

    clock.tick(60)

clock = pg.time.Clock()
if should_show_instructions():
  display_instructions_screen()
else:
  display_main_screen(0, 0)
  play_game()

# Game Over