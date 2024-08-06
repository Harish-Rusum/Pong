import pygame

pygame.init()
pygame.mixer.pre_init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong V.2")

unscaled_bg_img = pygame.image.load("img/Table.png").convert()
bg_img = pygame.transform.scale(unscaled_bg_img, (unscaled_bg_img.get_width() * 10, unscaled_bg_img.get_height() * 10))
unscaled_welcome_screen = pygame.image.load("img/Welcome.png").convert()
welcome_screen = pygame.transform.scale(unscaled_welcome_screen, (unscaled_welcome_screen.get_width() * 10, unscaled_welcome_screen.get_height() * 10))

clock = pygame.time.Clock()
fps = 60

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
        if self.rect.top + dy < 10:
            dy = 0
            self.y_vel = 0
            self.rect.y = 10
        if self.rect.bottom + dy > screen_height - 10:
            dy = 0
            self.y_vel = 0
            self.rect.y = screen_height - 10 - self.rect.height
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

class Ball:
    def __init__(self):
        self.active = False
        self.reset_time = 0
        self.speed_x = 4
        self.speed_y = 4
        self.img = pygame.transform.smoothscale(pygame.image.load("img/Ping_Pong_Ball.png"), (20,20))
        self.rect = self.img.get_rect()
        self.rect.x = screen_width // 2 - (self.img.get_width() // 2)
        self.rect.y = screen_height // 2 - (self.img.get_height() // 2) 

    def reset(self):
        self.rect.x = screen_width // 2 - (self.img.get_width() // 2)
        self.rect.y = screen_height // 2 - (self.img.get_height() // 2)
        self.active = False
        self.reset_time = pygame.time.get_ticks()
        self.speed_x = -self.speed_x

    def update(self,slider1,slider2,surface):
        if self.active:
            self.rect.x += self.speed_x 
            self.rect.y += self.speed_y 

            if self.rect.top <= 0 or self.rect.bottom >= screen_height:
                self.speed_y = -self.speed_y
            if self.rect.colliderect(slider2.rect) or self.rect.colliderect(slider1.rect):
                self.speed_x = -self.speed_x

            if self.rect.left <= slider1.rect.right - 10:
                self.reset()
            if self.rect.right >= slider2.rect.left + 10:
                self.reset()

        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.reset_time >= 2000:
                self.active = True
        self.render(surface) 

    def render(self,surf):
        surf.blit(self.img,self.rect)

def main(fps, clock, width, show_menu=True):
    s1 = Slider( width // 16, 1, 1, 10, False)
    s2 = Slider(width - (width // 16 + s1.rect.width), 1, 1, 10, True)
    ball = Ball()
    run = True
    while run:
        if show_menu:
            screen.blit(welcome_screen, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    show_menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key ==  pygame.K_ESCAPE:
                        run = False
                    else:
                        show_menu = False
        else:
            screen.blit(bg_img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key ==  pygame.K_ESCAPE:
                        run = False

            s1.update(True)
            screen.blit(s1.img, s1.rect)
            s2.update(False)
            screen.blit(s2.img, s2.rect)
            ball.update(s1,s2,screen)

        pygame.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    main(fps, clock, screen_width)

