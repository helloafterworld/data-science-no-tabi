# main.py

import pygame
import sys
from settings import *
from classes import BlueBall, OrangeBall, GreenBall, PurpleBall, YellowBall, PinkBall, AbilityPickup
from ui import draw_team_card, draw_character_card

# --- INISIALISASI PYGAME ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2v2 Modular Battle Arena")
clock = pygame.time.Clock()

# --- SETUP UTAMA GAME ---
team1 = [PinkBall(arena_rect.left + 100, 200, "Tim Pink"), 
         YellowBall(arena_rect.left + 100, 500, "Tim Biru")]
team2 = [PurpleBall(arena_rect.right - 140, 200, "Tim Oranye"), 
         OrangeBall(arena_rect.right - 140, 500, "Tim Oranye")]

for ball in team1: ball.set_opponents(team2)
for ball in team2: ball.set_opponents(team1)
    
balls = team1 + team2
projectiles, ability_pickups = [], [AbilityPickup() for _ in range(7)]
spawn_timer, game_over, winner_team_name = 90, False, ""

# ============================
# --- GAME LOOP UTAMA ---
# ============================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(), sys.exit()

    if not game_over:
        # --- UPDATE LOGIKA ---
        for ball in balls:
            if ball.current_hp > 0:
                new_projs = ball.update()
                if new_projs: projectiles.extend(new_projs)
        
        for p in projectiles[:]:
            p.move()
            if p.target.current_hp > 0 and p.target.rect.collidepoint(p.pos):
                p.on_hit()
                projectiles.remove(p)
            elif not arena_rect.collidepoint(p.pos) or p.target.current_hp <= 0:
                projectiles.remove(p)
                
        if len(ability_pickups) < 10 and spawn_timer <= 0:
            ability_pickups.append(AbilityPickup()); spawn_timer = 120
        else: spawn_timer -= 1
            
        for ball in balls:
            for pickup in ability_pickups[:]:
                if ball.current_hp > 0 and ball.rect.colliderect(pickup.rect):
                    new_proj = ball.activate_special()
                    if new_proj: projectiles.append(new_proj)
                    ability_pickups.remove(pickup)
                    
        team1_alive = any(ball.current_hp > 0 for ball in team1)
        team2_alive = any(ball.current_hp > 0 for ball in team2)
        if not team1_alive: game_over, winner_team_name = True, team2[0].team
        elif not team2_alive: game_over, winner_team_name = True, team1[0].team

    # --- MENGGAMBAR SEMUA ELEMEN ---
    screen.fill(UI_BG_COLOR)
    pygame.draw.rect(screen, ARENA_BG_COLOR, arena_rect)

    for ball in balls:
        if ball.current_hp > 0: ball.draw(screen); ball.draw_health_bar(screen)
    for p in projectiles: p.draw(screen)
    for ap in ability_pickups: ap.draw(screen)
    
    TEAM_CARD_SIZE = (UI_WIDTH - 20, 140)
    INDIV_CARD_SIZE = (UI_WIDTH - 20, 100)
    draw_team_card(screen, team1, (10, 20), TEAM_CARD_SIZE, BLUE)
    for i, ball in enumerate(team1):
        pos_y = 20 + TEAM_CARD_SIZE[1] + (i * (INDIV_CARD_SIZE[1] + 10)) + 10
        draw_character_card(screen, ball, (10, pos_y), INDIV_CARD_SIZE)
        
    draw_team_card(screen, team2, (arena_rect.right + 10, 20), TEAM_CARD_SIZE, ORANGE)
    for i, ball in enumerate(team2):
        pos_y = 20 + TEAM_CARD_SIZE[1] + (i * (INDIV_CARD_SIZE[1] + 10)) + 10
        draw_character_card(screen, ball, (arena_rect.right + 10, pos_y), INDIV_CARD_SIZE)

    if game_over and winner_team_name:
        win_text = font_lg.render(f"PEMENANG: {winner_team_name}!", True, ORANGE if winner_team_name == team2[0].team else BLUE)
        screen.blit(win_text, (SCREEN_WIDTH/2 - win_text.get_width()/2, SCREEN_HEIGHT/2))

    pygame.display.flip()
    clock.tick(60)
    