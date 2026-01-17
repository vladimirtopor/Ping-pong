import pygame as py
import random

class GameSprites(py.sprite.Sprite):
    def __init__(self, name, size, x, y, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.spd = speed
        self.image = py.transform.scale(py.image.load(name), size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
    def show(self):
        window.blit(self.image, (self.x, self.y))

class Player(GameSprites):
    def __init__(self, name, size, x, y, movement):
        super().__init__(name, size, x, y, 3)
        self.mode = movement

    def move_ws(self):
        if py.key.get_pressed()[py.K_w]:
            self.y -= self.spd
        if py.key.get_pressed()[py.K_s]:
            self.y += self.spd
        self.rect[1] = self.y
    def move_ud(self):
        if py.key.get_pressed()[py.K_UP]:
            self.y -= self.spd
        if py.key.get_pressed()[py.K_DOWN]:
            self.y += self.spd
        self.rect[1] = self.y

class Ball(GameSprites):
    def __init__(self, name, size, x, y, spd, spdy):
        super().__init__(name, size, x, y, spd)
        self.spdx = spd
        self.spdy = spdy
    def move(self):
        global boink
        if self.y >= 460 or self.y <= 0:
            self.spdy *= -1
        if py.sprite.collide_rect(self, p1) or py.sprite.collide_rect(self, p2):
            boink += 1
            if boink % 4 == 0:
                self.spdx *= random.choice([1.05, 1.075, 1.1, 1.125, 1.15, 1.175, 1.2])
                self.spdy *= random.choice([1.05, 1.075, 1.1, 1.125, 1.15, 1.175])
            self.spdx *= -1

        self.x, self.y = self.x - self.spdx, self.y - self.spdy
        self.rect.topleft = (self.x, self.y)
# сделать отдельные зоны у платформы (хитбоксы), которые при косании мяча будут выставлять свой self.spdy мячику (например, self.spdy будет равен 0, если мяч прилетел в центральный хитбокс платформы)

window = py.display.set_mode((700, 500))

py.font.init()
txtFont = py.font.SysFont('Arial', 45)
playerstxt = py.font.SysFont('Arial', 35)

p1txt = playerstxt.render('P1', True,  (50, 50, 50))
p2txt = playerstxt.render('P2', True,  (50, 50, 50))
left_win = txtFont.render('Left player win!', True, (219, 42, 42))
right_win = txtFont.render('Right Player win!', True, (219, 42, 42))

p1 = Player('platform.png', (20, 150), 20, 175, 'ws')
p2 = Player('platform.png', (20, 150), 660, 175, 'arrow')
ball = Ball('Tennis-Ball.png', (40, 40), 330, 230, 3, 2)

boink = 0
clock = py.time.Clock()
finnish = 0
finnish_time = 0
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = 0

    if not finnish:
        p1.move_ws()
        p2.move_ud()
        ball.move()

        if ball.rect[0] >= 640:
            winner = 1
            finnish = 1
        elif ball.rect[0] <= 20:
            winner = 2
            finnish = 1

        window.fill((187, 237, 252))
        p1.show()
        p2.show()
        ball.show()
        window.blit(p1txt, (10, 5))
        window.blit(p2txt, (655, 5))
    elif finnish:
        finnish_time += 1
        if winner == 1:
            window.blit(left_win, (215, 150))
        elif winner == 2:
            window.blit(right_win, (215, 150))
    if finnish_time >= 180:
        running = 0
    py.display.update()
    clock.tick(60)