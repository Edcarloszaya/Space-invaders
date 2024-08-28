import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT ,MUSIC_END,MUSIC_GAME,MUSIC_WON
from player import Bullet, Player
from enemy import EnemyManager
from game import Game


def Game_main():
    pygame.init()

    pygame.mixer.init()
    pygame.mixer_music.load(MUSIC_GAME)
    pygame.mixer_music.play(-1)

    sound_end = pygame.mixer.Sound(MUSIC_END)
    sound_end.set_volume(0.2)

    sound_win = pygame.mixer.Sound(MUSIC_WON)
    sound_win.set_volume(0.2)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()

    player = Player(370, 535)
    bullet = Bullet(player.rect.x, player.rect.y)
    enemies_manager = EnemyManager(250, 200, 10, 15, 30, 40)
    game_manager = Game(player)
    


    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

                # verifica se player atirou
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not bullet.active:
                        bullet.fire( player)

            # verefica event game over
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_manager.check_click(mouse_pos,game_manager.botton_play_again):
                    pygame.quit()
                elif game_manager.check_click(mouse_pos,game_manager.botton_quit):
                    Game_main()
                    sound_end.stop()
                    sound_win.stop()


        screen.fill("black")

        # desenha os objetos
        game_manager.draw(screen)
        player.draw(screen)
        bullet.draw(screen)
        enemies_manager.draw(screen)

        # inimigos se move
        enemies_manager.move()

        # inimigos atira
        enemies_manager.fire()

        

        # verifica se teve colisao com player
        if game_manager.player_collision(player, enemies_manager.all_rockets_big):
            player.reset()
        player.update()

        if game_manager.player_collision(player, enemies_manager.all_rockets_small):
            player.reset()
        player.update()

        if game_manager.player_collision(player, enemies_manager.all_rockets_small_top):
            player.reset()
        player.update()

        # verifica colisao com enimigo
        if game_manager.enemies_collision(
            enemies_manager.all_enemies_big, bullet, game_manager.big_points
        ):

            bullet.reset(player)

        elif game_manager.enemies_collision(
            enemies_manager.all_enemies_small, bullet, game_manager.small_points
        ):
            bullet.reset(player)

        elif game_manager.enemies_collision(
            enemies_manager.boss, bullet, game_manager.boss_points
        ):
            bullet.reset(player)

        elif game_manager.enemies_collision(
            enemies_manager.all_enemies_small_top, bullet, game_manager.small_points
        ):
            bullet.reset(player)

        # atualiza tiro
        bullet.fire_update()

        # verifica tiro
        bullet.ckeck_fire(player)

        # verifica movimento do player
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player.move_left()

        elif keys[pygame.K_d]:
            player.move_right()
        
        # verifica se o o game acabou
        if game_manager.player_life  == 0:
            game_manager.game_end(screen,"You Lost")
            enemies_manager.clear_all_enemies()
            pygame.mixer_music.stop()
            sound_end.play()
             
        elif game_manager.player_score  == 660:
            game_manager.game_end(screen,"You Won")
            pygame.mixer_music.stop()
            sound_win.play()
            
            
            

        pygame.display.flip()

        clock.tick(144)

    pygame.quit()

# inicia o game 
Game_main()