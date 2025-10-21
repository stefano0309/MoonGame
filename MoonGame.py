import pygame
import time
import math
import os
import random

pygame.init()
pygame.mixer.init()
#Inizializzazione gioco
w = 700
h = 400
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Moon Game")
pygame.display.set_icon(pygame.image.load("images/icon.png").convert_alpha())
clock = pygame.time.Clock()
running = True
stage = 0

#Inizializazione musica
pygame.mixer_music.load("music/music.mp3")
volume = 0.25
pygame.mixer.music.set_volume(volume)  # valori di musica da 0 a 1
pygame.mixer.music.play(-1)   # loop

#Background
background = pygame.image.load("images/background.jpg").convert_alpha()

#stage 0
title = pygame.image.load("images/title.png").convert_alpha()
title_rect = title.get_rect(center=(350, 100))


#stage 1 gameplay

#funzioni punteggio basato sul timer ovvero sul numero di meteoriti evitati
def point(timer):
    if timer//10 >= 1:
        point = timer * (timer/10)
    else:
        point = 0
    return point


#funzioni livelli basato sul timer ovvero sul numero di meteoriti evitati
def level (timer):
    level = timer // 10 + 1
    speed = 1 + level * 0.5
    if level <= 5:
        dif = "very easy"
        if speed >= 2:
            speed = 2
    elif level <= 10:
        dif = "easy"
        if speed >= 3:
            speed = 3
    elif level <= 15:
        dif = "medium"
        if speed >= 3.5:
            speed = 3.5
    elif level <= 20:
        dif = "hard"
        if speed >= 4:
            speed = 4
    elif level <= 25:
        dif = "very hard"
        if speed >= 4.5:
            speed = 4.5
    return level, dif, speed


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
player_hitbox = player_rect.inflate(-55, -50)

timer = 0

#Miglior punteggio
if os.path.exists("best_score.txt"):
    with open("best_score.txt", "r") as f:
        if os.stat("best_score.txt").st_size == 0:
            best_score = 0
        else:
            best_score = float(f.read())
            f.close()
#stage 2 game over
go = pygame.image.load("images/gameOver.png").convert_alpha()
go_rect = go.get_rect(center=(350, 100))

#point text
font_var = pygame.font.Font("font/Pixels.ttf", 50)

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
                else:
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
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                kd = True                 
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                ka = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                kw = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                ks = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                kd = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                ka = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                kw = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                ks = False
    screen.blit(background, (0,0))

    #stage 0
    if stage == 0:
        screen.blit(title, title_rect)
        screen.blit(play_red, play_rect)
        screen.blit(quit_red, quit_rect)
        best_score_text = font_var.render("best score: "+ str(best_score), False, (255, 255, 255))
        best_score_rect = best_score_text.get_rect(center=(350, 250))
        screen.blit(best_score_text, best_score_rect)

    #stage 1
    if stage == 1:
        pygame.mixer.music.pause() 
        level_text = font_var.render("Level: "+ str(level(timer)[0])+ " Dif: "+str(level(timer)[1]), False, (255, 255, 255))
        level_rect = level_text.get_rect(center=(350, 25))
        screen.blit(level_text, level_rect)
        screen.blit(player_red, player_rect)
        #debug player
        #pygame.draw.rect(screen, "red", player_hitbox, 2)
        for meteor_rect in meteor_pos:
            meteor_rect.y += 2 * level(timer)[2]
            if level(timer)[0] < 26:
                screen.blit(meteor_red, meteor_rect)
            if meteor_rect.top > h:
                meteor_rect.x = random.randint(0, w-50)
                meteor_rect.y = random.randint(-200, -100)
                timer += 1
            #debug meteor
            #pygame.draw.rect(screen, "red", meteor_rect, 2)
            if player_hitbox.colliderect(meteor_rect) and level(timer)[0] < 26:
                pygame.mixer.Sound("effect/crash.mp3").play()
                time.sleep(2)
                volume = 0
                stage += 1
                #debug game over
                #print(timer)
                #print(point(timer))
                #print("Game Over")
        if level(timer)[0] > 25:
            ka , kd , kw , ks = False, False, False, False
            player_rect.y -= 2 * level(timer)[2]
            player_hitbox.y -= 2* level(timer)[2]
            if player_rect.top <= 0:
                stage = 3 #win condition

    #stage 2
    if stage == 2:
        volume += 0.003
        if point(timer) > best_score:
            best_score = point(timer)
            with open("best_score.txt", "w") as f:
                f.write(str(best_score))
            f.close()
        if volume >= 0.25:
            volume = 0.25
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.unpause() 
        screen.blit(go, go_rect)
        play_rect.center = (250, 200)
        screen.blit(play_red, play_rect)
        quit_rect.center = (450, 200)
        screen.blit(quit_red, quit_rect)
        point_text = font_var.render("Points: "+ str(math.floor(point(timer))), False, (255, 255, 255))
        point_rect = point_text.get_rect(center=(350, 250))
        screen.blit(point_text, point_rect)
    
    #stage 3
    if stage == 3:
        volume += 0.003
        if volume >= 0.25:
            volume = 0.25
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.unpause() 
        win_text = font_var.render("You Win!", False, (255, 255, 255))
        win_rect = win_text.get_rect(center=(350, 150))
        screen.blit(win_text, win_rect)
        play_rect.center = (250, 250)
        screen.blit(play_red, play_rect)
        quit_rect.center = (450, 250)
        screen.blit(quit_red, quit_rect)
        point_text = font_var.render("Points: "+ str(point(timer)), False, (255, 255, 255))
        point_rect = point_text.get_rect(center=(350, 200))
        screen.blit(point_text, point_rect)
        
    
    #start animation
    if start:
        volume -= 0.003
        if volume <= 0:
            volume = 0
        pygame.mixer.music.set_volume(volume)
        title_rect.y -= 2
        best_score_rect.y += 2
        play_rect.x -= 4
        quit_rect.x += 4
        if title_rect.bottom <= 0 and play_rect.right <= 0 and quit_rect.left >= w and volume == 0:
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
        player_rect.x += 2 * level(timer)[2]
        player_hitbox.x += 2* level(timer)[2]
    if ka:
        player_rect.x -= 2 * level(timer)[2]
        player_hitbox.x -= 2* level(timer)[2]
    #Movimenti su y
    if kw:
        player_rect.y -= 2 * level(timer)[2]
        player_hitbox.y -= 2* level(timer)[2]
    if ks:
        player_rect.y += 2 * level(timer)[2]
        player_hitbox.y += 2* level(timer)[2]
    

    pygame.display.update()

pygame.quit()