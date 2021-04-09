import pygame
import random

pygame.init()
W,H = 800,800
FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W,H))
gameOver = False
pygame.mixer.init()
font = pygame.font.SysFont("meera",36)
sound0 = pygame.mixer.Sound("310.wav")
sound1 = pygame.mixer.Sound("415.wav")
sound2 = pygame.mixer.Sound("540.wav")
sound3 = pygame.mixer.Sound("640.wav")
allSprites = pygame.sprite.Group()
score = 0
p1Move,cpuMove = False, True
delayAnimation = False

class SuccessIndicator(pygame.sprite.Sprite):
    def __init__(self,success):
        print("SPAWNED")
        pygame.sprite.Sprite.__init__(self)
        if success:
            self.image = pygame.image.load("check.jpg").convert_alpha()
        else:
            self.image = pygame.image.load("redx.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = W/2
        self.rect.centery = H/2
        self.now = pygame.time.get_ticks()
    def update(self):
        self.currentTime = pygame.time.get_ticks()
        if self.currentTime -self.now > 350:
            self.kill()
            print("DEAD")
            global cpuMove
            global delayAnimation
            delayAnimation = False
            cpuMove = True
	    

class Marker(pygame.sprite.Sprite):
    def __init__(self,position,isCPUturn):
        pygame.sprite.Sprite.__init__(self)
        if not isCPUturn:
            self.image = pygame.image.load("hand.png").convert_alpha()
        else:
            self.image = pygame.Surface((190,190))
            self.image.fill((0,0,0))
        self.now = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        if position == 0:
            sound0.play()
            self.rect.centerx = 200
            self.rect.centery = 200
        elif position == 1:
            sound1.play()
            self.rect.centerx = 600
            self.rect.centery = 200
        elif position == 2:
            sound2.play()
            self.rect.centerx = 200
            self.rect.centery = 600
        else:
            sound3.play()
            self.rect.centerx = 600
            self.rect.centery = 600


    def update(self):
        self.currentTime = pygame.time.get_ticks()
        if self.currentTime -self.now > 120:
            self.kill()

class CPU:
    def __init__(self):
        self.last = pygame.time.get_ticks()
        self.presses = 0
        self.pressesPerTurn = 2
        self.choices = [random.randint(0,3) for x in range(0,self.pressesPerTurn)]
        
    def takeTurn(self):
        global cpuMove
        if self.presses < self.pressesPerTurn and cpuMove:
            now = pygame.time.get_ticks()
            if now - self.last > 600:
                self.last = now
                x = self.choices[self.presses]
                if x == 0:
                    m = Marker(0,True)
                    allSprites.add(m)
                    self.presses += 1
                elif x == 1:
                    m = Marker(1,True)
                    allSprites.add(m)
                    self.presses += 1
                elif x == 2:
                    m = Marker(2,True)
                    allSprites.add(m)
                    self.presses += 1
                else:
                    m = Marker(3,True)
                    allSprites.add(m)
                    self.presses += 1
        else:
            drawBoard()
            self.choices = self.choices + [random.randint(0,3)]
            self.presses = 0
            p1Move = True
            cpuMove = False
            self.pressesPerTurn += 1

    
def drawBoard():
    screen.fill((255,255,255))
    pygame.draw.line(screen,(0,0,0),(W/2,0),(W/2,H),3)
    pygame.draw.line(screen,(0,0,0),(0,H/2),(W,H/2),3)
    pygame.draw.rect(screen,(0,255,0),(0,0,(W/2)-2,(H/2)-2))
    pygame.draw.rect(screen,(255,0,0),(W/2+1,0,(W/2)-2,(H/2)-2))
    pygame.draw.rect(screen,(255,255,0),(0,H/2+1,(W/2)-2,(H/2)-2))
    pygame.draw.rect(screen,(0,0,255),(W/2+1,H/2+1,(W/2)-2,(H/2)-2))


c = CPU()
p1presses = 0
p1Choices = []
while not gameOver:
    drawBoard()
    if cpuMove:
        p1Choices = []                                   #reset player1's choices and presses
        p1presses = 0
        c.takeTurn()
        p1Move = True
    elif p1Move:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                gameOver = True
            xloc,yloc = pygame.mouse.get_pos()
            if xloc < W/2 and yloc < H/2:
                pygame.draw.rect(screen,(255,255,255),(0,0,W/2,H/2),4)
            elif xloc > W/2 and yloc < H/2:
                pygame.draw.rect(screen,(255,255,255),(W/2,0,W/2,H/2),4)
            elif xloc < W/2 and yloc > H/2:
                pygame.draw.rect(screen,(255,255,255),(0,H/2,W/2,H/2),4)
            else:
                pygame.draw.rect(screen,(255,255,255),(W/2,H/2,W/2,H/2),4)
            if e.type == pygame.MOUSEBUTTONDOWN:
                if xloc < W/2 and yloc < H/2:
                    p1Choices.append(0)
                    m = Marker(0,False)
                    allSprites.add(m)
                    p1presses += 1
                elif xloc > W/2 and yloc < H/2:
                    p1Choices.append(1)
                    m = Marker(1,False)
                    allSprites.add(m)
                    p1presses += 1
                elif xloc < W/2 and yloc > H/2:
                    p1Choices.append(2)
                    m = Marker(2,False)
                    allSprites.add(m)
                    p1presses += 1
                else:
                    p1Choices.append(3)
                    m = Marker(3,False)
                    allSprites.add(m)
                    p1presses += 1
                if p1presses >= c.pressesPerTurn - 1:
                    p1Move = False
                    delayAnimation = True     
    else:
        if p1Choices != c.choices[0:len(c.choices)-1]:
            s = SuccessIndicator(False)
            allSprites.add(s)
            score = 0
            c.pressesPerTurn = 2
            c.choices = [random.randint(0,3) for x in range(0,c.pressesPerTurn)]
        else:
            s = SuccessIndicator(True)
            allSprites.add(s)
            score += 1

          
    scoreText = font.render("SCORE: " + str(score),True,(0,0,0))  
    screen.blit(scoreText,(20,20))   
    allSprites.draw(screen)
    allSprites.update()   
    pygame.display.update()
    clock.tick(FPS)
pygame.QUIT
