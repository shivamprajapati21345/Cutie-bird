# import pygame, random, time
# from pygame.locals import *
# from model import init_db, save_score, get_top_scores
# from settings import DB_PATH

# # --- BASE DESIGN RESOLUTION ---
# BASE_WIDTH = 400
# BASE_HEIGHT = 600

# # --- GAME CONSTANTS (scalable) ---
# SPEED = 20
# GRAVITY = 2.5
# GAME_SPEED = 25
# PIPE_WIDTH = 100
# PIPE_HEIGHT = 500
# PIPE_GAP = 230
# GROUND_HEIGHT = 30
# PIPE_DISTANCE = 300 

# # --- SOUND FILES ---
# WING_SOUND = 'assets/audio/wing.wav'
# HIT_SOUND = 'assets/audio/hit.wav'

# # --- INITIALIZE PYGAME ---
# pygame.init()
# pygame.mixer.init()
# init_db()

# # --- DISPLAY SETUP ---
# SCREEN_WIDTH, SCREEN_HEIGHT = BASE_WIDTH, BASE_HEIGHT
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
# pygame.display.set_caption('cutie birds Sky')

# # --- FONT & CLOCK ---
# font = pygame.font.Font(None, 50)
# clock = pygame.time.Clock()

# # --- FRONT SPLASH SCREEN ---
# front_image = pygame.image.load('assets/sprites/1message.png').convert()
# front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
# show_front = True

# while show_front:
#     screen.blit(front_image, (0, 0))
#     pygame.display.update()

#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit(); exit()
#         elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
#             show_front = False
#         elif event.type == VIDEORESIZE:
#             SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#             screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#             front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# # --- LOAD SOUNDS ---
# wing_sound = pygame.mixer.Sound(WING_SOUND)
# hit_sound = pygame.mixer.Sound(HIT_SOUND)

# pipe_color_toggle = True

# def scale_img(image, w, h):
#     return pygame.transform.scale(image, (int(w), int(h)))

# def get_scale():
#     return SCREEN_HEIGHT / BASE_HEIGHT

# class Bird(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.original_images = [
#             pygame.image.load('assets/sprites/18upflap.png').convert_alpha(),
#             pygame.image.load('assets/sprites/18midflap.png').convert_alpha(),
#             pygame.image.load('assets/sprites/18downflap.png').convert_alpha()
#         ]
#         self.current_image = 0
#         self.update_scaled_image()
#         self.speed = SPEED

#     def update_scaled_image(self):
#         scale = get_scale()
#         self.images = [scale_img(img, 70 * scale, 70 * scale) for img in self.original_images]
#         self.image = self.images[self.current_image]
#         self.mask = pygame.mask.from_surface(self.image)
#         self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))

#     def update(self):
#         self.current_image = (self.current_image + 1) % 3
#         self.image = self.images[self.current_image]
#         self.speed += GRAVITY
#         self.rect.y += int(self.speed)

#     def bump(self):
#         self.speed = -SPEED

#     def begin(self):
#         self.current_image = (self.current_image + 1) % 3
#         self.image = self.images[self.current_image]

# class Pipe(pygame.sprite.Sprite):
#     def __init__(self, inverted, xpos, ysize, color='red'):
#         super().__init__()
#         scale = get_scale()
#         image = pygame.image.load(f'assets/sprites/pipe-{color}.png').convert_alpha()
#         self.image = scale_img(image, PIPE_WIDTH * scale, PIPE_HEIGHT * scale)
#         if inverted:
#             self.image = pygame.transform.flip(self.image, False, True)
#             self.rect = self.image.get_rect()
#             self.rect.x = xpos
#             self.rect.y = -(self.rect.height - ysize)
#         else:
#             self.rect = self.image.get_rect()
#             self.rect.x = xpos
#             self.rect.y = SCREEN_HEIGHT - ysize
#         self.mask = pygame.mask.from_surface(self.image)

#     def update(self):
#         self.rect.x -= GAME_SPEED

# class Ground(pygame.sprite.Sprite):
#     def __init__(self, xpos):
#         super().__init__()
#         image = pygame.image.load('assets/sprites/base.png').convert_alpha()
#         scale = get_scale()
#         self.image = scale_img(image, 2 * SCREEN_WIDTH, GROUND_HEIGHT * scale)
#         self.rect = self.image.get_rect()
#         self.rect.x = xpos
#         self.rect.y = SCREEN_HEIGHT - int(GROUND_HEIGHT * scale)
#         self.mask = pygame.mask.from_surface(self.image)

#     def update(self):
#         self.rect.x -= GAME_SPEED

# def is_off_screen(sprite):
#     return sprite.rect.right < 0

# def get_random_pipes(xpos):
#     global pipe_color_toggle
#     size = random.randint(150, 300)
#     color = 'green' if pipe_color_toggle else 'red'
#     pipe_color_toggle = not pipe_color_toggle
#     return Pipe(False, xpos, size, color), Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP, color)

# def draw_buttons(paused):
#     pause_button = pygame.Rect(SCREEN_WIDTH - 140, 20, 100, 40)
#     resume_button = pygame.Rect(SCREEN_WIDTH - 140, 70, 100, 40)

#     if not paused:
#         pygame.draw.rect(screen, (50, 50, 50), pause_button)
#         screen.blit(font.render("Pause", True, (255, 255, 255)), (SCREEN_WIDTH - 130, 25))
#     else:
#         pygame.draw.rect(screen, (50, 50, 50), resume_button)
#         screen.blit(font.render("Resume", True, (255, 255, 255)), (SCREEN_WIDTH - 130, 75))

#     return pause_button, resume_button

# def run_game():
#     global SCREEN_WIDTH, SCREEN_HEIGHT, screen

#     BACKGROUND = pygame.image.load('assets/sprites/1background-P.png').convert()
#     def rescale_background():
#         return scale_img(BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)
#     background = rescale_background()
#     top_scores = get_top_scores(limit=3)

#     home_active = True
#     while home_active:
#         screen.blit(background, (0, 0))

#         # Buttons
#         start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
#         exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 160, 200, 50)
#         screen.blit(font.render("Start Game", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 110))
#         screen.blit(font.render("Exit", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 170))

#         # === Top Scores Title ===
#         title_surface = font.render("Top Scores:", True, (255, 255, 0))
#         screen.blit(title_surface, (50, 40))  # Top-left above table

#         # Table dimensions and position on left
#         table_x = 50   # left margin
#         table_y = 80   # below "Top Scores"
#         col_widths = [80, 200, 120]
#         row_height = 50

#         # Table header
#         headers = ["Sr", "Name", "Score"]
#         for col, text in enumerate(headers):
#             cell_rect = pygame.Rect(table_x + sum(col_widths[:col]), table_y, col_widths[col], row_height)
#             pygame.draw.rect(screen, (200, 200, 200), cell_rect, 2)
#             header_text = font.render(text, True, (255, 255, 0))
#             screen.blit(header_text, (cell_rect.x + 10, cell_rect.y + 10))

#         # Table rows
#         for i, (name, score) in enumerate(top_scores):
#             for col, value in enumerate([str(i + 1), name, str(score)]):
#                 cell_rect = pygame.Rect(table_x + sum(col_widths[:col]), table_y + (i + 1) * row_height, col_widths[col], row_height)
#                 pygame.draw.rect(screen, (255, 255, 255), cell_rect, 2)
#                 cell_text = font.render(value, True, (255, 255, 255))
#                 screen.blit(cell_text, (cell_rect.x + 10, cell_rect.y + 10))

#         pygame.display.update()

#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == MOUSEBUTTONDOWN:
#                 pos = pygame.mouse.get_pos()
#                 if start_button.collidepoint(pos):
#                     home_active = False
#                 elif exit_button.collidepoint(pos):
#                     pygame.quit(); exit()
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background()

#     player_name = ""
#     # Game setup...
#     bird_group = pygame.sprite.Group()
#     bird = Bird()
#     bird.update_scaled_image()
#     bird_group.add(bird)

#     ground_group = pygame.sprite.Group()
#     for i in range(2):
#         ground = Ground(SCREEN_WIDTH * i)
#         ground_group.add(ground)

#     pipe_group = pygame.sprite.Group()
#     for i in range(2):
#         pipes = get_random_pipes(SCREEN_WIDTH + i * 350)
#         pipe_group.add(pipes[0])
#         pipe_group.add(pipes[1])

#     begin = True
#     while begin:
#         clock.tick(15)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == KEYDOWN:
#                 if event.key in (K_SPACE, K_UP):
#                     bird.bump()
#                     wing_sound.play()
#                     begin = False
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background()
#                 bird.update_scaled_image()

#         screen.blit(background, (0, 0))
#         bird.begin()
#         ground_group.update()
#         for ground in ground_group:
#             if is_off_screen(ground):
#                 ground_group.remove(ground)
#                 ground_group.add(Ground(SCREEN_WIDTH - 100))
#         bird_group.draw(screen)
#         ground_group.draw(screen)
#         pygame.display.update()

#     score = 1
#     paused = False
#     while True:
#         clock.tick(15)
#         pause_btn, resume_btn = draw_buttons(paused)

#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background()
#                 bird.update_scaled_image()
#             elif event.type == KEYDOWN:
#                 if event.key in (K_SPACE, K_UP) and not paused:
#                     bird.bump()
#                     score += 1
#                     wing_sound.play()
#                 elif event.key == K_RETURN:
#                     paused = not paused
#             elif event.type == MOUSEBUTTONDOWN:
#                 pos = pygame.mouse.get_pos()
#                 if not paused and pause_btn.collidepoint(pos):
#                     paused = True
#                 elif paused and resume_btn.collidepoint(pos):
#                     paused = False

#         screen.blit(background, (0, 0))

#         if not paused:
#             if is_off_screen(pipe_group.sprites()[0]):
#                 pipe_group.remove(pipe_group.sprites()[0])
#                 pipe_group.remove(pipe_group.sprites()[0])
#                 new_pipes = get_random_pipes(SCREEN_WIDTH + 300)
#                 pipe_group.add(new_pipes[0])
#                 pipe_group.add(new_pipes[1])

#             bird_group.update()
#             pipe_group.update()
#             ground_group.update()

#         bird_group.draw(screen)
#         pipe_group.draw(screen)
#         ground_group.draw(screen)

#         name_surface = font.render(player_name, True, (255, 255, 255))
#         score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
#         screen.blit(name_surface, (10, 20))
#         screen.blit(score_surface, (20, 70))

#         draw_buttons(paused)
#         pygame.display.update()

#         if not paused and (
#             pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
#             pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask) or
#             bird.rect.top <= 0 or
#             bird.rect.bottom >= SCREEN_HEIGHT
#         ):
#             hit_sound.play()
#             game_over = font.render("Game Over!", True, (255, 0, 0))
#             screen.blit(game_over, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
#             pygame.display.update()
#             time.sleep(1.5)
#             save_score(player_name, score)
#             return

# # MAIN LOOP
# while True:
#     run_game()


















# import pygame, random, time
# # from pygame.locals import *
# from model import init_db, save_score, get_top_scores

# # --- BASE DESIGN RESOLUTION ---
# BASE_WIDTH = 400
# BASE_HEIGHT = 600

# # --- GAME CONSTANTS (scalable) ---
# SPEED = 20
# GRAVITY = 2.5
# GAME_SPEED = 25
# PIPE_WIDTH = 100
# PIPE_HEIGHT = 500
# PIPE_GAP = 230
# GROUND_HEIGHT = 30
# PIPE_DISTANCE = 300 
# # --- SOUND FILES ---
# WING_SOUND = 'assets/audio/wing.wav'
# HIT_SOUND = 'assets/audio/hit.wav'

# # --- INITIALIZE PYGAME ---
# pygame.init()
# pygame.mixer.init()

# # --- DISPLAY SETUP ---
# SCREEN_WIDTH, SCREEN_HEIGHT = BASE_WIDTH, BASE_HEIGHT
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
# pygame.display.set_caption('cutie birds Sky')

# # --- FONT & CLOCK ---
# font = pygame.font.Font(None, 50)
# clock = pygame.time.Clock()
# # --- FRONT SPLASH SCREEN ---
# front_image = pygame.image.load('assets/sprites/1message.png').convert()
# front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
# show_front = True

# while show_front:
#     screen.blit(front_image, (0, 0))
#     pygame.display.update()

#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit(); exit()
#         elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
#             show_front = False
#         elif event.type == VIDEORESIZE:
#             SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#             screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#             front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# # --- LOAD SOUNDS ---
# wing_sound = pygame.mixer.Sound(WING_SOUND)
# hit_sound = pygame.mixer.Sound(HIT_SOUND)

# # --- GLOBAL PIPE COLOR TOGGLE ---
# pipe_color_toggle = True

# # --- HELPER: SCALE IMAGE ---
# def scale_img(image, w, h):
#     return pygame.transform.scale(image, (int(w), int(h)))

# def get_scale():
#     return SCREEN_HEIGHT / BASE_HEIGHT

# # --- BIRD SPRITE ---
# class Bird(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.original_images = [
#             pygame.image.load('assets/sprites/18upflap.png').convert_alpha(),
#             pygame.image.load('assets/sprites/18midflap.png').convert_alpha(),
#             pygame.image.load('assets/sprites/18downflap.png').convert_alpha()
#         ]
#         self.current_image = 0
#         self.update_scaled_image()
#         self.speed = SPEED

#     def update_scaled_image(self):
#         scale = get_scale()
#         self.images = [scale_img(img, 70 * scale, 70 * scale) for img in self.original_images]
#         self.image = self.images[self.current_image]
#         self.mask = pygame.mask.from_surface(self.image)
#         self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))

#     def update(self):
#         self.current_image = (self.current_image + 1) % 3
#         self.image = self.images[self.current_image]
#         self.speed += GRAVITY
#         self.rect.y += int(self.speed)

#     def bump(self):
#         self.speed = -SPEED

#     def begin(self):
#         self.current_image = (self.current_image + 1) % 3
#         self.image = self.images[self.current_image]

# # --- PIPE SPRITE ---
# class Pipe(pygame.sprite.Sprite):
#     def __init__(self, inverted, xpos, ysize, color='red'):
#         super().__init__()
#         scale = get_scale()
#         image = pygame.image.load(f'assets/sprites/pipe-{color}.png').convert_alpha()
#         self.image = scale_img(image, PIPE_WIDTH * scale, PIPE_HEIGHT * scale)
#         if inverted:
#             self.image = pygame.transform.flip(self.image, False, True)
#             self.rect = self.image.get_rect()
#             self.rect.x = xpos
#             self.rect.y = -(self.rect.height - ysize)
#         else:
#             self.rect = self.image.get_rect()
#             self.rect.x = xpos
#             self.rect.y = SCREEN_HEIGHT - ysize
#         self.mask = pygame.mask.from_surface(self.image)

#     def update(self):
#         self.rect.x -= GAME_SPEED

# # --- GROUND SPRITE ---
# class Ground(pygame.sprite.Sprite):
#     def __init__(self, xpos):
#         super().__init__()
#         image = pygame.image.load('assets/sprites/base.png').convert_alpha()
#         scale = get_scale()
#         self.image = scale_img(image, 2 * SCREEN_WIDTH, GROUND_HEIGHT * scale)
#         self.rect = self.image.get_rect()
#         self.rect.x = xpos
#         self.rect.y = SCREEN_HEIGHT - int(GROUND_HEIGHT * scale)
#         self.mask = pygame.mask.from_surface(self.image)

#     def update(self):
#         self.rect.x -= GAME_SPEED

# # --- HELPERS ---
# def is_off_screen(sprite):
#     return sprite.rect.right < 0

# def get_random_pipes(xpos):
#     global pipe_color_toggle
#     size = random.randint(150, 300)
#     color = 'green' if pipe_color_toggle else 'red'
#     pipe_color_toggle = not pipe_color_toggle
#     return Pipe(False, xpos, size, color), Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP, color)

# def draw_buttons(paused):
#     pause_button = pygame.Rect(SCREEN_WIDTH - 140, 20, 100, 40)
#     resume_button = pygame.Rect(SCREEN_WIDTH - 140, 70, 100, 40)

#     if not paused:
#         pygame.draw.rect(screen, (50, 50, 50), pause_button)
#         screen.blit(font.render("Pause", True, (255, 255, 255)), (SCREEN_WIDTH - 130, 25))
#     else:
#         pygame.draw.rect(screen, (50, 50, 50), resume_button)
#         screen.blit(font.render("Resume", True, (255, 255, 255)), (SCREEN_WIDTH - 130, 75))

#     return pause_button, resume_button

# # --- MAIN GAME FUNCTION ---
# def run_game():
#     global SCREEN_WIDTH, SCREEN_HEIGHT, screen

#     BACKGROUND = pygame.image.load('assets/sprites/1background-P.png').convert()
#     def rescale_background():
#         return scale_img(BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)
#     background = rescale_background()

#     # --- HOME SCREEN ---
#     home_active = True
#     while home_active:
#         screen.blit(background, (0, 0))
#         start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
#         exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)

#         screen.blit(font.render("Start Game", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 40))
#         screen.blit(font.render("Exit", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 30))
#         pygame.display.update()

#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == MOUSEBUTTONDOWN:
#                 pos = pygame.mouse.get_pos()
#                 if start_button.collidepoint(pos):
#                     home_active = False
#                 elif exit_button.collidepoint(pos):
#                     pygame.quit(); exit()
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background()

#     # --- NAME INPUT ---
#     player_name = ""
#     input_active = True
#     while input_active:
#         screen.blit(background, (0, 0))
#         text_surface = font.render("Enter your name: " + player_name, True, (255, 255, 255))
#         screen.blit(text_surface, (50, SCREEN_HEIGHT // 2))
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == KEYDOWN:
#                 if event.key == K_RETURN and player_name:
#                     input_active = False
#                 elif event.key == K_BACKSPACE:
#                     player_name = player_name[:-1]
#                 elif len(player_name) < 12 and event.unicode.isprintable():
#                     player_name += event.unicode
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background()

#     # --- INIT GAME OBJECTS ---
#     bird_group = pygame.sprite.Group()
#     bird = Bird()
#     bird.update_scaled_image()
#     bird_group.add(bird)

#     ground_group = pygame.sprite.Group()
#     for i in range(2):
#         ground = Ground(SCREEN_WIDTH * i)
#         ground_group.add(ground)

#     pipe_group = pygame.sprite.Group()
#     for i in range(2):
#         pipes = get_random_pipes(SCREEN_WIDTH + i * 350)
#         pipe_group.add(pipes[0])
#         pipe_group.add(pipes[1])

#     # --- WAIT FOR START ---
#     begin = True
#     while begin:
#         clock.tick(15)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == KEYDOWN:
#                 if event.key in (K_SPACE, K_UP):
#                     bird.bump()
#                     wing_sound.play()
#                     begin = False
#                 elif event.key == K_F11:
#                     pygame.display.toggle_fullscreen()
#                 elif event.key == K_m:
#                     pygame.display.iconify()
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background()
#                 bird.update_scaled_image()

#         screen.blit(background, (0, 0))
#         bird.begin()
#         ground_group.update()
#         for ground in ground_group:
#             if is_off_screen(ground):
#                 ground_group.remove(ground)
#                 ground_group.add(Ground(SCREEN_WIDTH - 100))
#         bird_group.draw(screen)
#         ground_group.draw(screen)
#         pygame.display.update()

#     # --- GAME LOOP ---
#     score = 1
#     paused = False
#     while True:
#         clock.tick(15)
#         pause_btn, resume_btn = draw_buttons(paused)

#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background()
#                 bird.update_scaled_image()
#             elif event.type == KEYDOWN:
#                 if event.key in (K_SPACE, K_UP) and not paused:
#                     bird.bump()
#                     score += 1
#                     wing_sound.play()
#                 elif event.key == K_RETURN:  # Toggle pause on Enter
#                     paused = not paused
#                 elif event.key == K_p:
#                     paused = True
#                 elif event.key == K_r:
#                     paused = False
#                 elif event.key == K_p:
#                     paused = True
#                 elif event.key == K_r:
#                     paused = False
#                 elif event.key == K_F11:
#                     pygame.display.toggle_fullscreen()
#                 elif event.key == K_m:
#                     pygame.display.iconify()
#             elif event.type == MOUSEBUTTONDOWN:
#                 pos = pygame.mouse.get_pos()
#                 if not paused and pause_btn.collidepoint(pos):
#                     paused = True
#                 elif paused and resume_btn.collidepoint(pos):
#                     paused = False

#         screen.blit(background, (0, 0))

#         if not paused:
#             if is_off_screen(pipe_group.sprites()[0]):
#                 pipe_group.remove(pipe_group.sprites()[0])
#                 pipe_group.remove(pipe_group.sprites()[0])
#                 new_pipes = get_random_pipes(SCREEN_WIDTH + 300)
#                 pipe_group.add(new_pipes[0])
#                 pipe_group.add(new_pipes[1])

#             bird_group.update()
#             pipe_group.update()
#             ground_group.update()

#         bird_group.draw(screen)
#         pipe_group.draw(screen)
#         ground_group.draw(screen)

#         name_surface = font.render(player_name, True, (255, 255, 255))
#         score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
#         screen.blit(name_surface, (10, 20))
#         screen.blit(score_surface, (20, 70))

#         draw_buttons(paused)
#         pygame.display.update()

#         if not paused and (
#             pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
#             pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask) or
#             bird.rect.top <= 0 or
#             bird.rect.bottom >= SCREEN_HEIGHT
#         ):
#             hit_sound.play()
#             game_over = font.render("Game Over!", True, (255, 0, 0))
#             screen.blit(game_over, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
#             pygame.display.update()
#             time.sleep(1.5)
#             return

# # --- MAIN LOOP ---
# while True:
#     run_game()


import pygame, random, time
from pygame.locals import *
from model import init_db, save_score, get_top_scores
from settings import DB_PATH

# --- BASE DESIGN RESOLUTION ---
BASE_WIDTH = 1380
BASE_HEIGHT = 700

# --- GAME CONSTANTS (scalable) ---
SPEED = 19
GRAVITY = 2.5
PIPE_WIDTH = 100
PIPE_HEIGHT = 500
PIPE_GAP = 230  # This will now be dynamic based on level
GROUND_HEIGHT = 30
PIPE_DISTANCE = 400
COIN_SPAWN_CHANCE = 1    # Probability of a coin spawning with a new pipe (0.0 to 1.0), increased for testing
COIN_HORIZONTAL_RANGE = (100, BASE_WIDTH - 100) # Range for coin X position (was Y)
COIN_VERTICAL_CLEARANCE = 100 # Minimum vertical space from pipe edges for coins (Increased for more clearance)

# --- NEW COIN CONFIGURATION ---
NUM_COINS_PER_PIPE_GAP = 1 # Number of coins to potentially spawn in a gap
COIN_SPACING = 5          # Horizontal spacing between coins (Increased for larger coins)
COIN_SIZE_BASE = 100 # Base size for coin scaling (Increased for larger coins - WAS 70)

# --- SOUND FILES ---
WING_SOUND = 'assets/audio/wing.wav'
HIT_SOUND = 'assets/audio/hit.wav'
COIN_SOUND = 'assets/audio/point.wav'      # Assuming you have a coin sound, if not, it will be skipped
COIN_IMAGE = 'assets/sprites/coin.png'  # Path to your uploaded coin image

# --- INITIALIZE PYGAME ---
pygame.init()
pygame.mixer.init()
init_db()

# --- DISPLAY SETUP ---
SCREEN_WIDTH, SCREEN_HEIGHT = BASE_WIDTH, BASE_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('cutie birds Sky')

# --- FONT & CLOCK ---
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

# --- FRONT SPLASH SCREEN ---
front_image = pygame.image.load('assets/sprites/1message.png').convert()
front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
show_front = True

# Timer for the splash screen (4 seconds)
SPLASH_SCREEN_DURATION = 4000 # milliseconds
pygame.time.set_timer(USEREVENT + 1, SPLASH_SCREEN_DURATION) # Set a custom event to trigger after 4 seconds

while show_front:
    screen.blit(front_image, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); exit()
        elif event.type in (KEYDOWN, MOUSEBUTTONDOWN): # User can still click/key to skip
            show_front = False
            pygame.time.set_timer(USEREVENT + 1, 0) # Disable the timer if user skips
        elif event.type == USEREVENT + 1: # Timer expired
            show_front = False
            pygame.time.set_timer(USEREVENT + 1, 0) # Disable the timer
        elif event.type == VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# --- LOAD SOUNDS ---
wing_sound = pygame.mixer.Sound(WING_SOUND)
hit_sound = pygame.mixer.Sound(HIT_SOUND)
try:
    coin_sound = pygame.mixer.Sound(COIN_SOUND)
except pygame.error:
    coin_sound = None  # If sound file is missing, just don't play it

pipe_color_toggle = True

def scale_img(image, w, h):
    return pygame.transform.scale(image, (int(w), int(h)))

def get_scale():
    return SCREEN_HEIGHT / BASE_HEIGHT

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_images = [
            pygame.image.load('assets/sprites/18upflap.png').convert_alpha(),
            pygame.image.load('assets/sprites/18midflap.png').convert_alpha(),
            pygame.image.load('assets/sprites/18downflap.png').convert_alpha()
        ]
        self.current_image = 0
        self.update_scaled_image()
        self.speed = SPEED


    def update_scaled_image(self):
        scale = get_scale()
        self.images = [scale_img(img, 70 * scale, 70 * scale) for img in self.original_images]
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        # Ensure rect is created or updated
        if not hasattr(self, 'rect'):
            self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))
        else:
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)


    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect.y += int(self.speed)

    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize, color='red', game_speed=25):
        super().__init__()
        scale = get_scale()
        image = pygame.image.load(f'assets/sprites/pipe-{color}.png').convert_alpha()
        self.image = scale_img(image, PIPE_WIDTH * scale, PIPE_HEIGHT * scale)
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect()
            self.rect.x = xpos
            self.rect.y = -(self.rect.height - ysize)
        else:
            self.rect = self.image.get_rect()
            self.rect.x = xpos
            self.rect.y = SCREEN_HEIGHT - ysize
        self.mask = pygame.mask.from_surface(self.image)
        self.game_speed = game_speed
        self.passed = False

    def update(self):
        self.rect.x -= self.game_speed

    def update_speed(self, new_speed):
        self.game_speed = new_speed

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos, initial_game_speed):
        super().__init__()
        image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        scale = get_scale()
        self.image = scale_img(image, 2 * SCREEN_WIDTH, GROUND_HEIGHT * scale)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = SCREEN_HEIGHT - int(GROUND_HEIGHT * scale)
        self.mask = pygame.mask.from_surface(self.image)
        self.current_game_speed = initial_game_speed

    def update(self):
        self.rect.x -= self.current_game_speed

    def update_speed(self, new_speed):
        self.current_game_speed = new_speed

class Coin(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, game_speed):
        super().__init__()
        self.original_image = pygame.image.load("assets/sprites/coin.png").convert_alpha()
        self.value = 1 # Each coin adds 1 to the collected_coins count

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

        self.update_scaled_image()
        self.game_speed = game_speed

    def update_scaled_image(self):
        scale = get_scale()
        # Store current center to maintain position after scaling
        if hasattr(self, 'rect'):
            old_center = self.rect.center
        else:
            old_center = (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)

        self.image = scale_img(self.original_image, COIN_SIZE_BASE * scale, COIN_SIZE_BASE * scale)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=old_center)

    def update(self):
        self.rect.x -= self.game_speed

    def update_speed(self, new_speed):
        self.game_speed = new_speed

def is_off_screen(sprite):
    return sprite.rect.right < 0

def get_random_pipes(xpos, pipe_gap, current_game_speed):
    global pipe_color_toggle
    size = random.randint(150, 300)
    color = 'green' if pipe_color_toggle else 'red'
    pipe_color_toggle = not pipe_color_toggle
    return Pipe(False, xpos, size, color, current_game_speed), Pipe(True, xpos, SCREEN_HEIGHT - size - pipe_gap, color, current_game_speed)

def draw_buttons(paused):
    pause_button = pygame.Rect(SCREEN_WIDTH - 140, 20, 100, 40)
    resume_button = pygame.Rect(SCREEN_WIDTH - 140, 70, 100, 40)
    back_button = None # Initialize back_button

    if not paused:
        pygame.draw.rect(screen, (50, 50, 50), pause_button)
        screen.blit(font.render("Pause", True, (255, 255, 255)), (SCREEN_WIDTH - 130, 25))
    else:
        pygame.draw.rect(screen, (50, 50, 50), resume_button)
        screen.blit(font.render("Resume", True, (255, 255, 255)), (SCREEN_WIDTH - 130, 75))
        
        # Draw the "Back" button when paused
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50)
        draw_3d_button(back_button, "Back")

    return pause_button, resume_button, back_button # Return back_button

def draw_3d_button(rect, text):
    shadow_color = (30, 30, 30)
    highlight_color = (200, 200, 200)
    base_color = (100, 100, 255)
    text_color = (255, 255, 255)

    # Shadow
    shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
    pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=10)

    # Highlight
    highlight_rect = pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4)
    pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=10)

    # Main button
    pygame.draw.rect(screen, base_color, rect, border_radius=10)

    # Text
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def run_game():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen

    # Load and scale the background for the game (scrolling)
    GAME_BACKGROUND = pygame.image.load('assets/sprites/background3.png').convert()
    def rescale_game_background():
        # Change this to scale only to SCREEN_WIDTH, not SCREEN_WIDTH * 2,
        # if you want a static background without scrolling.
        return scale_img(GAME_BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Load and scale the static background for home/name input screens
    STATIC_BACKGROUND = pygame.image.load('assets/sprites/1background-P.png').convert() # You can change this to a different image if you want a distinct static background
    def rescale_static_background():
        return scale_img(STATIC_BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    game_background = rescale_game_background()
    static_background = rescale_static_background()

    top_scores = get_top_scores(limit=3)

    # Home screen name input
    player_name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            elif event.type == VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                game_background = rescale_game_background() # Re-scale for potential future use if game_background is used later
                static_background = rescale_static_background() # Rescale static background
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == K_RETURN and len(player_name) > 0:
                    input_active = False
                elif len(player_name) < 10 and event.unicode.isprintable():
                    player_name += event.unicode

        # --- Draw static background for name input screen ---
        screen.blit(static_background, (0, 0))

        prompt = font.render("Enter your Name: " + player_name, True, (255, 255, 255))
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3)) # Center the prompt
        screen.blit(prompt, prompt_rect)
        pygame.display.update()

    # Home screen with scores and buttons
    home_active = True

    while home_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            elif event.type == MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    home_active = False
                elif exit_button.collidepoint(event.pos):
                    pygame.quit(); exit()
            elif event.type == VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                game_background = rescale_game_background() # Re-scale for potential future use if game_background is used later
                static_background = rescale_static_background() # Rescale static background

        # --- Draw static background for home screen ---
        screen.blit(static_background, (0, 0))

        # Buttons
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 160, 200, 50)
        draw_3d_button(start_button, "Start Game")
        draw_3d_button(exit_button, "Exit")

        # Top Scores Title
        title_surface = font.render("Top Scores:", True, (255, 255, 0))
        screen.blit(title_surface, (50, 40))
        # Table
        table_x, table_y = 50, 80
        col_widths = [80, 200, 120]
        row_height = 50
        headers = ["Sr", "Name", "Score",]
        for col, text in enumerate(headers):
            cell = pygame.Rect(table_x + sum(col_widths[:col]), table_y, col_widths[col], row_height)
            pygame.draw.rect(screen, (200, 200, 200), cell, 2)
            screen.blit(font.render(text, True, (255, 255, 0)), (cell.x+10, cell.y+10))
        for i, (name, score_val) in enumerate(top_scores):
            for col, val in enumerate([str(i+1), name, str(score_val)]):
                cell = pygame.Rect(table_x + sum(col_widths[:col]), table_y+(i+1)*row_height, col_widths[col], row_height)
                pygame.draw.rect(screen, (255, 255, 255), cell, 2)
                screen.blit(font.render(val, True, (255, 255, 255)), (cell.x+10, cell.y+10))
        pygame.display.update()

    # Rest of your game setup and main game loop remains the same
    # ... (no changes below this point for your request)
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird.update_scaled_image()
    bird_group.add(bird)

    game_level = 1
    current_game_speed = 25
    current_pipe_gap = 230

    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground_group.add(Ground(SCREEN_WIDTH * i, current_game_speed))

    pipe_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()

    for i in range(2):
        p1, p2 = get_random_pipes(SCREEN_WIDTH + i * PIPE_DISTANCE, current_pipe_gap, current_game_speed)
        p1.passed = False
        p2.passed = False
        pipe_group.add(p1); pipe_group.add(p2)

        if random.random() < COIN_SPAWN_CHANCE:
            gap_top = p1.rect.y + p1.rect.height
            gap_bottom = p2.rect.y
            
            scaled_coin_width = COIN_SIZE_BASE * get_scale()
            scaled_coin_height = COIN_SIZE_BASE * get_scale()
            vertical_clearance = COIN_VERTICAL_CLEARANCE * get_scale()

            available_vertical_space = gap_bottom - gap_top
            
            if available_vertical_space >= scaled_coin_height + (2 * vertical_clearance):
                center_y_in_gap = gap_top + (available_vertical_space / 2)
                coin_y = center_y_in_gap - (scaled_coin_height / 2)
                
                if coin_y < gap_top + vertical_clearance:
                    coin_y = gap_top + vertical_clearance
                elif coin_y + scaled_coin_height > gap_bottom - vertical_clearance:
                    coin_y = gap_bottom - vertical_clearance - scaled_coin_height
            else:
                coin_y = gap_top + (available_vertical_space / 2) - (scaled_coin_height / 2)

            total_coin_row_width = (NUM_COINS_PER_PIPE_GAP * scaled_coin_width) + \
                                   ((NUM_COINS_PER_PIPE_GAP - 1) * COIN_SPACING * get_scale())

            pipe_spawn_x = p1.rect.x
            system_center_x = pipe_spawn_x + (PIPE_WIDTH * get_scale() / 2)
            start_x_for_coins = system_center_x - (total_coin_row_width / 2)

            for j in range(NUM_COINS_PER_PIPE_GAP):
                coin_x = start_x_for_coins + j * (scaled_coin_width + COIN_SPACING * get_scale())
                coin_x = max(int(COIN_HORIZONTAL_RANGE[0] * get_scale()), coin_x)
                coin_x = min(int(COIN_HORIZONTAL_RANGE[1] * get_scale()) - int(scaled_coin_width), coin_x)
                coin_group.add(Coin(coin_x, coin_y, current_game_speed))

    begin = True
    while begin:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            elif event.type in (KEYDOWN,) and event.key in (K_SPACE, K_UP):
                bird.bump(); wing_sound.play(); begin = False
            elif event.type == VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                game_background = rescale_game_background(); bird.update_scaled_image()
                for p in pipe_group:
                    p.image = scale_img(pygame.image.load(f'assets/sprites/pipe-{"green" if pipe_color_toggle else "red"}.png').convert_alpha(), PIPE_WIDTH * get_scale(), PIPE_HEIGHT * get_scale())
                    p.mask = pygame.mask.from_surface(p.image)
                    p.rect.x = int(p.rect.x * (SCREEN_WIDTH / BASE_WIDTH))  
                    if p.rect.y < 0:
                        p.rect.y = -(p.image.get_height() - (SCREEN_HEIGHT - p.rect.bottom - current_pipe_gap))
                    else:
                        p.rect.y = SCREEN_HEIGHT - p.image.get_height()
                    p.update_speed(current_game_speed)
                for g in ground_group:
                    g.image = scale_img(pygame.image.load('assets/sprites/base.png').convert_alpha(), 2 * SCREEN_WIDTH, GROUND_HEIGHT * get_scale())
                    g.rect.y = SCREEN_HEIGHT - int(GROUND_HEIGHT * get_scale())
                    g.update_speed(current_game_speed)
                for c in coin_group:
                    c.update_scaled_image()
                    c.update_speed(current_game_speed)

        # --- Draw static background for begin screen ---
        screen.blit(static_background, (0, 0))

        bird.begin();
        for g in ground_group:
            g.update_speed(current_game_speed)
            g.update()
            if is_off_screen(g):
                rightmost_g = max(ground_group, key=lambda x: x.rect.x)
                g.rect.x = rightmost_g.rect.x + rightmost_g.rect.width - current_game_speed
                g.update_speed(current_game_speed)
        bird_group.draw(screen); ground_group.draw(screen);
        pygame.display.update()

    # Main game loop
    score = 0
    collected_coins = 0 # Variable to track collected coins
    paused = False

    score_change_message = ""
    message_timer = 0
    MESSAGE_DURATION = 60
    JUMP_SCORE_INCREMENT = 1 # Score added per jump

    while True:
        clock.tick(15)

        if message_timer > 0:
            message_timer -= 1
        else:
            score_change_message = ""

        pause_btn, resume_btn, back_btn = draw_buttons(paused)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            elif event.type == VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                # Instead of rescale_game_background, you would rescale the static background for the game here
                game_background = rescale_game_background() # Now it will just be SCREEN_WIDTH wide
                bird.update_scaled_image()

                for p in pipe_group:
                    p.image = scale_img(pygame.image.load(f'assets/sprites/pipe-{"green" if pipe_color_toggle else "red"}.png').convert_alpha(), PIPE_WIDTH * get_scale(), PIPE_HEIGHT * get_scale())
                    p.mask = pygame.mask.from_surface(p.image)
                    p.rect.x = int(p.rect.x * (SCREEN_WIDTH / BASE_WIDTH))
                    if p.rect.y < 0:
                        p.rect.y = -(p.image.get_height() - (SCREEN_HEIGHT - p.rect.bottom - current_pipe_gap))
                    else:
                        p.rect.y = SCREEN_HEIGHT - p.image.get_height()
                    p.update_speed(current_game_speed)

                for g in ground_group:
                    g.image = scale_img(pygame.image.load('assets/sprites/base.png').convert_alpha(), 2 * SCREEN_WIDTH, GROUND_HEIGHT * get_scale())
                    g.rect.y = SCREEN_HEIGHT - int(GROUND_HEIGHT * get_scale())
                    g.update_speed(current_game_speed)
                for c in coin_group:
                    c.update_scaled_image()
                    c.update_speed(current_game_speed)

            elif event.type == KEYDOWN:
                if event.key in (K_SPACE, K_UP) and not paused:
                    bird.bump()
                    wing_sound.play()
                    # --- NEW: Increase score on jump ---
                    score += JUMP_SCORE_INCREMENT
                    #score_change_message = f"Jump! (+{JUMP_SCORE_INCREMENT})"
                    message_timer = MESSAGE_DURATION
                elif event.key == K_RETURN:
                    paused = not paused
            elif event.type == MOUSEBUTTONDOWN:
                if not paused and pause_btn.collidepoint(event.pos):
                    paused = True
                elif paused and resume_btn.collidepoint(event.pos):
                    paused = False
                elif paused and back_btn and back_btn.collidepoint(event.pos):
                    return

        # --- Draw the static background for the main game loop ---
        # The background will no longer scroll, so just blit it at (0,0)
        screen.blit(game_background, (0, 0)) # Using game_background, but it's now scaled to SCREEN_WIDTH

        if not paused:
            for p in pipe_group.sprites():
                if p.rect.right < bird.rect.left and not p.passed:
                    p.passed = True
                    score += 1 # Score for passing a pipe
                    score_change_message = " " # Clears previous message if any
                    message_timer = MESSAGE_DURATION

                    if score > 0 and score % 20 == 0: # Level increases every 20 points
                        game_level += 1
                        current_game_speed = 25 + (game_level - 1) * 5
                        current_pipe_gap = max(150, 230 - (game_level - 1) * 10)
                        for pipe_sprite in pipe_group:
                            pipe_sprite.update_speed(current_game_speed)
                        for ground_sprite in ground_group:
                            ground_sprite.update_speed(current_game_speed)
                        for coin_sprite in coin_group:
                            coin_sprite.update_speed(current_game_speed)
                        break # Break out of inner loop after updating speed to prevent multiple level ups in one frame

            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0]); pipe_group.remove(pipe_group.sprites()[0])
                p1, p2 = get_random_pipes(SCREEN_WIDTH + PIPE_DISTANCE, current_pipe_gap, current_game_speed)
                p1.passed = False
                p2.passed = False
                pipe_group.add(p1); pipe_group.add(p2)

                if random.random() < COIN_SPAWN_CHANCE:
                    gap_top = p1.rect.y + p1.rect.height
                    gap_bottom = p2.rect.y
                    
                    scaled_coin_width = COIN_SIZE_BASE * get_scale()
                    scaled_coin_height = COIN_SIZE_BASE * get_scale()
                    vertical_clearance = COIN_VERTICAL_CLEARANCE * get_scale()

                    available_vertical_space = gap_bottom - gap_top
                    
                    if available_vertical_space >= scaled_coin_height + (2 * vertical_clearance):
                        center_y_in_gap = gap_top + (available_vertical_space / 2)
                        coin_y = center_y_in_gap - (scaled_coin_height / 2)
                        
                        if coin_y < gap_top + vertical_clearance:
                            coin_y = gap_top + vertical_clearance
                        elif coin_y + scaled_coin_height > gap_bottom - vertical_clearance:
                            coin_y = gap_bottom - vertical_clearance - scaled_coin_height
                    else:
                        coin_y = gap_top + (available_vertical_space / 2) - (scaled_coin_height / 2)

                    total_coin_row_width = (NUM_COINS_PER_PIPE_GAP * scaled_coin_width) + \
                                           ((NUM_COINS_PER_PIPE_GAP - 1) * COIN_SPACING * get_scale())

                    pipe_spawn_x = p1.rect.x
                    system_center_x = pipe_spawn_x + (PIPE_WIDTH * get_scale() / 2)
                    start_x_for_coins = system_center_x - (total_coin_row_width / 2)

                    for j in range(NUM_COINS_PER_PIPE_GAP):
                        coin_x = start_x_for_coins + j * (scaled_coin_width + COIN_SPACING * get_scale())
                        coin_x = max(int(COIN_HORIZONTAL_RANGE[0] * get_scale()), coin_x)
                        coin_x = min(int(COIN_HORIZONTAL_RANGE[1] * get_scale()) - int(scaled_coin_width), coin_x)
                        coin_group.add(Coin(coin_x, coin_y, current_game_speed))

            for coin_sprite in coin_group.copy():
                if is_off_screen(coin_sprite):
                    coin_group.remove(coin_sprite)

            bird_group.update()
            pipe_group.update()
            ground_group.update()
            coin_group.update()

            for g in ground_group:
                if is_off_screen(g):
                    rightmost_g = max(ground_group, key=lambda x: x.rect.x)
                    g.rect.x = rightmost_g.rect.x + rightmost_g.rect.width - current_game_speed
                    g.update_speed(current_game_speed)

            collected_coins_dict = pygame.sprite.groupcollide(bird_group, coin_group, False, True, pygame.sprite.collide_mask)
            if collected_coins_dict:
                for bird_sprite, collected_coin_list in collected_coins_dict.items():
                    for collected_coin in collected_coin_list:
                        collected_coins += collected_coin.value # Increment collected_coins
                        score += collected_coin.value # Also add to main score
                        if coin_sound:
                            coin_sound.play()
                        score_change_message = f"Coin collected! (+{collected_coin.value})" # More specific message
                        message_timer = MESSAGE_DURATION

        bird_group.draw(screen); pipe_group.draw(screen); ground_group.draw(screen); coin_group.draw(screen)
        screen.blit(font.render(player_name, True, (255, 255, 255)), (10, 20))
        screen.blit(font.render(f"scores: {score}", True, (255, 255, 255)), (20, 70)) # Renamed for clarity
        screen.blit(font.render(f"Coins scores: {collected_coins}", True, (255, 255, 255)), (20, 120)) # New display for coins
        screen.blit(font.render(f"Level: {game_level}", True, (255, 255, 255)), (20, 170)) # Adjusted Y position

        if score_change_message:
            message_surface = font.render(score_change_message, True, (0, 255, 0))
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(message_surface, message_rect)

        draw_buttons(paused)
        pygame.display.update()

        if not paused and (
            pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask) or
            bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT
        ):
            hit_sound.play()

            game_over_font = pygame.font.Font(None, 75)
            small_font = pygame.font.Font(None, 40)

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
            player_score_text = small_font.render(f"Player: {player_name}", True, (255, 255, 255))
            pipes_passed_text = small_font.render(f"Scores: {score - collected_coins}", True, (255, 255, 255)) # Display pipes passed (total score - coins)
            coins_collected_text = small_font.render(f"Coins scores: {collected_coins}", True, (255, 255, 255)) # Display coins collected
            final_score_text = small_font.render(f"Final Score: {score}", True, (255, 255, 255)) # Total score including jumps, pipes, and coins
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)) # Adjusted Y
            player_score_rect = player_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)) # Adjusted Y
            pipes_passed_rect = pipes_passed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)) # New Y
            coins_collected_rect = coins_collected_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)) # New Y
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110)) # New Y

            screen.blit(game_over_text, game_over_rect)
            screen.blit(player_score_text, player_score_rect)
            screen.blit(pipes_passed_text, pipes_passed_rect)
            screen.blit(coins_collected_text, coins_collected_rect)
            screen.blit(final_score_text, final_score_rect)

            pygame.display.update()

            # Save the combined score for ranking (jumps + pipes + coins)
            save_score(player_name, score) 

            time.sleep(2)  
            return

# MAIN LOOP
while True:
    run_game()