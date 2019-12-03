import math, random, time
import sys, pygame, os
from pygame.locals import *
vec = pygame.math.Vector2

from settings import *
from maps import *
from Sprites import *

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Zumbif")


'''carregar imagens'''
ICON = pygame.image.load(os.path.join(imgs_folder, 'icon.png'))
pygame.display.set_icon(ICON)

PLAYER_IMG = pygame.image.load(os.path.join(imgs_folder, PLAYER_PNG)).convert_alpha()
ZUMBIIMG = pygame.image.load(os.path.join(mobs_folder, ZUMBI_IMG)).convert_alpha()
WALL_IMG = pygame.image.load(os.path.join(blocos_folder, PAREDE_PNG)).convert_alpha()
TIRO_IMG = pygame.Surface((5, 5))
BOSSES = {'speed':(pygame.image.load(os.path.join(mobs_folder, 'boss_speed.png')).convert_alpha()),
          'life':(pygame.image.load(os.path.join(mobs_folder, 'boss_life.png')).convert_alpha())}

BULLET_IMG = pygame.image.load(os.path.join(itens_folder, 'bullet_.png')).convert_alpha()
BULLET_20_IMG = pygame.image.load(os.path.join(itens_folder, '+20.png')).convert_alpha()
CHAO_IMG = pygame.image.load(os.path.join(blocos_folder, CHAO_PNG)).convert_alpha()
ESTRADA_IMG = pygame.image.load(os.path.join(blocos_folder, ESTRADA_PNG)).convert_alpha()
MATINHO_IMG = pygame.image.load(os.path.join(blocos_folder, MATINHO_PNG)).convert_alpha()
AREIA_IMG = [
    pygame.image.load(os.path.join(blocos_folder, AREIA_PNG[0])).convert_alpha(),
    pygame.image.load(os.path.join(blocos_folder, AREIA_PNG[1])).convert_alpha(),
    pygame.image.load(os.path.join(blocos_folder, AREIA_PNG[2])).convert_alpha(),
    pygame.image.load(os.path.join(blocos_folder, AREIA_PNG[3])).convert_alpha()
]
MADEIRA_IMG = pygame.image.load(os.path.join(blocos_folder, 'madeira.png')).convert_alpha()
NEVE_IMG = pygame.image.load(os.path.join(blocos_folder, 'neve.png')).convert_alpha()
FOLHAGEM_IMG = pygame.image.load(os.path.join(blocos_folder, 'folhagem.png')).convert_alpha()
BRICK_IMG = pygame.image.load(os.path.join(blocos_folder, 'brick.png')).convert_alpha()



def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

class game:
    def main(self):
        """Contém os valores iniciais do jogo"""
        self.player_img = pygame.image.load(os.path.join(imgs_folder, 'Player__.png')).convert_alpha()
        self.imglife = pygame.Surface((0,0))
        self.rectlife = self.imglife.get_rect()
        self.score = 0
        self.contador = 0
        self.in_boss = False
        self.perdeu = False
        self.venceu = False


        '''load sprites'''
        self.Player = Player(self, tamanho*2, tamanho*2)
        self.all_sprites = pygame.sprite.Group()
        self.Zumbis = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.block_list = pygame.sprite.Group()
        self.Tiros = pygame.sprite.Group()
        self.ItemList = pygame.sprite.Group()
          
        #Carregar mapa    
        self.load_map()
        self.camera = Camera(self.map.width, self.map.height)
        
        #Gerar Zumbi, wave 1
        self.n_wave = 1
        self.random_zumbi(1)

        global automatize
        #Criar mapa em si
        for line, tiles in enumerate(self.map.map_data):
            for col, tile in enumerate(tiles):
                '''parâmetros para os tiles'''
                tile_config = {
                    'W':[self, Wall, WALL_IMG, self.wall_list, col, line],
                    'C':[self, Bloco, CHAO_IMG, self.block_list, col, line],
                    'E':[self, Bloco, ESTRADA_IMG, self.block_list, col, line],
                    'M':[self, Bloco, MATINHO_IMG, self.block_list, col, line],
                    'Z':[self, Bloco, AREIA_IMG[0], self.block_list, col, line],
                    'z':[self, Bloco, AREIA_IMG[3], self.block_list, col, line],
                    'x':[self, Bloco, AREIA_IMG[2], self.block_list, col, line],
                    'X':[self, Bloco, AREIA_IMG[1], self.block_list, col, line],
                    'm':[self, Bloco, MADEIRA_IMG, self.block_list, col, line],
                    'N':[self, Bloco, NEVE_IMG, self.block_list, col, line],
                    'F':[self, Bloco, FOLHAGEM_IMG, self.block_list, col, line],
                    'B':[self, Bloco, BRICK_IMG, self.block_list, col, line]
                }
                
                '''carregar visualmente o mapa'''
                if not tile in ',_\n':
                    lista = tile_config[tile]
                    automatize(lista[0], lista[1], lista[2], lista[3], lista[4], lista[5])
            
        '''Carregar points +20 de munição'''
        for POS in POSICOES_20:
            item = Itens.BALA_20(self, BULLET_20_IMG, POS[0]*tamanho, POS[1]*tamanho)
            self.ItemList.add(item)
 
        clock = pygame.time.Clock()

        '''invocar bosses'''
        global Bosses
        Bosses = Bosses()
        self.FUNC_WAVES = {5:Bosses.Spawn_boss_speed, 11:Bosses.Spawn_boss_vida}
        
        self.qt_zumbi = len(self.Zumbis)

        self.run = True
        while self.run:
            clock.tick(FPS)
            events()
        
            #Atualizar e desenhar
            self.update_sprites()
            self.draw_sprites()
            

            pygame.display.flip()
            
    def update_sprites(self):
        """Atualiza todos os Sprites e realiza eventos"""
        screen.fill(black)
        self.camera.update(self.Player)
        
        self.Zumbis.update()
        self.Player.update()
        self.Tiros.update()
        self.ItemList.update()

        '''Gerar zumbis se passar da wave e não for a wave de boss'''
        if len(self.Zumbis) == 0 and self.n_wave not in self.FUNC_WAVES.keys():
            self.contador = 0 
            self.qt_zumbi += 2

            self.random_zumbi(self.qt_zumbi)
            if not self.venceu:
                time.sleep(0.6)
                self.n_wave += 1
            
        
        #nascer boss
        elif self.n_wave in self.FUNC_WAVES.keys():
            boss = self.FUNC_WAVES[self.n_wave]
            
            if len(self.Zumbis) == 0 and self.contador == 0:  
                boss(self)
                self.in_boss = True
            elif len(self.Zumbis) == 0:
                self.in_boss = False
                self.n_wave += 1
                

        #Tiro collide Wall
        for tiro in self.Tiros:  
            Tiro_collide_wall = pygame.sprite.spritecollide(tiro, self.wall_list, False)
            if Tiro_collide_wall and tiro.ESPECIAL:
                for wall in self.wall_list:
                    if wall.x in range(tiro.rect.x-100, tiro.rect.x+100) and wall.y in range(tiro.rect.y-100, tiro.rect.y+100):
                        wall.kill()
                        tiro.kill()
            elif Tiro_collide_wall:
                tiro.kill()

    def draw_sprites(self):
        """escreve todos os sprites na tela"""
        for block in self.block_list:
            screen.blit(block.image, self.camera.apply(block))
        for tiros in self.Tiros:
            screen.blit(tiros.image, self.camera.apply(tiros))
        for wall in self.wall_list:
            screen.blit(wall.image, self.camera.apply(wall))
        for zumbi in self.Zumbis:
            screen.blit(zumbi.image, self.camera.apply(zumbi))
            screen.blit(zumbi.imglife, self.camera.apply_rect(zumbi.rectlife))

        for item in self.ItemList:
            screen.blit(item.image, self.camera.apply(item))
        screen.blit(self.Player.image, self.camera.apply(self.Player))
        screen.blit(self.Player.imglife, self.camera.apply_rect(self.Player.rectlife))

        self.texto_screen(FONT_WAVE, 'WAVE %s'%(self.n_wave), 300, tamanho, RED)
        self.bala_screen(self.Player.n_bala)
        self.score_screen(self.score)

        if self.perdeu:
            self.texto_screen(FONT_WAVE, 'VOCÊ PERDEU :(', 200, 200, (255, 0, 255))
 
        if self.in_boss:
            self.texto_screen(FONT_WAVE, 'Boss!!', 300, 300, (255, 165, 0))

        if self.venceu:
            self.texto_screen(FONT_WAVE, 'VOCÊ VENCEU!!!', 250, 250, (255, 255, 255))

            
    def load_map(self):
        """carrega mapa"""
        game_folder = os.path.dirname(__file__)
        arquivo = os.path.join(maps_folder, 'map_atualizado__.txt')
        self.map = Map(arquivo)


    
    """Funções para os Sprites"""
    def random_xy(self, minimo):
        '''pega um (x,y) aleatório'''
        self.line = random.randint(minimo, len(self.map.map_data)-1)
        self.col = random.randint(minimo, len(self.map.map_data[self.line].split(','))-1)
        
        return self.col, self.line #x, y

    def random_zumbi(self, quantidade):
        '''gera zumbis aleatórios de acordo com o espaço e a wave'''
        if self.n_wave < 12:
            for i in range(quantidade):
                self.random_xy(4)
                
                if self.n_wave < 5:
                    while self.line > 27 or self.col > 27:     # se os zumbis sairem do cenário
                        self.random_xy(4)
                elif 5 <= self.n_wave <= 8:
                    while self.col < 13 or self.col > 50 or self.line < 37 or self.line > 40:     # se os zumbis sairem do cenário
                        self.random_xy(4)
                elif 9 <= self.n_wave <= 11:
                    while self.col < 58 or self.col > 68 or self.line < 35 or self.line > 50:     # se os zumbis sairem do cenário
                        self.random_xy(4)

                zumbi = Zumbi(self, ZUMBIIMG, self.col*tamanho, self.line*tamanho, False)
                self.Zumbis.add(zumbi)
        else:
            self.venceu = True
    
    def texto_screen(self, fonte, texto, x, y, cor):
        text = fonte.render(texto, 1, cor)
        screen.blit(text, (x, y))

    def bala_screen(self, n_bala):
        text = FONT_BALA.render('x%d'%(n_bala), 1, BROWN)
        screen.blit(text, (width-tamanho*3, tamanho//2))
        screen.blit(BULLET_IMG, (width-tamanho*5, tamanho//2))
    
    def score_screen(self, score):
        text = FONT_BALA.render('Score: %d'%(score), 1, BROWN)
        screen.blit(text, (tamanho*3, tamanho//2))


'''Roda o programa'''
game = game()
if __name__ == "__main__":
    game.main()
