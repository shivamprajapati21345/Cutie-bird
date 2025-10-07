import pygame, random, time
from pygame.locals import *
from model import init_db, save_score, get_top_scores
from settings import DB_PATH

# BASE DESIGN RESOLUTION 
BASE_WIDTH = 1380
BASE_HEIGHT = 700

#  GAME CONSTANTS (scalable) 
SPEED = 20
GRAVITY = 2.5
PIPE_WIDTH = 100
PIPE_HEIGHT = 500
PIPE_GAP = 200
PIPE_DISTANCE = 400
NUM_INITIAL_PIPES_SYSTEMS = 4
SYSTEM_HORIZONTAL_GAP = 400
GROUND_HEIGHT = 30
COIN_SPAWN_CHANCE = 1
COIN_HORIZONTAL_RANGE = (600, BASE_WIDTH - 800)
COIN_VERTICAL_CLEARANCE = 150

# NEW COIN CONFIGURATION 
NUM_COINS_PER_PIPE_GAP = 1
COIN_SPACING = 1
COIN_SIZE_BASE = 120

# SOUND FILES 
WING_SOUND = 'assets/audio/wing.wav'
HIT_SOUND = 'assets/audio/hit.wav'
COIN_SOUND = 'assets/audio/point.wav'
COIN_IMAGE = 'assets/sprites/coin.png'

# INITIALIZE PYGAME 
pygame.init()
pygame.mixer.init()
init_db()

# DISPLAY SETUP 
SCREEN_WIDTH, SCREEN_HEIGHT = BASE_WIDTH, BASE_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('cutie birds Sky')

# FONT & CLOCK 
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

# FRONT SPLASH SCREEN 
front_image = pygame.image.load('assets/sprites/1message.png').convert()
front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
show_front = True

# Timer for the splash screen (1 seconds)
SPLASH_SCREEN_DURATION = 1000
pygame.time.set_timer(USEREVENT + 1, SPLASH_SCREEN_DURATION)

while show_front:
    screen.blit(front_image, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); exit()
        elif event.type in (KEYDOWN, MOUSEBUTTONDOWN):
            show_front = False
            pygame.time.set_timer(USEREVENT + 1, 0)
        elif event.type == USEREVENT + 1:
            show_front = False
            pygame.time.set_timer(USEREVENT + 1, 0)
        elif event.type == VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            front_image = pygame.transform.scale(front_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

#  LOAD SOUNDS 
wing_sound = pygame.mixer.Sound(WING_SOUND)
hit_sound = pygame.mixer.Sound(HIT_SOUND)
try:
    coin_sound = pygame.mixer.Sound(COIN_SOUND)
except pygame.error:
    coin_sound = None

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
    def __init__(self, inverted, xpos, ysize, color='red', game_speed=20):
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
        self.game_speed = game_speed

    def update(self):
        self.rect.x -= self.game_speed

    def update_speed(self, new_speed):
        self.game_speed = new_speed

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos, initial_game_speed):
        super().__init__()
        image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        scale = get_scale()
        self.image = scale_img(image, 4 * SCREEN_WIDTH, GROUND_HEIGHT * scale)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = SCREEN_HEIGHT - int(GROUND_HEIGHT * scale)
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
    size = random.randint(200, 300)
    color = 'green' if pipe_color_toggle else 'red'
    pipe_color_toggle = not pipe_color_toggle
    return Pipe(False, xpos, size, color, current_game_speed), Pipe(True, xpos, SCREEN_HEIGHT - size - pipe_gap, color, current_game_speed)

def draw_buttons(paused):
    pause_button = pygame.Rect(SCREEN_WIDTH - 140, 20, 100, 40)
    resume_button = pygame.Rect(SCREEN_WIDTH - 140, 70, 100, 40)
    back_button = None

    if not paused:
        pygame.draw.rect(screen, (250, 0, 0), pause_button)
        screen.blit(font.render("Pause", True, (255, 255, 255)), (SCREEN_WIDTH - 130, 25))
    else:
        pygame.draw.rect(screen, (250, 50, 50), resume_button)
        screen.blit(font.render("Resume", True, (255, 255, 255)), (SCREEN_WIDTH - 130, 75))

        # Draw the "Back" button when paused
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50)
        draw_3d_button(back_button, "Back")
    return pause_button, resume_button, back_button

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
    GAME_BACKGROUND = pygame.image.load('assets/sprites/10.png').convert()
    def rescale_game_background():
        return scale_img(GAME_BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Load and scale the static background for home/name input screens
    STATIC_BACKGROUND = pygame.image.load('assets/sprites/1background-P.png').convert()
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
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
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


        #  Draw static background for home screen 
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
        headers = ["Sr", "Name", "Score"]
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
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird.update_scaled_image()
    bird_group.add(bird)

    game_level = 1
    current_game_speed = 25
    current_pipe_gap = 230
    level_up_score = 20 

    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground_group.add(Ground(SCREEN_WIDTH * i, current_game_speed))

    pipe_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()

    # Initial pipe generation: place pipes with consistent SYSTEM_HORIZONTAL_GAP
    for i in range(NUM_INITIAL_PIPES_SYSTEMS):
        if i == 0:
            pipe_x_pos = SCREEN_WIDTH + SYSTEM_HORIZONTAL_GAP
        else:
            last_pipe_system_right = pipe_group.sprites()[-1].rect.right if pipe_group.sprites() else 0
            pipe_x_pos = last_pipe_system_right + SYSTEM_HORIZONTAL_GAP

        p1, p2 = get_random_pipes(pipe_x_pos, current_pipe_gap, current_game_speed)
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

            if available_vertical_space >= scaled_coin_height + ( vertical_clearance):
                center_y_in_gap = gap_top + (available_vertical_space )
                coin_y = center_y_in_gap - (scaled_coin_height )

                if coin_y < gap_top + vertical_clearance:
                    coin_y = gap_top + vertical_clearance
                elif coin_y + scaled_coin_height > gap_bottom - vertical_clearance:
                    coin_y = gap_bottom - vertical_clearance - scaled_coin_height
            else:
                coin_y = gap_top + (available_vertical_space ) - (scaled_coin_height )

            total_coin_row_width = (NUM_COINS_PER_PIPE_GAP * scaled_coin_width) + \
                                   ((NUM_COINS_PER_PIPE_GAP ) * COIN_SPACING * get_scale())

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

            #When resizing, recalculate pipe position based on original x ratio, not just absolute x
                    p.rect.x = int(p.rect.x * (SCREEN_WIDTH / BASE_WIDTH))
                    if p.rect.y < 0:
                        p.rect.y = -(p.image.get_height() - (SCREEN_HEIGHT - p.rect.bottom - current_pipe_gap))
                    else:
                        p.rect.y = SCREEN_HEIGHT - p.image.get_height()
                    p.update_speed(current_game_speed)

        #  Draw static background for begin screen 
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
    collected_coins = 0
    paused = False

    score_change_message = ""
    message_timer = 0
    MESSAGE_DURATION = 60
    JUMP_SCORE_INCREMENT = 1

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
                game_background = rescale_game_background()
                bird.update_scaled_image()

                for p in pipe_group:
                    p.image = scale_img(pygame.image.load(f'assets/sprites/pipe-{"green" if pipe_color_toggle else "red"}.convert_alpha()'), PIPE_WIDTH * get_scale(), PIPE_HEIGHT * get_scale())
                    p.mask = pygame.mask.from_surface(p.image)
                    p.rect.x = int(p.rect.x * (SCREEN_WIDTH / BASE_WIDTH))
                    if p.rect.y < 0:
                        p.rect.y = -(p.image.get_height() - (SCREEN_HEIGHT - p.rect.bottom - current_pipe_gap))
                    else:
                        p.rect.y = SCREEN_HEIGHT - p.image.get_height()
                    p.update_speed(current_game_speed)


            elif event.type == KEYDOWN:
                if event.key in (K_SPACE, K_UP) and not paused:
                    bird.bump()
                    wing_sound.play()
                    score += JUMP_SCORE_INCREMENT
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

        screen.blit(game_background, (0, 0))

        if not paused:
            for p in pipe_group.sprites():
                if p.rect.right < bird.rect.left and not p.passed:
                    p.passed = True
                    score += 1
                    score_change_message = " "
                    message_timer = MESSAGE_DURATION

            #  Check for level up
            if score >= level_up_score:
                game_level += 1
                current_game_speed = 20 + (game_level - 1) * 10
                current_pipe_gap = max(150, 230 - (game_level - 1) * 10)
                level_up_score += 20  # next level
                
                for pipe_sprite in pipe_group:
                    pipe_sprite.update_speed(current_game_speed)
                for ground_sprite in ground_group:
                    ground_sprite.update_speed(current_game_speed)
                for coin_sprite in coin_group:
                    coin_sprite.update_speed(current_game_speed)


            # Consistent pipe generation after one goes off screen
            if len(pipe_group.sprites()) >= 2 and is_off_screen(min(pipe_group.sprites(), key=lambda x: x.rect.x)):
                pipes_to_remove = []
                sorted_pipes = sorted(pipe_group.sprites(), key=lambda x: x.rect.x)
                if len(sorted_pipes) >= 2:
            # Assuming the first two in the sorted list are the current leftmost system
                    pipes_to_remove.append(sorted_pipes[0])
                    pipes_to_remove.append(sorted_pipes[1])
                    for p_remove in pipes_to_remove:
                        pipe_group.remove(p_remove)
       
        # Find the rightmost pipe after removal to place the new one consistently
                rightmost_pipe_x = 0
                if pipe_group.sprites():
                    rightmost_pipe_x = max(p.rect.right for p in pipe_group.sprites())
        
        # Add a new pair of pipes with the consistent horizontal gap
                new_pipe_x_pos = rightmost_pipe_x + SYSTEM_HORIZONTAL_GAP
                p1, p2 = get_random_pipes(new_pipe_x_pos, current_pipe_gap, current_game_speed)
                p1.passed = False
                p2.passed = False
                pipe_group.add(p1); pipe_group.add(p2)
                
         # Handle coins for the newly added pipe system
                if random.random() < COIN_SPAWN_CHANCE:
                    scaled_coin_width = COIN_SIZE_BASE * get_scale()
                    scaled_coin_height = COIN_SIZE_BASE * get_scale()
                    vertical_clearance = COIN_VERTICAL_CLEARANCE * get_scale()

                    available_vertical_space = p2.rect.y - (p1.rect.y + p1.rect.height)
                    if available_vertical_space >= scaled_coin_height + (2 * vertical_clearance):
                        center_y_in_gap = (p1.rect.y + p1.rect.height) + (available_vertical_space / 2)
                        coin_y = center_y_in_gap - (scaled_coin_height / 2)

                        if coin_y < (p1.rect.y + p1.rect.height) + vertical_clearance:
                            coin_y = (p1.rect.y + p1.rect.height) + vertical_clearance
                        elif coin_y + scaled_coin_height > p2.rect.y - vertical_clearance:
                            coin_y = p2.rect.y - vertical_clearance - scaled_coin_height
                    else:
                        coin_y = (p1.rect.y + p1.rect.height) + (available_vertical_space / 2) - (scaled_coin_height / 2)

                    total_coin_row_width = (NUM_COINS_PER_PIPE_GAP * scaled_coin_width) + \
                                           ((NUM_COINS_PER_PIPE_GAP - 2) * COIN_SPACING * get_scale())

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
                        score_change_message = f"Coin collected! (+{collected_coin.value})"# More specific message
                        message_timer = MESSAGE_DURATION

        bird_group.draw(screen); pipe_group.draw(screen); ground_group.draw(screen); coin_group.draw(screen)
        screen.blit(font.render(f"player name:{player_name}", True, (255, 255, 255)), (10, 20))
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
            pipes_passed_text = small_font.render(f"Scores: {score}", True, (255, 255, 255))
            coins_collected_text = small_font.render(f"Coins scores: {collected_coins}", True, (255, 255, 255))
            final_score_text = small_font.render(f"Final Score: {score}", True, (255, 255, 255))

            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            player_score_rect = player_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            pipes_passed_rect = pipes_passed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            coins_collected_rect = coins_collected_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))

            screen.blit(game_over_text, game_over_rect)
            screen.blit(player_score_text, player_score_rect)
            screen.blit(pipes_passed_text, pipes_passed_rect)
            screen.blit(coins_collected_text, coins_collected_rect)
            screen.blit(final_score_text, final_score_rect)
            pygame.display.update()
            
            # Save the combined score for ranking (jumps + pipes + coins)
            save_score(player_name, score)
            time.sleep(3)
            return

# MAIN LOOP
while True:
    run_game()