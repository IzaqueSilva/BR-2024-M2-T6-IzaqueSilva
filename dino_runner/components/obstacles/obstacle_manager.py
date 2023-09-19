from dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE, SCREEN_WIDTH, SCREEN_HEIGHT, AUDIOS
import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        obstacle_type = [
            Cactus(),
            Bird(),
        ]

        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[random.randint(0,1)])

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    # responsável por fazer morrer
                    AUDIOS['death'].play()
                    pygame.mixer.music.stop()
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                else:
                    # aqui ele tem power up
                    AUDIOS['critical'].play()

                    if game.player.type == SHIELD_TYPE:
                        obstacle.is_dead = True
                        pass
                    elif game.player.type == HAMMER_TYPE:
                        self.obstacles.remove(obstacle)

    def draw(self, screen, game_speed):
        for obstacle in self.obstacles:
            if obstacle.is_dead:
                obstacle.rect.x += game_speed + 50
                obstacle.rect.y -= 50
            
            if obstacle.rect.x > SCREEN_WIDTH or obstacle.rect.y < 0:
                self.obstacles.remove(obstacle)
                continue
                
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []