import pygame as pg, sys, random, pdb, time
from pygame.locals import *

pg.mixer.init()

click_sound = pg.mixer.Sound("click.wav")
restart_sound = pg.mixer.Sound("restart.wav")
high_score_sound = pg.mixer.Sound("high_score.wav")
win_sound = pg.mixer.Sound("win.wav")
timeout_sound = pg.mixer.Sound("timeout.wav")
pg.mixer.music.load("background_music.wav")
pg.mixer.music.set_volume(0.5)  # Adjust volume
pg.mixer.music.play(-1)

class Timer:
  def __init__(self):
    self.start_time = time.time()

  def elapsed(self, compare_time = None, milliseconds = False):
    compare_time = compare_time or time.time()
    elapsed = compare_time - self.start_time
    if milliseconds:
      return int(elapsed * 1000)
    else:
      return int(elapsed)

  def reset(self, offset = 0):
    self.start_time = time.time() - offset


def high_score(cur_score, f_name = "high_score.txt"):
  try:
    f = open(f_name, "r")
    hs = int(f.read())
    f.close()
  except (FileNotFoundError, ValueError) as e:
    # if the file doesn't exist, or it's contents cannot be cast to an int, just set hs = 0
    hs = 0
  if cur_score > hs:
    f = open("high_score.txt", "w")
    f.write(str(cur_score))
    f.close()
    verb = "beat"
    color = GREEN
  elif cur_score == hs:
    verb = "tied"
    color = YELLOW
  else:
    verb = "failed to beat"
    color = RED
  return [verb, hs, color]

cl_args = list(map(lambda x: x.lower(), sys.argv[1:]))
cheat = "cheat" in cl_args
debug = "debug" in cl_args
allowed_secs = 300

BLACK = (0, 0, 0)
MED_GRAY = (160, 160, 160)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

move_count = 0



# Thoughts
# we have nine rects, 0 - 8 which make up the board
# 0 1 2
# 3 4 5
# 6 7 8

# Assign nums randomly to the rects (0 will represent blank)
# don't blit the blank rect it will have the background color
# note the rect thats blank, it's num will define adjacent rects
# mousedown in adjacent rects will move the num from that rect to what was blank rect and it will become blank
# mousedown in non-adjacent rect will do nothing
# l.insert(newindex, l.pop(oldindex))
positions = list(range(9))
random.shuffle(positions)

pg.init()
resolution = (302, 336)
screen = pg.display.set_mode(resolution)
screen.fill(color = BLACK)
# centers = [(51, 85), (151, 85), (251, 85), (51, 185), (151, 185), (251, 185), (51, 285), (151, 285), (251, 285)]
# font_rect_size = [12, 22]


font_origins = [(45, 74), (145, 74), (245, 74), (45, 174), (145, 174), (245, 174), (45, 274), (145, 274), (245, 274)]

font = pg.font.Font(None, 32)

status_rect = pg.Rect(0, 0, 302, 34)
status_surf = pg.Surface((status_rect.w, status_rect.h))
status_surf.fill(BLACK)

restart_button_rect = pg.Rect(200, 5, 90, 24)
restart_text = font.render("Exit", True, BLACK)
quit_button_rect = pg.Rect(21, 270, 120, 24)
quit_text = font.render("Quit", True, BLACK)
play_again_button_rect = pg.Rect(161, 270, 120, 24)
play_again_text = font.render("Play again", True, BLACK)



rects = []
surfs = []


idx = 0
for y in [36, 136, 236]:
  for x in [2, 102, 202]:
    # if y == y_pos[-1] and x == x_pos[-1]:
    #   continue
    r = pg.Rect(x, y, 98, 98)
    r_surf =  pg.Surface((r.w, r.h))
    r_surf.fill(color = MED_GRAY)
    rects.append(r)
    surfs.append(r_surf)
    idx += 1

font_surfs = []
for x in range(9):
  # we're never gonna use surfs[0] with "0", but it just keeps things tidy to have index = actual digit
  s = font.render(str(x), True, BLACK)
  font_surfs.append(s)

# These control where clicks can do something
# the index is the rect number of the blank tile
# the element is a list of rect numbers that are adjacent to that blank tile
adjacent_rects = [[1,3], [0,2,4], [1,5], [0, 4, 6], [1, 3, 5, 7], [2, 4, 8], [3, 7], [4, 6, 8], [5, 7]]

def swap_with_zero(num):
  global move_count
  zero_pos = positions.index(0)
  num_pos = positions.index(num)
  positions[zero_pos] = num
  positions[num_pos] = 0
  move_count += 1

def get_clicked_num(c_pos):
  for x in range(len(rects)):
    if rects[x].collidepoint(c_pos):
      if x in adjacent_rects[positions.index(0)]:
        # we have a click in a cell adjacent to the blank cell
        click_sound.play()
        return positions[x]
      # we found the rect but it wasn't adjacent
      return -1
  # click was not in a monitored Rect (it was in a border or in the status Rect)
  return -1

def get_x_coord(surf, screen_width = 302):
  return (screen_width - surf.get_rect().width) // 2

def shuffle_positions(timer):
  global move_count
  random.shuffle(positions)
  move_count = 0
  timer.reset()

def update_screen(elapsed):
  screen.fill(BLACK)
  timer_surf = font.render(f"{str(allowed_secs - elapsed)}", True, WHITE)
  screen.blit(timer_surf, ((302 - timer_surf.get_width()) // 2, 5))

  moves_text = font.render(f"Moves: {move_count}", True, WHITE)
  screen.blit(moves_text, (10, 5))

  pg.draw.rect(screen, RED, restart_button_rect)
  screen.blit(restart_text, (restart_button_rect.x + 22, restart_button_rect.y + 2))

  for idx in range (len(positions)):
    if positions[idx] != 0:
      screen.blit(surfs[idx], (rects[idx].x, rects[idx].y))
      screen.blit(font_surfs[positions[idx]], font_origins[idx])
  pg.display.flip()

def check_for_win():
  #currently ignores the blank tile, should we change?
  check = 1
  for x in positions:
    if x == 0:
      continue
    if x > check:
      return False
    check += 1
  keys = []
  return True

def game_won(score):
  global move_count
  screen.fill(color = BLACK)
  hs_verb, hs, hs_text_color = high_score(score)
  if hs_verb == "beat":
    high_score_sound.play()
  win_sound.play()
  if debug:
    print(f"Your score of: {score} {hs_verb} the previous high score of {hs}")
    print(f"Moves used: {move_count}")
  over_surf_1 = font.render(f"Your score of:", True, WHITE)
  over_surf_2 = font.render(f"{score} ", True, hs_text_color)
  over_surf_3 = font.render(f"{hs_verb} the previous", True, hs_text_color)
  over_surf_4 = font.render(f"high score of", True, WHITE)
  over_surf_5 = font.render(f"{hs}", True, WHITE)
  moves_surf = font.render(f"Moves used: {move_count}", True, WHITE)
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
          random.shuffle(positions)
          move_count = 0
          play_game()
          restart_sound.play()
      pg.event.clear()
    clock.tick(60)

def game_exit(display_text, play_sound = False ):
  global move_count
  if play_sound:
    timeout_sound.play()
  # TODO refactor to game_over to handle both win and timeout
  screen.fill(color = BLACK)
  over_surf_1 = font.render(f"{display_text}", True, WHITE)
  screen.blit(over_surf_1, (get_x_coord(over_surf_1), 140))
  pg.draw.rect(screen, RED, quit_button_rect)
  screen.blit(quit_text, (quit_button_rect.x + 35, quit_button_rect.y + 2))
  pg.draw.rect(screen, GREEN, play_again_button_rect)
  screen.blit(play_again_text, (play_again_button_rect.x + 6, play_again_button_rect.y + 2))
  pg.display.flip()
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
          random.shuffle(positions)
          move_count = 0
          restart_sound.play()
          play_game()
      pg.event.clear()
    clock.tick(60)

def play_game():
  global positions
  clickpos = None
  timer = Timer()
  while True:
    update_screen(timer.elapsed())
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
      sys.exit(0)
    if cheat and keys[pg.K_c] and (keys[pg.K_RCTRL] or keys[pg.K_LCTRL]):
      # quickly get in position to solve
      # must pass command line argument "cheat" (no quotes, case insensitive)
      # for cheat to work
      positions = [1, 2, 3, 4, 8, 5, 7, 6, 0]
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
          clicked_num = get_clicked_num(clickpos)
          if clicked_num != -1:
            swap_with_zero(clicked_num)
        pg.event.clear()
    if check_for_win():
      game_won(allowed_secs - timer.elapsed())
      break
    if allowed_secs - timer.elapsed() < 1:
      game_exit("Time expired", True)
      break

    clock.tick(60)

clock = pg.time.Clock()
update_screen(0)
play_game()

# Game Over