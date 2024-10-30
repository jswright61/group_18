import pygame as pg, sys, random, pdb, time
from pygame.locals import *

pg.mixer.init()

click_sound = pg.mixer.Sound("click.wav")
restart_sound = pg.mixer.Sound("restart.wav")
high_score_sound = pg.mixer.Sound("high_score.wav")
win_sound = pg.mixer.Sound("win.wav")
pg.mixer.music.load("background_music.wav")
pg.mixer.music.set_volume(0.5)  # Adjust volume
pg.mixer.music.play(-1)

class Timer:
  def __init__(self):
    self.start_time = time.time()

  def elapsed(self, compare_time = None, milliseconds = True):
    compare_time = compare_time or time.time()
    elapsed = compare_time - self.start_time
    if milliseconds:
      return int(elapsed * 1000)
    else:
      return int(elapsed)


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
  elif cur_score == hs:
    verb = "tied"
  else:
    verb = "failed to beat"
  return [verb, hs]

cl_args = list(map(lambda x: x.lower(), sys.argv[1:]))
cheat = "cheat" in cl_args
debug = "debug" in cl_args
start_secs = 300

BLACK = (0, 0, 0)
MED_GRAY = (160, 160, 160)
WHITE = (255, 255, 255)

move_count = 0
restart_button_rect = pg.Rect(200, 5, 90, 24)

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
        # we have a click in a cell adjacent to the blank
        click_sound.play()
        return positions[x]
      # we found the rect but it wasn't adjacent
      return -1
  # click was not in a monitored Rect (it was in a border or in the status Rect)
  return -1

def get_x_coord(surf, screen_width = 302):
  return (screen_width - surf.get_rect().width) // 2

def shuffle_positions():
  global positions, move_count, timer
  random.shuffle(positions)
  move_count = 0
  timer = Timer()

def update_screen(elapsed):
  screen.fill(BLACK)
  # screen.blit(status_surf, (status_rect.x, status_rect.y))
  timer_surf = font.render(f"{str(start_secs - elapsed // 1000)}", True, WHITE)
  timer_surf_rect = timer_surf.get_rect()
  screen.blit(timer_surf, ((151 - timer_surf_rect.width // 2), 5))

  moves_text = font.render(f"Moves: {move_count}", True, WHITE)
  screen.blit(moves_text, (10, 5))

  pg.draw.rect(screen, MED_GRAY, restart_button_rect)
  restart_text = font.render("Restart", True, BLACK)
  screen.blit(restart_text, (restart_button_rect.x + 5, restart_button_rect.y + 2))

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
  screen.fill(color = BLACK)
  hs_verb, hs = high_score(score)
  if hs_verb == "beat":
    high_score_sound.play()
  win_sound.play()
  won_surf1 = font.render(f"Your score of:", False, WHITE)
  won_surf2 = font.render(f"{score} ", False, WHITE)
  won_surf3 = font.render(f"{hs_verb} the previous", False, WHITE)
  won_surf4 = font.render(f"high score of", False, WHITE)
  won_surf5 = font.render(f"{hs}", False, WHITE)
  moves_surf = font.render(f"Moves used: {move_count}", False, WHITE)
  for x in range(300):
    for event in pg.event.get():
      if event.type == QUIT:
        sys.exit(0)
      pg.event.clear()
    screen.blit(won_surf1, (get_x_coord(won_surf1), 70))
    screen.blit(won_surf2, (get_x_coord(won_surf2), 105))
    screen.blit(won_surf3, (get_x_coord(won_surf3), 135))
    screen.blit(won_surf4, (get_x_coord(won_surf4), 165))
    screen.blit(won_surf5, (get_x_coord(won_surf5), 195))
    screen.blit(moves_surf, (get_x_coord(moves_surf), 210))
    pg.display.flip()
    clock.tick(60)




clock = pg.time.Clock()
update_screen(0)

clickpos = None
timer = Timer()
while True:
  update_screen(timer.elapsed())
  for event in pg.event.get():
    keys = pg.key.get_pressed()
    if event.type == QUIT:
      sys.exit(0)
    if keys[pg.K_ESCAPE]:
      sys.exit(0)
    if event.type == pg.MOUSEBUTTONDOWN:
      clickpos = pg.mouse.get_pos()
      if restart_button_rect.collidepoint(clickpos):
        restart_sound.play()
        shuffle_positions()
      else:
        clicked_num = get_clicked_num(clickpos)
        if clicked_num != -1:
          swap_with_zero(clicked_num)
      pg.event.clear()
    if keys[pg.K_c]:
      # quickly get in position to solve
      # must pass command line argument "cheat" (no quotes, case insensitive)
      # for cheat to work
      if cheat:
        positions = [1, 2, 3, 4, 8, 5, 7, 6, 0]
    if keys[pg.K_p]:
      # pause for debugging
      # must pass command line argument "debug" (no quotes, case insensitive)
      # for pause to work
      if debug:
        breakpoint()
  if check_for_win():
    score = start_secs - timer.elapsed() // 1000
    game_won(score)
    break
  clock.tick(60)

# Game Over