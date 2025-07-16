# classes.py

import pygame
import random
import math
from settings import *

# --- KELAS PROYEKTIL (Didefinisikan lebih dulu agar bisa digunakan di kelas lain) ---
class Projectile:
    def __init__(self, start_pos, target_obj, owner=None, is_special=False):
        self.pos = pygame.math.Vector2(start_pos)
        self.target, self.owner, self.is_special = target_obj, owner, is_special
        self.damage, self.speed = 15, 10
        direction = pygame.math.Vector2(self.target.rect.center) - self.pos
        self.velocity = direction.normalize() * self.speed if direction.length() > 0 else pygame.math.Vector2(0, -1) * self.speed
        
    def on_hit(self): self.target.take_damage(self.damage)
    def move(self): self.pos += self.velocity
    def draw(self, surface): pygame.draw.circle(surface, WHITE, self.pos, 5)

class IceProjectile(Projectile):
    def __init__(self, start_pos, target_obj, owner=None, is_special=False):
        super().__init__(start_pos, target_obj, owner, is_special)
        self.damage = 10 # Damage dikurangi agar efek slow lebih terasa
    def on_hit(self):
        super().on_hit()
        self.target.speed_multiplier, self.target.slow_timer = 0.5, 120
    def draw(self, surface): pygame.draw.circle(surface, ICE_COLOR, self.pos, 7)

class PoisonProjectile(Projectile):
    def on_hit(self):
        super().on_hit()
        self.target.is_poisoned, self.target.poison_timer, self.target.poison_damage = True, 300, 5 if self.is_special else 2
    def draw(self, surface): pygame.draw.circle(surface, POISON_COLOR, self.pos, 5)

class LifestealProjectile(Projectile):
    def on_hit(self):
        super().on_hit()
        lifesteal_ratio = 1.0 if self.is_special else 0.25
        self.owner.heal(self.damage * lifesteal_ratio)
    def draw(self, surface): pygame.draw.circle(surface, LIFESTEAL_COLOR, self.pos, 5)

class HomingProjectile(Projectile):
    def __init__(self, start_pos, target_obj, owner=None, is_special=False):
        super().__init__(start_pos, target_obj, owner, is_special)
        self.speed = 7
        self.turn_speed = 0.05
        self.damage = 20

        # INIT velocity langsung ke target
        direction_vec = pygame.math.Vector2(self.target.rect.center) - self.pos
        if direction_vec.length_squared() != 0:
            direction_vec.normalize_ip()
        else:
            direction_vec = pygame.math.Vector2(0, -1)
        self.velocity = direction_vec * self.speed

    def move(self):
        if self.target.current_hp > 0:
            direction_vec = pygame.math.Vector2(self.target.rect.center) - self.pos
            if direction_vec.length_squared() != 0:
                direction_vec.normalize_ip()
            else:
                direction_vec = pygame.math.Vector2(0, 0)
            
            self.velocity = direction_vec * self.speed

        self.pos += self.velocity
        print("Homing pos:", self.pos, "target:", self.target.rect.center)


    def draw(self, surface):
        pygame.draw.circle(surface, PINK, (int(self.pos.x), int(self.pos.y)), 8)
        pygame.draw.circle(surface, WHITE, (int(self.pos.x), int(self.pos.y)), 4)
    
    


# --- KELAS SENJATA ---
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
            proj_class = {"poison": PoisonProjectile, "lifesteal": LifestealProjectile, "homing": HomingProjectile}.get(self.projectile_type, Projectile)
            owner_arg = self.owner if self.projectile_type == "lifesteal" else None
            new_projectile = proj_class(self.rect.center, target, owner=owner_arg)
            self.cooldown_timer = self.shoot_cooldown / haste_multiplier
            return new_projectile
        return None
    def draw(self, surface): pygame.draw.ellipse(surface, (255,200,0), self.rect)

# --- KELAS BOLA PETARUNG (Induk & Anak) ---
class FighterBall:
    def __init__(self, x, y, color, name, team, projectile_type="normal"):
        self.name, self.color, self.team = name, color, team
        self.rect = pygame.Rect(x, y, 40, 40)
        self.orbit_angle = 0
        self.speed_x, self.speed_y = random.choice([-4, 4]), random.choice([-4, 4])
        self.max_hp, self.current_hp = DEFAULT_HP, DEFAULT_HP
        self.opponents = []
        self.speed_multiplier, self.slow_timer = 1.0, 0
        self.is_poisoned, self.poison_timer, self.poison_tick_timer, self.poison_damage = False, 0, 0, 0
        self.haste_timer = 0
        self.weapons = [OrbitingWeapon(self, DEFAULT_WEAPON_COOLDOWN, projectile_type) for _ in range(STARTING_WEAPONS)]
        self.recalculate_orbit_distance()
    def activate_special(self): return None
    def set_opponents(self, opponent_list): self.opponents = opponent_list
    def recalculate_orbit_distance(self):
        base_dist = 50
        for i, weapon in enumerate(self.weapons): weapon.orbit_distance = base_dist + ((i // 8) * 5)
    def update(self):
        self.auto_move()
        self.update_status_effects()
        return self.update_weapons() # Mengembalikan proyektil baru
    def auto_move(self):
        self.rect.x += self.speed_x * self.speed_multiplier
        self.rect.y += self.speed_y * self.speed_multiplier
        if self.rect.left <= arena_rect.left or self.rect.right >= arena_rect.right: self.speed_x *= -1
        if self.rect.top <= arena_rect.top or self.rect.bottom >= arena_rect.bottom: self.speed_y *= -1
        self.rect.clamp_ip(arena_rect)
    def update_weapons(self):
        new_projectiles = []
        self.orbit_angle += 0.03
        haste_multiplier = 2.0 if self.haste_timer > 0 else 1.0
        for i, weapon in enumerate(self.weapons):
            angle = self.orbit_angle + (i * (2 * math.pi / len(self.weapons)))
            weapon.update(angle)
            living_opponents = [opp for opp in self.opponents if opp.current_hp > 0]
            if living_opponents:
                new_proj = weapon.shoot(random.choice(living_opponents), haste_multiplier)
                if new_proj: new_projectiles.append(new_proj)
        return new_projectiles
    def update_status_effects(self):
        if self.slow_timer > 0: self.slow_timer -= 1; self.speed_multiplier = 1.0 if self.slow_timer == 0 else self.speed_multiplier
        if self.haste_timer > 0: self.haste_timer -= 1; self.speed_multiplier = 1.0 if self.haste_timer == 0 else self.speed_multiplier
        if self.is_poisoned:
            self.poison_timer -= 1; self.poison_tick_timer -= 1
            if self.poison_tick_timer <= 0: self.take_damage(self.poison_damage); self.poison_tick_timer = 60
            if self.poison_timer <= 0: self.is_poisoned = False
    def take_damage(self, amount): self.current_hp -= amount
    def heal(self, amount): self.current_hp = min(self.max_hp, self.current_hp + amount)
    def draw(self, surface):
        final_color = self.color
        if self.slow_timer > 0: final_color = (100, 100, 255)
        elif self.is_poisoned: final_color = GREEN
        elif self.haste_timer > 0: final_color = STATUS_HASTE_COLOR
        pygame.draw.ellipse(surface, final_color, self.rect)
        for weapon in self.weapons: weapon.draw(surface)
    def draw_health_bar(self, surface):
        bar_width, bar_height, bar_x, bar_y = 60, 10, self.rect.centerx - 30, self.rect.top - 15
        pygame.draw.rect(surface, HP_BAR_BG, (bar_x, bar_y, bar_width, bar_height))
        health_percentage = max(0, self.current_hp / self.max_hp)
        pygame.draw.rect(surface, HP_BAR_FG_GREEN, (bar_x, bar_y, bar_width * health_percentage, bar_height))

class BlueBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, BLUE, "Biru (Ice)", team)
    def activate_special(self):
        if self.opponents and (opps := [o for o in self.opponents if o.current_hp > 0]):
            return IceProjectile(self.rect.center, random.choice(opps))
        return None
class OrangeBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, ORANGE, "Oranye (Heal)", team)
    def activate_special(self): self.heal(250); return None
class GreenBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, GREEN, "Hijau (Poison)", team, projectile_type="poison")
    def activate_special(self):
        if self.opponents and (opps := [o for o in self.opponents if o.current_hp > 0]):
            return PoisonProjectile(self.rect.center, random.choice(opps), is_special=True)
        return None
class PurpleBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, PURPLE, "Ungu (Vampire)", team, projectile_type="lifesteal")
    def activate_special(self):
        if self.opponents and (opps := [o for o in self.opponents if o.current_hp > 0]):
            return LifestealProjectile(self.rect.center, random.choice(opps), self, is_special=True)
        return None
class YellowBall(FighterBall):
    def __init__(self, x, y, team): super().__init__(x, y, YELLOW, "Kuning (Haste)", team)
    def activate_special(self): self.speed_multiplier = 2.0; self.haste_timer = 180; return None

class PinkBall(FighterBall):
    def __init__(self, x, y, team):
        super().__init__(x, y, PINK, "Pink (Homing Rain)", team)
        self.is_special_active = False
        self.special_timer = 0
        self.special_cooldown = 0

    def activate_special(self):
        # Mirip YellowBall → pasang status durasi
        self.is_special_active = True
        self.special_timer = 300        # durasi 5 detik
        self.special_cooldown = 0       # tembak langsung di frame pertama
        return None

    def update(self):
        new_proj = []

        # Logika special berjalan jika active
        if self.is_special_active:
            self.special_timer -= 1
            self.special_cooldown -= 1

            if self.special_cooldown <= 0:
                if self.opponents and (opps := [o for o in self.opponents if o.current_hp > 0]):
                    new_proj.append(HomingProjectile(self.rect.center, random.choice(opps), self, is_special=True))
                    self.special_cooldown = 30    # tembak setiap 0.5 detik

            if self.special_timer <= 0:
                self.is_special_active = False

        # tambahkan logic update lain kalau ada
        return new_proj

    
class AbilityPickup:
    def __init__(self):
        x = random.randint(arena_rect.left + 20, arena_rect.right - 20)
        y = random.randint(arena_rect.top + 20, arena_rect.bottom - 20)
        self.rect = pygame.Rect(x, y, 20, 20)
    def draw(self, surface): pygame.draw.rect(surface, ABILITY_PICKUP_COLOR, self.rect)