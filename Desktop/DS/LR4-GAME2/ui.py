# ui.py

import pygame
from settings import *

def draw_team_card(surface, team, position, card_size, team_color):
    card_surf = pygame.Surface(card_size, pygame.SRCALPHA)
    card_surf.fill((*CARD_BG_COLOR, 180))
    total_current_hp = sum(ball.current_hp for ball in team)
    total_max_hp = sum(ball.max_hp for ball in team)
    total_power = sum(len(ball.weapons) for ball in team)
    team_name = team[0].team
    team_text = font_lg.render(team_name, True, team_color)
    card_surf.blit(team_text, (15, 10))
    hp_text = font_md.render(f"HP: {int(total_current_hp)} / {total_max_hp}", True, WHITE)
    card_surf.blit(hp_text, (15, 60))
    power_text = font_md.render(f"Power: {total_power}", True, WHITE)
    card_surf.blit(power_text, (15, 95))
    surface.blit(card_surf, position)

def draw_character_card(surface, ball, position, card_size):
    card_surf = pygame.Surface(card_size, pygame.SRCALPHA)
    is_alive = ball.current_hp > 0
    bg_alpha = 160 if is_alive else 80
    card_surf.fill((*CARD_BG_COLOR, bg_alpha))
    name_text = font_md.render(ball.name, True, ball.color if is_alive else (100, 100, 100))
    card_surf.blit(name_text, (10, 5))
    if is_alive:
        hp_text = font_sm.render(f"HP: {int(ball.current_hp)}/{ball.max_hp}", True, WHITE)
        power_text = font_sm.render(f"Weapons: {len(ball.weapons)}", True, WHITE)
        card_surf.blit(hp_text, (10, 40))
        card_surf.blit(power_text, (150, 40))
        status_text, status_color = "", WHITE
        if ball.slow_timer > 0: status_text, status_color = "SLOWED", (100, 150, 255)
        elif ball.is_poisoned: status_text, status_color = "POISONED", (150, 255, 150)
        elif ball.haste_timer > 0: status_text, status_color = "HASTE", STATUS_HASTE_COLOR
        if status_text:
            status_render = font_sm.render(status_text, True, status_color)
            card_surf.blit(status_render, (10, 65))
    else:
        defeated_text = font_md.render("DEFEATED", True, (100, 100, 100))
        card_surf.blit(defeated_text, (card_size[0]/2 - defeated_text.get_width()/2, 45))
    surface.blit(card_surf, position)