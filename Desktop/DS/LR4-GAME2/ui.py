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
        # 1. Sesuaikan posisi teks HP
        hp_text = font_sm.render(f"HP: {int(ball.current_hp)}/{ball.max_hp}", True, WHITE)
        card_surf.blit(hp_text, (10, 35))

        # 2. Hitung persentase dan gambar health bar
        health_percentage = max(0, ball.current_hp / ball.max_hp)
        bar_pos = (10, 60)
        bar_size = (card_size[0] - 20, 12)
        # Latar belakang bar
        pygame.draw.rect(card_surf, HP_BAR_BG, (*bar_pos, *bar_size), border_radius=3)
        # Bar HP saat ini
        pygame.draw.rect(card_surf, HP_BAR_FG_GREEN, (bar_pos[0], bar_pos[1], bar_size[0] * health_percentage, bar_size[1]), border_radius=3)

        # 3. Sesuaikan posisi teks Power dan Status
        power_text = font_sm.render(f"Weapons: {len(ball.weapons)}", True, WHITE)
        card_surf.blit(power_text, (10, 80))
        
        status_text, status_color = "", WHITE
        if ball.slow_timer > 0: status_text, status_color = "SLOWED", (100, 150, 255)
        elif ball.is_poisoned: status_text, status_color = "POISONED", (150, 255, 150)
        elif ball.haste_timer > 0: status_text, status_color = "HASTE", STATUS_HASTE_COLOR
        
        if status_text:
            status_render = font_sm.render(status_text, True, status_color)
            card_surf.blit(status_render, (card_size[0] - status_render.get_width() - 10, 80))
    else:
        defeated_text = font_md.render("DEFEATED", True, (100, 100, 100))
        card_surf.blit(defeated_text, (card_size[0]/2 - defeated_text.get_width()/2, 45))

    surface.blit(card_surf, position)

def draw_button(surface, rect, text, is_hovered):
    """Menggambar sebuah tombol interaktif."""
    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(surface, color, rect, border_radius=10)
    text_surf = font_md.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def draw_menu_screen(surface, selections, ball_options, button_rects, hovered_button):
    """Menggambar seluruh layar menu pemilihan."""
    surface.fill(UI_BG_COLOR)
    
    # Judul
    title_text = font_lg.render("Pilih Komposisi Tim", True, WHITE)
    surface.blit(title_text, (surface.get_width()/2 - title_text.get_width()/2, 50))

    # Opsi Tim 1
    team1_title = font_md.render("Tim 1 (Biru)", True, BLUE)
    surface.blit(team1_title, (UI_WIDTH / 2 - team1_title.get_width()/2, 150))
    for i, member_key in enumerate(['member1', 'member2']):
        text = selections['team1'][member_key]
        rect = button_rects['team1'][i]
        is_hovered = rect.collidepoint(pygame.mouse.get_pos())
        draw_button(surface, rect, text, is_hovered)

    # Opsi Tim 2
    team2_title = font_md.render("Tim 2 (Oranye)", True, ORANGE)
    surface.blit(team2_title, (SCREEN_WIDTH - UI_WIDTH / 2 - team2_title.get_width()/2, 150))
    for i, member_key in enumerate(['member1', 'member2']):
        text = selections['team2'][member_key]
        rect = button_rects['team2'][i]
        is_hovered = rect.collidepoint(pygame.mouse.get_pos())
        draw_button(surface, rect, text, is_hovered)

    # Tombol Mulai
    start_rect = button_rects['start']
    is_start_hovered = start_rect.collidepoint(pygame.mouse.get_pos())
    draw_button(surface, start_rect, "Mulai Pertandingan", is_start_hovered)