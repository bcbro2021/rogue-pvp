import pygame, sys, os
from pygame.locals import *
from .settings import *
from .player import *
from .assets import *
from .client import *
from .helper import *
from .text import *
import json

class Game:
    def __init__(self):
        # window
        self.win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        pygame.display.set_caption(WIN_TITLE)
        self.clock = pygame.time.Clock()

        # multiplayer stuff
        self.id = sys.argv[1]
        self.client = Client("127.0.0.1", 1234, 1234, int(sys.argv[2]))
        self.rooms = self.client.get_rooms()
        self.uuid = self.client.register()
        self.client.autojoin()

        self.update_capacity = 10

        # map
        self.text_map = self.client.get_map()
        # converting text map to game map
        self.game_map = create_game_map_from_text(self.text_map)

        # map tiles
        self.water, self.tiles = load_map_tiles(self.game_map,grass_imgs,water_img)
        self.bushes_data = self.client.get_bushes()
        self.bushes = generate_deco(self.bushes_data,bush_img)

        # collidable tiles
        self.ctiles = self.water

        # player puppets
        self.players = {}
        self.player_datas = {}

        # player
        self.player = Player(1644,1132, player_idle[0])
        self.player.id = self.id

        # every objects
        self.objs = []

    def draw(self):
        #(95,205,228)
        self.win.fill((0,0,0))

        # drawing map
        for tile in self.tiles:
            if tile.rect.colliderect(self.player.render_collider):
                tile.draw(self.win,self.player.scroll)
        
        for water in self.water:
            if water.rect.colliderect(self.player.render_collider):
                water.draw(self.win,self.player.scroll)

        # draw objs
        for obj in sorted(self.objs,key = lambda sprite: sprite.rect.centery):
            obj.draw(self.win,self.player.scroll) # other objs like bushes

    def send_player_data(self):
        data = {"id": self.id, 
                "x": self.player.rect.x, 
                "y": self.player.rect.y,
                "current_anim": self.player.animator.current_anim,
                "frame": self.player.animator.frame,
                "uuid": self.uuid,
                "health": self.player.health,
                "damage": self.player.damage,
                "attack": self.player.attack}
        self.client.send(data)

    def update(self):
        #reset the objs
        self.objs = []
    
        self.player.update(self.ctiles)
        

        # data to be sent
        self.send_player_data()

        # get data from other clients
        messages = self.client.get_messages()
        if len(messages) != 0:
            for message in messages:
                message = json.loads(message)
                for key, item in message.items():
                    # gettings the puppet of the other players
                    data = message[key]

                    # set the data for the players
                    if data["id"] != self.id:
                        self.player_datas[data["id"]] = data

                    if data["id"] != self.id:
                        self.players[data["id"]] = Entity(self.player_datas[data["id"]]["x"],
                                                        self.player_datas[data["id"]]["y"])
                        self.players[data["id"]].id = data["id"]
                    
                    # animating the other players using the local player frames
                    if data["id"] != self.id:
                        self.players[data["id"]].img = self.player.animator.animations[self.player_datas[data["id"]]["current_anim"]][self.player_datas[data["id"]]["frame"]]
            
        # update the objs
        for key in self.players: # delete player from players dictionary if dead
            if self.player_datas[key]["health"] <= 0:
                del self.players[key]
                del self.player_datas[key]
                break

        multi_players = []
        for key in self.players:
            multi_players.append(self.players[key])
        
        if self.player.health > 0: # only add player to the objs group if alive
            self.objs.append(self.player)
        self.objs.extend(multi_players)
        self.objs.extend(self.bushes)

        # player damage and attack system
        for key in self.players:
            if self.player.rect.colliderect(self.players[key].rect):
                if self.player_datas[key]["attack"]:
                    self.player.health -= self.player_datas[key]["damage"]

    def events(self,event):
        if event.type == QUIT:
            self.player.health = 0
            for x in range(5): # sending it multiple times just to make sure the other clients get the message
                self.send_player_data()
            self.client.leave_room()
            pygame.quit()
            os._exit(1)

        # this allows the player to attack other players
        self.player.attack_event(event)