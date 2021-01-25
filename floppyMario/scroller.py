import pygame
import random


"""
This is a replica of the once loved "Flappy Bird" iOS app.

"""

pygame.init()
FPS = 60
gameOver = False
score = 0
scrollSpeedX = 3
screenCornerX = 0
W,H = 800,768
screen = pygame.display.set_mode((W,H))
bg = pygame.image.load("abcdefg.jpg").convert_alpha()
pipe1 = pygame.image.load("pipe1.png").convert_alpha()
pipe2 = pygame.image.load("pipe2.png").convert_alpha()
clock = pygame.time.Clock()
allSprites = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
font = pygame.font.SysFont("impact",36)
dustImgs = ["dust0.png","dust1.png","dust2.png","dust3.png","dust4.png","dust5.png","dust6.png"]
coinImgs = ["stars0.png","stars1.png","stars2.png","stars3.png","stars4.png","stars5.png","stars6.png","stars7.png"]
gapLenghts = [x for x in range(355,485,15)]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mario1.png").convert_alpha()
        self.deathImg = pygame.image.load("mario2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 175
        self.rect.centery = 400
        self.speedx = 0
        self.speedy = 0
        self.isJumping = False
        self.isFalling = True
        self.isDead = False
        self.jumpMag = -18
        self.fallSpeed = 5
        self.rot = 0
    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        if abs(self.jumpMag) > 24:
            self.jumpMag = -18
        if self.isJumping:
            self.speedy = (self.jumpMag)*.85
            self.jumpMag += 0.75
            if self.jumpMag > 2:
                self.isFalling = True
                self.isJumping = False
        elif self.isFalling:
            self.jumpMag -= 0.75
            self.speedy = -(self.jumpMag)*0.75
            if self.speedy > 10:
                self.speedy = 10
                self.isFalling = False
        if self.rect.centery > H:
            self.kill()
        if self.isDead:
            self.image = self.deathImg
            self.speedy = self.fallSpeed
            self.fallSpeed += 0.1
            self.rot -= 3
            self.image = pygame.transform.rotate(self.image,self.rot)
            self.rect = self.image.get_rect(center = (self.rect.centerx,self.rect.centery))
            

class dustExplode(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image = pygame.image.load(dustImgs[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = p.rect.centerx
        self.rect.centery = p.rect.centery
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(dustImgs):
                self.kill()
            else:
                self.image = pygame.image.load(dustImgs[self.frame]).convert_alpha()

class coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image = pygame.image.load(coinImgs[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 60
        self.rect.centery = 100
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(coinImgs):
                self.kill()
            else:
                self.image = pygame.image.load(coinImgs[self.frame]).convert_alpha()
    
        
class obstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,top,speed):
        pygame.sprite.Sprite.__init__(self)
        if top:
            self.image = pipe1
        else:
            self.image = pipe2
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = speed
        self.speedy = 0
        self.isFlashing = False
        self.value = 0
        self.newColor = [0,0,0,0]
    def update(self):
        self.rect.centerx += self.speedx
        if self.isFlashing:
            self.cp = self.image.copy()
            self.value += 50
            self.newColor[0] = self.value%255 
            self.cp.fill(self.newColor[0:3] + [0,], None, pygame.BLEND_RGBA_ADD)
            screen.blit(self.cp,self.rect)
        if self.rect.right < 0:
            global score
            score += 0.5
            c = coin()
            allSprites.add(c)
            self.kill()
    
def spawnObstacle():
    xPos = random.randint(700,1500)
    yPos = random.randint(50,175)
    obstacleSpeedX = -8
    ob = obstacle(xPos,yPos,True,obstacleSpeedX)
    ob2 = obstacle(xPos,ob.rect.bottom + (random.choice(gapLenghts)),False,obstacleSpeedX)
    obstacles.add(ob,ob2)
    allSprites.add(ob,ob2)


p = Player()
playerGroup.add(p)
allSprites.add(p)

while not gameOver:
    if len(playerGroup) < 1:
        score = 0
        p = Player()
        allSprites.add(p)
        playerGroup.add(p)
    if len(obstacles) < 2:
        spawnObstacle()
    playerHitObs = pygame.sprite.groupcollide(obstacles,playerGroup,False,False)
    if playerHitObs:
        d = dustExplode()
        allSprites.add(d)
        p.isDead = True
        for x in playerHitObs:
            x.isFlashing = True
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            gameOver = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if not p.isJumping and not p.isDead:
                    p.isJumping = True
    rel_x = screenCornerX % bg.get_rect().width
    screen.blit(bg,(rel_x-bg.get_rect().width,0))
    if rel_x < W:
        screen.blit(bg,(rel_x,0))
    screenCornerX -= scrollSpeedX
    scoreText = font.render("SCORE: "+str(int(score)),True,(255,255,255))
    screen.blit(scoreText,(20,20))
    allSprites.draw(screen)
    allSprites.update()
    pygame.display.update()
    clock.tick(FPS)
