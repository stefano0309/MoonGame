import pygame
import time
import random

pygame.init()

#Inizializzazione
w = 700
h = 400
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Moon Game")
pygame.display.set_icon(pygame.image.load("images/icon.png").convert_alpha())
clock = pygame.time.Clock()
running = True
stage = 0

#Background
background = pygame.image.load("images/background.jpg").convert_alpha()

#stage 0
title = pygame.image.load("images/title.png").convert_alpha()
title_rect = title.get_rect(center=(350, 100))

#stage 1
def point(timer):
    if timer//10 >= 1:
        point = timer * (timer/10)
    else:
        point = 0
    return point

def speed(timer):
    level = timer // 10 +1
    speed = 1 + level * 0.5
    if speed >= 3:
        speed = 3
    return speed

timer = 0

#stage 2
go = pygame.image.load("images/gameOver.png").convert_alpha()
go_rect = go.get_rect(center=(350, 100))

#Play button
play = pygame.image.load("images/playText2.png").convert_alpha()
play_red = pygame.transform.scale(play, (play.get_width()*1.5,play.get_height()*1.5))
play_rect = play_red.get_rect(center=(250,200))

#Quit button
quit = pygame.image.load("images/quitText2.png").convert_alpha()
quit_red = pygame.transform.scale(quit, (quit.get_width()*1.5,quit.get_height()*1.5))
quit_rect = quit_red.get_rect(center=(450,200))

#meteor
meteor = pygame.image.load("images/meteor.png").convert_alpha()
meteor_red = pygame.transform.scale(meteor, (50,50))

meteor_pos = []
for i in range(5):
    x = random.randint(0, w-50)
    y = random.randint(-200, -100)
    meteor_pos.append(pygame.FRect(x, y, 50, 50))



#player
player = pygame.image.load("images/player.png").convert_alpha()
player_red = pygame.transform.scale(player, (90,100))
player_rect = player_red.get_rect(center=(350, 200))
player_hitbox = player_rect.inflate(-50, -50)


#Stage cond
start = False

#Tasti movimento
kd = False
ka = False
kw = False
ks = False


while running:
    dt =clock.tick(60) / 1000
    #Eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                if stage == 0:
                    start = True
                if stage == 2:
                    # reset posizioni del gioco
                    stage = 1
                    player_rect.center = (300, 200)
                    player_hitbox = player_rect.inflate(-50, -50)
                    timer = 0
                    meteor_pos = []
                    for i in range(5):
                        x = random.randint(0, w-50)
                        y = random.randint(-200, -100)
                        meteor_pos.append(pygame.FRect(x, y, 50, 50))
            if quit_rect.collidepoint(event.pos):
                running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                kd = True                 
            if event.key == pygame.K_a:
                ka = True
            if event.key == pygame.K_w:
                kw = True
            if event.key == pygame.K_s:
                ks = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                kd = False
            if event.key == pygame.K_a:
                ka = False
            if event.key == pygame.K_w:
                kw = False
            if event.key == pygame.K_s:
                ks = False
    screen.blit(background, (0,0))

    #start
    if stage == 0:
        screen.blit(title, title_rect)
        screen.blit(play_red, play_rect)
        screen.blit(quit_red, quit_rect)

    #game
    if stage == 1:
        screen.blit(player_red, player_rect)
        #debug player
        #pygame.draw.rect(screen, "red", player_hitbox, 2)
        for meteor_rect in meteor_pos:
            meteor_rect.y += 2 * speed(timer)
            screen.blit(meteor_red, meteor_rect)
            if meteor_rect.top > h:
                meteor_rect.x = random.randint(0, w-50)
                meteor_rect.y = random.randint(-200, -100)
                timer += 1
            #debug meteor
            #pygame.draw.rect(screen, "red", meteor_rect, 2)
            if player_hitbox.colliderect(meteor_rect):
                stage += 1
                #debug game over
                #print(timer)
                #print(point(timer))
                #print("Game Over")

    #game over
    if stage == 2:
        screen.blit(go, go_rect)
        play_rect.center = (250, 200)
        screen.blit(play_red, play_rect)
        quit_rect.center = (450, 200)
        screen.blit(quit_red, quit_rect)
        
        
    
    #start animation
    if start:
        title_rect.y -= 2
        play_rect.x -= 4
        quit_rect.x += 4
        if title_rect.bottom <= 0 and play_rect.right <= 0 and quit_rect.left >= w:
            stage += 1
            start = False


    #Bordo schermo x player
    if player_rect.right >= w:
        kd = False
    if player_rect.left <= 0:
        ka = False
    
    #Bordo schermo y player
    if player_rect.top <= 0:
        kw = False
    if player_rect.bottom >= h:
        ks = False

    #Movimenti su x
    if kd:
        player_rect.x += 2 * speed(timer)
        player_hitbox.x += 2* speed(timer)
    if ka:
        player_rect.x -= 2 * speed(timer)
        player_hitbox.x -= 2* speed(timer)
    #Movimenti su y
    if kw:
        player_rect.y -= 2 * speed(timer)
        player_hitbox.y -= 2* speed(timer)
    if ks:
        player_rect.y += 2 * speed(timer)
        player_hitbox.y += 2* speed(timer)
    

    pygame.display.update()

pygame.quit()