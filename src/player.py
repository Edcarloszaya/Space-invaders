import pygame

from settings import PLAYER_IMG, PLAYER_SPEED, PLAYER_LASER


class Player:

    def __init__(self, x, y):

        self.image = pygame.image.load(PLAYER_IMG)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.initial_x = x
        self.initial_y = y
        self.life = 3
        self.speed = PLAYER_SPEED
        self.score = 0
        self.reset_delay = 1000
        self.start_time = 0
        self.is_resetting = False

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def reset(self):
        self.is_resetting = True
        self.start_time = pygame.time.get_ticks()
        self.rect.x = -100

    def update(self):
        if self.is_resetting:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.reset_delay:  # 1 segundos
                self.rect.x = self.initial_x
                self.rect.y = self.initial_y
                self.is_resetting = False


    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.laser_image = pygame.image.load(
            PLAYER_LASER
        )  # Substitua pelo caminho correto da imagem
        self.laser_image = pygame.transform.scale(self.laser_image, (5, 20))
        self.rect = self.laser_image.get_rect(topleft=(x,y))
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.active = False

    def fire(self, player):
        self.active = True
        self.rect.x =  player.rect.x + player.rect.width // 2 - self.rect.width // 2
        self.rect.y -= self.speed

    def fire_update(self):
        if self.active:
            self.rect.y -= 1.5

    def ckeck_fire(self,player):
        if self.rect.y <= 0:
            self.reset(player)


    def reset(self, player):
        self.active = False
        self.rect.x =  player.rect.x + player.rect.width // 2 - self.rect.width // 2
        self.rect.y =  player.rect.y + player.rect.height // 2 - self.rect.height // 2

    def draw(self, screen):
        if self.active:
            screen.blit(
                self.laser_image, self.rect.topleft
            )  # Desenha a imagem da bala na tela
