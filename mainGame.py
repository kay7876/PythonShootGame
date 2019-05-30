# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random


# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('OSS프로젝트')
life = 2  # 게임 시작 시 초기 라이프 갯수

# 게임 음악 로드 중
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 배경 이미지 로드 중
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

# 플레이어 관련 매개 변수 설정
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 플레이어 스프라이트 이미지 영역
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 플레이어 폭발 스프라이트 이미지 영역
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# 총알 개채가 사용하는 surface매개변수 
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 적기 개채가 사용하는 surface매개변수
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()

# 파괴된 비행기 스프라이트 저장
enemies_down = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0

player_down_index = 16

score = 0

clock = pygame.time.Clock()

running = True

while running:
    # 게임 제어 최대 프레임 60
    clock.tick(60)

    # 적기를 생성
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    # 창을 벗어난 총알은 삭제
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # 창을 벗어난 적기 삭제
    for enemy in enemies1:
        enemy.move()
        # 플레이어 피격 여부 판단
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            life = life - 1
            player_rect = []
            player_rect.append(pygame.Rect(0, 99, 102, 126))        # 플레이어 스프라이트 이미지 영역
            player_rect.append(pygame.Rect(165, 360, 102, 126))
            player_rect.append(pygame.Rect(165, 234, 102, 126))     # 플레이어 폭발 스프라이트 이미지 영역
            player_rect.append(pygame.Rect(330, 624, 102, 126))
            player_rect.append(pygame.Rect(330, 498, 102, 126))
            player_rect.append(pygame.Rect(432, 624, 102, 126))
            player_pos = [200, 600]
            player = Player(plane_img, player_rect, player_pos)
            if life<0:
                    game_over_sound.play()
                    player.is_hit=True

    # 파괴된 적기를 저장
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # 배경
    screen.fill(0)
    screen.blit(background, (0, 0))

    # 플레이어 비행기 이미지
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # 更换图片索引使飞机有动画效果
        player.img_index = shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    # 파괴된 비행기 이미지
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 총알과 적기 이미지
    player.bullets.draw(screen)
    enemies1.draw(screen)

    # 점수
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)
    
    #라이프 포인트
    life_font = pygame.font.Font(None, 36)
    life_text = life_font.render(str(life), True, (128, 128, 128))
    text_rect = life_text.get_rect()
    text_rect.topleft = [80, 40]
    screen.blit(life_text, text_rect)

    # 최종 화면 업데이트
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # 키보드 입력
    key_pressed = pygame.key.get_pressed()
    # 플레이어 피격 시, 입력 무효
    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()
        # 키 입력시 총알 발사
        if key_pressed[K_z]: 
                if shoot_frequency % 8 == 0:
                    bullet_sound.play()
                    player.shoot(bullet_img)
                shoot_frequency += 1
                if shoot_frequency >= 8:
                    shoot_frequency = 0

font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
