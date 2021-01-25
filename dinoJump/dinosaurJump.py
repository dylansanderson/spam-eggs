import pygame
import random
import math

W, H = 800, 800
pygame.init()
fps = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W,H))
bg = pygame.image.load("cloud.jpg").convert()
font = pygame.font.SysFont("Arial",36)
smallFont = pygame.font.SysFont("Arial",14)
PLAYERFALLSPEED = 6
dinosaurFacingRight = pygame.image.load("dinosaurSheet0.png").convert_alpha()
dinosaurFacingLeft = pygame.image.load("dinosaurSheet3.png").convert_alpha()
dinosaurJumpingRight = pygame.image.load("dinosaurSheet1.png").convert_alpha()
dinosaurLiedownRight = pygame.image.load("dinosaurSheet4.png").convert_alpha()
dinosaurLiedownLeft = pygame.image.load("dinosaurSheet5.png").convert_alpha()
dinosaurShoot1 = pygame.image.load("dinosaurShoot1.png").convert_alpha()
dinosaurShoot2 = pygame.image.load("dinosaurShoot2.png").convert_alpha()
bulletImgR = pygame.image.load("flame2.png").convert_alpha()
bulletImgL = pygame.image.load("flame.png").convert_alpha()
angles = []
for i in range(0,1000,3):
    angles.append(-i)
y = 0
score = 0
health = 100
bombImg = pygame.image.load("bomb.png").convert_alpha()
explodeImgList =["lol0.png","lol1.png","lol2.png","lol3.png","lol4.png","lol5.png","lol6.png","lol7.png"]
fruitImgs = [pygame.image.load('grape.png').convert_alpha(),pygame.image.load('cherry.png').convert_alpha(),pygame.image.load('pancake.png').convert_alpha()]
shieldIMG = pygame.image.load("playerShield.png").convert_alpha()
shieldIMGsmall = pygame.image.load("playerShield2.png").convert_alpha()
screenSpeed = 6

class bomb(pygame.sprite.Sprite):
    def __init__(self,vel,angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = bombImg
        self.coinToss = random.randint(0,1)
        if self.coinToss == 0:
            self.X = 0
        else:
            self.X = W
        self.Y = random.randint(0,H-200)
        self.Xoffset = self.X
        self.Yoffset = self.Y
        self.rect = self.image.get_rect(center = (self.X,self.Y))
        self.angle = angle
        self.vel = vel
        self.t = 0
        if self.coinToss == 0:
            self.vx = (self.vel * math.cos(math.radians(self.angle)))
        else:
            self.vx = -(self.vel * math.cos(math.radians(self.angle)))
        self.vy = (self.vel * math.sin(math.radians(self.angle)))
    def update(self):
        self.rect = self.image.get_rect(center = (self.X,self.Y))
        self.X = self.Xoffset + self.vx * self.t
        self.Y = self.Yoffset - (self.vy*self.t-(9.81/2)*self.t*self.t)
        self.t += 0.2
        if self.Y > H:
            self.kill()
    


class bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletImgR
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = -6
        self.speedx = 10
        self.now = pygame.time.get_ticks()
    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        if self.rect.centerx > W:
            self.kill()

class bullet2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletImgL
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = -6
        self.speedx = -10
        self.now = pygame.time.get_ticks()
    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        if self.rect.centerx < 0:
            self.kill()



class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = dinosaurFacingRight
        self.rect = self.image.get_rect()
        self.rect.centerx = W/2
        self.rect.centery = H/3
        self.rect = self.image.get_rect(center= (self.rect.centerx, self.rect.centery))
        self.rect = self.rect.inflate(-30, 0)
        self.sprintImage1 = pygame.image.load("wind0.png").convert_alpha()
        self.sprintImage2 = pygame.image.load("wind1.png").convert_alpha()
        self.speedx = 0
        self.accel = 1
        self.speedy = 8
        self.shield = False
        self.isJump = False
        self.jumpMag = -17
        self.isDead = False
        self.rot = 0
        self.angleIndex = 0
    def update(self):
        self.rot += 1
        self.rect.centerx += self.speedx*self.accel
        self.rect.centery += self.speedy
        pygame.draw.line(screen,(0,0,0),(self.rect.left,self.rect.bottom),(self.rect.right,self.rect.bottom))
        self.speedx = 0
        if self.shield:
            screen.blit(shieldIMG,(self.rect.centerx - 65,self.rect.centery-80))
        if self.isJump and not p1.isDead:
            self.image = dinosaurJumpingRight
            self.speedy = self.jumpMag
            self.jumpMag += .5
            if self.jumpMag > -1.8:
                self.isJump = False
                self.jumpMag = -17
        if self.rect.bottom > H and not self.isDead:
            global health
            health -= 20
            self.rect.centery = self.rect.centery - 450
        if self.rect.centery < 0 and not self.isJump:
            health -= .5
        ks = pygame.key.get_pressed()
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.accel = 2
            self.Running = True
            if self.image == dinosaurFacingRight:
                screen.blit(self.sprintImage1,(self.rect.centerx-100,self.rect.centery-35))
            else:
                screen.blit(self.sprintImage2,(self.rect.centerx+75,self.rect.centery-35))
        else:
            self.accel = 1
        if ks[pygame.K_d] and not p1.isDead:
            self.image = dinosaurFacingRight
            self.speedx = 7
        if ks[pygame.K_a] and not p1.isDead:
            self.image = dinosaurFacingLeft
            self.speedx = -7
    def jump(self):
        if p1.speedy != PLAYERFALLSPEED:
            self.isJump = True
    def die(self):
        self.isDead = True
        self.isJump = True
        if self.rot % 1 == 0:
            self.image = dinosaurLiedownRight
            self.image = pygame.transform.rotate(self.image,angles[self.angleIndex])
            self.angleIndex += 1
        if self.angleIndex == len(angles):
            self.angleIndex = 0
        self.speedy = PLAYERFALLSPEED
        if self.rect.centery > H -1:
            self.kill()
            global gameOver
            gameOver = True



class platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.randomRocketNumber = int(random.uniform(1,60))
        self.randomPlatformNumber = int(random.uniform(1,30))
        self.randomShieldNumber = int(random.uniform(1,60))
        self.image=pygame.image.load("cloudPlatform.png").convert_alpha()
        self.transformedIMG = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.uniform(25,W-40)
        self.rect.centery = H + random.uniform(10,H)
        self.speedx = random.randint(-2,2)
        self.speedy = random.randint(4,8)
        self.fruitChoice= random.choice(fruitImgs)
        self.touched = False
        
    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery -= self.speedy
        if self.rect.right > W:
            self.speedx = -self.speedx
        if self.rect.left < 0:
            self.rect.centerx = self.rect.centerx + 3
            self.speedx = -self.speedx
        if self.rect.bottom < 0:
            global score
            score += 1
            self.randomShieldNumber = int(random.uniform(1,60))
            self.randomRocketNumber = int(random.uniform(1,60))
            self.randomPlatformNumber = int(random.uniform(1,30))
            self.touched = False
            self.rect = self.image.get_rect()
            self.rect.centerx = random.uniform(25,W-40)
            self.rect.centery = H + random.uniform(0,2*H)
            self.speedx = random.randint(-2,2)
            self.speedy = random.randint(4,8)
            if score > 50 and score < 150:
                self.speedy = random.randint(6,9)
            if score >= 150 and score <= 200:
                self.speedy = random.randint(7,10)
                self.speedx = random.randint(-3,3)
            if score > 200:
                self.speedy = random.randint(9,12)
                self.speedx = random.randint(-3,3)
        if self.randomPlatformNumber == 2:
            self.image = self.transformedIMG
        else:
            self.image = pygame.image.load("cloudPlatform.png").convert_alpha()

        if self.randomPlatformNumber == 5:
            if not self.touched:
                screen.blit(self.fruitChoice,(self.rect.centerx-20,self.rect.centery-50))
        if self.randomShieldNumber == 7:
            if not self.touched:
                screen.blit(shieldIMGsmall,(self.rect.centerx-20,self.rect.centery-50))
        if self.touched:
            if self.randomPlatformNumber == 2:
                self.rect = self.image.get_rect(center = (p1.rect.centerx,random.randint(0,H)))
                self.touched = False
        if self.randomRocketNumber % 5 == 0:
            coinFlip = random.randint(0,3)
            if coinFlip == 0:
                r = Rocket(0,random.randint(0,H))
                rocketGroup.add(r)
                all_sprites.add(r)
            elif coinFlip == 1:
                r = Rocket2(W-1,random.randint(0,H))
                rocketGroup.add(r)
                all_sprites.add(r)
            elif coinFlip == 2:
                r = Rocket3(random.randint(0,W),H)
                rocketGroup.add(r)
                all_sprites.add(r)
            else:
                r = Rocket4(random.randint(0,W),0)
                rocketGroup.add(r)
                all_sprites.add(r)
            self.randomRocketNumber = random.randint(1,25)


class Rocket(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("missile.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 3
        self.speedy = random.randint(-9,-3)
    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        if self.rect.left > W:
            self.kill()

class Rocket2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("missile2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 3
        self.speedy = random.randint(-9,-3)
    def update(self):
        self.rect.centerx -= self.speedx
        self.rect.centery += self.speedy
        if self.rect.right < 0:
            self.kill()

class Rocket3(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("missile3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = random.randint(-2,2)
        self.speedy = screenSpeed + 6
    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery -= self.speedy
        if self.rect.bottom < 0:
            self.kill()
    


class Rocket4(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("missile4.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = random.randint(-2,2)
        self.speedy = -5
    def update(self):
        self.rect.centery -= self.speedy
        self.rect.centerx += self.speedx
        if self.rect.bottom < 0:
            self.kill()


class explode(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("lol0.png").convert_alpha()
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
            if self.frame == len(explodeImgList):
                self.kill()
            else:
                self.image = pygame.image.load(explodeImgList[self.frame]).convert_alpha()

gameOver = False
all_sprites = pygame.sprite.Group()
platformGroup = pygame.sprite.Group()
rocketGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
bombGroup = pygame.sprite.Group()

for i in range(10):
    p = platform()
    all_sprites.add(p)
    platformGroup.add(p)

p1 = player()
playerGroup = pygame.sprite.Group()
playerGroup.add(p1)
all_sprites.add(p1)

while not gameOver:
    bombNumber = random.randint(0,750)
    if bombNumber == 50:
        b = bomb(50,45)
        all_sprites.add(b)
        bombGroup.add(b)
    if len(platformGroup) < 10:
        p = platform()
        all_sprites.add(p)
        platformGroup.add(p)
    bombHitPlayer = pygame.sprite.groupcollide(playerGroup,bombGroup,False,True)
    bombHitPlat = pygame.sprite.groupcollide(bombGroup,platformGroup,True,True)
    playerHitPlat = pygame.sprite.groupcollide(platformGroup,playerGroup,False,False)
    rocketHitPlat = pygame.sprite.groupcollide(rocketGroup,platformGroup,True,True)
    rocketHitDino = pygame.sprite.groupcollide(rocketGroup,playerGroup,True,False)
    bulletHitRocket = pygame.sprite.groupcollide(bulletGroup,rocketGroup,True,True)
    if bombHitPlayer:
        for i in bombHitPlayer:
            if not p1.shield:
                health -= 50
            else:
                p1.shield = False
            e = explode(i.rect.centerx,i.rect.centery)
            all_sprites.add(e)
    if bombHitPlat:
        for i in bombHitPlat:
            e = explode(i.rect.centerx,i.rect.centery)
            all_sprites.add(e)
    if rocketHitDino:
        for i in rocketHitDino:
            e = explode(i.rect.centerx,i.rect.centery)
            all_sprites.add(e)
            if not p1.shield:
                health -= 50
            else:
                p1.shield = False
    if health < 1:
        health = 0
        p1.die()
    if playerHitPlat and not p1.isJump:
        for i in playerHitPlat:
            if i.randomPlatformNumber == 5:
                if health <= 75:
                    health += 25
                else:
                    health = 100
                i.randomPlatformNumber = 6
            if i.randomShieldNumber == 7:
                p1.shield = True
                i.randomShieldNumber = 8
            if p1.rect.bottom <= i.rect.centery+25:
                i.touched = True
                p1.speedy = -i.speedy
                ks = pygame.key.get_pressed()
                if ks[pygame.K_d] or ks[pygame.K_a]:
                    pass
                else:
                    p1.speedx = i.speedx
    else:
        if not p1.isJump:
            p1.speedy = PLAYERFALLSPEED

    if rocketHitPlat:
        for i in rocketHitPlat:
            e = explode(i.rect.centerx,i.rect.centery)
            p = platform()
            all_sprites.add(p)
            platformGroup.add(p)
            all_sprites.add(e)
    
    rel_y = y % screen.get_rect().height
    screen.blit(bg,(0,rel_y - screen.get_rect().height))
    if rel_y < H:
        screen.blit(bg,(0,rel_y))
    y -= screenSpeed
    all_sprites.draw(screen)
    all_sprites.update()
    posText = smallFont.render("("+str(p1.rect.centerx) + "," + str(p1.rect.centery) +")",True,(0,0,0))
    scoreText = font.render("SCORE: "+str(score),True,(0,0,0))
    healthText = smallFont.render(str(health),True,(0,0,0))
    pygame.draw.rect(screen,(0,0,255),(W-205,2,200,20))
    pygame.draw.rect(screen,(255,0,0),(W-205,2,2*health,20))
    pygame.draw.line(screen,(255,0,0),(0,1),(W,1),4)
    screen.blit(scoreText,(20,20))
    screen.blit(healthText,(W-50,20))
    screen.blit(posText,(W/2,25))
    pygame.display.update()
    clock.tick(fps)
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                p1.jump()
            if e.key == pygame.K_t:
                b = bomb(random.randint(25,50),45)
                bombGroup.add(b)
                all_sprites.add(b)
        if e.type == pygame.MOUSEBUTTONDOWN:
            if p1.image == dinosaurFacingRight or p1.image == dinosaurShoot1:
                p1.image = dinosaurShoot1
                b = bullet(p1.rect.centerx,p1.rect.centery)
                all_sprites.add(b)
                bulletGroup.add(b)
            if p1.image == dinosaurFacingLeft or p1.image == dinosaurShoot2:
                p1.image = dinosaurShoot2
                b = bullet2(p1.rect.centerx,p1.rect.centery)
                all_sprites.add(b)
                bulletGroup.add(b)
        if e.type == pygame.QUIT:
            gameOver = True
print("DONE")
quit()