# main.py

import pygame
import sys
from settings import *
# Impor semua kelas bola dan pickup
from classes import (BlueBall, OrangeBall, GreenBall, PurpleBall, YellowBall, PinkBall, SniperBall, GrayBall, 
                     AbilityPickup, Projectile, OrbitingWeapon)
# Impor semua fungsi UI
from ui import draw_team_card, draw_character_card, draw_menu_screen, draw_button

# ============================
# --- FUNGSI UTAMA GAME ---
# ============================

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Color Wars - Battle Simulator")
    clock = pygame.time.Clock()

    game_state = 'menu' # Status awal permainan

    # Variabel untuk menyimpan semua objek game saat status 'gameplay'
    game_objects = {}

    # Pengaturan untuk menu
    ball_options = list(BALL_CLASSES.keys())
    selections = {
        "team1": {"member1": ball_options[2], "member2": ball_options[4]}, # Green, Yellow
        "team2": {"member1": ball_options[3], "member2": ball_options[1]}  # Purple, Orange
    }
    
    button_rects = {
        'team1': [
            pygame.Rect(50, 200, 200, 50),
            pygame.Rect(50, 270, 200, 50)
        ],
        'team2': [
            pygame.Rect(SCREEN_WIDTH - 250, 200, 200, 50),
            pygame.Rect(SCREEN_WIDTH - 250, 270, 200, 50)
        ],
        'start': pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT - 100, 300, 60)
    }

    # ============================
    # --- GAME LOOP UTAMA ---
    # ============================
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # --- PENANGANAN EVENT ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == 'menu':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Logika klik tombol di menu
                    if button_rects['start'].collidepoint(mouse_pos):
                        game_objects = start_game(selections) # Mulai game dengan pilihan
                        game_state = 'gameplay'
                    
                    # Logika ganti pilihan bola
                    for i, rect in enumerate(button_rects['team1']):
                        if rect.collidepoint(mouse_pos):
                            current_selection = selections['team1'][f'member{i+1}']
                            current_index = ball_options.index(current_selection)
                            new_index = (current_index + 1) % len(ball_options)
                            selections['team1'][f'member{i+1}'] = ball_options[new_index]
                    
                    for i, rect in enumerate(button_rects['team2']):
                        if rect.collidepoint(mouse_pos):
                            current_selection = selections['team2'][f'member{i+1}']
                            current_index = ball_options.index(current_selection)
                            new_index = (current_index + 1) % len(ball_options)
                            selections['team2'][f'member{i+1}'] = ball_options[new_index]

        # --- LOGIKA & GAMBAR BERDASARKAN STATUS GAME ---
        if game_state == 'menu':
            draw_menu_screen(screen, selections, ball_options, button_rects, mouse_pos)
        
        elif game_state == 'gameplay':
            # Update logika game
            update_gameplay(game_objects)
            # Gambar semua elemen game
            draw_gameplay(screen, game_objects)

        pygame.display.flip()
        clock.tick(60)

def start_game(selections):
    """Inisialisasi semua objek game berdasarkan pilihan dari menu."""
    # Dapatkan kelas sebenarnya dari nama string
    # globals() memungkinkan kita mengakses kelas berdasarkan namanya
    team1_classes = [globals()[BALL_CLASSES[name]] for name in selections['team1'].values()]
    team2_classes = [globals()[BALL_CLASSES[name]] for name in selections['team2'].values()]

    team1 = [team1_classes[0](arena_rect.left + 100, 200, "Tim Biru"), 
             team1_classes[1](arena_rect.left + 100, 500, "Tim Biru")]
    team2 = [team2_classes[0](arena_rect.right - 140, 200, "Tim Oranye"), 
             team2_classes[1](arena_rect.right - 140, 500, "Tim Oranye")]

    for ball in team1: ball.set_opponents(team2)
    for ball in team2: ball.set_opponents(team1)

    return {
        "team1": team1,
        "team2": team2,
        "balls": team1 + team2,
        "projectiles": [],
        "ability_pickups": [AbilityPickup() for _ in range(7)],
        "visual_effects": [],
        "spawn_timer": 90,
        "game_over": False,
        "winner_team_name": ""
    }

def update_gameplay(go): # 'go' adalah singkatan dari game_objects
    """Menjalankan semua logika update untuk status gameplay."""
    if go['game_over']: return

    for ball in go['balls']:
        if ball.current_hp > 0:
            new_projs = ball.update()
            if new_projs: go['projectiles'].extend(new_projs)
    
    for p in go['projectiles'][:]:
        p.move()
        if p.target.current_hp > 0 and p.target.rect.collidepoint(p.pos):
            p.on_hit()
            go['projectiles'].remove(p)
        elif not arena_rect.collidepoint(p.pos) or p.target.current_hp <= 0:
            go['projectiles'].remove(p)
            
    if len(go['ability_pickups']) < 10 and go['spawn_timer'] <= 0:
        go['ability_pickups'].append(AbilityPickup())
        go['spawn_timer'] = 120
    else: go['spawn_timer'] -= 1
        
    for ball in go['balls']:
        for pickup in go['ability_pickups'][:]:
            if ball.current_hp > 0 and ball.rect.colliderect(pickup.rect):
                result = ball.activate_special()
                if result:
                    # Cek apakah hasilnya proyektil atau data efek
                    if isinstance(result, Projectile):
                        go['projectiles'].append(result)
                    elif isinstance(result, list): # <-- Tambahkan cek ini
                        go['projectiles'].extend(result)
                    elif isinstance(result, dict):
                        go['visual_effects'].append(result)
                go['ability_pickups'].remove(pickup)

        
    for effect in go['visual_effects'][:]:
        effect['timer'] -= 1
        
        # Logika saat timer efek selesai
        if effect['timer'] <= 0:
            if effect['type'] == 'sniper_charge':
                # Berikan damage ke target
                effect['target'].take_damage(effect['damage'])
                # Buat efek garis tembakan sebagai umpan balik
                shot_effect = {
                    "type": "sniper_line",
                    "start": effect['owner'].rect.center,
                    "end": effect['target'].rect.center,
                    "timer": 10,
                    "color": WHITE
                }
                go['visual_effects'].append(shot_effect)

            go['visual_effects'].remove(effect) # Hapus efek yang sudah selesai
          
                
    team1_alive = any(ball.current_hp > 0 for ball in go['team1'])
    team2_alive = any(ball.current_hp > 0 for ball in go['team2'])
    if not team1_alive: go['game_over'], go['winner_team_name'] = True, go['team2'][0].team
    elif not team2_alive: go['game_over'], go['winner_team_name'] = True, go['team1'][0].team

def draw_gameplay(surface, go):
    """Menggambar semua elemen untuk status gameplay."""
    surface.fill(UI_BG_COLOR)
    pygame.draw.rect(surface, ARENA_BG_COLOR, arena_rect)

    for ball in go['balls']:
        if ball.current_hp > 0: ball.draw(surface); ball.draw_health_bar(surface)
    for p in go['projectiles']: p.draw(surface)
    for ap in go['ability_pickups']: ap.draw(surface)
    for effect in go['visual_effects']:
        if effect['type'] == 'sniper_line':
            pygame.draw.line(surface, effect['color'], effect['start'], effect['end'], 4)
        
        elif effect['type'] == 'sniper_charge':
            # Gambar lingkaran yang mengecil di atas target
            target_pos = effect['target'].rect.center
            max_radius = 50
            # Radius mengecil seiring berjalannya waktu
            current_radius = int(max_radius * (effect['timer'] / effect['duration']))
            
            if current_radius > 0:
                pygame.draw.circle(surface, WHITE, target_pos, current_radius, 3) # '3' adalah tebal garis
    
    
    TEAM_CARD_SIZE = (UI_WIDTH - 20, 140)
    INDIV_CARD_SIZE = (UI_WIDTH - 20, 100)
    draw_team_card(surface, go['team1'], (10, 20), TEAM_CARD_SIZE, BLUE)
    for i, ball in enumerate(go['team1']):
        pos_y = 20 + TEAM_CARD_SIZE[1] + (i * (INDIV_CARD_SIZE[1] + 10)) + 10
        draw_character_card(surface, ball, (10, pos_y), INDIV_CARD_SIZE)
        
    draw_team_card(surface, go['team2'], (arena_rect.right + 10, 20), TEAM_CARD_SIZE, ORANGE)
    for i, ball in enumerate(go['team2']):
        pos_y = 20 + TEAM_CARD_SIZE[1] + (i * (INDIV_CARD_SIZE[1] + 10)) + 10
        draw_character_card(surface, ball, (arena_rect.right + 10, pos_y), INDIV_CARD_SIZE)

    if go['game_over'] and go['winner_team_name']:
        win_text = font_lg.render(f"PEMENANG: {go['winner_team_name']}!", True, ORANGE if go['winner_team_name'] == go['team2'][0].team else BLUE)
        surface.blit(win_text, (SCREEN_WIDTH/2 - win_text.get_width()/2, SCREEN_HEIGHT/2))

if __name__ == '__main__':
    main()