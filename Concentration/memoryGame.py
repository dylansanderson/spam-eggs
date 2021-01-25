import pygame
import random



chars = ["k.png","k.png","mario.png","mario.png","Luigi.jpeg","Luigi.jpeg","bowser.jpeg","bowser.jpeg","peach.png","peach.png","toad.png","toad.png","gumba.jpeg","gumba.jpeg","wario.jpg","wario.jpg","waluigi.png","waluigi.png","yoshi.png","yoshi.png","Falcon.png","Falcon.png","samus.jpeg","samus.jpeg","dk.png","dk.png","daisy.png","daisy.png","koopa.jpeg","koopa.jpeg","zelda.png","zelda.png","bomb.png","bomb.png","shyguy.jpg","shyguy.jpg"]
scoreFileName = "scoresHard.txt"
W,H = 800,800
offset,xOffset = 150,0
matchCount, attempts = 0,0
xVels = [-4,4]
pygame.mixer.init()
flipSound = pygame.mixer.Sound("flop.wav")
random.shuffle(chars)

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 60
        self.image = pygame.Surface((self.width,self.height))
        self.halfWidth = self.width/2
        self.charIndex = random.randint(0,len(chars)-1)
        self.imgName = chars[self.charIndex]
        self.flippedImg = pygame.image.load(chars[self.charIndex])
        chars.remove(self.imgName)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = random.choice(xVels)
        self.maxX = self.rect.centerx + self.halfWidth
        self.minX = self.rect.centerx - self.halfWidth
        self.minY = self.rect.centery - self.halfWidth
        self.maxY = self.rect.centery + self.halfWidth
        self.flipped = False
        self.isShown = False
        self.isMoving = False
    def update(self):
        x,y = pygame.mouse.get_pos()
        if (x > self.minX and x < self.maxX) and (y> self.minY and y < self.maxY):
            pygame.draw.rect(screen, (255, 100, 0), (self.rect.centerx-self.halfWidth, self.rect.centery-self.halfWidth, 62, 62), 4) 
        if self.flipped:
            self.image = self.flippedImg
        if self.isMoving:
            self.rect.centerx += self.speedx
        if self.rect.right > W or self.rect.left < 0:
            self.kill()

    def flipBack(self):
        self.image = pygame.Surface((self.width,self.height))
        self.flipped = False

def mouseCoordToGridPos(pos):
    for x in tiles:
        if not x.isShown:
            if (pos[0] > x.minX and pos[0] < x.maxX) and (pos[1] > x.minY and pos[1] < x.maxY):
                flipSound.play()
                x.flipped = True
                flippedTiles.add(x)
        

def spawnBoard():
    for i in range(0,len(grid)):
        for j in range(0,len(grid[i])):
            t = Tile((i*100)+offset + xOffset,(j*100)+offset)
            tiles.add(t)
            allSprites.add(t)

def getLowestScoreFromFile():
    f = open(scoreFileName,"r")
    scores = []
    for score in f:
        try:
            scores.append(int(score))
        except:
            pass
    f.close()
    return str(min(scores))


pygame.init()
font = pygame.font.SysFont("meera",36)
diffText = font.render("DIFFICULTY SELECT",True,(0,0,0))
easyText = font.render("EASY",True,(0,0,0))
medText = font.render("MEDIUM",True,(0,0,0))
hardText = font.render("HARD",True,(0,0,0))
grid = [['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','','']]
screen = pygame.display.set_mode((W,H))
bg = pygame.image.load("m.png").convert_alpha()
match = False
clock = pygame.time.Clock()
FPS = 60
gameOver = False
waitingForClick = False
allSprites = pygame.sprite.Group()
flippedTiles = pygame.sprite.Group()
tiles = pygame.sprite.Group()
startScreen = True
while startScreen:
    y = pygame.mouse.get_pos()[1]
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            startScreen = False
            gameOver = True
        if e.type == pygame.MOUSEBUTTONDOWN:
            if y < H/3:           #easy
                grid = [['','','',''],['','','',''],['','','',''],['','','','']]
                chars = ["k.png","k.png","mario.png","mario.png","Luigi.jpeg","Luigi.jpeg","bowser.jpeg","bowser.jpeg","peach.png","peach.png","toad.png","toad.png","gumba.jpeg","gumba.jpeg","wario.jpg","wario.jpg"]
                offset = 250
                scoreFileName = "scoresEasy.txt"
                startScreen = False
            elif y > H/3 and y < 2*(H/3):#medium
                xOffset = 100
                grid = [['','','','','',''],['','','','','',''],['','','','','',''],['','','','','','']]
                chars = ["k.png","k.png","mario.png","mario.png","Luigi.jpeg","Luigi.jpeg","bowser.jpeg","bowser.jpeg","peach.png","peach.png","toad.png","toad.png","gumba.jpeg","gumba.jpeg","wario.jpg","wario.jpg","waluigi.png","waluigi.png","yoshi.png","yoshi.png","Falcon.png","Falcon.png","samus.jpeg","samus.jpeg"]
                scoreFileName = "scoresMedium.txt"
                startScreen = False
            else:
                startScreen = False
            random.shuffle(chars)
            maxMatches = len(chars)/2
    screen.fill((255,255,255))
    pygame.draw.rect(screen,(0,255,0),(0,0,W,H/3))
    pygame.draw.rect(screen,(224,255,14),(0,(H/3),W,(H/3)))
    pygame.draw.rect(screen,(255,0,0),(0,2*(H/3),W,2*(H/3)))
    screen.blit(diffText,(W/2 - (W/7),20))
    screen.blit(easyText,(W/2 - (W/10),H/2-(H/4)))
    screen.blit(medText,(W/2 - (W/10),H/2))
    screen.blit(hardText,(W/2 - (W/10),H/2+(H/4)))
    if y < H/3:
        pygame.draw.rect(screen,(255,255,255),(0,0,W,H/3),4)
    elif y > H/3 and y < 2*(H/3):
        pygame.draw.rect(screen,(255,255,255),(0,H/3,W,H/3),4)
    else:
        pygame.draw.rect(screen,(255,255,255),(0,2*(H/3),W,2*(H/3)),4)

    pygame.display.update()
    clock.tick(FPS)
spawnBoard()
screen.fill((0,0,0))
while not gameOver:
    if len(flippedTiles) == 2:
        imgList = []
        for x in flippedTiles:
            imgList.append(x.imgName)
        if imgList[0] == imgList[1]:
            for x in flippedTiles:
                x.isShown = True
            match = True
        waitingForClick = True
    screen.blit(bg,(0,0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            gameOver = True
        if e.type == pygame.MOUSEBUTTONDOWN:
            if not waitingForClick:
                mouseCoordToGridPos(pygame.mouse.get_pos())
            else:
                if not match:
                    for x in flippedTiles:
                        x.flipBack()
                    waitingForClick = False
                else:
                    attempts -= 1
                    matchCount += 1
                flippedTiles.empty()
                match = False
                attempts += 1
    if matchCount >= maxMatches:
        f = open(scoreFileName,"a")
        f.write("\n")
        f.write(str(attempts+1))
        f.close()
        if scoreFileName == "scoresHard.txt":
            chars = ["k.png","k.png","mario.png","mario.png","Luigi.jpeg","Luigi.jpeg","bowser.jpeg","bowser.jpeg","peach.png","peach.png","toad.png","toad.png","gumba.jpeg","gumba.jpeg","wario.jpg","wario.jpg","waluigi.png","waluigi.png","yoshi.png","yoshi.png","Falcon.png","Falcon.png","samus.jpeg","samus.jpeg","dk.png","dk.png","daisy.png","daisy.png","koopa.jpeg","koopa.jpeg","zelda.png","zelda.png","bomb.png","bomb.png","shyguy.jpg","shyguy.jpg"]
        elif scoreFileName == "scoresMedium.txt":
            chars = ["k.png","k.png","mario.png","mario.png","Luigi.jpeg","Luigi.jpeg","bowser.jpeg","bowser.jpeg","peach.png","peach.png","toad.png","toad.png","gumba.jpeg","gumba.jpeg","wario.jpg","wario.jpg","waluigi.png","waluigi.png","yoshi.png","yoshi.png","Falcon.png","Falcon.png","samus.jpeg","samus.jpeg"]
        else:
            chars = ["k.png","k.png","mario.png","mario.png","Luigi.jpeg","Luigi.jpeg","bowser.jpeg","bowser.jpeg","peach.png","peach.png","toad.png","toad.png","gumba.jpeg","gumba.jpeg","wario.jpg","wario.jpg"]       
        random.shuffle(chars)
        matchCount = 0
        attempts = -1
        for x in allSprites:
            x.isMoving = True
        spawnBoard()
    allSprites.draw(screen)
    attemptsText = font.render("Attempts: " + str(attempts),True,(0,0,0))
    matchesText = font.render("Matches: " + str(matchCount),True,(0,0,0))
    bestText = font.render("Best: "+ getLowestScoreFromFile(),True,(0,0,0))
    screen.blit(matchesText,(W/2 -75,10))
    screen.blit(bestText,(W-200,10))
    screen.blit(attemptsText,(60,10))
    allSprites.update()
    pygame.display.update()
    clock.tick(FPS)