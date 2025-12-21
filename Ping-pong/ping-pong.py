import pygame as py

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
        if self.y >= 460 or self.y <= 0:
            self.spdy *= -1
        if py.sprite.collide_rect(self, p1) or py.sprite.collide_rect(self, p2):
            self.spdx *= -1

        self.x, self.y = self.x - self.spdx, self.y - self.spdy
        self.rect.topleft = (self.x, self.y)

window = py.display.set_mode((700, 500))

p1 = Player('platform.png', (20, 150), 20, 175, 'ws')
p2 = Player('platform.png', (20, 150), 660, 175, 'arrow')
ball = Ball('Tennis-Ball.png', (40, 40), 330, 230, 3, 2)

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
            print('Left player win!')
            finnish = 1
        elif ball.rect[0] <= 20:
            print('Right Player win!')
            finnish = 1

        window.fill((187, 237, 252))
        p1.show()
        p2.show()
        ball.show()
    elif finnish:
        finnish_time += 1
    if finnish_time >= 180:
        running = 0
    py.display.update()
    clock.tick(60)