# Class: CSE 1321
# Section: WE1
# Term: Fall 2024
# Instructor: Nick Mrphy
# Group 18
# Members: Ernie Fichtel, Seqouya Jackson, Oneeb Kahn, Jonathan Parson, Scott Wright
# Group Project



import pygame as pg, sys, random, pdb
from timer import Timer
from high_score import HighScore
from colors import *
from board import Board
from sound_player import SoundPlayer
from pygame.locals import *


sound_player = SoundPlayer(0.2)

pg.init()
tile_font = pg.font.Font(None, 32)
status_font = pg.font.Font(None, 32)
end_screen_font = pg.font.Font(None, 32)
button_font = pg.font.Font(None, 32)
board = Board(98, tile_font)

cl_args = list(map(lambda x: x.lower(), sys.argv[1:]))
cheat = "cheat" in cl_args
debug = "debug" in cl_args
allowed_secs = 300

resolution = (board.screen_size)
screen = pg.display.set_mode(resolution)
screen.fill(color = BLACK)

status_rect = pg.Rect(0, 0, 302, 34)
status_surf = pg.Surface((status_rect.w, status_rect.h))
status_surf.fill(BLACK)

exit_button_rect = pg.Rect(206, 5, 90, 24)
exit_text = button_font.render("Exit", True, BLACK)
quit_button_rect = pg.Rect(21, 270, 120, 24)
quit_text = button_font.render("Quit", True, BLACK)
play_again_button_rect = pg.Rect(161, 270, 120, 24)
play_again_text = button_font.render("Play again", True, BLACK)


def get_x_coord(surf, screen_width = resolution[0]):
  return (screen_width - surf.get_rect().width) // 2

def update_main_screen(elapsed, move_count):
  screen.fill(BLACK)
  timer_surf = status_font.render(f"{str(allowed_secs - elapsed)}", True, WHITE)
  screen.blit(timer_surf, ((302 - timer_surf.get_width()) // 2, 5))

  moves_text = status_font.render(f"Moves: {move_count}", True, WHITE)
  screen.blit(moves_text, (10, 5))

  pg.draw.rect(screen, RED, exit_button_rect)
  screen.blit(exit_text, (exit_button_rect.x + 22, exit_button_rect.y + 2))
  board.blit(screen)

  pg.display.flip()

def game_won(score, move_count):
  hi_score = HighScore()
  sound_player.bg_stop()
  screen.fill(color = BLACK)
  prev_hs, hs_verb, hs_text_color = hi_score.check_high_score(score)
  if score > prev_hs:
    sound_player.play("high_score")
  sound_player.play("win")
  if debug:
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
  pg.draw.rect(screen, RED, quit_button_rect)
  screen.blit(quit_text, (quit_button_rect.x + 35, quit_button_rect.y + 2))
  pg.draw.rect(screen, GREEN, play_again_button_rect)
  screen.blit(play_again_text, (play_again_button_rect.x + 6, play_again_button_rect.y + 2))
  pg.display.flip()
  while True:
    # This shows the screen indefinitely while processing events
    # no need to blit the screen or flip display because it's static
    # the sound is off
    for event in pg.event.get():
      if event.type == QUIT:
        sys.exit(0)
      if event.type == pg.MOUSEBUTTONDOWN:
        clickpos = pg.mouse.get_pos()
        if quit_button_rect.collidepoint(clickpos):
          sys.exit(0)
        if play_again_button_rect.collidepoint(clickpos):
          random.shuffle(board.positions)
          move_count = 0
          play_game()
          sound_player.play("restart")
      pg.event.clear()
    clock.tick(60)

def game_exit(display_text, play_sound = False ):
  sound_player.bg_stop()
  if play_sound:
    sound_player.play("time_expired")
  screen.fill(color = BLACK)
  over_surf_1 = end_screen_font.render(f"{display_text}", True, WHITE)
  screen.blit(over_surf_1, (get_x_coord(over_surf_1), 140))
  pg.draw.rect(screen, RED, quit_button_rect)
  screen.blit(quit_text, (quit_button_rect.x + 35, quit_button_rect.y + 2))
  pg.draw.rect(screen, GREEN, play_again_button_rect)
  screen.blit(play_again_text, (play_again_button_rect.x + 6, play_again_button_rect.y + 2))
  pg.display.flip()
  while True:
    for event in pg.event.get():
      if event.type == QUIT:
        sys.exit(0)
      if event.type == pg.MOUSEBUTTONDOWN:
        clickpos = pg.mouse.get_pos()
        if quit_button_rect.collidepoint(clickpos):
          sys.exit(0)
        if play_again_button_rect.collidepoint(clickpos):
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
  if cheat and key == pg.K_c and modifiers & pg.KMOD_CTRL:
    # c plus CTRL only in cheat mode
      board.cheat()
  if cheat and key == pg.K_e and modifiers & pg.KMOD_CTRL:
    # e plus CTRL only in cheat mode
    timer.reset(allowed_secs - 5)
  if debug and key == pg.K_p:
    breakpoint()
  if debug and key == pg.K_s  and modifiers & pg.KMOD_CTRL:
    sound_player.play("sound not present")

def play_game():
  sound_player.bg_start()
  move_count = 0
  clickpos = None
  timer = Timer()
  while True:
    update_main_screen(timer.elapsed(), move_count)
    for event in pg.event.get():
      if event.type == QUIT:
        sys.exit(0)
      if event.type == pg.MOUSEBUTTONDOWN:
        clickpos = pg.mouse.get_pos()
        if exit_button_rect.collidepoint(clickpos):
          game_exit("Game exited")
        else:
          if board.click(clickpos) == 1:
            move_count += 1
            sound_player.play("click")
        pg.event.clear()
      if event.type == pg.KEYDOWN:
        process_special_keys(event.key, pg.key.get_mods(), timer)
    if board.is_game_won():
      game_won(allowed_secs - timer.elapsed(), move_count)
      break
    if allowed_secs - timer.elapsed() < 1:
      game_exit("Time expired", True)
      break

    clock.tick(60)

clock = pg.time.Clock()
update_main_screen(0, 0)
play_game()

# Game Over