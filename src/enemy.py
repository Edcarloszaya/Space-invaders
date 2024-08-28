import pygame
from time import sleep

from settings import ENEMY_1, BOOS, ROCKET, ENEMY_2


class EnemyBig(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        # Carregar a imagem do inimigo (uma vez por gerenciador)
        self.image = pygame.image.load(ENEMY_1)
        self.ajust_width = 7
        self.ajust_hight = 3
        self.image = pygame.transform.scale(
            self.image,
            (
                (width + self.ajust_width),
                (height + self.ajust_hight),
            ),  # Ajustar o tamanho da imagem
        )
        self.rect = self.image.get_rect(topleft=(x, y))


class EnemySmall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        # Carregar a imagem do inimigo (uma vez por gerenciador)
        self.image = pygame.image.load(ENEMY_2)
        self.image = pygame.transform.scale(
            self.image, (width, height)
        )  # Ajustar o tamanho da imagem
        self.rect = self.image.get_rect(topleft=(x, y))


class EnemySmallTop(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        # Carregar a imagem do inimigo (uma vez por gerenciador)
        self.image = pygame.image.load(ENEMY_2)
        self.image = pygame.transform.scale(
            self.image, (width, height)
        )  # Ajustar o tamanho da imagem
        self.rect = self.image.get_rect(topleft=(x, y))


class EnemyBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(BOOS)
        self.ajust_width = 40
        self.ajust_hight = 42
        self.image = pygame.transform.scale(
            self.image, ((width + self.ajust_width), (height + self.ajust_hight))
        )
        self.rect = self.image.get_rect(topleft=(x, y))


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load(ROCKET)
        self.image = pygame.transform.scale(self.image, (5, 25))
        self.rect = self.image.get_rect(topleft=(x, y))


class EnemyManager():
    def __init__(self, start_x, start_y, spacing_x, spacing_y, width, height):

        # Grupo para armazenar os inimigos
        self.all_enemies_small = pygame.sprite.Group()
        self.all_enemies_small_top = pygame.sprite.Group()
        self.all_enemies_big = pygame.sprite.Group()  
        self.boss = pygame.sprite.Group()

        # Grupo para armazenar os rockets
        self.all_rockets_big = pygame.sprite.Group()
        self.all_rockets_small = pygame.sprite.Group()
        self.all_rockets_small_top = pygame.sprite.Group()

        # posicao na telA
        self.start_x = start_x
        self.start_y = start_y
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.width = width
        self.height = height
        self.ajust_x = 3

        #  tempo do ultimo desparo de cada
        self.last_fire_time = pygame.time.get_ticks()
        self.last_fire_time_small = pygame.time.get_ticks()
        self.last_fire_time_small_top = pygame.time.get_ticks()

        # intervalo de disparo
        self.fire_delay = 3300
        # verifica estado pra limpa a tela
        self.clean_screen = True

        # direcao de cada objeto
        self.direction = 1
        self.speed = 1
        self.boss_direction = 1

        # cria enimigos
        self.create_enemies_big()
        self.create_enemies_small()
        self.create_enemies_small_top()
        self.create_all_boss()
        

    def create_enemies_big(self):
        for i in range(8):
            x = (self.start_x - self.ajust_x) + i * (self.width + self.spacing_y)
            y = self.start_y
            enemy_ = EnemyBig(
                x, y, self.width, self.height
            )  # Passar largura e altura para o Enemy
            self.all_enemies_big.add_internal(enemy_)

    def create_enemies_small(self):
        for col in range(8):
            for row in range(1):
                x = self.start_x + col * (self.width + self.spacing_y)
                y = (self.start_y - 50) + row * (self.height + self.spacing_x)
                enemy_ = EnemySmall(
                    x, y, self.width, self.height
                )  # Passar largura e altura para o Enemy
                self.all_enemies_small.add_internal(enemy_)

    def create_enemies_small_top(self):

        for col in range(8):
            for row in range(1):
                x = self.start_x + col * (self.width + self.spacing_y)
                y = (self.start_y - 100) + row * (self.height + self.spacing_x)
                enemy_ = EnemySmallTop(
                    x, y, self.width, self.height
                )  # Passar largura e altura para o Enemy
                self.all_enemies_small_top.add_internal(enemy_)

    def create_all_boss(self):
        x = self.start_x - 250
        y = self.start_y - 195
        width = 40
        height = 15
        boss = EnemyBoss(x, y, width, height)
        self.boss.add_internal(boss)

    def enemies_create_rocket(self, list_rockets, list_enemies):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_fire_time >= self.fire_delay:
            for enemy1 in list_enemies:
                x = enemy1.rect.x
                y = enemy1.rect.y
                new_rocket = Rocket(x, y)
                list_rockets.add_internal(new_rocket)

            self.last_fire_time = current_time

    def enemies_create_rocket_small(self, list_enemies, list_enemies_2, list_rockets):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_fire_time_small >= self.fire_delay:
            for enemy1 in list_enemies:
                free = True
                for enemy2 in list_enemies_2:
                    if abs(enemy1.rect.centerx - enemy2.rect.centerx) <= 15:
                        free = False
                        break
                if free:
                    x = enemy1.rect.x
                    y = enemy1.rect.y
                    new_rocket = Rocket(x, y)
                    list_rockets.add_internal(new_rocket)

            self.last_fire_time_small = current_time

    def enemies_create_rocket_small_top(self, list_enemies, list_enemies_2, list_rockets):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_fire_time_small_top >= self.fire_delay:
            for enemy1 in list_enemies:
                free = True
                for enemy2 in list_enemies_2:
                    if abs(enemy1.rect.centerx - enemy2.rect.centerx) <= 15:
                        free = False
                        break
                if free:
                    x = enemy1.rect.x
                    y = enemy1.rect.y
                    new_rocket = Rocket(x, y)
                    list_rockets.add_internal(new_rocket)

            self.last_fire_time_small_top = current_time

    def enemies_fire(self, list_rockts):
        for rocket in list_rockts:
            rocket.rect.y += self.speed

    def enemies_update_fire(self, list_rockts):
        for rocket in list_rockts:
            if rocket.rect.y >= 600:
                list_rockts.remove_internal(rocket)

    def fire(self):

        # cria
        self.enemies_create_rocket(self.all_rockets_big, self.all_enemies_big)
        self.enemies_create_rocket_small(

            self.all_enemies_small, 
            self.all_enemies_big, 
            self.all_rockets_small,
            
        )
        self.enemies_create_rocket_small_top(

            self.all_enemies_small_top,
            self.all_enemies_small,
            self.all_rockets_small_top,
            
        )

        # atira
        self.enemies_fire(self.all_rockets_big)
        self.enemies_fire(self.all_rockets_small)
        self.enemies_fire(self.all_rockets_small_top)

        # atualiza
        self.enemies_update_fire(self.all_rockets_big)
        self.enemies_update_fire(self.all_rockets_small)
        self.enemies_update_fire(self.all_rockets_small_top)

    def move(self):

        #   se movem
        self.move_enemies(self.all_enemies_big)
        self.move_enemies(self.all_enemies_small)
        self.move_enemies(self.all_enemies_small_top)
        self.move_boss(self.boss)

        # atualiza movimento

        self.move_enemies_update(self.all_enemies_big)
        self.move_enemies_update(self.all_enemies_small)
        self.move_enemies_update(self.all_enemies_small_top)
        self.move_boss_update(self.boss)

    def move_enemies(self, list_enemies):

        for enemy in list_enemies:
            enemy.rect.x += self.direction

    def move_enemies_update(self, list_enemies):

        for enemy in list_enemies:
            if enemy.rect.x <= 0:
                self.direction = 1
                break

            if enemy.rect.x >= 760:
                self.direction = -1
                break

    def move_boss(self, list_boss):
        for boss in list_boss:
            boss.rect.x += self.boss_direction
            
    def move_boss_update(self, list_boss):

        for boss in list_boss:
            if boss.rect.x <= -600:
                self.boss_direction = 1

            if boss.rect.x >= 1060:
                self.boss_direction = -1

    def kill_enemies(self,list_enemies):
        for enemy in list_enemies:
            list_enemies.remove_internal(enemy)

    def clear_all_enemies(self):

        if self.clean_screen:
            self.kill_enemies(self.all_enemies_small)
            self.kill_enemies(self.all_enemies_small_top)
            self.kill_enemies(self.all_enemies_big)
            self.kill_enemies(self.boss)
                
        self.clean_screen = False

    def draw(self, screen):
        self.all_enemies_big.draw(screen)
        self.all_enemies_small.draw(screen)
        self.all_enemies_small_top.draw(screen)
        self.boss.draw(screen)
        self.all_rockets_big.draw(screen)
        self.all_rockets_small.draw(screen)
        self.all_rockets_small_top.draw(screen)
