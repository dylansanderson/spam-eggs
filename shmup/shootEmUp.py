import pygame
import random

WIDTH = 800
HEIGHT = 800
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
effect = pygame.mixer.Sound('laser.wav')
effect2 = pygame.mixer.Sound('damage.wav')
effect3 = pygame.mixer.Sound('health.wav')
effect4 = pygame.mixer.Sound('d2.wav')
x2 = pygame.image.load("x2.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
font = pygame.font.SysFont("Arial",24)
mList = ["m1.png","m2.png","m3.png","m4.png","m5.png","m6.png","m7.png","m8.png","m9.png","m10.png","m11.png","m12.png","m13.png","m14.png","m15.png","m16.png","m17.png","m18.png","m19.png","m20.png","m21.png","m22.png"]
# LOAD Graphics
background = pygame.image.load("img.jpg")
background_rect = background.get_rect()

player_img = pygame.image.load("s11.png")
meteor_img = pygame.image.load(random.choice(mList))
bullet_img = pygame.image.load("l1.png")

class bulletSpeed(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("x2.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,WIDTH)
        self.rect.y = 400
        self.speedy = 2
    def update(self):
        self.rect.y += self.speedy



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0
        self.lives = 3
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -12
        if keystate[pygame.K_RIGHT]:
            self.speedx = 12
        self.rect.x += self.speedx
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
    def loseLife(self):
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0
        for i in mobs:
            i.rect.y = -500
            i.rect.centerx = WIDTH / 2
            i.speedy = random.randrange(5,10)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(random.choice(mList))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,WIDTH-self.rect.width)
        self.rect.y = random.randint(-100,40)
        self.speedy = random.randrange(8,12)
        self.speedx = random.randrange(-2,7)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 10:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig,self.rot)
            
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0,WIDTH-self.rect.width)
            self.rect.y = random.randint(-100,40)
            self.speedy = random.randrange(5,15)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class healthPack(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load('hpack.png')
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = random.randint(6,11)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 10:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig,self.rot)
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
    


score = 0
scoreColor = WHITE
scoreMult = 1
playerHealth = 100
player = Player()



hGroup = pygame.sprite.Group()
bull= pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(player)


gameOver = False
running = True
healthDropped = False
h2Dropped = False
h3Dropped = False
mobSpawn = False

def spawnMobs(x):
    for i in range(x):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

spawnMobs(12)
while running:
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                effect.play()
                player.shoot()
    if not mobSpawn:
        mobSpawn = True
        spawnMobs(random.randint(3,6))   #respawn first group of mobs
    if score > 50 and not healthDropped:
        b = bulletSpeed()
        bull.add(b)
        all_sprites.add(b)
        h = healthPack(random.randint(0,WIDTH),-100)
        hGroup.add(h)
        all_sprites.add(h)
        healthDropped = True
        for i in mobs:
            i.rect.y = -500
            i.rect.centerx = WIDTH / 2
            i.speedy = random.randrange(10,14)

    if score > 60 and not h2Dropped:
        mobSpawn = False      #respawn another group of mobs
        h2 = healthPack(random.randint(0,WIDTH),-100)
        hGroup.add(h2)
        all_sprites.add(h2)
        h2Dropped = True
        scoreColor = (0,255,0)
        background = pygame.image.load("img2.jpg")
        for i in mobs:
            i.speedy = random.randrange(14,18)
            i.rect.y = -600
            i.rect.centerx = WIDTH / 2
    if score > 3000 and not h3Dropped:
        mobSpawn = False                #respawn another group of mobs
        h3 = healthPack(random.randint(0,WIDTH),-100)
        hGroup.add(h3)
        all_sprites.add(h3)
        h3Dropped = True
        for i in mobs:
            i.rect.y = -1500
            i.rect.centerx = WIDTH / 2
            i.speedy = random.randrange(18,22)
    # Update
    all_sprites.update()
    #collision check
    healthHit = pygame.sprite.spritecollide(player,hGroup,True)
    bx2hit = pygame.sprite.groupcollide(bullets,bull,True,True)

    if bx2hit:
        player.lives = player.lives * 2
    if healthHit:
        effect3.play()
        playerHealth += 20
    hits = pygame.sprite.spritecollide(player, mobs,True)
    if hits:
        playerHealth -= int((hits[0].rect.bottom - hits[0].rect.top)/4)
        effect4.play()
        if playerHealth < 1:
            player.loseLife()
            player.lives -= 1
            playerHealth = 100
    for i in hits:
        m = Mob()          # spawn a new meteor each time player gets hit
        all_sprites.add(m)
        mobs.add(m)
    if player.lives< 1:
        running = False
    meteors = pygame.sprite.groupcollide(bullets,mobs,True,True)
    for i in meteors:
        scoreMult *= 1.04
        effect2.play()
        score += scoreMult
        m = Mob()           # spawn a new meteor each time bullet hits meteor
        all_sprites.add(m)
        mobs.add(m)
        
  
    # Draw / render
    
    score = int(score)
    screen.blit(background,background_rect)
    disclaimertext = font.render("SCORE:" + str(score), True, scoreColor)   # score bar
    screen.blit(disclaimertext, (2, 20))
    lifeText = font.render("LIVES: "+ str(player.lives),True,scoreColor)
    screen.blit(lifeText,(700,20))

    all_sprites.draw(screen)
    pygame.draw.rect(screen,BLUE,(20,HEIGHT-20,200,50))                 #health bar
    pygame.draw.rect(screen,RED,(20,HEIGHT-20,abs(2*playerHealth),47))
    
    # *after* drawing everything, flip the display
    pygame.display.flip()
gameOver = True
gameOverText = font.render("GAME OVER, SCORE:" + str(score),True,scoreColor)
while gameOver:
    screen.blit(gameOverText,(400,400))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
                                



