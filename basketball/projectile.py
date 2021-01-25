import pygame
import math
import random
pygame.init()
W,H = 800,800
fps = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W,H))

monsterImg1 = pygame.image.load("monster.png").convert_alpha()
monsterImg2 = pygame.image.load("monster2.png").convert_alpha()
stars =["stars1.png","stars2.png","stars3.png","stars4.png","stars5.png","stars6.png"]
font = pygame.font.SysFont("Arial",25)


arrowText1 = font.render("-->",True,(0,0,0))
arrowText2 = font.render("<--",True,(0,0,0))

class basket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,10))
        self.image2 = pygame.image.load("net.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,W-30)
        self.rect.centery = random.randint(400,600)
        self.speedx = random.randint(-3,3)
        self.hit = False
    def update(self):
        self.rect.centerx += self.speedx
        if self.rect.right > W:
            self.rect.centerx = self.rect.centerx - 1
            self.speedx = -self.speedx
        if self.rect.left < 0:
            self.rect.centerx += 1
            self.speedx =-self.speedx
        screen.blit(self.image2,(self.rect.centerx-40,self.rect.centery))
        if self.hit:
            self.hit = False
    def move(self):
        self.speedx = random.randint(-3,3)
        self.rect.centerx = random.randint(0,W-30)
        self.rect.centery = random.randint(400,600)
        self.rect = self.image.get_rect(center = (self.rect.centerx,self.rect.centery))
    def explode(self):
        s = starExplode()
        ALL_SPRITES.add(s)


class ball(pygame.sprite.Sprite):
    def __init__(self,vel, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bball.png").convert_alpha()
        self.X = p1.rect.centerx
        self.Y = p1.rect.centery
        self.rect = self.image.get_rect(center = (self.X,self.Y))
        self.Xoffset = p1.rect.centerx
        self.Yoffset = p1.rect.centery
        self.madeShot = False
        self.t = 0
        self.vel = vel
        self.acc = 3
        self.angle = angle
        self.vx = (self.vel * math.cos(math.radians(self.angle)))
        self.vy = (self.vel * math.sin(math.radians(self.angle)))
        self.Yvalues = []
        self.hitRim = False
        self.rot = 0
    def update(self):
        self.rot += 1
        if self.rot % 3 == 0:
            self.image = pygame.transform.rotate(self.image,90)
        if self.madeShot:
            self.rot = 0
            self.rect = self.image.get_rect(center = (self.X,self.Y+50))
            p1.shot = False
            self.Y += self.acc
            self.acc += .3
            self.t += 0.2
            if self.Y > H:
                self.kill()
        if self.hitRim:
            self.rect = self.image.get_rect(center = (self.X,self.Y))
            p1.shot = False
            self.Y = self.Y + (self.acc - 1)
            self.acc += .3
            if self.Y > H:
                self.kill()
        if not (self.madeShot or self.hitRim):
            self.rect = self.image.get_rect(center = (self.X,self.Y))
            p1.shot = False
            self.X = self.Xoffset + self.vx * self.t
            self.Y = self.Yoffset - (self.vy*self.t-(9.81/2)*self.t*self.t)
            self.Yvalues.append(self.Y)
            self.t += 0.2
            if self.X > W:
                self.kill()
            if self.Y > H:
                self.kill()
        
class starExplode(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image = pygame.image.load(stars[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = basket1.rect.centerx
        self.rect.centery = basket1.rect.centery
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30
        self.done = False
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(stars):
                self.done = True
                self.kill()
            else:
                self.image = pygame.image.load(stars[self.frame]).convert_alpha()
        

           

class ball2(pygame.sprite.Sprite):
    def __init__(self,vel, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bball.png")
        self.X = p1.rect.centerx
        self.Y = p1.rect.centery
        self.Xoffset = p1.rect.centerx
        self.Yoffset = p1.rect.centery
        self.rect = self.image.get_rect(center = (self.X,self.Y))
        self.t = 0
        self.vel = vel
        self.madeShot = False
        self.acc = 3
        self.angle = angle
        self.vx = -(self.vel * math.cos(math.radians(self.angle)))
        self.vy = (self.vel * math.sin(math.radians(self.angle)))
        self.Yvalues = []
        self.rot = 0
        self.hitRim = False
    def update(self):
        self.rot += 1
        if self.rot % 3 == 0:
            self.image = pygame.transform.rotate(self.image,-90)
        if self.madeShot:
            self.rot = 0
            self.rect = self.image.get_rect(center = (self.X,self.Y))
            p1.shot = False
            self.Y = self.Y + self.acc
            self.acc += .3
            self.t += 0.2
            if self.Y > H:
                self.kill()
        if self.hitRim:
            self.rect = self.image.get_rect(center = (self.X,self.Y))
            p1.shot = False
            self.Y = self.Y + self.acc -1
            self.acc += .3
            self.t += 0.2
            if self.Y > H:
                self.kill()
        if not (self.madeShot or self.hitRim):
            self.rect = self.image.get_rect(center = (self.X,self.Y))
            p1.shot = False
            self.X = self.Xoffset + self.vx * self.t
            self.Y = self.Yoffset - (self.vy*self.t-(9.81/2)*self.t*self.t)
            self.Yvalues.append(self.Y)
            self.t += 0.2
            if self.X > W:
                self.kill()
            if self.Y > H:
                self.kill()

      
class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = monsterImg1
        self.rect = self.image.get_rect()
        self.rect.centerx = W/2
        self.rect.centery = H - 100
        self.speedx = 0
        self.speedy = 0.0
        self.accel = 1.0
        self.jumping = False
        self.health = 100
        self.shot = False
        self.angle = 75
        self.shootVel = 50
        self.LeftToRight = True
        self.isJump = False
        self.jumpMag = 10
    def update(self):
        self.rect.centerx += self.speedx*self.accel
        self.rect.centery -= self.speedy
        self.speedx = 0
        if self.isJump:
            self.speedy = self.jumpMag
            self.jumpMag -= .5
        if self.rect.centery > 700:
            self.rect.centery = 700
            self.isJump = False
            self.speedy = 0
            self.jumpMag = 10
        pygame.draw.rect(screen,(0,0,255),(self.rect.centerx,self.rect.centery - 40,self.shootVel/1.4,20))
        ks = pygame.key.get_pressed()
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.accel = 2
        else:
            self.accel = 1
        if ks[pygame.K_d]:
            self.LeftToRight = True
            self.image = monsterImg1
            self.speedx = 5
        if ks[pygame.K_a]:
            self.LeftToRight = False
            self.image = monsterImg2
            self.speedx = -5
        if ks[pygame.K_f]:
            self.shootVel += 2
        else:
            if self.shootVel > 50:
                self.shootVel -= 4
        if self.LeftToRight:
            screen.blit(arrowText1,(p1.rect.centerx + 20,p1.rect.centery + 10))
        else:
            screen.blit(arrowText2,(p1.rect.centerx - 20,p1.rect.centery + 10))
    def shoot(self):
        if not self.shot and self.LeftToRight:
            b = ball(self.shootVel,self.angle)
            ALL_SPRITES.add(b)
            ballGroup1.add(b)
        elif not self.shot and not self.LeftToRight:
            b2 = ball2(self.shootVel,self.angle)
            ALL_SPRITES.add(b2)
            ballGroup1.add(b2)
    def jump(self):
        self.isJump = True
   
            
        
        
        

gameOver = False
ALL_SPRITES = pygame.sprite.Group()
baskets = pygame.sprite.Group()
p1 = player()
playerGroup = pygame.sprite.Group()
playerGroup.add(p1)
basket1 = basket()
baskets.add(basket1)
ALL_SPRITES.add(basket1)
ALL_SPRITES.add(p1)
ballGroup1 = pygame.sprite.Group()


timeSec = 60
previousTime = pygame.time.get_ticks()
bg = pygame.image.load("city.png").convert_alpha()

madeShots = 0
while not gameOver:
    score = madeShots
    screen.blit(bg,(0,0))
    time = (int(pygame.time.get_ticks()/1000))
    timeText = font.render("REMAINING TIME: "+str(60-time+2*madeShots),True,(0,0,0))
    text = font.render(str(p1.angle),True,(0,0,0))
    scoreText = font.render("SCORE: "+str(score),True,(0,0,0))
    ALL_SPRITES.draw(screen)
    ALL_SPRITES.update()
    screen.blit(text,(20,20))
    screen.blit(scoreText,(100,100))
    screen.blit(timeText,(50,50))
    ballHitBasket = pygame.sprite.groupcollide(baskets,ballGroup1,False,False)
    ballHitBasket2 = pygame.sprite.groupcollide(ballGroup1,baskets,False,False)
    if (60 - time + 2*madeShots) == 0:
        gameOver = True
    if ballHitBasket:
        for i in ballHitBasket2:
            if (i.Y > min(i.Yvalues) and i.Y <= basket1.rect.top) and not i.hitRim:
                i.madeShot = True
                madeShots += 1
                p1.shot = False
                for i in ballHitBasket:
                    i.explode()
                    i.move()
            else:
                i.hitRim = True
    pygame.display.update()
    clock.tick(fps)
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                p1.isJump = True
                p1.jump()
        if e.type == pygame.QUIT:
            gameOver = True
        if e.type == pygame.MOUSEBUTTONDOWN:
            current = pygame.time.get_ticks()
            if current - previousTime > 500:
                previousTime = current
                p1.shoot()

    