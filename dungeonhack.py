import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Item:
    def __init__(self, name, item_type, effect=None):
        self.name = name
        self.type = item_type
        self.effect = effect

class LightSource:
    def __init__(self, scene, x, y, radius):
        self.scene = scene
        self.x = x
        self.y = y
        self.radius = radius

class Entity:
    def __init__(self, scene, x, y, char, color=WHITE):
        self.scene = scene
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.lastMoveTime = 0
        self.stats = {
            'hp': 100
        }

    def draw(self, screen):
        font = pygame.font.Font(None, TILE_SIZE)
        text = font.render(self.char, True, self.color)
        screen.blit(text, (self.x * TILE_SIZE, self.y * TILE_SIZE))

class Player(Entity):
    def __init__(self, scene, x, y, char='@', color=WHITE):
        super().__init__(scene, x, y, char, color)
        self.inventory = []
        self.equipped = {
            'weapon': None,
            'armor': None
        }

    def removeItem(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def useItem(self, item, target):
        if self.removeItem(item):
            item.effect(target)
            return True
        return False

    def equipItem(self, item):
        if item.type == 'weapon':
            if self.equipped['weapon']:
                self.inventory.append(self.equipped['weapon'])
            self.equipped['weapon'] = item
        elif item.type == 'armor':
            if self.equipped['armor']:
                self.inventory.append(self.equipped['armor'])
            self.equipped['armor'] = item
        self.removeItem(item)

class Monster(Entity):
    def __init__(self, scene, x, y, char='M', color=WHITE):
        super().__init__(scene, x, y, char, color)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeonhack")
        self.clock = pygame.time.Clock()
        self.scene = []
        self.player = Player(self.scene, 5, 5)
        self.monsters = [Monster(self.scene, random.randint(0, 24), random.randint(0, 18)) for _ in range(5)]
        self.light_sources = [LightSource(self.scene, 5, 5, 5)]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(BLACK)
            self.player.draw(self.screen)
            for monster in self.monsters:
                monster.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()