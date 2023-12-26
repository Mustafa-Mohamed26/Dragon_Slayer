import pygame
import sys
import os

from PIL import ImageTk


class AnimatedObject:
    def __init__(self, image_folder, image_files, frame_rate, speed):
        self.images = [pygame.image.load(os.path.join(image_folder, img)).convert_alpha() for img in image_files]
        self.current_frame = 0
        self.frame_rate = frame_rate
        self.speed = speed
        self.x, self.y = 0, 0
        self.key_state = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}

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
                if key == pygame.K_LEFT:
                    self.x -= self.speed
                elif key == pygame.K_RIGHT:
                    self.x += self.speed
                elif key == pygame.K_UP:
                    self.y -= self.speed
                elif key == pygame.K_DOWN:
                    self.y += self.speed

        self.current_frame = (self.current_frame + 1) % len(self.images)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.images[self.current_frame], (self.x, self.y))


# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Animation")

# Set up clock to control the frame rate
clock = pygame.time.Clock()

# Create AnimatedObject instance
animated_object = AnimatedObject(
    "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE",
    ["D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\IDLE\\1_IDLE_000.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE\\1_IDLE_001.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE\\1_IDLE_002.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE\\1_IDLE_003.png",
     "D:\\My programming projects\\PyCharm projects\\Dragon Slayer\\imges\\Fire Wizard\\IDLE\\1_IDLE_004.png"],
    frame_rate=12, speed=10)
animated_object.x = 100
animated_object.y = 200
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        animated_object.handle_events(event)

    animated_object.update()
    animated_object.draw(screen)

    pygame.display.flip()
    clock.tick(animated_object.frame_rate)
