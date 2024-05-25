import pygame

from settings import *
from support import crop_img, fill_chr

class AnimationBlock(pygame.sprite.Sprite):
    def __init__(self, pos, groups, 
                 animation_id: int = None, file_path: str = None, 
                 animation_speed: float = 0.15, 
                 unit_move_route: list[tuple[float, float]] | None = None, interval: int = 60, loop: int = -1):
        """interval: frames of moving between two points"""
        if unit_move_route is None:
            unit_move_route = []

        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.name = fill_chr(str(animation_id)) if animation_id is not None else None
        self.size = ANIMATION_BLOCK_SIZE_LIST[animation_id]

        # graphics setup
        self.import_graphics(file_path)
        self.image = self.animations[self.frame_index]
    
        # movement
        y_offset = -int(self.size[1] * 0.3125) if self.size[1] <= 128 else -int(self.size[1] * 0.5)
        x_offset = 0 if self.size[0] <= 128 else -int(self.size[0] * 0.3)
        # self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(bottomleft = (pos[0], pos[1] + TILESIZE))
        self.hitbox = self.rect.inflate(x_offset, y_offset)
        self.unit_move_route: list[tuple[float, float]] = unit_move_route
        self.interval = interval
        self.interval_count = 0

        self.remain_loop = loop
        self.is_loop_over = False
        self.paused = False

        self.pos_num = 0
        self.last_pos = None
        self.next_pos = None
        self.percentage = 0
        

    def import_graphics(self, filepath: str = None):
        if filepath is None:
            filepath = f"../Graphics/animations/{self.name}.png"
        self.animations = crop_img(filepath, self.size[0], self.size[1])

    def set_pos(self, pos):
        self.rect.bottomleft = (pos[0], pos[1])
        self.hitbox.center = self.rect.center

    def move(self):
        if len(self.unit_move_route) == 0 or self.is_loop_over or self.paused:
            return 
        if self.last_pos is None:
            self.last_pos = pygame.Vector2(self.rect.bottomleft)
            self.next_pos = pygame.Vector2(self.unit_move_route[self.pos_num]) * TILESIZE
        
        self.interval_count += 1
        if self.interval_count >= self.interval:
            self.interval_count = 0
            self.percentage = 0
            self.pos_num += 1
            if self.pos_num >= len(self.unit_move_route):
                if self.remain_loop != 0:
                    self.remain_loop -= 1
                    self.pos_num = 0
                else:
                    self.is_loop_over = True
                    return 
            self.last_pos = pygame.Vector2(self.rect.bottomleft)
            unit_pos = self.unit_move_route[self.pos_num]
            self.next_pos = pygame.Vector2((unit_pos[0], unit_pos[1] + 1)) * TILESIZE
        
        self.percentage = self.interval_count / self.interval

        pos = self.last_pos * (1-self.percentage) + self.next_pos * self.percentage
        self.set_pos(pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
        self.image = self.animations[int(self.frame_index)]

    def update(self):
        self.animate()
        self.move()


