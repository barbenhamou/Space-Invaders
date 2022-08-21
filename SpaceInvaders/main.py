import random
import pygame as pg
import math
import time

# Initialize pygame
pg.init()


def ship(x, y):
    screen.blit(spaceshipImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))


def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def enemyAttack(x, y):
    global fireState
    fireState = "fire"
    screen.blit(fireImg, (x + 16, y + 16))


def isCollision(eX, eY, bX, bY):
    distance = math.sqrt((eX - bX) * (eX - bX) + (eY - bY) * (eY - bY))
    if distance < 27:
        return True
    return False


def drawAllEnemies(num):
    for i in range(num):
        enemy(enemyX[i], enemyY[i], i)


def showScore(x, y):
    score = font.render(f"Score: {scoreVal}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def randomI():
    return random.randint(0, numOfEnemies - 1)


# Screen settings
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("SpaceInvaders")
pg.display.set_icon(pg.image.load('ufo.png'))
over = pg.image.load('over.png')
win = pg.image.load('win.png')
winner = False

# Spaceship settings
spaceshipImg = pg.image.load('spaceship.png')
shipX = 360
shipY = 480
shipChangeX = 0

# Enemy settings
enemyImg = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
numOfEnemies = 30
collided = False

for i in range(numOfEnemies):
    enemyImg.append(pg.image.load('enemy.png'))
    enemyX.append((735 / 30) * i)
    enemyY.append(50)
    enemyChangeX.append(0.3)
    enemyChangeY.append(40)

# Bullet settings
bulletImg = pg.image.load('bullet.png')
bulletX = 0
bulletY = shipY
bulletChangeY = 5
# Ready - ready to be fired
# Fire - fired
bulletState = "ready"

# Fire settings
fireImg = pg.image.load('fire.png')
fireX = 0
fireY = 0
fireChangeY = 1
# Ready - ready to be fired
# Fire - fired
fireState = "ready"

scoreVal = 0
font = pg.font.Font('freesansbold.ttf', 24)
textX = 10
textY = 10
showScore(textX, textY)
# Game loop
running = True
while running:
    start = time.time()
    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                shipChangeX = 2
            if event.key == pg.K_a:
                shipChangeX -= 2
            if event.key == pg.K_SPACE:
                if bulletState == "ready":
                    # Current coordinates of the bullet
                    bulletX = shipX
                    fireBullet(shipX, bulletY)

        if event.type == pg.KEYUP:
            if event.key == pg.K_d or event.key == pg.K_a:
                shipChangeX = 0

    # Ship movement
    shipX += shipChangeX
    if shipX <= 0:
        shipX = 0
    elif shipX >= 736:
        shipX = 735

    # Enemy movement
    j = 0
    while j < numOfEnemies:
        enemyX[j] += enemyChangeX[j]
        if enemyX[j] <= 0:
            enemyChangeX[j] = 0.3
            enemyY[j] += enemyChangeY[j]
        elif enemyX[j] >= 736:
            enemyChangeX[j] = -0.3
            enemyY[j] += enemyChangeY[j]

        # Collision
        collision = isCollision(enemyX[j], enemyY[j], bulletX, bulletY)
        if collision:
            bulletY = 480
            bulletState = "ready"
            scoreVal += 1
            enemyImg.pop(j)
            enemyX.pop(j)
            enemyY.pop(j)
            enemyChangeX.pop(j)
            enemyChangeY.pop(j)
            numOfEnemies -= 1

        j += 1

    if numOfEnemies == 0:
        shipX = 2000
        fireX = 2000
        bulletX = 2000
        ship(shipX, shipY)
        drawAllEnemies(numOfEnemies)
        pg.display.update()
        winner = True
        break

    collision2 = isCollision(shipX, shipY, fireX, fireY)

    if collision2:
        for i in range(numOfEnemies):
            enemyX[i] = 2000
        shipX = 2000
        fireX = 2000
        bulletX = 2000
        ship(shipX, shipY)
        drawAllEnemies(numOfEnemies)
        pg.display.update()
        break

    # Bullet movement
    if bulletY <= 0:
        bulletY = shipY
        bulletState = "ready"
    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletChangeY

    x = randomI()
    if fireState == "ready":
        fireY = enemyY[x]
        fireX = enemyX[x]
        enemyAttack(enemyX[x], fireY)

    # Fire movement
    if fireY >= 600:
        fireY = enemyY[x]
        fireState = "ready"
    if fireState == "fire":
        enemyAttack(fireX, fireY)
        fireY += fireChangeY

    drawAllEnemies(numOfEnemies)
    showScore(textX, textY)
    ship(shipX, shipY)
    pg.display.update()

    elapsed = time.time() - start
    toSleep = 0.001 - elapsed
    if toSleep > 0:
        time.sleep(toSleep)


#The end of the game
screen.fill((0, 0, 0))
if winner:
    screen.blit(win, (0, 0))
else:
    screen.blit(over, (0, 0))
pg.display.update()
i = -5
time.sleep(3)
