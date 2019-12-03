import pygame
from settings import *

def collide_hit_rect(one, two):
    #retorna se colidiu
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        '''pegar dados do mapa'''
        self.map_data = []
        with open(filename, 'rt') as file:
            for linha in file:
                self.map_data.append(linha)
        self.tileWidth = len(self.map_data[0])
        self.tileHeight = len(self.map_data)
        self.width = self.tileWidth*tamanho
        self.height = self.tileHeight*tamanho

class Camera:
    '''aplicar camera nos dados do mapa'''
    def __init__(self, width_c, height_c):
        self.camera = pygame.Rect(0, 0, width_c, height_c)
        self.width = width_c
        self.height = height_c
    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        #mover câmera
        x = -target.rect.centerx + int(width/2)
        y = -target.rect.centery + int(height/2)

        #limites da camera
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width/2 - width), x)
        y = max(-(self.height - height), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)
        
