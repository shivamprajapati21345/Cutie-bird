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
# # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)

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
#         elif event.type in (KEYDOWN, MOUSEBUTTONDOWN):
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

# def draw_3d_button(rect, text):
#     shadow_color = (30, 30, 30)
#     highlight_color = (200, 200, 200)
#     base_color = (100, 100, 255)
#     text_color = (255, 255, 255)

#     # Shadow
#     shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
#     pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=10)

#     # Highlight
#     highlight_rect = pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4)
#     pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=10)

#     # Main button
#     pygame.draw.rect(screen, base_color, rect, border_radius=10)

#     # Text
#     label = font.render(text, True, text_color)
#     label_rect = label.get_rect(center=rect.center)
#     screen.blit(label, label_rect)

# def run_game():
#     global SCREEN_WIDTH, SCREEN_HEIGHT, screen

#     BACKGROUND = pygame.image.load('assets/sprites/1background-P.png').convert()
#     def rescale_background():
#         return scale_img(BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)
#     background = rescale_background()
#     top_scores = get_top_scores(limit=3)

#     # Home screen name input
#     player_name = ""
#     input_active = True
#     while input_active:
#         screen.blit(background, (0, 0))
#         prompt = font.render("Enter Name: " + player_name, True, (255, 255, 255))
#         screen.blit(prompt, (SCREEN_WIDTH//4, SCREEN_HEIGHT//3))
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background()
#             elif event.type == KEYDOWN:
#                 if event.key == K_BACKSPACE:
#                     player_name = player_name[:-1]
#                 elif event.key == K_RETURN and len(player_name) > 0:
#                     input_active = False
#                 elif len(player_name) < 10 and event.unicode.isprintable():
#                     player_name += event.unicode

#     # Home screen with scores and buttons
#     home_active = True
    
#     while home_active:
#         screen.blit(background, (0, 0))
#         # Buttons
#         start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
#         exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 160, 200, 50)
#         # screen.blit(font.render("Start Game", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 110))
#         # screen.blit(font.render("Exit", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 170))
#         draw_3d_button(start_button, "Start Game")
#         draw_3d_button(exit_button, "Exit")

#         # Top Scores Title
#         title_surface = font.render("Top Scores:", True, (255, 255, 0))
#         screen.blit(title_surface, (50, 40))
#         # Table
#         table_x, table_y = 50, 80
#         col_widths = [80, 200, 120]
#         row_height = 50
#         headers = ["Sr", "Name", "Score"]
#         for col, text in enumerate(headers):
#             cell = pygame.Rect(table_x + sum(col_widths[:col]), table_y, col_widths[col], row_height)
#             pygame.draw.rect(screen, (200, 200, 200), cell, 2)
#             screen.blit(font.render(text, True, (255, 255, 0)), (cell.x+10, cell.y+10))
#         for i, (name, score) in enumerate(top_scores):
#             for col, val in enumerate([str(i+1), name, str(score)]):
#                 cell = pygame.Rect(table_x + sum(col_widths[:col]), table_y+(i+1)*row_height, col_widths[col], row_height)
#                 pygame.draw.rect(screen, (255, 255, 255), cell, 2)
#                 screen.blit(font.render(val, True, (255, 255, 255)), (cell.x+10, cell.y+10))
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == MOUSEBUTTONDOWN:
#                 if start_button.collidepoint(event.pos):
#                     home_active = False
#                 elif exit_button.collidepoint(event.pos):
#                     pygame.quit(); exit()
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background()

#     # Game setup...
#     bird_group = pygame.sprite.Group()
#     bird = Bird()
#     bird.update_scaled_image()
#     bird_group.add(bird)
#     ground_group = pygame.sprite.Group()
#     for i in range(2): ground_group.add(Ground(SCREEN_WIDTH * i))
#     pipe_group = pygame.sprite.Group()
#     for i in range(2):
#         p1, p2 = get_random_pipes(SCREEN_WIDTH + i * 350)
#         pipe_group.add(p1); pipe_group.add(p2)

#     # Begin flap loop
#     begin = True
#     while begin:
#         clock.tick(15)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type in (KEYDOWN,) and event.key in (K_SPACE, K_UP):
#                 bird.bump(); wing_sound.play(); begin = False
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background(); bird.update_scaled_image()
#         screen.blit(background, (0, 0)); bird.begin(); ground_group.update()
#         for g in ground_group:
#             if is_off_screen(g): ground_group.remove(g); ground_group.add(Ground(SCREEN_WIDTH - 100))
#         bird_group.draw(screen); ground_group.draw(screen);
#         pygame.display.update()

#     # Main game loop
#     score = 1; paused = False
#     while True:
#         clock.tick(15)
#         pause_btn, resume_btn = draw_buttons(paused)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit(); exit()
#             elif event.type == VIDEORESIZE:
#                 SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
#                 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
#                 background = rescale_background(); bird.update_scaled_image()
#             elif event.type == KEYDOWN:
#                 if event.key in (K_SPACE, K_UP) and not paused:
#                     bird.bump(); score += 1; wing_sound.play()
#                 elif event.key == K_RETURN:
#                     paused = not paused
#             elif event.type == MOUSEBUTTONDOWN:
#                 if not paused and pause_btn.collidepoint(event.pos): paused = True
#                 elif paused and resume_btn.collidepoint(event.pos): paused = False

#         screen.blit(background, (0, 0))
#         if not paused:
#             if is_off_screen(pipe_group.sprites()[0]):
#                 pipe_group.remove(pipe_group.sprites()[0]); pipe_group.remove(pipe_group.sprites()[0])
#                 p1, p2 = get_random_pipes(SCREEN_WIDTH + PIPE_DISTANCE)
#                 pipe_group.add(p1); pipe_group.add(p2)
#             bird_group.update(); pipe_group.update(); ground_group.update()

#         bird_group.draw(screen); pipe_group.draw(screen); ground_group.draw(screen)
#         screen.blit(font.render(player_name, True, (255, 255, 255)), (10, 20))
#         screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (20, 70))
#         draw_buttons(paused)
#         pygame.display.update()

#         # Collision or bounds check
#         if not paused and (
#             pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
#             pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask) or
#             bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT
#         ):
#             hit_sound.play()
#             screen.blit(font.render("Game Over!", True, (255, 0, 0)), (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
#             pygame.display.update(); time.sleep(1.5)
#             save_score(player_name, score)
#             return

# # MAIN LOOP
# while True:
#     run_game()
import pygame, random, time
from pygame.locals import *
from model import init_db, save_score, get_top_scores
from settings import DB_PATH

# --- Game Constants ---
BASE_WIDTH, BASE_HEIGHT = 1380, 700
SPEED, GRAVITY = 20, 2.5
PIPE_WIDTH, PIPE_HEIGHT, PIPE_GAP = 100, 500, 230
GROUND_HEIGHT, PIPE_DISTANCE = 30, 400
WING_SOUND, HIT_SOUND = 'assets/audio/wing.wav', 'assets/audio/hit.wav'

pygame.init(); pygame.mixer.init(); init_db()
SCREEN_WIDTH, SCREEN_HEIGHT = BASE_WIDTH, BASE_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('cutie birds Sky')
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

wing_sound = pygame.mixer.Sound(WING_SOUND)
hit_sound = pygame.mixer.Sound(HIT_SOUND)
pipe_color_toggle = True
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

# --- FRONT SPLASH SCREEN ---
front_image = pygame.image.load('assets/sprites/1message.png').convert()
front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
show_front = True

while show_front:
    screen.blit(front_image, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); exit()
        elif event.type in (KEYDOWN, MOUSEBUTTONDOWN):
            show_front = False
        elif event.type == VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def scale_img(img, w, h):
    return pygame.transform.scale(img, (int(w), int(h)))

def get_scale():
    return SCREEN_HEIGHT / BASE_HEIGHT

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_images = [pygame.image.load(f'assets/sprites/18{flap}flap.png').convert_alpha() for flap in ['up','mid','down']]
        self.current_image, self.speed = 0, SPEED
        self.update_scaled_image()

    def update_scaled_image(self):
        scale = get_scale()
        self.images = [scale_img(i, 70*scale, 70*scale) for i in self.original_images]
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//6, SCREEN_HEIGHT//2))
        self.mask = pygame.mask.from_surface(self.image)

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
        img = pygame.image.load(f'assets/sprites/pipe-{color}.png').convert_alpha()
        self.image = scale_img(img, PIPE_WIDTH * scale, PIPE_HEIGHT * scale)
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(x=xpos, y=-(self.image.get_height() - ysize))
        else:
            self.rect = self.image.get_rect(x=xpos, y=SCREEN_HEIGHT - ysize)
        self.mask = pygame.mask.from_surface(self.image)
        self.game_speed = game_speed
        self.passed = False

    def update(self):
        self.rect.x -= self.game_speed

    def update_speed(self, new_speed):
        self.game_speed = new_speed

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos, game_speed):
        super().__init__()
        scale = get_scale()
        img = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = scale_img(img, 2 * SCREEN_WIDTH, GROUND_HEIGHT * scale)
        self.rect = self.image.get_rect(x=xpos, y=SCREEN_HEIGHT - int(GROUND_HEIGHT * scale))
        self.mask = pygame.mask.from_surface(self.image)
        self.current_game_speed = game_speed

    def update(self):
        self.rect.x -= self.current_game_speed

    def update_speed(self, new_speed):
        self.current_game_speed = new_speed

def is_off_screen(sprite):
    return sprite.rect.right < 0

def get_random_pipes(xpos, gap, speed):
    global pipe_color_toggle
    size = random.randint(150, 300)
    color = 'green' if pipe_color_toggle else 'red'
    pipe_color_toggle = not pipe_color_toggle
    return (
        Pipe(False, xpos, size, color, speed),
        Pipe(True, xpos, SCREEN_HEIGHT - size - gap, color, speed)
    )

def draw_buttons(paused):
    pause_btn = pygame.Rect(SCREEN_WIDTH - 140, 20, 100, 40)
    resume_btn = pygame.Rect(SCREEN_WIDTH - 140, 70, 100, 40)
    back_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40, 200, 50) if paused else pause_btn
    if not paused:
        pygame.draw.rect(screen, (50,50,50), pause_btn)
        screen.blit(font.render("Pause", 1, (255,255,255)), (pause_btn.x+10, pause_btn.y+5))
    else:
        pygame.draw.rect(screen, (50,50,50), resume_btn)
        screen.blit(font.render("Resume", 1, (255,255,255)), (resume_btn.x+10, resume_btn.y+5))
        draw_3d_button(back_btn, "Back")
    return pause_btn, resume_btn, back_btn

def draw_3d_button(rect, text):
    pygame.draw.rect(screen, (30,30,30), pygame.Rect(rect.x+4, rect.y+4, rect.width, rect.height), border_radius=10)
    pygame.draw.rect(screen, (200,200,200), pygame.Rect(rect.x-2, rect.y-2, rect.width+4, rect.height+4), border_radius=10)
    pygame.draw.rect(screen, (100,100,255), rect, border_radius=10)
    label = font.render(text, True, (255,255,255))
    screen.blit(label, label.get_rect(center=rect.center))

def show_home_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen
    BACKGROUND = pygame.image.load('assets/sprites/1background-P.png').convert()
    background = scale_img(BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)
    top_scores = get_top_scores(limit=3)
    name = ""; active = True

    while active:
        screen.blit(background, (0, 0))
        prompt = font.render("Enter Name: " + name, True, (255,255,255))
        screen.blit(prompt, (SCREEN_WIDTH//4, SCREEN_HEIGHT//3))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: pygame.quit(); exit()
            elif e.type == VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = e.w, e.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                background = scale_img(BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)
            elif e.type == KEYDOWN:
                if e.key == K_BACKSPACE: name = name[:-1]
                elif e.key == K_RETURN and name: active = False
                elif len(name) < 10 and e.unicode.isprintable(): name += e.unicode

    while True:
        screen.blit(background, (0, 0))
        sb = pygame.Rect(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+100, 200, 50)
        eb = pygame.Rect(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+160, 200, 50)
        draw_3d_button(sb, "Start Game")
        draw_3d_button(eb, "Exit")
        screen.blit(font.render("Top Scores:", 1, (255,255,0)), (50,40))
        cols = [80, 200, 120]; headers = ["Sr", "Name", "Score"]
        for i, h in enumerate(headers):
            r = pygame.Rect(50 + sum(cols[:i]), 80, cols[i], 50)
            pygame.draw.rect(screen, (200,200,200), r, 2)
            screen.blit(font.render(h, 1, (255,255,0)), (r.x+10, r.y+10))
        for i, (n, s) in enumerate(top_scores):
            for j, val in enumerate([str(i+1), n, str(s)]):
                r = pygame.Rect(50 + sum(cols[:j]), 80+(i+1)*50, cols[j], 50)
                pygame.draw.rect(screen, (255,255,255), r, 2)
                screen.blit(font.render(val, 1, (255,255,255)), (r.x+10, r.y+10))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: pygame.quit(); exit()
            elif e.type == MOUSEBUTTONDOWN:
                if sb.collidepoint(e.pos): return name
                elif eb.collidepoint(e.pos): pygame.quit(); exit()
            elif e.type == VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = e.w, e.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                background = scale_img(BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)

def run_game(player_name):
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen
    BACKGROUND = pygame.image.load('assets/sprites/1background-P.png').convert()
    background = scale_img(BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)
    bird_group = pygame.sprite.Group(); bird = Bird(); bird_group.add(bird)
    game_level, score, current_speed, pipe_gap = 1, 0, 25, 230

    pipe_group = pygame.sprite.Group()
    for i in range(2):
        p1, p2 = get_random_pipes(SCREEN_WIDTH + i * PIPE_DISTANCE, pipe_gap, current_speed)
        pipe_group.add(p1); pipe_group.add(p2)

    ground_group = pygame.sprite.Group()
    for i in range(2): ground_group.add(Ground(SCREEN_WIDTH*i, current_speed))

    begin = True
    while begin:
        clock.tick(15)
        for e in pygame.event.get():
            if e.type == QUIT: pygame.quit(); exit()
            elif e.type == KEYDOWN and e.key in (K_SPACE, K_UP): bird.bump(); wing_sound.play(); begin = False
        screen.blit(background, (0, 0)); bird.begin()
        for g in ground_group: g.update(); screen.blit(g.image, g.rect)
        bird_group.draw(screen); pygame.display.update()

    paused = False
    while True:
        clock.tick(15)
        pause_btn, resume_btn, back_btn = draw_buttons(paused)
        for e in pygame.event.get():
            if e.type == QUIT: pygame.quit(); exit()
            elif e.type == VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = e.w, e.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                background = scale_img(BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT); bird.update_scaled_image()
            elif e.type == KEYDOWN:
                if e.key in (K_SPACE, K_UP) and not paused: bird.bump(); wing_sound.play()
                elif e.key == K_RETURN: paused = not paused
            elif e.type == MOUSEBUTTONDOWN:
                if not paused and pause_btn.collidepoint(e.pos): paused = True
                elif paused and resume_btn.collidepoint(e.pos): paused = False
                elif paused and back_btn.collidepoint(e.pos):
                    save_score(player_name, score)
                    return  # Go back to score screen (home)

        if not paused:
            for p in pipe_group:
                if p.rect.right < bird.rect.left and not p.passed:
                    score += 1; p.passed = True
                    if score % 10 == 0:
                        game_level += 1
                        current_speed = 25 + (game_level - 1) * 5
                        pipe_gap = max(150, 230 - (game_level - 1) * 10)
                        for g in ground_group: g.update_speed(current_speed)
                        for p in pipe_group: p.update_speed(current_speed)
                    break
            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0]); pipe_group.remove(pipe_group.sprites()[0])
                p1, p2 = get_random_pipes(SCREEN_WIDTH + PIPE_DISTANCE, pipe_gap, current_speed)
                pipe_group.add(p1); pipe_group.add(p2)
            bird_group.update(); pipe_group.update(); ground_group.update()
            for g in ground_group:
                if is_off_screen(g):
                    r = max(ground_group, key=lambda x: x.rect.x)
                    g.rect.x = r.rect.x + r.rect.width - current_speed

        screen.blit(background, (0,0))
        bird_group.draw(screen); pipe_group.draw(screen); ground_group.draw(screen)
        screen.blit(font.render(player_name, 1, (255,255,255)), (10,20))
        screen.blit(font.render(f"Score: {score}", 1, (255,255,255)), (20,70))
        screen.blit(font.render(f"Level: {game_level}", 1, (255,255,255)), (20,120))
        draw_buttons(paused)
        pygame.display.update()

        if not paused and (
            pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask) or
            bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT):
            hit_sound.play()
            screen.blit(font.render("Game Over!", 1, (255, 0, 0)), (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            pygame.display.update(); time.sleep(1.5)
            save_score(player_name, score)
            return

# --- Main Loop ---
while True:
    player = show_home_screen()
    run_game(player)
