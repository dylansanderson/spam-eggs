import pygame
from time import sleep
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 74
HEIGHT = 74
 
# This sets the margin between each cell
MARGIN = 5
 #test
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
#grid[1][5] = 1
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 800]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
blockColumnLeft = 4
blockColumnMid = 5
blockColumnRight = 6
currentRow = 9
fallingRow = 0
fallCol = 0
fallCol2 = 0
last_update = 0
previousUpdate = 0
leftToRight = True
rightToLeft = False
size = 3
SPEED = 180
def clearGrid():
    for row in range(10):
        for col in range(10):
            grid[row][col] = 0
    
def checkEmptyRow(row):
    count = 0
    for i in range(9):
        if grid[row][i] == 1:
            count += 1
    return count

fallingBlock = False
twoFallingBlocks = False


        
# -------- Main Program Loop -----------
while not done:
    # Set the screen background
    screen.fill(BLACK)
    # Draw the grid
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    if currentRow == -1:
        clearGrid()
        currentRow = 9
        SPEED = 180
        size = 3
        blockColumnLeft = 4
        blockColumnMid = 5
        blockColumnRight = 6

    if currentRow < 7 and size == 3:
        size = 2
    elif currentRow < 3 and size == 2:
        size = 1

    if size == 3:
        grid[currentRow][blockColumnLeft] = 1
        grid[currentRow][blockColumnMid] = 1
        grid[currentRow][blockColumnRight] = 1
    elif size == 2:
        grid[currentRow][blockColumnLeft] = 0
        grid[currentRow][blockColumnMid] = 1
        grid[currentRow][blockColumnRight] = 1
    elif size == 1:
        grid[currentRow][blockColumnLeft] = 0
        grid[currentRow][blockColumnMid] = 0
        grid[currentRow][blockColumnRight] = 1
    else:
        done = True

    if fallingBlock:
        currentTime = pygame.time.get_ticks()
        if currentTime - previousUpdate > 140 and fallingRow < 10:
            if grid[fallingRow][fallCol] != 1:
                grid[fallingRow-1][fallCol] = 0
                previousUpdate = currentTime
                grid[fallingRow][fallCol] = 1
                fallingRow += 1
            else:
                grid[fallingRow-1][fallCol] = 0
        elif fallingRow >= 9:
            currentTime = pygame.time.get_ticks()
            grid[fallingRow-1][fallCol] = 1
            if currentTime - previousUpdate > 140:
                print("PASS")
                fallingBlock = False
                grid[fallingRow-1][fallCol] = 0
        
    if twoFallingBlocks:
        currentTime = pygame.time.get_ticks()
        if currentTime - previousUpdate > 140 and fallingRow < 10:
            grid[fallingRow-1][fallCol] = 0
            grid[fallingRow-1][fallCol2] = 0
            previousUpdate = currentTime
            grid[fallingRow][fallCol] = 1
            grid[fallingRow][fallCol2] = 1
            fallingRow += 1
        else:
            grid[fallingRow-1][fallCol] = 0
            grid[fallingRow-1][fallCol2] = 0
        if fallingRow >= 9:
            currentTime = pygame.time.get_ticks()
            grid[fallingRow-1][fallCol] = 1
            grid[fallingRow-1][fallCol2] = 1
            if currentTime - previousUpdate > 140:
                print("PASS")
                twoFallingBlocks = False
                grid[fallingRow-1][fallCol] = 0
                grid[fallingRow-1][fallCol2] = 0
    
    if leftToRight:
        now = pygame.time.get_ticks()
        if now - last_update > SPEED:
            last_update = now
            if size == 3:
                grid[currentRow][blockColumnLeft] = 0
                blockColumnLeft += 1
                blockColumnMid += 1
                blockColumnRight += 1
                if blockColumnRight == 9:
                    leftToRight = False
                    rightToLeft = True
            elif size == 2:
                grid[currentRow][blockColumnMid] = 0
                grid[currentRow][blockColumnLeft] = 0
                blockColumnMid += 1
                blockColumnRight += 1
                if blockColumnRight == 9:
                    leftToRight = False
                    rightToLeft = True
            else:
                grid[currentRow][blockColumnMid] = 0
                grid[currentRow][blockColumnLeft] = 0
                grid[currentRow][blockColumnRight] = 0
                blockColumnRight += 1
                if blockColumnRight == 9:
                    leftToRight = False
                    rightToLeft = True
    else:
        now = pygame.time.get_ticks()
        if now - last_update > SPEED:
            last_update = now
            if size == 3:
                grid[currentRow][blockColumnRight] = 0
                blockColumnLeft -= 1
                blockColumnMid -= 1
                blockColumnRight -= 1
                if blockColumnLeft == 0:
                    leftToRight = True
                    rightToLeft = False
            elif size == 2:
                grid[currentRow][blockColumnMid] = 0
                grid[currentRow][blockColumnRight] = 0
                blockColumnMid -= 1
                blockColumnRight -= 1
                if blockColumnMid == 0:
                    rightToLeft = False
                    leftToRight = True
            else:
                grid[currentRow][blockColumnMid] = 0
                grid[currentRow][blockColumnLeft] = 0
                grid[currentRow][blockColumnRight] = 0
                blockColumnRight -= 1
                if blockColumnRight == 0:
                    rightToLeft = False
                    leftToRight = True

    

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                currentRow -= 1
                if SPEED >= 80:
                    SPEED -= 20
                if currentRow < 8 and checkEmptyRow(currentRow+2) > 0:
                    if size == 1:
                        if grid[currentRow+1][blockColumnRight] == grid[currentRow+2][blockColumnRight]:
                            print("perfect")
                        else:
                            print("YOU LOST")
                            done = True
                    elif size == 2:
                        if (grid[currentRow+1][blockColumnMid] == grid[currentRow+2][blockColumnMid]) and (grid[currentRow+1][blockColumnRight] == grid[currentRow+2][blockColumnRight]):
                            print("perfect!")
                        else:
                            if grid[currentRow+1][blockColumnMid] != grid[currentRow+2][blockColumnMid]:
                                size -= 1
                                fallCol = blockColumnMid
                                fallingRow = currentRow + 1
                                fallingBlock = True
                                grid[currentRow+1][blockColumnMid] = 0
                                print("DOWNSIZE 2-->1")
                            if grid[currentRow+1][blockColumnRight] != grid[currentRow+2][blockColumnRight]:
                                size -= 1
                                fallCol = blockColumnRight
                                fallingRow = currentRow + 1
                                fallingBlock = True
                                print("DOWNSIZE 2-->1")
                                grid[currentRow+1][blockColumnRight] = 0
                    else:
                        if (grid[currentRow+1][blockColumnLeft] == grid[currentRow+2][blockColumnLeft] and grid[currentRow+1][blockColumnMid] == grid[currentRow+2][blockColumnMid]) and grid[currentRow+1][blockColumnRight] == grid[currentRow+2][blockColumnRight]:
                            print("perfect <3")
                            
                        else:
                            if grid[currentRow+1][blockColumnLeft] != grid[currentRow+2][blockColumnLeft]:
                                size -= 1
                                fallCol = blockColumnLeft
                                fallingRow = currentRow + 1
                                print("DOWNSIZE 3-->2")
                                grid[currentRow+1][blockColumnLeft] = 0
                            if grid[currentRow+1][blockColumnRight] != grid[currentRow+2][blockColumnRight]:
                                size -= 1
                                fallCol = blockColumnRight
                                fallingRow = currentRow + 1
                                print("Downsize 3 --> 2")
                                grid[currentRow+1][blockColumnRight] = 0
                            if grid[currentRow+1][blockColumnMid] != grid[currentRow+2][blockColumnMid]:
                                size -= 1
                                fallCol2 = blockColumnMid
                                fallingRow = currentRow + 1
                                print("DOWNSIZE 3--> 1")
                                grid[currentRow+1][blockColumnMid] = 0
                            if size == 1:
                                twoFallingBlocks = True
                            elif size == 2:
                                fallingBlock = True
                else:
                    if currentRow < 8:
                        if size == 2:
                            grid[currentRow+2][blockColumnRight] = 1
                            grid[currentRow+2][blockColumnMid] = 1
                        elif size == 3:
                            grid[currentRow+2][blockColumnRight] = 1
                            grid[currentRow+2][blockColumnMid] = 1
                            grid[currentRow+2][blockColumnLeft] = 1
                        else:
                            grid[currentRow+2][blockColumnRight] = 1



                    
                
 
    # Limit to 60 frames per second
    clock.tick(300)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.update()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()