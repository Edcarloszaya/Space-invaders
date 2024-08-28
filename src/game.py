import pygame


class Game:

    def __init__(self, player) -> None:
        self.player_life = player.life
        self.player_score = player.score
        self.cor = "white"
        self.big_points = 30
        self.small_points = 20
        self.boss_points = 100
        self.x = 15
        self.y = 570
        self.score_x = 660

        # criar rect dos botton
        self.botton_quit = pygame.Rect(200,350,150,50)
        self.botton_play_again = pygame.Rect(500,350,100,50)


    def player_collision(self, player, list_rockts):
        collision_rocket = False

        for rocket in list_rockts:
            if pygame.sprite.collide_rect(player, rocket):
                collision_rocket = True
                list_rockts.remove_internal(rocket)
                break

        if collision_rocket:
            self.player_life -= 1
            return True
        else:
            return False

    def enemies_collision(self, list_enemies , bullet,points):
        
        collision_bullet = False
        
        for enemy in list_enemies :
            if pygame.sprite.collide_rect(enemy, bullet):
                collision_bullet = True
                list_enemies.remove_internal(enemy)
                break
        if collision_bullet:
            self.player_score += points
            return True
        else:
            return False

    def plate(self):
        font = pygame.font.Font(None, 36)
        life = font.render(str(f"life: {self.player_life}"), True, (self.cor))
        score = font.render(str(f"score:{ self.player_score}"), True, (self.cor))
        return life, score
   
    def check_life(self):
        if self.player_life == 0:
            return True

    def game_end(self,screen,msg):
       
        pygame.draw.rect(screen, (0,5,0), self.botton_quit,border_radius=25)
        pygame.draw.rect(screen, (0,5,0), self.botton_play_again,border_radius=25)

        font = pygame.font.Font(None, 36)
        text_play = font.render("Quit", True, (0,255,0))
        text_quit = font.render("Play Again", True, (0,255,0))
        msg_end = font.render(msg, True, (0,255,0))

        screen.blit(text_quit,(self.botton_quit.x + 15,self.botton_quit.y + 10))
        screen.blit(text_play,(self.botton_play_again.x + 15,self.botton_play_again.y + 10))
        screen.blit(msg_end,(350,150))
        
    def check_click(self,mouse_pos,botton):
        if botton.collidepoint(mouse_pos):
            return True

    def draw(self, screen):
        life_draw, score_draw = self.plate()
        screen.blit(life_draw, (self.x, self.y))
        screen.blit(score_draw, (self.score_x, self.y))
