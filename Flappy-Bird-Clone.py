import pygame, sys, random
from random import randint

pygame.init()

screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption('Flappy')
clock = pygame.time.Clock()

#background
ground_surface = pygame.image.load('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/sprites/base.png')
ground_surface = pygame.transform.scale2x(ground_surface)
background_surface = pygame.image.load('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/sprites/background-day.png')
background_surface_height = background_surface.get_height()
background_surface = pygame.transform.scale(background_surface, (500, background_surface_height))

def get_score():
        global current_time, start_time     
        current_time = pygame.time.get_ticks() - start_time
        return round(current_time/1000)

def bird_animation(bird_animation_surface_list):
        global bird_index
        bird_index += 0.1      
        if bird_index > 1:
            bird_index = 0
        if bird_surface_downflap_rect.y <= -100:
                game_active = False
        if bird_surface_downflap_rect.y >= 310:
                game_active = False        
        return bird_animation_surface_list[round(bird_index)]
    
def pipe_movement(pipe_rect_list):
    global pipe_speed     
    if pipe_rect_list:
        for rect in pipe_rect_list:
            screen.blit(pipe_surface_bottom, rect)
            rect.x -= 5 + pipe_speed
        pipe_rect_list = [obstacle for obstacle in pipe_rect_list if rect.x >= -50]
        return pipe_rect_list
    else:
        return []

def upper_pipe_movement(upper_pipe_rect_list):
    if upper_pipe_rect_list:
        for rect in upper_pipe_rect_list:
            screen.blit(pipe_surface_upper, rect)
            rect.x -= 5 + pipe_speed
        upper_pipe_rect_list = [obstacle for obstacle in upper_pipe_rect_list if rect.x >= -50]
        return upper_pipe_rect_list
    else:
        return []

def pipe_collisons(bird_rect, pipe_rect_list, upper_pipe_rect_list):
        if pipe_rect_list or upper_pipe_rect_list:
                for rect in pipe_rect_list:
                        if rect.colliderect(bird_rect):
                                die_sound.play()
                                return False
                for rect in upper_pipe_rect_list:
                        if rect.colliderect(bird_rect):
                                die_sound.play()
                                return False                
        if bird_rect.bottom > 310 or bird_rect.y < -70:
                die_sound.play()
                return False
        return True  

def game_over_animation(game_over_text_rect_list):
        global game_over_text_index 
        game_over_text_index += 0.05
        if game_over_text_index > 1:
                game_over_text_index = 0
        return game_over_text_rect_list[round(game_over_text_index)]

#player
bird_surface_downflap = pygame.image.load('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/sprites/bluebird-downflap.png')
bird_surface_midflap = pygame.image.load('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/sprites/bluebird-upflap.png')
bird_surface_upflap = pygame.image.load('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/sprites/bluebird-downflap.png')

bird_surface_downflap_rect = bird_surface_downflap.get_rect(midbottom = (100, 180))
bird_animation_surface_list = [bird_surface_downflap, bird_surface_midflap]

#pipes
pipe_surface_bottom = pygame.image.load('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/sprites/pipe-green.png')
pipe_rect_list = []
pipe_surface_upper = pygame.image.load('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/sprites/pipe-red.png')
pipe_surface_upper = pygame.transform.rotate(pipe_surface_upper, 180)
upper_pipe_rect_list  = []

#score
test_font = pygame.font.Font('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/joystix/joystix monospace.ttf', 20)

#game over text
game_over_text_surface = pygame.image.load('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/sprites/gameover.png')
game_over_text_surface = pygame.transform.scale(game_over_text_surface, (290, 70))
game_over_text_surface_rect = game_over_text_surface.get_rect(center = (250, 200))
game_over_text_surface_rect_scaled = game_over_text_surface_rect.inflate(10, 10)
game_over_text_rect_list = [game_over_text_surface_rect, game_over_text_surface_rect_scaled]

#sound
die_sound = pygame.mixer.Sound('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/audio/point.wav')
wing_sound = pygame.mixer.Sound('/Users/priyanshurastogi/Downloads/Flappy-Bird-Clone-Pygame/audio/wing.wav')

#varibles
game_active = True
bird_index = 0
game_over_text_index = 0
gravity = 0
start_time = 0
pipe_speed = 0

#events
pipe_event = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_event, 1200)

upper_pipe_event = pygame.USEREVENT + 2
pygame.time.set_timer(upper_pipe_event, 1300)

while True:
    for e in pygame.event.get():
        
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if game_active:
                        wing_sound.play()
                gravity -= 6.5      
        if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                        if game_active == False:
                                game_active = True 
                                gravity = 0
                                pipe_speed = 0
                                pygame.time.delay(500)
                                bird_surface_downflap_rect.y = 100
                                start_time = pygame.time.get_ticks()
                                pipe_rect_list = []
                                upper_pipe_rect_list = []
        if e.type == pipe_event and game_active:
                num =  randint(0,2)
                if(num):
                        pipe_rect_list.append(pipe_surface_bottom.get_rect(midbottom = (randint(600, 2200), 525)))
                else:
                        upper_pipe_rect_list.append(pipe_surface_upper.get_rect(midbottom = (randint(600, 2200), 115)))
        
    if game_active:
        screen.blit(background_surface, (0,-100))
        
        bird_animation_surface = bird_animation(bird_animation_surface_list)
        screen.blit(bird_animation_surface, bird_surface_downflap_rect)
        
        #score
        score = get_score()
        text_surface = test_font.render('Score:'+str(score), None, 'Black')
        text_rect = text_surface.get_rect(midbottom = (250, 70))
        pygame.draw.rect(screen, '#ABEBC6', text_rect, 10)
        pygame.draw.rect(screen, '#ABEBC6', text_rect)
        screen.blit(text_surface, text_rect)
        
        #player physics
        gravity += 0.15
        bird_surface_downflap_rect.y += gravity
        
        #pipe
        if score%10 == 0:
                pipe_speed = pipe_speed + random.uniform(-0.01724137931, 0.03448275862)
        pipe_rect_list = pipe_movement(pipe_rect_list)
        upper_pipe_rect_list = upper_pipe_movement(upper_pipe_rect_list)
        game_active = pipe_collisons(bird_surface_downflap_rect, pipe_rect_list, upper_pipe_rect_list)
        
        screen.blit(ground_surface, (0, 310))
        
    else:
        screen.fill('#F7DC6F')
        game_over_animation_rect = game_over_animation(game_over_text_rect_list)
        screen.blit(game_over_text_surface, game_over_animation_rect)
        bird_animation_surface = bird_animation(bird_animation_surface_list)
        bird_animation_surface = pygame.transform.scale2x(bird_animation_surface)
        screen.blit(bird_animation_surface, (217, 50))
        text_surface = test_font.render('Press R to play/retry', None, 'Black')
        screen.blit(text_surface, (70, 300))
        
    pygame.display.update()
    clock.tick(50)