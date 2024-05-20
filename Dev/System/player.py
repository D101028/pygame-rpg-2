import pygame 

from entity import Entity
from settings import *
from support import import_folder

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, status: str
            #   create_attack,destroy_attack,create_magic
                ):
        super().__init__(groups)
        status = status.replace("_idle", "")
        self.image = pygame.image.load('../Graphics/test/player.png').convert_alpha()
        self.image = pygame.image.load(f'../Graphics/player/{status}/{status}_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

        # graphics setup
        self.import_player_assets()
        self.status = status

        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats = {'speed': 5}

        self.is_keyboard_forbidden = False

    def import_player_assets(self):
        character_path = '../Graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        # if not self.attacking:
        if not self.is_keyboard_forbidden:
            keys = pygame.key.get_pressed()

            # run
            if keys[pygame.K_LSHIFT]:
                self.stats['speed'] = 8
            else:
                self.stats['speed'] = 5

            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            # if not 'idle' in self.status and not 'attack' in self.status:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'

        # if self.attacking:
        #     self.direction.x = 0
        #     self.direction.y = 0
        #     if not 'attack' in self.status:
        #         if 'idle' in self.status:
        #             self.status = self.status.replace('_idle','_attack')
        #         else:
        #             self.status = self.status + '_attack'
        # else:
        #     if 'attack' in self.status:
        #         self.status = self.status.replace('_attack','')

    def animate(self):
        animation = self.animations[self.status]
        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker 
        # if not self.vulnerable:
        #     alpha = self.wave_value()
        #     self.image.set_alpha(alpha)
        # else:
        #     self.image.set_alpha(255)

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])