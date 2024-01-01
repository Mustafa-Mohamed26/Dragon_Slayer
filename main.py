import math

import pygame
import sys
import os
import random
from pygame import mixer


# Animation Class
class AnimatedObject:
    def __init__(self, image_folder, image_files, frame_rate, speed):
        self.images = [pygame.image.load(os.path.join(image_folder, img)).convert_alpha() for img in image_files]
        self.current_frame = 0
        self.frame_rate = frame_rate
        self.speed = speed
        self.x, self.y = 0, 0
        self.key_state = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
        self.is_animating = False

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_state:
                self.key_state[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in self.key_state:
                self.key_state[event.key] = False

    def update(self):
        for key, pressed in self.key_state.items():
            if pressed:
                if key == pygame.K_a:
                    self.x -= self.speed
                elif key == pygame.K_d:
                    self.x += self.speed
                elif key == pygame.K_w:
                    self.y -= self.speed
                elif key == pygame.K_s:
                    self.y += self.speed

        self.current_frame = (self.current_frame + 1) % len(self.images)

    def draw(self, screen):
        # screen.fill((255, 255, 255))
        screen.blit(self.images[self.current_frame], (self.x, self.y))

    def animate(self):
        self.is_animating = True


class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))


# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Slayer")
icon = pygame.image.load("D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\imges\\dragon-icon.png")
pygame.display.set_icon(icon)

# Sound
mixer.music.load("D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\background image.wav")
mixer.music.play(-1)

# Create a variable to track music state
music_playing = False
on = False
onSoundImg = pygame.image.load("D:\My programming projects\PyCharm projects\Dragon_Slayer\imges\on.jpg")
offSoundImg = pygame.image.load("D:\My programming projects\PyCharm projects\Dragon_Slayer\imges\off.png")


# Function to toggle music state
def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    music_playing = not music_playing


# player state
health_count = 10
score_value = 0
playerX = 50
playerY = 200
playerX_change = 0
playerY_change = 0

# Screens booleans
screen_1 = True
screen_2 = False
screen_3 = False
screen_4 = False
screen_5 = False

# All screen background
screenImg_1 = pygame.image.load("imges/Backgrounds/First Screen.png")
screenImg_2 = pygame.image.load("imges/Backgrounds/Second Screen.png")
screenImg_3 = pygame.image.load("imges/Backgrounds/Third Screen.png")
screenImg_4 = pygame.image.load("imges/Backgrounds/Fourth Screen.png")
screenImg_5 = pygame.image.load("imges/Backgrounds/Fourth Screen.png")

# things
logo = pygame.image.load("imges/Dragon_Slayer_logo.png")
health = pygame.image.load("imges/life-count.png")
helper = pygame.image.load("imges/helper.png")

# dragons
dragon = pygame.image.load("imges/Dragons/dragon-asleep.png")
dragonFire = pygame.image.load("imges/Dragons/dragon-awake.png")
boss = pygame.image.load("imges/Dragons/dragon_sleep_boss.png")
bossFire = pygame.image.load("imges/Dragons/dragon_boss.png")

# Set up clock to control the frame rate
clock = pygame.time.Clock()

# Create IDLE instance
idle = AnimatedObject(
    "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE",
    ["D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\IDLE\\1_IDLE_000.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE\\1_IDLE_001.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE\\1_IDLE_002.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE\\1_IDLE_003.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE\\1_IDLE_004.png"],
    frame_rate=11, speed=12)

# create Run instance
run = AnimatedObject(
    "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Run",
    ["D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\Run\\2_RUN_000.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Run\\2_RUN_001.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Run\\2_RUN_002.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Run\\2_RUN_003.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Run\\2_RUN_004.png"],
    frame_rate=11, speed=12)

# create Attack instance
attack = AnimatedObject(
    "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Attack",
    ["D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\Attack\\3_ATTACK_000.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Attack\\3_ATTACK_001.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Attack\\3_ATTACK_002.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Attack\\3_ATTACK_003.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Attack\\3_ATTACK_004.png"],
    frame_rate=11, speed=12)

# create Hurt instance
hurt = AnimatedObject(
    "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Hurt",
    ["D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\Hurt\\4_HURT_000.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Hurt\\4_HURT_001.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Hurt\\4_HURT_002.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Hurt\\4_HURT_003.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\Hurt\\4_HURT_004.png"],
    frame_rate=11, speed=12)
# Font
font = pygame.font.Font('freesansbold.ttf', 32)

# animation booleans
idle_Animation = True
run_Animation = False
attack_Animation = False
hurt_Animation = False

# Wizard Fire Attack
wizard_Fire_Img = pygame.image.load(
    'D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\imges\\Fire Wizard\\Wizard_Fire.png')
wizard_Fire_ImgX = 50
wizard_Fire_ImgY = 0
wizard_Fire_Img_ChangeX = 60
wizard_Fire_Img_ChangeY = 0
wizard_Fire_Img_state = "ready"

# Dragon
enemyImg = []
enemyImg2 = []
enemyX = enemyX2 = []
enemyY = enemyY2 = []
enemyX_change = enemyX2_change = []
enemyY_change = enemyY2_change = []
num_of_enemies = 5
attackImg = []

for i in range(num_of_enemies):
    enemyImg.append(
        pygame.image.load('D:\My programming projects\PyCharm projects\Dragon_Slayer\imges\Dragons\dragon-awake.png'))
    enemyY.append(random.randint(116, 368))
    enemyX.append(600)
    enemyY_change.append(4)
    attackImg.append(False)

# dragon boss
bossImg = pygame.image.load("imges/Dragons/dragon_boss.png")
bossX = 0
bossY = 0
bossX_change = 0
bossY_change = 4

# dragons life
dragon_0_Health = HealthBar(enemyX[0], enemyY[0] + 75, 250, 10, 100)
dragon_0_Health.hp = 100
dragon_0_alife = True
dragon_1_Health = HealthBar(enemyX[0], enemyY[0] + 75, 250, 10, 100)
dragon_1_Health.hp = 100
dragon_1_alife = True
dragon_2_Health = HealthBar(enemyX[2], enemyY[2] + 75, 250, 10, 100)
dragon_2_Health.hp = 100
dragon_2_alife = True
dragon_3_Health = HealthBar(enemyX[3], enemyY[3] + 75, 250, 10, 100)
dragon_3_Health.hp = 100
dragon_3_alife = True
dragon_4_Health = HealthBar(enemyX[4], enemyY[4] + 75, 250, 10, 100)
dragon_4_Health.hp = 100
dragon_4_alife = True
boss_Health = HealthBar(bossX, bossY + 275, 250, 10, 200)
boss_Health.hp = 200
boss_alife = True

# dragon Fire Attack
dragon_Fire_Img = []
dragon_Fire_ImgX = []
dragon_Fire_ImgY = []
dragon_Fire_Img_ChangeX = []
dragon_Fire_Img_ChangeY = []
dragon_Fire_Img_state = []
num_Of_frames = []
num_Of_balls = 15

for i in range(num_Of_balls):
    dragon_Fire_Img.append(
        pygame.image.load('D:\My programming projects\PyCharm projects\Dragon_Slayer\imges\Dragons\Dragon_Fire.png'))
    dragon_Fire_ImgX.append(enemyX[0] - 100)
    dragon_Fire_ImgY.append(enemyY)
    dragon_Fire_Img_ChangeX.append(-10)
    dragon_Fire_Img_state.append("ready")
    num_Of_frames.append(0)


def fire_Wizard(x, y):
    global wizard_Fire_Img_state
    wizard_Fire_Img_state = "fire"
    screen.blit(wizard_Fire_Img, (x + 125, y + 10))


def fire_dragon(x, y, z):
    global dragon_Fire_Img_state
    dragon_Fire_Img_state[z] = "fire"
    screen.blit(dragon_Fire_Img[z], (x, y))


shoot = True


def isCollision(eX, eY, fireX, fireY):
    distance = math.sqrt(math.pow(eX - fireX, 2) + (math.pow(eY - fireY, 2)))
    if distance < 50:
        return True
    else:
        return False


over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))
    ScoreNum = font.render("Score: " + str(score_value), True, (255, 225, 225))
    screen.blit(ScoreNum, (400, 350))

    global dragon_0_alife
    dragon_0_alife = False
    global dragon_1_alife
    dragon_1_alife = False
    global dragon_2_alife
    dragon_2_alife = False
    global dragon_3_alife
    dragon_3_alife = False
    global dragon_4_alife
    dragon_4_alife = False
    global idle_Animation
    idle_Animation = False
    global run_Animation
    run_Animation = False
    global attack_Animation
    attack_Animation = False
    global hurt_Animation
    hurt_Animation = False
    global boss_alife
    boss_alife = False


def Winner():
    over_text = over_font.render("You Win", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))
    ScoreNum = font.render("Score: " + str(score_value), True, (255, 225, 225))
    screen.blit(ScoreNum, (400, 350))

    global dragon_0_alife
    dragon_0_alife = False
    global dragon_1_alife
    dragon_1_alife = False
    global dragon_2_alife
    dragon_2_alife = False
    global dragon_3_alife
    dragon_3_alife = False
    global dragon_4_alife
    dragon_4_alife = False
    global idle_Animation
    idle_Animation = False
    global run_Animation
    run_Animation = False
    global attack_Animation
    attack_Animation = False
    global hurt_Animation
    hurt_Animation = False
    global boss_alife
    boss_alife = False


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if idle_Animation:
            idle.handle_events(event)
        if run_Animation:
            run.handle_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER:
                if screen_1:
                    screen_2 = True
                    idle.x = run.x = attack.x = hurt.x = 50
                    idle.y = run.y = attack.y = hurt.y = 450
                    screen_1 = False
                elif screen_2:
                    screen_3 = True
                    idle.x = run.x = attack.x = hurt.x = 50
                    idle.y = run.y = attack.y = hurt.y = 200
                    enemyX[0] = 700
                    enemyY[0] = 180
                    enemyX[1] = 700
                    enemyY[1] = 300
                    screen_2 = False

            if event.key == pygame.K_a:
                idle_Animation = False
                run_Animation = True
                playerX_change -= 12
            if event.key == pygame.K_d:
                idle_Animation = False
                run_Animation = True
                playerX_change += 12
            if event.key == pygame.K_w:
                idle_Animation = False
                run_Animation = True
                playerY_change -= 12
            if event.key == pygame.K_s:
                idle_Animation = False
                run_Animation = True
                playerY_change += 12
            if event.key == pygame.K_SPACE:
                if wizard_Fire_Img_state == "ready":
                    Wizard_Fire_Img_Sound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\magic spell.wav")
                    Wizard_Fire_Img_Sound.play()
                    # Get the current x cordinate of the spaceship
                    idle_Animation = False
                    run_Animation = False
                    attack_Animation = True
                    wizard_Fire_ImgX = playerX
                    wizard_Fire_ImgY = playerY
                    fire_Wizard(wizard_Fire_ImgX, wizard_Fire_ImgY)
            if event.key == pygame.K_i:
                if on:
                    on = False
                elif not on:
                    on = True
                toggle_music()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                idle_Animation = True
                run_Animation = False
                playerX_change = 0
                playerY_change = 0
            if event.key == pygame.K_d:
                idle_Animation = True
                run_Animation = False
                playerX_change = 0
                playerY_change = 0
            if event.key == pygame.K_w:
                idle_Animation = True
                run_Animation = False
                playerX_change = 0
                playerY_change = 0
            if event.key == pygame.K_s:
                idle_Animation = True
                run_Animation = False
                playerX_change = 0
                playerY_change = 0
            if event.key == pygame.K_SPACE:
                idle_Animation = True
                run_Animation = False
                attack_Animation = False

    playerX += playerX_change
    playerY += playerY_change

    idle.x = run.x = attack.x = hurt.x = playerX
    idle.y = run.y = attack.y = hurt.y = playerY

    # draw first screen
    if screen_1:
        screen.blit(screenImg_1, (0, 0))
        screen.blit(logo, (250, 15))
        Enter = font.render("Press Enter To Start", True, (255, 255, 255))
        screen.blit(Enter, (350, 400))

    if screen_2:
        screen.blit(screenImg_2, (0, 0))
        screen.blit(helper, (700, 450))

        text1 = font.render('You are in a land full of dragons. In front of you,', True, (255, 0, 0))
        screen.blit(text1, (150, 150))

        text2 = font.render('You must defeat the king of the dragon,', True, (255, 0, 0))
        screen.blit(text2, (150, 200))

        text3 = font.render('you will be in difficult challenges', True, (255, 0, 0))
        screen.blit(text3, (150, 250))

        text4 = font.render('you must avenge for our village.', True, (255, 0, 0))
        screen.blit(text4, (150, 300))

        text5 = font.render("you will win if you defeat all the dragons", True, (255, 0, 0))
        screen.blit(text5, (150, 350))

        text6 = font.render("press Enter to continue", True, (255, 0, 0))
        screen.blit(text6, (150, 400))
        idle.x = run.x = attack.x = hurt.x = 50
        idle.y = run.y = attack.y = hurt.y = 450
        idle.update()
        idle.draw(screen)

    if screen_3:
        screen.blit(screenImg_3, (0, 0))
        level1 = font.render("Level 1 ", True, (255, 0, 0))
        screen.blit(level1, (850, 10))

        # dragon 0
        # movement
        if dragon_0_alife:
            if dragon_0_Health.hp == 0:
                dragon_0_alife = False
            enemyY[0] += enemyY_change[0]
            if enemyY[0] <= 100:
                enemyY_change[0] = 4
                enemyY[0] += enemyY_change[0]
            elif enemyY[0] >= 400:
                enemyY_change[0] = -4
                enemyY[0] += enemyY_change[0]

            # collision of the player
            collision = isCollision(enemyX[0], enemyY[0], wizard_Fire_ImgX, wizard_Fire_ImgY)
            if collision:
                explosionSound = mixer.Sound(
                    "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                explosionSound.play()
                wizard_Fire_ImgX = 1000
                wizard_Fire_Img_state = "ready"
                score_value += 50
                dragon_0_Health.hp -= 25

            screen.blit(enemyImg[0], (enemyX[0], enemyY[0]))
            dragon_0_Health.x = enemyX[0]
            dragon_0_Health.y = enemyY[0] + 150
            dragon_0_Health.draw(screen)

            # dragon shoot
            num_Of_frames[0] += 1
            if num_Of_frames[0] <= 2000:
                # ball 1
                if dragon_Fire_Img_state[0] == "ready":
                    dragon_Fire_ImgX[0] = enemyX[0] - 100
                    dragon_Fire_ImgY[0] = enemyY[0]
                    fire_dragon(dragon_Fire_ImgX[0], dragon_Fire_ImgY[0], 0)
                    # Get the current x cordinate of the spaceship
                if num_Of_frames[0] <= 2000:
                    dragon_Fire_ImgX[0] += dragon_Fire_Img_ChangeX[0]
                    fire_dragon(dragon_Fire_ImgX[0], dragon_Fire_ImgY[0], 0)
                    if dragon_Fire_ImgX[0] == -1000:
                        dragon_Fire_ImgX[0] = enemyX[0] - 100
                        dragon_Fire_ImgY[0] = enemyY[0]

                    if dragon_Fire_ImgY[0] == enemyY[0]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[0] == 2000:
                        num_Of_frames[0] = 0
                        dragon_Fire_Img_state[0] = "ready"

            # collision of the player
            collision1 = isCollision(playerX, playerY, dragon_Fire_ImgX[0], dragon_Fire_ImgY[0])
            if collision1:
                explosionSound = mixer.Sound(
                    "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                explosionSound.play()
                dragon_Fire_ImgX[0] = -900
                dragon_Fire_ImgY[0] = enemyY[0]
                dragon_Fire_ImgX[0] += dragon_Fire_Img_ChangeX[0]
                health_count -= 1

                # ball 2
                if dragon_Fire_Img_state[1] == "ready":
                    dragon_Fire_ImgX[1] = enemyX[0] - 100
                    dragon_Fire_ImgY[1] = enemyY[0]
                    fire_dragon(dragon_Fire_ImgX[1], dragon_Fire_ImgY[1], 1)
                    # Get the current x cordinate of the spaceship
                if 60 <= num_Of_frames[0] <= 2000:
                    dragon_Fire_ImgX[1] += dragon_Fire_Img_ChangeX[1]
                    fire_dragon(dragon_Fire_ImgX[1], dragon_Fire_ImgY[1], 1)
                    if dragon_Fire_ImgX[1] == -1000:
                        dragon_Fire_ImgX[1] = enemyX[0] - 100
                        dragon_Fire_ImgY[1] = enemyY[0]

                    if dragon_Fire_ImgY[1] == enemyY[0]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[0] == 2000:
                        num_Of_frames[0] = 0
                        dragon_Fire_Img_state[1] = "ready"

                        # collision of the player
                collision2 = isCollision(playerX, playerY, dragon_Fire_ImgX[1], dragon_Fire_ImgY[1])
                if collision2:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[1] = -900
                    dragon_Fire_ImgY[1] = enemyY[0]
                    dragon_Fire_ImgX[1] += dragon_Fire_Img_ChangeX[1]
                    health_count -= 1

                # ball 3
                if dragon_Fire_Img_state[2] == "ready":
                    dragon_Fire_ImgX[2] = enemyX[0] - 100
                    dragon_Fire_ImgY[2] = enemyY[0]
                    fire_dragon(dragon_Fire_ImgX[2], dragon_Fire_ImgY[2], 2)
                    # Get the current x cordinate of the spaceship
                if 120 <= num_Of_frames[0] <= 2000:
                    dragon_Fire_ImgX[2] += dragon_Fire_Img_ChangeX[2]
                    fire_dragon(dragon_Fire_ImgX[2], dragon_Fire_ImgY[2], 2)
                    if dragon_Fire_ImgX[2] == -1000:
                        dragon_Fire_ImgX[2] = enemyX[0] - 100
                        dragon_Fire_ImgY[2] = enemyY[0]

                    if dragon_Fire_ImgY[2] == enemyY[0]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[0] == 2000:
                        num_Of_frames[0] = 0
                        dragon_Fire_Img_state[2] = "ready"

                # collision of the player
                collision3 = isCollision(playerX, playerY, dragon_Fire_ImgX[2], dragon_Fire_ImgY[2])
                if collision3:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[2] = -900
                    dragon_Fire_ImgY[2] = enemyY[0]
                    dragon_Fire_ImgX[2] += dragon_Fire_Img_ChangeX[2]
                    health_count -= 1

        # dragon 1
        # movement
        if dragon_1_alife:
            if dragon_1_Health.hp == 0:
                dragon_1_alife = False
            enemyY[1] += enemyY_change[1]
            if enemyY[1] <= 100:
                enemyY_change[1] = 4
                enemyY[1] += enemyY_change[1]
            elif enemyY[1] >= 400:
                enemyY_change[1] = -4
                enemyY[1] += enemyY_change[1]

            # collection of the player
            collision = isCollision(enemyX[1], enemyY[1], wizard_Fire_ImgX, wizard_Fire_ImgY)
            if collision:
                explosionSound = mixer.Sound(
                    "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                explosionSound.play()
                wizard_Fire_ImgX = 1000
                wizard_Fire_Img_state = "ready"
                score_value += 50
                dragon_1_Health.hp -= 25
            screen.blit(enemyImg[1], (enemyX[1], enemyY[1]))
            dragon_1_Health.x = enemyX[1]
            dragon_1_Health.y = enemyY[1] + 150
            dragon_1_Health.draw(screen)

            # dragon 1 shoot
            num_Of_frames[1] += 1
            if num_Of_frames[1] <= 2000:
                # ball 1
                if dragon_Fire_Img_state[3] == "ready":
                    dragon_Fire_ImgX[3] = enemyX[1] - 100
                    dragon_Fire_ImgY[3] = enemyY[1]
                    fire_dragon(dragon_Fire_ImgX[3], dragon_Fire_ImgY[3], 3)
                    # Get the current x cordinate of the spaceship
                if 30 <= num_Of_frames[1] <= 2000:
                    dragon_Fire_ImgX[3] += dragon_Fire_Img_ChangeX[3]
                    fire_dragon(dragon_Fire_ImgX[3], dragon_Fire_ImgY[3], 3)
                    if dragon_Fire_ImgX[3] == -1000:
                        dragon_Fire_ImgX[3] = enemyX[1] - 100
                        dragon_Fire_ImgY[3] = enemyY[1]

                    if dragon_Fire_ImgY[3] == enemyY[1]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[1] == 2000:
                        num_Of_frames[1] = 0
                        dragon_Fire_Img_state[3] = "ready"

                collision4 = isCollision(playerX, playerY, dragon_Fire_ImgX[3], dragon_Fire_ImgY[3])
                if collision4:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[3] = -900
                    dragon_Fire_ImgY[3] = enemyY[1]
                    dragon_Fire_ImgX[3] += dragon_Fire_Img_ChangeX[3]
                    health_count -= 1

                # ball 2
                if dragon_Fire_Img_state[4] == "ready":
                    dragon_Fire_ImgX[4] = enemyX[1] - 100
                    dragon_Fire_ImgY[4] = enemyY[1]
                    fire_dragon(dragon_Fire_ImgX[4], dragon_Fire_ImgY[4], 4)
                    # Get the current x cordinate of the spaceship
                if 90 <= num_Of_frames[1] <= 2000:
                    dragon_Fire_ImgX[4] += dragon_Fire_Img_ChangeX[4]
                    fire_dragon(dragon_Fire_ImgX[4], dragon_Fire_ImgY[4], 4)
                    if dragon_Fire_ImgX[4] == -1000:
                        dragon_Fire_ImgX[4] = enemyX[1] - 100
                        dragon_Fire_ImgY[4] = enemyY[1]

                    if dragon_Fire_ImgY[4] == enemyY[1]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[1] == 2000:
                        num_Of_frames[1] = 0
                        dragon_Fire_Img_state[4] = "ready"

                collision5 = isCollision(playerX, playerY, dragon_Fire_ImgX[4], dragon_Fire_ImgY[4])
                if collision5:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[4] = -900
                    dragon_Fire_ImgY[4] = enemyY[1]
                    dragon_Fire_ImgX[4] += dragon_Fire_Img_ChangeX[4]
                    health_count -= 1

                # ball 3
                if dragon_Fire_Img_state[5] == "ready":
                    dragon_Fire_ImgX[5] = enemyX[1] - 100
                    dragon_Fire_ImgY[5] = enemyY[1]
                    fire_dragon(dragon_Fire_ImgX[5], dragon_Fire_ImgY[5], 5)
                    # Get the current x cordinate of the spaceship
                if 180 <= num_Of_frames[1] <= 2000:
                    dragon_Fire_ImgX[5] += dragon_Fire_Img_ChangeX[5]
                    fire_dragon(dragon_Fire_ImgX[5], dragon_Fire_ImgY[5], 5)
                    if dragon_Fire_ImgX[5] == -1000:
                        dragon_Fire_ImgX[5] = enemyX[1] - 100
                        dragon_Fire_ImgY[5] = enemyY[1]

                    if dragon_Fire_ImgY[5] == enemyY[1]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[1] == 2000:
                        num_Of_frames[1] = 0
                        dragon_Fire_Img_state[5] = "ready"

                collision6 = isCollision(playerX, playerY, dragon_Fire_ImgX[5], dragon_Fire_ImgY[5])
                if collision6:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[5] = -900
                    dragon_Fire_ImgY[5] = enemyY[1]
                    dragon_Fire_ImgX[5] += dragon_Fire_Img_ChangeX[5]
                    health_count -= 1

        # next level
        if playerX >= 948:
            screen_4 = True
            playerX = -10
            playerY = 200
            enemyX[2] = 700
            enemyY[2] = 100
            enemyX[3] = 700
            enemyY[3] = 200
            enemyX[4] = 700
            enemyY[4] = 300
            num_Of_frames[0] = num_Of_frames[1] = 0
            screen_3 = False

    if screen_4:
        screen.blit(screenImg_4, (0, 0))
        level1 = font.render("Level 2 ", True, (255, 0, 0))
        screen.blit(level1, (850, 10))

        # dragon 2
        # movement
        if dragon_2_alife:
            if dragon_2_Health.hp == 0:
                dragon_2_alife = False
            enemyY[2] += enemyY_change[2]
            if enemyY[2] <= 100:
                enemyY_change[2] = 4
                enemyY[2] += enemyY_change[2]
            elif enemyY[2] >= 400:
                enemyY_change[2] = -4
                enemyY[2] += enemyY_change[2]

            # collection of the player
            collision = isCollision(enemyX[2], enemyY[2], wizard_Fire_ImgX, wizard_Fire_ImgY)
            if collision:
                explosionSound = mixer.Sound(
                    "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                explosionSound.play()
                wizard_Fire_ImgX = 1000
                wizard_Fire_Img_state = "ready"
                score_value += 50
                dragon_2_Health.hp -= 25
            screen.blit(enemyImg[2], (enemyX[2], enemyY[2]))
            dragon_2_Health.x = enemyX[2]
            dragon_2_Health.y = enemyY[2] + 150
            dragon_2_Health.draw(screen)

            # dragon 2 shoot
            num_Of_frames[2] += 1
            if num_Of_frames[2] <= 2000:
                # ball 1
                if dragon_Fire_Img_state[4] == "ready":
                    dragon_Fire_ImgX[4] = enemyX[2] - 100
                    dragon_Fire_ImgY[4] = enemyY[2]
                    fire_dragon(dragon_Fire_ImgX[4], dragon_Fire_ImgY[4], 4)
                    # Get the current x cordinate of the spaceship
                if 30 <= num_Of_frames[2] <= 2000:
                    dragon_Fire_ImgX[4] += dragon_Fire_Img_ChangeX[4]
                    fire_dragon(dragon_Fire_ImgX[4], dragon_Fire_ImgY[4], 4)
                    if dragon_Fire_ImgX[4] == -1000:
                        dragon_Fire_ImgX[4] = enemyX[2] - 100
                        dragon_Fire_ImgY[4] = enemyY[2]

                    if dragon_Fire_ImgY[4] == enemyY[2]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[2] == 2000:
                        num_Of_frames[2] = 0
                        dragon_Fire_Img_state[4] = "ready"

                collision1 = isCollision(playerX, playerY, dragon_Fire_ImgX[4], dragon_Fire_ImgY[4])
                if collision1:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[4] = -900
                    dragon_Fire_ImgY[4] = enemyY[2]
                    dragon_Fire_ImgX[4] += dragon_Fire_Img_ChangeX[4]
                    health_count -= 1

                # ball 2
                if dragon_Fire_Img_state[5] == "ready":
                    dragon_Fire_ImgX[5] = enemyX[2] - 100
                    dragon_Fire_ImgY[5] = enemyY[2]
                    fire_dragon(dragon_Fire_ImgX[5], dragon_Fire_ImgY[5], 5)
                    # Get the current x cordinate of the spaceship
                if 120 <= num_Of_frames[2] <= 2000:
                    dragon_Fire_ImgX[5] += dragon_Fire_Img_ChangeX[5]
                    fire_dragon(dragon_Fire_ImgX[5], dragon_Fire_ImgY[5], 5)
                    if dragon_Fire_ImgX[5] == -1000:
                        dragon_Fire_ImgX[5] = enemyX[2] - 100
                        dragon_Fire_ImgY[5] = enemyY[2]

                    if dragon_Fire_ImgY[5] == enemyY[2]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[2] == 2000:
                        num_Of_frames[2] = 0
                        dragon_Fire_Img_state[5] = "ready"

                collision2 = isCollision(playerX, playerY, dragon_Fire_ImgX[5], dragon_Fire_ImgY[5])
                if collision2:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[5] = -900
                    dragon_Fire_ImgY[5] = enemyY[2]
                    dragon_Fire_ImgX[5] += dragon_Fire_Img_ChangeX[5]
                    health_count -= 1

                # ball 3
                if dragon_Fire_Img_state[6] == "ready":
                    dragon_Fire_ImgX[6] = enemyX[2] - 100
                    dragon_Fire_ImgY[6] = enemyY[2]
                    fire_dragon(dragon_Fire_ImgX[6], dragon_Fire_ImgY[6], 6)
                    # Get the current x cordinate of the spaceship
                if 210 <= num_Of_frames[2] <= 2000:
                    dragon_Fire_ImgX[6] += dragon_Fire_Img_ChangeX[6]
                    fire_dragon(dragon_Fire_ImgX[6], dragon_Fire_ImgY[6], 6)
                    if dragon_Fire_ImgX[6] == -1000:
                        dragon_Fire_ImgX[6] = enemyX[2] - 100
                        dragon_Fire_ImgY[6] = enemyY[2]

                    if dragon_Fire_ImgY[6] == enemyY[2]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[2] == 2000:
                        num_Of_frames[2] = 0
                        dragon_Fire_Img_state[6] = "ready"

                collision3 = isCollision(playerX, playerY, dragon_Fire_ImgX[6], dragon_Fire_ImgY[6])
                if collision3:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[6] = -900
                    dragon_Fire_ImgY[6] = enemyY[2]
                    dragon_Fire_ImgX[6] += dragon_Fire_Img_ChangeX[6]
                    health_count -= 1

        # dragon 3
        # movement
        if dragon_3_alife:
            if dragon_3_Health.hp == 0:
                dragon_3_alife = False
            enemyY[3] += enemyY_change[3]
            if enemyY[3] <= 100:
                enemyY_change[3] = 4
                enemyY[3] += enemyY_change[3]
            elif enemyY[3] >= 400:
                enemyY_change[3] = -4
                enemyY[3] += enemyY_change[3]

            # collection of the player
            collision = isCollision(enemyX[3], enemyY[3], wizard_Fire_ImgX, wizard_Fire_ImgY)
            if collision:
                explosionSound = mixer.Sound(
                    "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                explosionSound.play()
                wizard_Fire_ImgX = 1000
                wizard_Fire_Img_state = "ready"
                score_value += 50
                dragon_3_Health.hp -= 25
            screen.blit(enemyImg[3], (enemyX[3], enemyY[3]))
            dragon_3_Health.x = enemyX[3]
            dragon_3_Health.y = enemyY[3] + 150
            dragon_3_Health.draw(screen)

            # dragon 3 shoot
            num_Of_frames[3] += 1
            if num_Of_frames[3] <= 2000:
                # ball 1
                if dragon_Fire_Img_state[7] == "ready":
                    dragon_Fire_ImgX[7] = enemyX[3] - 100
                    dragon_Fire_ImgY[7] = enemyY[3]
                    fire_dragon(dragon_Fire_ImgX[7], dragon_Fire_ImgY[7], 7)
                    # Get the current x cordinate of the spaceship
                if 60 <= num_Of_frames[3] <= 2000:
                    dragon_Fire_ImgX[7] += dragon_Fire_Img_ChangeX[7]
                    fire_dragon(dragon_Fire_ImgX[7], dragon_Fire_ImgY[7], 7)
                    if dragon_Fire_ImgX[7] == -1000:
                        dragon_Fire_ImgX[7] = enemyX[3] - 100
                        dragon_Fire_ImgY[7] = enemyY[3]

                    if dragon_Fire_ImgY[7] == enemyY[3]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[3] == 2000:
                        num_Of_frames[3] = 0
                        dragon_Fire_Img_state[7] = "ready"

                collision1 = isCollision(playerX, playerY, dragon_Fire_ImgX[7], dragon_Fire_ImgY[7])
                if collision1:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[7] = -900
                    dragon_Fire_ImgY[7] = enemyY[3]
                    dragon_Fire_ImgX[7] += dragon_Fire_Img_ChangeX[7]
                    health_count -= 1

                # ball 2
                if dragon_Fire_Img_state[8] == "ready":
                    dragon_Fire_ImgX[8] = enemyX[3] - 100
                    dragon_Fire_ImgY[8] = enemyY[3]
                    fire_dragon(dragon_Fire_ImgX[8], dragon_Fire_ImgY[8], 8)
                    # Get the current x cordinate of the spaceship
                if 150 <= num_Of_frames[3] <= 2000:
                    dragon_Fire_ImgX[8] += dragon_Fire_Img_ChangeX[8]
                    fire_dragon(dragon_Fire_ImgX[8], dragon_Fire_ImgY[8], 8)
                    if dragon_Fire_ImgX[8] == -1000:
                        dragon_Fire_ImgX[8] = enemyX[3] - 100
                        dragon_Fire_ImgY[8] = enemyY[3]

                    if dragon_Fire_ImgY[8] == enemyY[3]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[3] == 2000:
                        num_Of_frames[3] = 0
                        dragon_Fire_Img_state[8] = "ready"

                collision2 = isCollision(playerX, playerY, dragon_Fire_ImgX[8], dragon_Fire_ImgY[8])
                if collision2:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[8] = -900
                    dragon_Fire_ImgY[8] = enemyY[2]
                    dragon_Fire_ImgX[8] += dragon_Fire_Img_ChangeX[8]
                    health_count -= 1

                # ball 3
                if dragon_Fire_Img_state[9] == "ready":
                    dragon_Fire_ImgX[9] = enemyX[3] - 100
                    dragon_Fire_ImgY[9] = enemyY[3]
                    fire_dragon(dragon_Fire_ImgX[9], dragon_Fire_ImgY[9], 9)
                    # Get the current x cordinate of the spaceship
                if 230 <= num_Of_frames[3] <= 2000:
                    dragon_Fire_ImgX[9] += dragon_Fire_Img_ChangeX[9]
                    fire_dragon(dragon_Fire_ImgX[9], dragon_Fire_ImgY[9], 9)
                    if dragon_Fire_ImgX[9] == -1000:
                        dragon_Fire_ImgX[9] = enemyX[3] - 100
                        dragon_Fire_ImgY[9] = enemyY[3]

                    if dragon_Fire_ImgY[9] == enemyY[3]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[3] == 2000:
                        num_Of_frames[3] = 0
                        dragon_Fire_Img_state[9] = "ready"

                collision3 = isCollision(playerX, playerY, dragon_Fire_ImgX[9], dragon_Fire_ImgY[9])
                if collision3:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[9] = -900
                    dragon_Fire_ImgY[9] = enemyY[3]
                    dragon_Fire_ImgX[9] += dragon_Fire_Img_ChangeX[9]
                    health_count -= 1
        # dragon 4
        # movement
        if dragon_4_alife:
            if dragon_4_Health.hp == 0:
                dragon_4_alife = False
            enemyY[4] += enemyY_change[4]
            if enemyY[4] <= 100:
                enemyY_change[4] = 4
                enemyY[4] += enemyY_change[4]
            elif enemyY[4] >= 400:
                enemyY_change[4] = -4
                enemyY[4] += enemyY_change[4]

            # collection of the player
            collision = isCollision(enemyX[4], enemyY[4], wizard_Fire_ImgX, wizard_Fire_ImgY)
            if collision:
                explosionSound = mixer.Sound(
                    "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                explosionSound.play()
                wizard_Fire_ImgX = 1000
                wizard_Fire_Img_state = "ready"
                score_value += 50
                dragon_4_Health.hp -= 25
            screen.blit(enemyImg[4], (enemyX[4], enemyY[4]))
            dragon_4_Health.x = enemyX[4]
            dragon_4_Health.y = enemyY[3] + 150
            dragon_4_Health.draw(screen)

            # dragon 4 shoot
            num_Of_frames[4] += 1
            if num_Of_frames[4] <= 2000:
                # ball 1
                if dragon_Fire_Img_state[10] == "ready":
                    dragon_Fire_ImgX[10] = enemyX[4] - 100
                    dragon_Fire_ImgY[10] = enemyY[4]
                    fire_dragon(dragon_Fire_ImgX[10], dragon_Fire_ImgY[10], 10)
                    # Get the current x cordinate of the spaceship
                if 90 <= num_Of_frames[4] <= 2000:
                    dragon_Fire_ImgX[10] += dragon_Fire_Img_ChangeX[10]
                    fire_dragon(dragon_Fire_ImgX[10], dragon_Fire_ImgY[10], 10)
                    if dragon_Fire_ImgX[10] == -1000:
                        dragon_Fire_ImgX[10] = enemyX[4] - 100
                        dragon_Fire_ImgY[10] = enemyY[4]

                    if dragon_Fire_ImgY[10] == enemyY[4]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[4] == 2000:
                        num_Of_frames[4] = 0
                        dragon_Fire_Img_state[10] = "ready"

                collision1 = isCollision(playerX, playerY, dragon_Fire_ImgX[10], dragon_Fire_ImgY[10])
                if collision1:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[10] = -900
                    dragon_Fire_ImgY[10] = enemyY[4]
                    dragon_Fire_ImgX[10] += dragon_Fire_Img_ChangeX[10]
                    health_count -= 1

                # ball 2
                if dragon_Fire_Img_state[11] == "ready":
                    dragon_Fire_ImgX[11] = enemyX[4] - 100
                    dragon_Fire_ImgY[11] = enemyY[4]
                    fire_dragon(dragon_Fire_ImgX[11], dragon_Fire_ImgY[11], 11)
                    # Get the current x cordinate of the spaceship
                if 180 <= num_Of_frames[4] <= 2000:
                    dragon_Fire_ImgX[11] += dragon_Fire_Img_ChangeX[11]
                    fire_dragon(dragon_Fire_ImgX[11], dragon_Fire_ImgY[11], 11)
                    if dragon_Fire_ImgX[11] == -1000:
                        dragon_Fire_ImgX[11] = enemyX[4] - 100
                        dragon_Fire_ImgY[11] = enemyY[4]

                    if dragon_Fire_ImgY[11] == enemyY[4]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[4] == 2000:
                        num_Of_frames[4] = 0
                        dragon_Fire_Img_state[11] = "ready"

                collision2 = isCollision(playerX, playerY, dragon_Fire_ImgX[11], dragon_Fire_ImgY[11])
                if collision2:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[11] = -900
                    dragon_Fire_ImgY[11] = enemyY[3]
                    dragon_Fire_ImgX[11] += dragon_Fire_Img_ChangeX[11]
                    health_count -= 1

                # ball 3
                if dragon_Fire_Img_state[12] == "ready":
                    dragon_Fire_ImgX[12] = enemyX[4] - 100
                    dragon_Fire_ImgY[12] = enemyY[4]
                    fire_dragon(dragon_Fire_ImgX[12], dragon_Fire_ImgY[12], 12)
                    # Get the current x cordinate of the spaceship
                if 260 <= num_Of_frames[4] <= 2000:
                    dragon_Fire_ImgX[12] += dragon_Fire_Img_ChangeX[12]
                    fire_dragon(dragon_Fire_ImgX[12], dragon_Fire_ImgY[12], 12)
                    if dragon_Fire_ImgX[12] == -1000:
                        dragon_Fire_ImgX[12] = enemyX[4] - 100
                        dragon_Fire_ImgY[12] = enemyY[4]

                    if dragon_Fire_ImgY[12] == enemyY[4]:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[4] == 2000:
                        num_Of_frames[4] = 0
                        dragon_Fire_Img_state[12] = "ready"

                collision3 = isCollision(playerX, playerY, dragon_Fire_ImgX[12], dragon_Fire_ImgY[12])
                if collision3:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[12] = -900
                    dragon_Fire_ImgY[12] = enemyY[4]
                    dragon_Fire_ImgX[12] += dragon_Fire_Img_ChangeX[12]
                    health_count -= 1
        # next level
        if playerX >= 948:
            screen_5 = True
            playerX = -10
            playerY = 200
            bossX = 600
            bossY = 300
            screen_4 = False

    if screen_5:
        screen.blit(screenImg_5, (0, 0))
        level1 = font.render("Level 3 ", True, (255, 0, 0))
        screen.blit(level1, (850, 10))

        if boss_alife:
            if boss_Health.hp == 0:
                boss_alife = False
            bossY += bossY_change
            if bossY <= 100:
                bossY_change = 4
                bossY += bossY_change
            elif bossY >= 400:
                bossY_change = -4
                bossY += bossY_change

            # collection of the player
            collision_b = isCollision(bossX, bossY, wizard_Fire_ImgX, wizard_Fire_ImgY)
            if collision_b:
                explosionSound = mixer.Sound(
                    "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                explosionSound.play()
                wizard_Fire_ImgX = 1000
                wizard_Fire_Img_state = "ready"
                score_value += 100
                boss_Health.hp -= 25
            screen.blit(bossImg, (bossX, bossY))
            boss_Health.x = bossX
            boss_Health.y = bossY + 150
            boss_Health.draw(screen)

            # boss
            num_Of_frames[5] += 1
            if num_Of_frames[5] <= 2000:
                # ball 1
                if dragon_Fire_Img_state[13] == "ready":
                    dragon_Fire_ImgX[13] = bossX - 100
                    dragon_Fire_ImgY[13] = bossY
                    fire_dragon(dragon_Fire_ImgX[13], dragon_Fire_ImgY[13], 13)
                    # Get the current x cordinate of the spaceship
                if 30 <= num_Of_frames[5] <= 2000:
                    dragon_Fire_ImgX[13] += dragon_Fire_Img_ChangeX[13]
                    fire_dragon(dragon_Fire_ImgX[13], dragon_Fire_ImgY[13], 13)
                    if dragon_Fire_ImgX[13] == 0:
                        dragon_Fire_ImgX[13] = bossX - 100
                        dragon_Fire_ImgY[13] = bossY

                    if dragon_Fire_ImgY[13] == bossY:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[5] == 2000:
                        num_Of_frames[5] = 0
                        dragon_Fire_Img_state[13] = "ready"

                collision1 = isCollision(playerX, playerY, dragon_Fire_ImgX[13], dragon_Fire_ImgY[13])
                if collision1:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[13] = -900
                    dragon_Fire_ImgY[13] = bossY
                    dragon_Fire_ImgX[13] += dragon_Fire_Img_ChangeX[13]
                    health_count -= 2

                # ball 2
                if dragon_Fire_Img_state[14] == "ready":
                    dragon_Fire_ImgX[14] = bossX - 100
                    dragon_Fire_ImgY[14] = bossY
                    fire_dragon(dragon_Fire_ImgX[14], dragon_Fire_ImgY[14], 14)
                    # Get the current x cordinate of the spaceship
                if 60 <= num_Of_frames[5] <= 2000:
                    dragon_Fire_ImgX[14] += dragon_Fire_Img_ChangeX[14]
                    fire_dragon(dragon_Fire_ImgX[14], dragon_Fire_ImgY[14], 14)
                    if dragon_Fire_ImgX[14] == 0:
                        dragon_Fire_ImgX[14] = bossX - 100
                        dragon_Fire_ImgY[14] = bossY

                    if dragon_Fire_ImgY[14] == bossY:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[5] == 2000:
                        num_Of_frames[5] = 0
                        dragon_Fire_Img_state[14] = "ready"

                collision2 = isCollision(playerX, playerY, dragon_Fire_ImgX[14], dragon_Fire_ImgY[14])
                if collision2:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[14] = -900
                    dragon_Fire_ImgY[14] = bossY
                    dragon_Fire_ImgX[14] += dragon_Fire_Img_ChangeX[14]
                    health_count -= 2

                # ball 3
                if dragon_Fire_Img_state[1] == "ready":
                    dragon_Fire_ImgX[1] = bossX - 100
                    dragon_Fire_ImgY[1] = bossY
                    fire_dragon(dragon_Fire_ImgX[1], dragon_Fire_ImgY[1], 1)
                    # Get the current x cordinate of the spaceship
                if 90 <= num_Of_frames[5] <= 2000:
                    dragon_Fire_ImgX[1] += dragon_Fire_Img_ChangeX[1]
                    fire_dragon(dragon_Fire_ImgX[1], dragon_Fire_ImgY[1], 1)
                    if dragon_Fire_ImgX[1] == 0:
                        dragon_Fire_ImgX[1] = bossX - 100
                        dragon_Fire_ImgY[1] = bossY

                    if dragon_Fire_ImgY[1] == bossY:
                        dragon_Fire_Img_Sound = mixer.Sound(
                            "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\dragon fire.wav")
                        dragon_Fire_Img_Sound.play()

                    if num_Of_frames[5] == 2000:
                        num_Of_frames[5] = 0
                        dragon_Fire_Img_state[1] = "ready"

                collision3 = isCollision(playerX, playerY, dragon_Fire_ImgX[1], dragon_Fire_ImgY[1])
                if collision3:
                    explosionSound = mixer.Sound(
                        "D:\\My programming projects\\PyCharm projects\\Dragon_Slayer\\audios\\explosion.wav")
                    explosionSound.play()
                    dragon_Fire_ImgX[1] = -900
                    dragon_Fire_ImgY[1] = bossY
                    dragon_Fire_ImgX[1] += dragon_Fire_Img_ChangeX[1]
                    health_count -= 2

    # sound img
    if on:
        screen.blit(onSoundImg, (0, 0))
    elif not on:
        screen.blit(offSoundImg, (0, 0))

    # game state
    if not screen_1 and not screen_2:
        screen.blit(health, (30, 550))
        healthNum = font.render(str(health_count), True, (255, 0, 0))
        screen.blit(healthNum, (60, 550))

        ScoreNum = font.render("Score: " + str(score_value), True, (255, 0, 0))
        screen.blit(ScoreNum, (120, 550))

        # screen edges for the player
        if playerX <= -10:
            playerX = -10
        if playerY <= 116:
            playerY = 116
        if playerY >= 368:
            playerY = 368

        # Wizard animation
        if idle_Animation:
            idle.update()
            idle.draw(screen)
        if run_Animation:
            run.update()
            run.draw(screen)
        if attack_Animation:
            attack.update()
            attack.draw(screen)

        # Wizard Fire Movement
        if wizard_Fire_ImgX >= 1000:
            wizard_Fire_ImgX = 0
            wizard_Fire_Img_state = "ready"

        if wizard_Fire_Img_state == "fire":
            fire_Wizard(wizard_Fire_ImgX, wizard_Fire_ImgY)
            wizard_Fire_ImgX += wizard_Fire_Img_ChangeX

        if health_count == 0:
            game_over_text()
        if boss_alife == False:
            Winner()



    pygame.display.flip()
    clock.tick(idle.frame_rate)
