import pygame
import random
import math
import time

W, H = 720, 800
pygame.init()
pygame.mixer.init()
laser = pygame.mixer.Sound('laser.wav')
boom = pygame.mixer.Sound('boom.wav')             #sounds
FPS = 60
score = 0
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W,H))

font = pygame.font.SysFont("Arial",36)
font2 = pygame.font.SysFont("Arial",24)
bulletSize = 10
y = 0
bgimg1 = pygame.image.load("parallax.JPG").convert_alpha()
bgimg2 = pygame.image.load("skyBG2.PNG").convert_alpha()
bgimg3 = pygame.image.load("parallax3.PNG").convert_alpha()
bgimg4 = pygame.image.load("parallax4.PNG").convert_alpha()           
                                                                                                                   #load all images
smallBGList = ["bgParallax.PNG","skyBG.PNG","parallax3i.PNG","parallax4i.PNG"]           #small BGs for choose background screen

shooterImage1 = pygame.image.load("SHOOTER.png").convert_alpha()
shooterImage2 = pygame.image.load("shooter2.PNG").convert_alpha()                         #3 character images
shooterImage3 = pygame.image.load("shooter3.PNG").convert_alpha()


explosions = ["exp0.png","exp1.png","exp2.png","exp3.png","exp4.png","exp5.png","exp6.png","exp7.png"]    # explosion sequence list
explosions2 = ["hugeExplode0.PNG","hugeExplode01.PNG","hugeExplode02.PNG","hugeExplode03.PNG","hugeExplode04.PNG","hugeExplode05.PNG","hugeExplode06.PNG","hugeExplode07.PNG","hugeExplode08.PNG","hugeExplode09.PNG"]


centerxPositions = []                     #all possible centerx positions for the bars 
for i in range(0,W,75):
    centerxPositions.append(i)


barSpeed = -5
p1speed = 8

class bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((bulletSize,bulletSize))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 35
        self.now = pygame.time.get_ticks()
    def update(self):
        self.rect.centery += self.speedy
        if self.rect.centery > H:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        if x == 0:
            self.image = shooterImage1
        if x == 1:
            self.image = shooterImage2
        if x == 2:
            self.image = shooterImage3
        self.rect = self.image.get_rect()
        self.rect.centerx = W / 2
        self.rect.centery = 50
        self.speedx = 0
        self.speedy = 0
    def update(self):
        if self.rect.right > W:
            self.rect.right = self.rect.right - 10
            self.speedx = -self.speedx
        if self.rect.left < 0:
            self.speedy = -self.speedy
            self.speedx = -self.speedx
            self.rect.centerx = self.rect.centerx + 10
        if self.rect.centery < 0:
            self.rect.centery = self.rect.centery + 1
            self.speedy = -self.speedy
        ks = pygame.key.get_pressed()
        if ks[pygame.K_d]:
            self.speedx = 6
        if ks[pygame.K_a]:
            self.speedx = -6
        
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        self.speedx = 0
        self.speedy = 0
    def shoot(self):
        bull = bullet(p1.rect.centerx + 5,p1.rect.centery + 50)
        ALL_SPRITES.add(bull)
        bullets.add(bull)



class explode(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("exp0.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosions):
                self.kill()
            else:
                self.image = pygame.image.load(explosions[self.frame]).convert_alpha()

class explode2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("hugeExplode0.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 45
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosions2):
                global gameOver
                gameOver = True
                self.kill()
            else:
                self.image = pygame.image.load(explosions2[self.frame]).convert_alpha()



class bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.platWidth = random.randint(50,175)
        self.num2 = random.randint(1,20)
        self.image=pygame.Surface((self.platWidth,30)).convert_alpha()
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(centerxPositions)
        self.rect.centery = H + random.uniform(10,H)
        self.speedx = 0
        self.speedy = barSpeed
        self.splitAmount= 2
        self.hitCount = 0
    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        if self.num2 == 2 or self.num2 == 3:
            self.image.fill((255,0,0))
        if self.rect.centery < 0:
            global score
            score += 1
            self.num2 = random.randint(1,20)
            self.hitCount = 0
            self.splitAmount= 2
            self.platWidth = random.randint(50,200)
            self.image=pygame.Surface((self.platWidth,30)).convert_alpha()
            self.image.fill((0,255,0))
            self.rect = self.image.get_rect()
            self.rect.centerx = random.uniform(0,W)
            self.rect.centery = H + random.uniform(10,H)
            self.speedx = 0
            self.speedy = barSpeed
        if self.num2 == 4:
            self.image.fill((255,255,255))
        if self.hitCount == 3:
            self.die()
            self.platWidth = random.randint(50,175)
            self.image=pygame.Surface((self.platWidth,30))
            self.image.fill((0,255,0))
            self.rect = self.image.get_rect()
            self.rect.centerx = random.uniform(0,W)
            self.rect.centery = H + random.uniform(10,H)
            self.speedx = 0
            self.speedy = -5
            self.splitAmount = 2
            self.hitCount = 0
        
    def split(self):
        self.image = pygame.Surface((self.platWidth / self.splitAmount,30))
        self.rect = self.image.get_rect(center = (self.rect.centerx,self.rect.centery))      #make platform smaller
        self.splitAmount += 0.7
    def die(self):
        e = explode(self.rect.centerx,self.rect.centery)                       #small explosion if bar is hit with bullet
        ALL_SPRITES.add(e)
    def HugeDie(self):
        e = explode2(self.rect.centerx,self.rect.centery)                            #big explosion if bar hits player
        ALL_SPRITES.add(e)
    




ALL_SPRITES = pygame.sprite.Group()
bullets = pygame.sprite.Group()             #Groups
bars = pygame.sprite.Group()


gameOver = False
startScreen = True      #initial bool values for 3 possible screens
charScreen = False
bgScreen = False


e = bar()
e2 = bar()
e3 = bar()                   #spawn 4 enemies initially
b = bar()
bars.add(e,e2,e3,b)
ALL_SPRITES.add(e,e2,e3,b)


bg = pygame.Surface((screen.get_size()))
index = 0
startText = font.render("START",True,(0,0,0))
arrow = font.render("<---",True,(0,0,0))                               #start screen text items
arrowpositions = [(W/2+100,H/2),(W/2+250,H/2 + 100)]
characterScreenText = font2.render("CHARACTER SELECT",True,(0,0,0))

prevTime = pygame.time.get_ticks()
bGIndex = 0
bg.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
while startScreen:
    now = pygame.time.get_ticks()
    if now - prevTime > 2000:
        prevTime = now
        bg.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))       
        bGIndex += 1
        if bGIndex >= len(bgImageList):
            bGIndex = 0
    screen.blit(bg,(0,0))
    screen.blit(startText,(W/2,H/2))
    screen.blit(characterScreenText,(W/2,H/2 + 100))
    screen.blit(arrow,arrowpositions[index])
    ALL_SPRITES.draw(screen)
    ALL_SPRITES.update()
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            startScreen = False
            gameOver = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN and index == 0:
                startScreen = False
                bgScreen = True
                p1 = Player(random.randint(0,2))
                ALL_SPRITES.add(p1)
            if e.key == pygame.K_RETURN and index == 1:
                startScreen = False
                charScreen = True
            if e.key == pygame.K_DOWN:
                if index < 1:
                    index += 1
            if e.key == pygame.K_UP:
                if index > 0:
                    index -= 1
    clock.tick(FPS)



index = 0
arrowpositions = [(W/2+50,H/2),(W/2+50,H/2 + 100),(W/2+50,H/2 + 200)]
while charScreen:
    screen.blit(bg,(0,0))
    bg.fill((0,255,255))
    screen.blit(characterScreenText,(W/2 - 100,50))
    screen.blit(arrow,arrowpositions[index])
    screen.blit(shooterImage1,(W/2,H/2))
    screen.blit(shooterImage2,(W/2,H/2 + 100))
    screen.blit(shooterImage3,(W/2,H/2 + 200))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            gameOver = True
            charScreen = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN and index == 0:
                charScreen = False
                bgScreen = True
                p1 = Player(0)
                ALL_SPRITES.add(p1)
            if e.key == pygame.K_RETURN and index == 1:
                charScreen = False
                bgScreen = True
                p1 = Player(1)
                ALL_SPRITES.add(p1)
            if e.key == pygame.K_RETURN and index == 2:
                charScreen = False
                bgScreen = True
                p1 = Player(2)
                ALL_SPRITES.add(p1)
            if e.key == pygame.K_DOWN:
                if index < 2:
                    index += 1
            if e.key == pygame.K_UP:
                if index > 0:
                    index -= 1
    pygame.display.update()
    clock.tick(FPS)



index = 0
arrowPositions = [(W/4+50,100),(W/2+200,100),(W/4+50,500),(W/2+200,500)]
bgText = font2.render("CHOOSE A BACKGROUND",True,(0,0,0))
bg = pygame.Surface((screen.get_size()))
while bgScreen:
    screen.blit(bg,(0,0))
    bg.fill((0,255,255))
    screen.blit(bgText,(W/2-250,0))
    screen.blit(pygame.image.load(smallBGList[0]),(W/4,100))
    screen.blit(pygame.image.load(smallBGList[1]),(W/2,100))
    screen.blit(pygame.image.load(smallBGList[2]),(W/4,500))
    screen.blit(pygame.image.load(smallBGList[3]),(W/2,500))
    screen.blit(arrow,arrowPositions[index])
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            gameOver = True
            bgScreen = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN and index == 0:
                bgScreen = False
                bg = bgimg1
            if e.key == pygame.K_RETURN and index == 1:
                bgScreen = False
                bg = bgimg2
            if e.key == pygame.K_RETURN and index == 2:
                bgScreen = False
                bg = bgimg3
            if e.key == pygame.K_RETURN and index == 3:
                bgScreen = False
                bg = bgimg4
            if e.key == pygame.K_DOWN:
                if index < 3:
                    index += 1
            if e.key == pygame.K_UP:
                if index > 0:
                    index -= 1
        pygame.display.update()
        clock.tick(FPS)
        

for i in bars:
    i.rect.centery = random.randint(H,H+500)

score = 0
while not gameOver:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            gameOver = True                    #event loop
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                laser.play()
                p1.shoot()
    rel_y = y % screen.get_rect().height
    screen.blit(bg,(0,rel_y - screen.get_rect().height))
    if rel_y < H:                                                
        screen.blit(bg,(0,rel_y))
    y -= barSpeed
    barHit = pygame.sprite.spritecollide(p1,bars,True)
    bulletHitBar = pygame.sprite.groupcollide(bars,bullets,False,True)
    if bulletHitBar:
        for i in bulletHitBar:
            if i.num2 == 1:
                i.image.fill((255,255,0))
                i.speedy = 1.5 * i.speedy
            if i.num2 == 2 or i.num2 == 3:
                boom.play()
                i.HugeDie()
                i.kill()
            if i.num2 == 4:
                i.rect.centery = i.rect.centery + 800
                i.rect.centerx = random.choice(centerxPositions)
                score += 1
            else:
                i.hitCount += 1
                i.split()
                score += 1
    if barHit:
        for i in barHit:
            boom.play()
            p1.kill()
            i.HugeDie()
    if score == 6:
        b2 = bar()
        bee = bar()
        ALL_SPRITES.add(b2,bee)
        bars.add(bee,b2)
        score += 1
    if score == 15:
        b3 = bar()
        b4 = bar()
        b5 = bar()
        bars.add(b3,b4,b5)
        ALL_SPRITES.add(b3,b4,b5)
        score += 1
    if score == 35:
        b6 = bar()
        bars.add(b6)
        ALL_SPRITES.add(b6)
        score += 1
    if score == 60:
        b7 = bar()
        b8 = bar()
        bars.add(b7,b8)
        ALL_SPRITES.add(b7,b8)
        score += 1
    if score == 120:
        b9 = bar()
        b10 = bar()
        ALL_SPRITES.add(b9,b10)
        bars.add(b9,b10)
        score += 1
    if score == 180:
        b11 = bar()
        ALL_SPRITES.add(b11)
        bars.add(b11)
        score += 1
    scoreText = font.render("SCORE:" + str(score) + "    BARS: " + str(len(bars)),True,(255,0,0))
    screen.blit(scoreText,(W/2,H-50))
    pygame.draw.line(screen,(0,0,0),(400,rel_y),(500,rel_y))
    ALL_SPRITES.draw(screen)
    ALL_SPRITES.update()
    pygame.display.update()
    clock.tick(FPS)
time.sleep(1)