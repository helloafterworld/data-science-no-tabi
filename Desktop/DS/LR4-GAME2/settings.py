# settings.py

import pygame

# --- PENGATURAN TATA LETAK LAYAR & ARENA ---
UI_WIDTH = 300
ARENA_WIDTH = 980
SCREEN_WIDTH = UI_WIDTH + ARENA_WIDTH + UI_WIDTH
SCREEN_HEIGHT = 720

# Mendefinisikan area pertempuran untuk diakses file lain
arena_rect = pygame.Rect(UI_WIDTH, 0, ARENA_WIDTH, SCREEN_HEIGHT)

# --- PENGATURAN FONT ---
pygame.font.init() # Inisialisasi modul font
font_lg = pygame.font.Font(None, 50)
font_md = pygame.font.Font(None, 32)
font_sm = pygame.font.Font(None, 28)

# --- WARNA ---
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
ARENA_BG_COLOR = (10, 10, 15)
UI_BG_COLOR = (5, 5, 10)
HP_BAR_BG, HP_BAR_FG_GREEN, HP_BAR_FG_RED = (50, 50, 50), (0, 255, 0), (255, 0, 0)
BLUE, ORANGE, GREEN, PURPLE, YELLOW = (0, 150, 255), (255, 100, 0), (0, 200, 100), (160, 32, 240), (255, 220, 0)
PINK = (255, 105, 180) # Warna untuk Bola Merah Muda
GRAY = (150, 150, 150) # Warna untuk Bola Abu-abu
WHITE_SNIPER = (220, 220, 220) # Warna untuk Bola Putih
RED, SNOW_COLOR = (255, 0, 0), (255, 250, 250) # Warna untuk Bola Merah dan Bola Salju
ICE_COLOR, POISON_COLOR, LIFESTEAL_COLOR = (173, 216, 230), (124, 252, 0), (220, 20, 60)
CARD_BG_COLOR = (30, 30, 50)
ABILITY_PICKUP_COLOR = (0, 255, 255)
STATUS_HASTE_COLOR = (255, 255, 150)

# --- PENGATURAN GAMEPLAY ---
DEFAULT_HP = 800
DEFAULT_WEAPON_COOLDOWN = 100
STARTING_WEAPONS = 2

# --- PENGATURAN MENU ---
BUTTON_COLOR = (80, 80, 150)
BUTTON_HOVER_COLOR = (120, 120, 200)
BUTTON_TEXT_COLOR = WHITE

# Kamus untuk memetakan nama string ke kelas aslinya
# Ini PENTING untuk menu pemilihan
BALL_CLASSES = {
    "Biru (Ice)": 'BlueBall',
    "Oranye (Heal)": 'OrangeBall',
    "Hijau (Poison)": 'GreenBall',
    "Ungu (Vampire)": 'PurpleBall',
    "Kuning (Haste)": 'YellowBall',
    "Pink (Homing)": 'PinkBall',
    "Putih (Sniper)": 'SniperBall',
    "Merah (Snow)": 'RedBall',
    "Abu-abu (Rapid)": 'GrayBall',
}