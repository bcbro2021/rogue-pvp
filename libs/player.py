from .entity import *
from .settings import *
from .animator import *
from .assets import player_idle

class Player(Entity):
    def __init__(self,x,y,img):
        super().__init__(x,y)
        self.img = img

        self.movement = [0,0]
        self.speed = 4

        # health stuff
        self.def_attack_cooldown = 10
        self.attack_cooldown = self.def_attack_cooldown
        self.def_attack_timer = 2
        self.attack_timer = self.def_attack_timer
        self.attack = False
        self.damage = 10
        self.def_health = 100
        self.health = self.def_health

        # animator
        self.animator = Anim_manager()
        self.animator.add_animation("idle",player_idle,delay=10)

        # render collider
        self.render_collider_size = (WIN_WIDTH+200,WIN_HEIGHT+200)
        self.render_collider = pygame.Rect(self.rect.x-self.render_collider_size[0]/2,
                                           self.rect.y-self.render_collider_size[1]/2,
                                           self.render_collider_size[0],
                                           self.render_collider_size[1])

    def draw(self,dis,scroll):
        dis.blit(self.animator.get_current_anim_frame(),(self.rect.x - scroll[0],self.rect.y - scroll[1]))
        #pygame.draw.rect(dis,(255,100,100),pygame.Rect(self.render_collider.x-self.scroll[0],(self.render_collider.y)-self.scroll[1],WIN_WIDTH,WIN_HEIGHT))

    def update(self,ctiles):
        keys = pygame.key.get_pressed()
        # update render collider
        self.render_collider.x = self.rect.x-self.render_collider_size[0]/2
        self.render_collider.y = self.rect.y-self.render_collider_size[1]/2

        # attack timer runout
        if self.attack:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attack = False
                self.attack_timer = self.def_attack_timer

        # attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # movement
        self.movement = [0,0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement[0] -= self.speed
        if keys[pygame.K_d]:
            self.movement[0] += self.speed
        if keys[pygame.K_w]:
            self.movement[1] -= self.speed
        if keys[pygame.K_s]:
            self.movement[1] += self.speed

        _ = self.move(ctiles)

        self.animator.play_animation("idle")

        # camera movement
        self.scroll[0] += (self.rect.x-self.scroll[0]-(WIN_WIDTH/2-self.rect.width/2))//20
        self.scroll[1] += (self.rect.y-self.scroll[1]-(WIN_HEIGHT/2-self.rect.height/2))//20

    def get_collided_tiles(self,tiles):
        collided_tiles = []
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                collided_tiles.append(tile)

        return collided_tiles

    def move(self,tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        self.rect.x += self.movement[0]
        collided_tiles = self.get_collided_tiles(tiles)
        for tile in collided_tiles:
            if self.movement[0] > 0:
                self.rect.right = tile.rect.left
                collision_types['right'] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.rect.right

        self.rect.y += self.movement[1]
        collided_tiles = self.get_collided_tiles(tiles)
        for tile in collided_tiles:
            if self.movement[1] > 0:
                self.rect.bottom = tile.rect.top
                collision_types['bottom'] = True
            if self.movement[1] < 0:
                self.rect.top = tile.rect.bottom
                collision_types['top'] = True
        
        return collision_types

    def attack_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.attack_cooldown <= 0:
                self.attack = True
                self.attack_cooldown = self.def_attack_cooldown