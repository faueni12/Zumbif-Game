import pygame
from Zumbif import *
from settings import *

def collide_with_walls(sprite, group, dir, boo):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(sprite, group, boo, collide_hit_rect)
            if hits:
                if sprite.vel.x > 0:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2.0
                if sprite.vel.x < 0:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x

        if dir == 'y':
            hits = pygame.sprite.spritecollide(sprite, group, boo, collide_hit_rect)
            if hits:
                if sprite.vel.y > 0:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
                if sprite.vel.y < 0:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y
                
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = PLAYER_IMG
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center

        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0


        self.n_bala = 100
        self.last_shot = 0
        self.bullet_rate = 150

        self.mover = True

        #life
        self.life = PLAYER_LIFE
        
        self.imglife = pygame.Surface((self.life*2, 5))
        self.imglife.fill((20,20,255))
        self.rectlife = self.imglife.get_rect()
        self.rectlife.centerx = self.rect.centerx
        self.rectlife.centery = self.rect.centery - 30
        
    def keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)

        keys = pygame.key.get_pressed()
        #rotacionar:
        if self.mover:
            if keys[pygame.K_LEFT]:
                self.rot_speed = ROT_SPEED
            if keys[pygame.K_RIGHT]:
                self.rot_speed = -ROT_SPEED

            #mover
            if keys[pygame.K_UP]:
                self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            if keys[pygame.K_DOWN]:
                self.vel = vec(-PLAYER_SPEED/2, 0).rotate(-self.rot)

            #atirar
            if keys[pygame.K_SPACE]:
                now = pygame.time.get_ticks()
                if now - self.last_shot > RATE_GUN and self.n_bala > 0: #tempo de cooldown da bala
                    pygame.mixer.music.set_volume(0.05)
                    pygame.mixer.music.load(som_tiro)
                    pygame.mixer.music.play()
                    self.last_shot = now
                    self.n_bala -= 1
                    direcao = vec(1, 0).rotate(-self.rot)
                    tiro = Tiro(game, self.rect.center, direcao)
                    self.game.Tiros.add(tiro)
            
            #especiais!!
            if keys[pygame.K_q]:
                if self.n_bala > 0:
                    direcao = vec(1, 0).rotate(-self.rot)
                    tiro = Tiro(game, self.rect.center, direcao)
                    self.game.Tiros.add(tiro)

            if keys[pygame.K_e]:
                now = pygame.time.get_ticks()
                if now - self.last_shot > RATE_ESPECIAL_GUN and self.n_bala > 0:
                    self.n_bala -= 1
                    self.last_shot = now
                    direcao = vec(1, 0).rotate(-self.rot)
                    tiro = Tiro(game, self.rect.center, direcao)
                    tiro.image = pygame.Surface((25, 25))
                    tiro.image.fill((255,0,0))
                    tiro.ESPECIAL = True
                    self.game.Tiros.add(tiro)


    def update(self):
        self.keys()   #movimentação
        
        #rotacionar
        self.rot = (self.rot + self.rot_speed) % 360
        self.image = pygame.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel
        
        #verificar colisão
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.wall_list, 'x', False)
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.wall_list, 'y', False)
        self.rect.center = self.hit_rect.center

        #mostrar vida
        self.imglife = pygame.Surface((self.life*2, 5))
        self.imglife.fill((20,20,255))
        self.rectlife = self.imglife.get_rect()
        self.rectlife.centerx = self.rect.centerx
        self.rectlife.centery = self.rect.centery - 30

class Tiro(pygame.sprite.Sprite):
    def __init__(self, game, position, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = TIRO_IMG
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        self.ESPECIAL = False
        self.velocity = direcao * SPEED_GUN
        
        self.pos = (position[0]+5, position[1]+8)
        self.rect.center = position
        self.spawn_time = pygame.time.get_ticks()
        
    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > LIFE_GUN:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, IMG, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = IMG
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
class Bloco(pygame.sprite.Sprite):
    def __init__(self, game, IMG, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Zumbi(pygame.sprite.Sprite):
    def __init__(self, game, IMG, x, y, boo):
        pygame.sprite.Sprite.__init__(self)
        self.IMG = IMG
        self.game = game
        self.image = IMG
        self.rect = self.image.get_rect()

        self.last_hit = 0
        self.boo = boo
        
        self.hit_rect = ZUMBI_WALL_HIT_RECT.copy()                   
        self.hit_rect.center = self.rect.center
        
        self.hit_rect_hit = ZUMBI_HIT_RECT.copy()
        
        self.SPEED_ZUMBI = SPEED_ZUMBI
        self.vel = vec(0, 0)
        self.aux_vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rect.center = self.pos

        self.rot = 0

        #life
        self.life = 30
        
        self.imglife = pygame.Surface((self.life*2, 5))
        self.imglife.fill((RED))
        self.rectlife = self.imglife.get_rect()
        self.rectlife.centerx = self.rect.centerx
        self.rectlife.centery = self.rect.centery - 30

    def update(self):
        #rotacionar e mover
        self.rot = (self.game.Player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pygame.transform.rotate(self.IMG, self.rot)
        self.rect = self.image.get_rect()
        self.move()
        self.rect.center = self.pos
        
        #collidir com paredes
        self.hit_rect.centerx = self.pos.x
        self.hit_rect_hit.centerx = self.pos.x
        collide_with_walls(self, self.game.wall_list, 'x', self.boo)
        collide_with_walls(self, self.game.wall_list, 'x', self.boo)
        self.hit_rect.centery = self.pos.y
        self.hit_rect_hit.centery = self.pos.y
        collide_with_walls(self, self.game.wall_list, 'y', self.boo)
        collide_with_walls(self, self.game.wall_list, 'y', self.boo)
        
        self.rect.center = self.hit_rect.center

        #life update
        self.imglife = pygame.Surface((self.life*2, 5))
        self.imglife.fill((RED))
        self.rectlife = self.imglife.get_rect()
        self.rectlife.centerx = self.rect.centerx
        self.rectlife.centery = self.rect.centery - 30

        #kill player
        if self.game.Player.rect.x in range(self.rect.x, self.rect.x+self.hit_rect.width) and self.game.Player.rect.y in range(self.rect.y, self.rect.y+self.hit_rect.height):
            now = pygame.time.get_ticks()
            if now - self.last_hit > RATE_HIT_ZUMBI:
                if self.game.Player.life > 0:
                    self.game.Player.life -= 10
                    self.last_hit = now
                if self.game.Player.life == 0:
                    self.game.Player.mover = False
                    self.game.perdeu = True
        #tiro kill zumbi
        for tiro in self.game.Tiros:
            if tiro.rect.x in range(self.rect.x, self.rect.x+self.hit_rect_hit.width) and tiro.rect.y in range(self.rect.y, self.rect.y+self.hit_rect_hit.height):
                self.life -= 10
                if self.life == 0:
                    som_zumbi_death = os.path.join(arquivos_folder, 'hurt_death.mp3')
                    pygame.mixer.music.load(som_zumbi_death)
                    pygame.mixer.music.set_volume(1.4)
                    pygame.mixer.music.play()
                    self.kill()
                    self.game.score += 1
                    
                tiro.kill()

    def move(self):
        self.aux_vel = vec(self.SPEED_ZUMBI, 0).rotate(-self.rot)
        self.aux_vel += self.vel * -1
        self.vel += self.aux_vel
        self.pos += self.vel +0.5*self.aux_vel

class Itens:
    class BALA_20(pygame.sprite.Sprite):
        def __init__(self, game, IMG, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.game = game
            self.image = IMG
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            #se o player pegar o item +20
            if self.game.Player.rect.centerx in range(self.rect.x, self.rect.x+tamanho) and self.game.Player.rect.centery in range(self.rect.y, self.rect.y+tamanho):
                self.game.Player.n_bala += 20
                self.kill()

class Bosses:
    class Spawn_boss_speed:
        def __init__(self, game):
            self.game = game
            boss = Zumbi(self.game, BOSSES['speed'], 29*tamanho, 50*tamanho, True)
            boss.hit_rect = BOSS_SPEED_HIT_RECT.copy()
            boss.SPEED_ZUMBI = 1.2
            boss.life = 220
            boss.hit_rect_hit = BOSS_SPEED_HIT_RECT_HIT.copy()
            self.game.Zumbis.add(boss)
            self.game.contador = 1
        
    class Spawn_boss_vida:
        def __init__(self, game):
            self.game = game
            boss = Zumbi(self.game, BOSSES['life'], 63*tamanho, 65*tamanho, True)
            boss.hit_rect = BOSS_LIFE_HIT_RECT.copy()
            boss.SPEED_ZUMBI = 1.05
            boss.life = 600
            boss.hit_rect_hit = BOSS_LIFE_HIT_RECT_HIT.copy()
            self.game.Zumbis.add(boss)
            self.game.contador = 1

#diminuir if's do tilemap
class automatize:
    def __init__(self, game, func, img, group, x, y):
        self.game = game
        bloco = func(self.game, img, x*tamanho/2, y*tamanho)
        group.add(bloco)
