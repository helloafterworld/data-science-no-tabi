import pygame
import sys
import random
import math

# --- INISIALISASI & PENGATURAN ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2v2 Ability-Based Auto-Battle")
clock = pygame.time.Clock()
font_lg = pygame.font.Font(None, 50)
font_md = pygame.font.Font(None, 32)
font_sm = pygame.font.Font(None, 28)

# --- WARNA & PENGATURAN BARU ---
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
HP_BAR_BG, HP_BAR_FG_GREEN, HP_BAR_FG_RED = (50, 50, 50), (0, 255, 0), (255, 0, 0)
BLUE, ORANGE, GREEN, PURPLE, YELLOW = (0, 150, 255), (255, 100, 0), (0, 200, 100), (160, 32, 240), (255, 220, 0)
ICE_COLOR, POISON_COLOR, LIFESTEAL_COLOR = (173, 216, 230), (124, 252, 0), (220, 20, 60)
CARD_BG_COLOR = (20, 20, 40)
ABILITY_PICKUP_COLOR = (0, 255, 255)
STATUS_HASTE_COLOR = (255, 255, 150)

# =====================================================================
# --- FUNGSI-FUNGSI UNTUK MENGGAMBAR KARTU STATUS ---
# =====================================================================

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

# =====================================================================
# --- KELAS-KELAS GAME ---
# =====================================================================

class FighterBall:
    def __init__(self, x, y, color, name, team, projectile_type="normal"):
        self.name, self.color, self.team = name, color, team
        self.rect = pygame.Rect(x, y, 40, 40)
        self.orbit_angle = 0
        self.speed_x, self.speed_y = random.choice([-4, 4]), random.choice([-4, 4])
        self.max_hp, self.current_hp = 200, 200
        self.opponents = []
        self.speed_multiplier, self.slow_timer = 1.0, 0
        self.is_poisoned, self.poison_timer, self.poison_tick_timer, self.poison_damage = False, 0, 0, 0
        self.haste_timer = 0
        self.weapons = [OrbitingWeapon(self, 200, projectile_type) for _ in range(4)]
        self.recalculate_orbit_distance()

    def activate_special(self): pass
    def set_opponents(self, opponent_list): self.opponents = opponent_list
    def recalculate_orbit_distance(self):
        base_dist = 50
        for i, weapon in enumerate(self.weapons):
            weapon.orbit_distance = base_dist + ((i // 8) * 5)
    def update(self):
        self.auto_move()
        self.update_weapons()
        self.update_status_effects()
    def auto_move(self):
        self.rect.x += self.speed_x * self.speed_multiplier
        self.rect.y += self.speed_y * self.speed_multiplier
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH: self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT: self.speed_y *= -1
    def update_weapons(self):
        self.orbit_angle += 0.03
        haste_multiplier = 2.0 if self.haste_timer > 0 else 1.0
        for i, weapon in enumerate(self.weapons):
            angle = self.orbit_angle + (i * (2 * math.pi / len(self.weapons)))
            weapon.update(angle)
            living_opponents = [opp for opp in self.opponents if opp.current_hp > 0]
            if living_opponents:
                weapon.shoot(random.choice(living_opponents), haste_multiplier)
    def update_status_effects(self):
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer == 0: self.speed_multiplier = 1.0
        if self.haste_timer > 0:
            self.haste_timer -= 1
            if self.haste_timer == 0: self.speed_multiplier = 1.0
        if self.is_poisoned:
            self.poison_timer -= 1
            self.poison_tick_timer -= 1
            if self.poison_tick_timer <= 0:
                self.take_damage(self.poison_damage)
                self.poison_tick_timer = 60
            if self.poison_timer <= 0: self.is_poisoned = False
    def take_damage(self, amount): self.current_hp -= amount
    def heal(self, amount): self.current_hp = min(self.max_hp, self.current_hp + amount)
    def draw(self):
        final_color = self.color
        if self.slow_timer > 0: final_color = (100, 100, 255)
        elif self.is_poisoned: final_color = GREEN
        elif self.haste_timer > 0: final_color = STATUS_HASTE_COLOR
        pygame.draw.ellipse(screen, final_color, self.rect)
        for weapon in self.weapons: weapon.draw()
    def draw_health_bar(self):
        bar_width, bar_height, bar_x, bar_y = 60, 10, self.rect.centerx - 30, self.rect.top - 15
        pygame.draw.rect(screen, HP_BAR_BG, (bar_x, bar_y, bar_width, bar_height))
        health_percentage = max(0, self.current_hp / self.max_hp)
        pygame.draw.rect(screen, HP_BAR_FG_GREEN, (bar_x, bar_y, bar_width * health_percentage, bar_height))

class BlueBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, BLUE, "Biru (Ice)", team)
    def activate_special(self):
        if self.opponents and (opps := [o for o in self.opponents if o.current_hp > 0]):
            projectiles.append(IceProjectile(self.rect.center, random.choice(opps)))
class OrangeBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, ORANGE, "Oranye (Heal)", team)
    def activate_special(self): self.heal(250)
class GreenBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, GREEN, "Hijau (Poison)", team, projectile_type="poison")
    def activate_special(self):
        if self.opponents and (opps := [o for o in self.opponents if o.current_hp > 0]):
            projectiles.append(PoisonProjectile(self.rect.center, random.choice(opps), is_special=True))
class PurpleBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, PURPLE, "Ungu (Vampire)", team, projectile_type="lifesteal")
    def activate_special(self):
        if self.opponents and (opps := [o for o in self.opponents if o.current_hp > 0]):
            projectiles.append(LifestealProjectile(self.rect.center, random.choice(opps), self, is_special=True))
class YellowBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, YELLOW, "Kuning (Haste)", team)
    def activate_special(self): self.speed_multiplier = 2.0; self.haste_timer = 180

class OrbitingWeapon:
    def __init__(self, owner, cooldown, projectile_type="normal"):
        self.owner, self.shoot_cooldown, self.projectile_type = owner, cooldown, projectile_type
        self.orbit_distance, self.rect = 60, pygame.Rect(0, 0, 15, 15)
        self.cooldown_timer = random.randint(0, cooldown)
    def update(self, angle):
        self.rect.centerx = self.owner.rect.centerx + self.orbit_distance * math.cos(angle)
        self.rect.centery = self.owner.rect.centery + self.orbit_distance * math.sin(angle)
        if self.cooldown_timer > 0: self.cooldown_timer -= 1
    def shoot(self, target, haste_multiplier=1.0):
        if self.cooldown_timer <= 0:
            proj_class = {"poison": PoisonProjectile, "lifesteal": LifestealProjectile}.get(self.projectile_type, Projectile)
            owner_arg = self.owner if self.projectile_type == "lifesteal" else None
            projectiles.append(proj_class(self.rect.center, target, owner=owner_arg))
            self.cooldown_timer = self.shoot_cooldown / haste_multiplier
    def draw(self): pygame.draw.ellipse(screen, (255,200,0), self.rect)

class Projectile:
    def __init__(self, start_pos, target_obj, owner=None, is_special=False):
        self.pos = pygame.math.Vector2(start_pos)
        self.target, self.owner, self.is_special = target_obj, owner, is_special
        self.damage, self.speed = 15, 10
        direction = pygame.math.Vector2(self.target.rect.center) - self.pos
        if direction.length() > 0: self.velocity = direction.normalize() * self.speed
        else: self.velocity = pygame.math.Vector2(0, -1) * self.speed
    def on_hit(self): self.target.take_damage(self.damage)
    def move(self): self.pos += self.velocity
    def draw(self): pygame.draw.circle(screen, WHITE, self.pos, 5)
class IceProjectile(Projectile):
    def __init__(self, start_pos, target_obj, owner=None, is_special=False):
        super().__init__(start_pos, target_obj, owner, is_special)
        self.damage = 5
    def on_hit(self):
        super().on_hit()
        self.target.speed_multiplier, self.target.slow_timer = 0.5, 120
    def draw(self): pygame.draw.circle(screen, ICE_COLOR, self.pos, 7)
class PoisonProjectile(Projectile):
    def on_hit(self):
        super().on_hit()
        self.target.is_poisoned = True
        self.target.poison_timer = 300
        self.target.poison_damage = 5 if self.is_special else 2
    def draw(self): pygame.draw.circle(screen, POISON_COLOR, self.pos, 5)
class LifestealProjectile(Projectile):
    def on_hit(self):
        super().on_hit()
        lifesteal_ratio = 1.0 if self.is_special else 0.25
        self.owner.heal(self.damage * lifesteal_ratio)
    def draw(self): pygame.draw.circle(screen, LIFESTEAL_COLOR, self.pos, 5)
class AbilityPickup:
    def __init__(self): self.rect = pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50), 20, 20)
    def draw(self): pygame.draw.rect(screen, ABILITY_PICKUP_COLOR, self.rect)

# =====================================================================
# --- SETUP UTAMA & GAME LOOP ---
# =====================================================================
team1 = [BlueBall(100, 200, "Tim Biru"), YellowBall(100, 500, "Tim Biru")]
team2 = [PurpleBall(SCREEN_WIDTH - 100, 200, "Tim Oranye"), OrangeBall(SCREEN_WIDTH - 100, 500, "Tim Oranye")]
for ball in team1: ball.set_opponents(team2)
for ball in team2: ball.set_opponents(team1)
balls = team1 + team2
projectiles, ability_pickups = [], [AbilityPickup() for _ in range(7)]
spawn_timer, game_over, winner_team_name = 90, False, ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(), sys.exit()

    if not game_over:
        for ball in balls:
            if ball.current_hp > 0: ball.update()
        for p in projectiles[:]:
            p.move()
            if p.target.current_hp > 0 and p.target.rect.collidepoint(p.pos):
                p.on_hit()
                projectiles.remove(p)
            elif not screen.get_rect().collidepoint(p.pos) or p.target.current_hp <= 0:
                projectiles.remove(p)
        if len(ability_pickups) < 10 and spawn_timer <= 0:
            ability_pickups.append(AbilityPickup())
            spawn_timer = 120
        else: spawn_timer -= 1
        for ball in balls:
            for pickup in ability_pickups[:]:
                if ball.current_hp > 0 and ball.rect.colliderect(pickup.rect):
                    ball.activate_special()
                    ability_pickups.remove(pickup)
        team1_alive = any(ball.current_hp > 0 for ball in team1)
        team2_alive = any(ball.current_hp > 0 for ball in team2)
        if not team1_alive: game_over, winner_team_name = True, team2[0].team
        elif not team2_alive: game_over, winner_team_name = True, team1[0].team

    screen.fill(BLACK)
    for ball in balls:
        if ball.current_hp > 0: ball.draw(), ball.draw_health_bar()
    for p in projectiles: p.draw()
    for ap in ability_pickups: ap.draw()
    
    TEAM_CARD_SIZE = (300, 140)
    INDIV_CARD_SIZE = (300, 100)
    draw_team_card(screen, team1, (20, 20), TEAM_CARD_SIZE, BLUE)
    for i, ball in enumerate(team1):
        pos_y = 20 + TEAM_CARD_SIZE[1] + (i * (INDIV_CARD_SIZE[1] + 10)) + 10
        draw_character_card(screen, ball, (20, pos_y), INDIV_CARD_SIZE)
    draw_team_card(screen, team2, (SCREEN_WIDTH - 320, 20), TEAM_CARD_SIZE, ORANGE)
    for i, ball in enumerate(team2):
        pos_y = 20 + TEAM_CARD_SIZE[1] + (i * (INDIV_CARD_SIZE[1] + 10)) + 10
        draw_character_card(screen, ball, (SCREEN_WIDTH - 320, pos_y), INDIV_CARD_SIZE)

    if game_over and winner_team_name:
        win_text = font_lg.render(f"PEMENANG: {winner_team_name}!", True, ORANGE if winner_team_name == team2[0].team else BLUE)
        screen.blit(win_text, (SCREEN_WIDTH/2 - win_text.get_width()/2, SCREEN_HEIGHT/2))

    pygame.display.flip()
    clock.tick(60)