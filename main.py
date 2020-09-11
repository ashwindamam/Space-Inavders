import pygame
import math
import random
from pygame import mixer
import cv2 as cv

# setting up faces and videocapture
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = icon = pygame.image.load('5697.jpg')

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('rocket.png')  # first loading the image
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders (1).png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(10)
    enemyY_change.append(40)

# Bullet
# Ready- you cant see the bullet on the screen
# Fire- the bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 60
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running & cap.isOpened():
    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    _, img = cap.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    rect1 = cv.rectangle(img, (10, 155), (200, 345), (0, 0, 255), 3)
    rect2 = cv.rectangle(img, (440, 155), (630, 345), (0, 0, 255), 3)
    rect3 = cv.rectangle(img, (225, 155), (415, 345), (0, 0, 255), 3)

    for (x, y, w, h) in faces:
        rect = cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
        is_between1 = x in range(10, 200)
        is_between2 = (x+w) in range(440, 640)
        is_between3 = x in range(225, 415)

        if is_between1:
            playerX_change = 20
        elif is_between2:
            playerX_change = -20
        else:
            playerX_change = 0
        if bullet_state is "ready":
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()
            bulletX = playerX
            fire_bullet(bulletX, bulletY)

    cv.imshow('img', img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

        # if event.type == pygame.KEYDOWN:
        #   if event.key == pygame.K_LEFT:
        #      playerX_change = -2
        #  if event.key == pygame.K_RIGHT:
        # playerX_change = 2
        # if event.key == pygame.K_SPACE:
        #   if bullet_state is "ready":
        # bullet_sound = mixer.Sound('laser.wav')
        # bullet_sound.play()
        # bulletX = playerX
        # fire_bullet(bulletX, bulletY)

        # if event.type == pygame.KEYUP:
        #   if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        # playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 10
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -10
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

cap.release()
