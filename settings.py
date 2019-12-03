import pygame, os

#folders
game_folder = os.path.dirname(__file__)
imgs_folder = os.path.join(game_folder, 'imagens')
maps_folder = os.path.join(game_folder, 'maps')
arquivos_folder = os.path.join(game_folder, 'arquivos')
blocos_folder = os.path.join(game_folder, 'imagens/blocos')
itens_folder = os.path.join(game_folder, 'imagens/itens')
mobs_folder = os.path.join(game_folder, 'imagens/mobs')

#settings
size = width, height = 800, 544
FPS = 120
tamanho = 32

black = 0, 0, 0
white = 255, 255, 255
blue = 0, 0, 255
RED = 255, 0, 0
BROWN = 150, 75, 0

pygame.font.init()
FONT = 'glasgow'
FONT_WAVE = pygame.font.SysFont(FONT, 70, bold=False, italic=True)
FONT_MORREU = pygame.font.SysFont(FONT, 100)
FONT_BALA = pygame.font.SysFont(FONT, 45)


#gun
LIFE_GUN = 1000
SPEED_GUN = 10
RATE_GUN = 200
RATE_ESPECIAL_GUN = 10000
POSICOES_20 = [[9, 28], [18, 15],[13, 10],[54, 39],[63, 54],[61, 55], [21, 28], [50, 58], [26,36], [29,50], [15,32], [19,40], [22,40], [35,40], [49, 40], [50, 38],[57, 42], [68, 40], [62, 32],[67,70],[62,65], [64, 55]]

#zumbi
SPEED_ZUMBI = 1.05    
ZUMBI_IMG = 'zumbi_+90.png'
ZUMBI_HIT_RECT = pygame.Rect(0, 0, 34, 48)
ZUMBI_WALL_HIT_RECT = pygame.Rect(0, 0, 20, 20)

RATE_HIT_ZUMBI = 500

#player
PLAYER_PNG = 'Player__.png'
ROT_SPEED = 2
PLAYER_SPEED = 2
PLAYER_HIT_RECT = pygame.Rect(0, 0, 22, 22)
PLAYER_LIFE = 120

#bosses
BOSS_SPEED_HIT_RECT = pygame.Rect(0, 0, 83, 100)
BOSS_SPEED_HIT_RECT_HIT = pygame.Rect(0, 0, 83, 100)
BOSS_LIFE_HIT_RECT = pygame.Rect(0, 0, 140, 100)
BOSS_LIFE_HIT_RECT_HIT = pygame.Rect(0, 0, 140, 100)

#BLOCKS
PAREDE_PNG = 'parede1.png'
CHAO_PNG = 'piso_madeira.png'
ESTRADA_PNG = 'estrada_1.png'
MATINHO_PNG = 'matinho.png'
AREIA_PNG = ['areia1.png','areia2.png','areia.png','areia3.png'] #Diag Esquerda, Cima, Centro, Esquerda

#Som_tiro
som_tiro = os.path.join(arquivos_folder, 'tiro1.mp3')
pygame.mixer.init()