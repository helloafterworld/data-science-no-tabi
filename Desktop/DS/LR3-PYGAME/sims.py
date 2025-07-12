import pygame
import sys
import random

# --- FASE INISIALISASI & SETUP ---
pygame.init()
pygame.mixer.init()

# Pengaturan layar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulasi Pertarungan Bola")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
ATTACK_COLOR = (255, 255, 0) # Kuning untuk mode serangan
DAMAGE_COLOR = (255, 0, 0) # Merah saat terkena serangan

# Aset (Font & Suara)
try:
    ping_sound = pygame.mixer.Sound("ping.wav")
except pygame.error:
    print("File 'ping.wav' tidak ditemukan. Simulasi berjalan tanpa suara.")
    ping_sound = None

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# --- KELAS OBJEK ---
class Ball:
    def __init__(self, x, y, size, color, name):
        self.name = name
        self.original_color = color
        self.color = color
        self.size = size
        self.max_size = size # --- BARU: Menyimpan ukuran maksimal untuk kalkulasi health bar ---
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.speed_x = random.choice([-4, 4])
        self.speed_y = random.choice([-4, 4])
        self.is_attacking = False
        self.attack_duration = 180
        self.attack_cooldown = 300
        self.attack_timer = 0
        self.is_hit = 0
        
    def move(self):
        if self.size <= 5:
            return
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def update(self):
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.color = self.original_color
                self.attack_cooldown = random.randint(300, 600)
        else:
            self.attack_cooldown -= 1
            if self.attack_cooldown <= 0:
                self.is_attacking = True
                self.color = ATTACK_COLOR
                self.attack_timer = self.attack_duration
        
        if self.is_hit > 0:
            self.is_hit -= 1
            if self.is_hit == 0 and not self.is_attacking:
                self.color = self.original_color

    def take_damage(self, amount):
        if self.size > 5: # Hanya terima damage jika masih hidup
            self.size -= amount
            self.is_hit = 20
            self.color = DAMAGE_COLOR
            center = self.rect.center
            self.rect = pygame.Rect(0, 0, self.size, self.size)
            self.rect.center = center

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    # --- BARU: Metode untuk menggambar health bar ---
    def draw_health_bar(self, surface):
        if self.size > 0:
            # Kalkulasi persentase kesehatan
            health_percentage = self.size / self.max_size
            
            # Pengaturan posisi dan ukuran bar
            bar_width = self.max_size
            bar_height = 8
            bar_x = self.rect.centerx - (bar_width / 2)
            bar_y = self.rect.top - bar_height - 5 # 5 piksel di atas bola

            # Gambar latar belakang bar (merah)
            pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
            # Gambar bar kesehatan saat ini (hijau)
            pygame.draw.rect(surface, GREEN, (bar_x, bar_y, bar_width * health_percentage, bar_height))


# --- MEMBUAT OBJEK ---
ball1 = Ball(100, 100, 50, GREEN, "Hijau")
ball2 = Ball(700, 500, 50, GREY, "Abu-abu")
balls = [ball1, ball2]
game_over_message = ""

# ============================
# --- GAME LOOP UTAMA ---
# ============================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over_message:
        for ball in balls:
            ball.move()
            ball.update()

        for ball in balls:
            if ball.rect.left <= 0 or ball.rect.right >= screen_width: ball.speed_x *= -1
            if ball.rect.top <= 0 or ball.rect.bottom >= screen_height: ball.speed_y *= -1

        if ball1.rect.colliderect(ball2.rect):
            if ping_sound: ping_sound.play()
            p1_attack = ball1.is_attacking and not ball2.is_attacking
            p2_attack = ball2.is_attacking and not ball1.is_attacking
            if p1_attack: ball2.take_damage(90)
            elif p2_attack: ball1.take_damage(90)
            ball1.speed_x, ball2.speed_x = ball2.speed_x, ball1.speed_x
            ball1.speed_y, ball2.speed_y = ball2.speed_y, ball1.speed_y

        if ball1.size <= 5: game_over_message = f"Pemenangnya adalah {ball2.name}!"
        elif ball2.size <= 5: game_over_message = f"Pemenangnya adalah {ball1.name}!"

    # --- Menggambar di Layar ---
    screen.fill(BLACK)
    
    for ball in balls:
        ball.draw(screen)
        ball.draw_health_bar(screen) # --- BARU: Panggil fungsi gambar health bar ---
    
    if game_over_message:
        text = font.render(game_over_message, True, BLACK)
        screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
    else:
        for ball in balls:
            if ball.is_attacking:
                status_text = small_font.render(f"{ball.name} Menyerang!", True, ATTACK_COLOR)
                pos_y = 10 if ball.name == "Hijau" else 50
                screen.blit(status_text, (10, pos_y))

    # --- Update Tampilan ---
    pygame.display.flip()
    pygame.time.Clock().tick(60)