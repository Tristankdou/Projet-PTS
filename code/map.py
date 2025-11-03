import pygame
import pytmx #importer la bibliothèque pytmx pour charger les cartes au format tmx
import pyscroll #importer la bibliothèque pyscroll pour afficher les cartes tmx

from screen import Screen
from player import Player

class Map: #créer une classe map qui contient l'écran sur lequel on affiche tout
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None #variable qui contient les données de la carte
        self.map_layer = None
        self.group = None

        self.switch_map("map_0")
        self.player : Player = None

    def switch_map(self, map: str): #fonction qui permet de changer de carte
        self.tmx_data = pytmx.load_pygame(f"../assets/map/{map}.tmx") #charger les données de la carte
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 3  # définir le niveau de zoom de la carte
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

    def add_player(self, player): #fonction qui ajoute le joueur à la carte
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()

    def update(self): #fonction qui met à jour l'affichage de la carte
        self.group.update()
        self.group.center(self.player.rect.center) #centrer la carte sur le joueur
        self.group.draw(self.screen.get_display())