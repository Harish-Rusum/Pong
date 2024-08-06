import pygame

# Initialize Pygame and the mixer for sounds
pygame.init()
pygame.mixer.pre_init()

# Set up the screen dimensions and display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong V.2")

# Load and scale background images
unscaled_bg_img = pygame.image.load("img/Table.png").convert()
bg_img = pygame.transform.scale(unscaled_bg_img, (unscaled_bg_img.get_width() * 10, unscaled_bg_img.get_height() * 10))
unscaled_welcome_screen = pygame.image.load("img/Welcome.png").convert()
welcome_screen = pygame.transform.scale(unscaled_welcome_screen, (unscaled_welcome_screen.get_width() * 10, unscaled_welcome_screen.get_height() * 10))

# Setting up fps thing
clock = pygame.time.Clock()
fps = 60

# Define the Slider class for player paddles
class Slider:
    def __init__(self, x, acc, decc, max_speed, flip):
        self.unscaled_img = pygame.image.load("img/Slider.png").convert()
        self.img = pygame.transform.scale(self.unscaled_img, (self.unscaled_img.get_width() * 6, self.unscaled_img.get_height() * 6))
        if flip:
            self.img = pygame.transform.flip(self.img, True, False)
        self.img.set_colorkey((0, 0, 0))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = screen_height // 2 - self.rect.height // 2
        self.y_vel = 0
        self.acc = acc
        self.decc = decc
        self.max_speed = max_speed

    def update_pos(self, dx, dy):
        if self.rect.top + dy < 40:
            dy = 0
            self.y_vel = 0
            self.rect.y = 40
        if self.rect.bottom + dy > screen_height - 40:
            dy = 0
            self.y_vel = 0
            self.rect.y = screen_height - 40 - self.rect.height
        self.y_vel = max(-self.max_speed, min(self.max_speed, self.y_vel))
        self.rect.x += dx
        self.rect.y += dy

    def move_up(self):
        self.y_vel -= self.acc

    def move_down(self):
        self.y_vel += self.acc

    def idle(self):
        if self.y_vel > 0:
            self.y_vel = max(0, self.y_vel - self.decc)
        else:
            self.y_vel = min(0, self.y_vel + self.decc)

    def update(self, is_right_player):
        keys = pygame.key.get_pressed()
        if is_right_player:
            if keys[pygame.K_w]:
                self.move_up()
            elif keys[pygame.K_s]:
                self.move_down()
            else:
                self.idle()
        else:
            if keys[pygame.K_UP]:
                self.move_up()
            elif keys[pygame.K_DOWN]:
                self.move_down()
            else:
                self.idle()
        self.update_pos(0, self.y_vel)

# Main function to run the game
def main(fps, clock, width, show_menu=True):
    # Player slider definitions
    s1 = Slider( width // 16, 1, 1, 10, False)
    s2 = Slider(width - (width // 16 + s1.rect.width), 1, 1, 10, True)

    # Run the game loop
    run = True
    while run:
        if show_menu:
            screen.blit(welcome_screen, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    show_menu = False
        else:
            screen.blit(bg_img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Update and render sliders
            s1.update(True)
            screen.blit(s1.img, s1.rect)
            s2.update(False)
            screen.blit(s2.img, s2.rect)

        pygame.display.update()
        clock.tick(fps)

# Run the game if the script is executed
if __name__ == "__main__":
    main(fps, clock, screen_width)

