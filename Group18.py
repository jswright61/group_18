# Class: CSE 1321
# Section: WE1
# Term: Fall 2024
# Instructor: Nick Mrphy
# Group 18
# Members: Ernie Fichtel, Seqouya Jackson, Oneeb Kahn, Jonathan Parson, Scott Wright
# Group Project



import pygame as pg, sys, random, pdb
from timer import Timer
from colors import *
from board import Board
from pygame.locals import *

pg.mixer.init()
click_sound = pg.mixer.Sound("click.wav")
restart_sound = pg.mixer.Sound("restart.wav")
high_score_sound = pg.mixer.Sound("high_score.wav")
win_sound = pg.mixer.Sound("win.wav")
timeout_sound = pg.mixer.Sound("timeout.wav")
pg.mixer.music.load("background_music.wav")
pg.mixer.music.set_volume(0.2)  # Adjust volume
pg.mixer.music.play(-1)

pg.init()
tile_font = pg.font.Font(None, 32)
status_font = pg.font.Font(None, 32)
end_screen_font = pg.font.Font(None, 32)
button_font = pg.font.Font(None, 32)
board = Board(98, tile_font)

def high_score(cur_score, f_name = "high_score.txt"):
  try:
    f = open(f_name, "r")
    hs = int(f.read())
    f.close()
  except (FileNotFoundError, ValueError) as e:
    # if the file doesn't exist, or it's contents cannot be cast to an int, just set hs = 0
    hs = 0
  new_hs = False
  if cur_score > hs:
    f = open("high_score.txt", "w")
    f.write(str(cur_score))
    f.close()
    verb = "beat"
    color = GREEN
    new_hs = True
  elif cur_score == hs:
    verb = "tied"
    color = YELLOW
  else:
    verb = "failed to beat"
    color = RED
  return [hs, verb, color, new_hs]

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

restart_button_rect = pg.Rect(200, 5, 90, 24)
restart_text = button_font.render("Exit", True, BLACK)
quit_button_rect = pg.Rect(21, 270, 120, 24)
quit_text = button_font.render("Quit", True, BLACK)
play_again_button_rect = pg.Rect(161, 270, 120, 24)
play_again_text = button_font.render("Play again", True, BLACK)


def get_x_coord(surf, screen_width = 302):
  return (screen_width - surf.get_rect().width) // 2

def update_screen(elapsed, move_count):
  screen.fill(BLACK)
  timer_surf = status_font.render(f"{str(allowed_secs - elapsed)}", True, WHITE)
  screen.blit(timer_surf, ((302 - timer_surf.get_width()) // 2, 5))

  moves_text = status_font.render(f"Moves: {move_count}", True, WHITE)
  screen.blit(moves_text, (10, 5))

  pg.draw.rect(screen, RED, restart_button_rect)
  screen.blit(restart_text, (restart_button_rect.x + 22, restart_button_rect.y + 2))

  for idx in range (len(board.positions)):
    if board.positions[idx] != 0:
      screen.blit(board.surfs[idx], (board.rects[idx].x, board.rects[idx].y))
      screen.blit(board.font_surfs[board.positions[idx]], board.font_origins[idx])
  pg.display.flip()

def game_won(score, move_count):
  screen.fill(color = BLACK)
  hs, hs_verb, hs_text_color, new_hs = high_score(score)
  if new_hs:
    high_score_sound.play()
  win_sound.play()
  if debug:
    print(f"Your score of: {score} {hs_verb} the previous high score of {hs}")
    print(f"Moves used: {move_count}")
  over_surf_1 = end_screen_font.render(f"Your score of:", True, WHITE)
  over_surf_2 = end_screen_font.render(f"{score} ", True, hs_text_color)
  over_surf_3 = end_screen_font.render(f"{hs_verb} the previous", True, hs_text_color)
  over_surf_4 = end_screen_font.render(f"high score of", True, WHITE)
  over_surf_5 = end_screen_font.render(f"{hs}", True, WHITE)
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
          restart_sound.play()
      pg.event.clear()
    clock.tick(60)

def game_exit(display_text, play_sound = False ):
  if play_sound:
    timeout_sound.play()
  # TODO refactor to game_over to handle both win and timeout
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
          restart_sound.play()
          play_game()
      pg.event.clear()
    clock.tick(60)

def play_game():
  move_count = 0
  clickpos = None
  timer = Timer()
  while True:
    update_screen(timer.elapsed(), move_count)
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
      sys.exit(0)
    if cheat and keys[pg.K_c] and (keys[pg.K_RCTRL] or keys[pg.K_LCTRL]):
      # quickly get in position to solve
      # must pass command line argument "cheat" (no quotes, case insensitive)
      # for cheat to work
      board.cheat()
    if cheat and keys[pg.K_e]  and (keys[pg.K_RCTRL] or keys[pg.K_LCTRL]):
      # This will take seconds off the clock to allow testing timeout
      timer.reset(295)
    if debug and keys[pg.K_p] and (keys[pg.K_RCTRL] or keys[pg.K_LCTRL]):
      # pause for debugging
      # must pass command line argument "debug" (no quotes, case insensitive)
      # for pause to work
      breakpoint()
    for event in pg.event.get():
      if event.type == QUIT:
        sys.exit(0)
      if event.type == pg.MOUSEBUTTONDOWN:
        clickpos = pg.mouse.get_pos()
        if restart_button_rect.collidepoint(clickpos):
          game_exit("Game exited")
        else:
          if board.click(clickpos) == 1:
            move_count += 1
            click_sound.play()
        pg.event.clear()
    if board.is_game_won():
      game_won(allowed_secs - timer.elapsed(), move_count)
      break
    if allowed_secs - timer.elapsed() < 1:
      game_exit("Time expired", True)
      break

    clock.tick(60)

clock = pg.time.Clock()
update_screen(0, 0)
play_game()

# Game Over