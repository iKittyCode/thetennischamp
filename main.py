import pygame
import time
pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("The Championships")
clock = pygame.time.Clock()
running = True

game_state = "start_menu"
start_menu_image = pygame.image.load("images/startscreen.png")
fedimage = pygame.image.load("images/ezgif-split/tile000.png")
fedimage = pygame.transform.scale(fedimage, (128, 128))
rafaimage = pygame.image.load("images/ezgif-split/tile009.png")
rafaimage = pygame.transform.scale(rafaimage, (128, 128))
novakimage = pygame.image.load("images/ezgif-split/tile005.png")
novakimage = pygame.transform.scale(novakimage, (128, 128))

font = pygame.font.Font("fonts/PixelifySans-Regular.ttf", 48)

last_move_time = 0
move_delay = 200 
fedchoose_x = -fedimage.get_width()
fedchoose_y = 150
fedchooseslide_target_x = 60
slide_speed = 5
rafachoose_x = -rafaimage.get_width()
rafachoose_y = 155
rafachooseslide_target_x = 236
novakchoose_x = -novakimage.get_width()
novakchoose_y=151
novakchooseslide_target_x = 418
selected_index = 0  

characters = [
    {"image": fedimage, "x": lambda: fedchoose_x, "y": fedchoose_y},
    {"image": rafaimage, "x": lambda: rafachoose_x, "y": rafachoose_y},
    {"image": novakimage, "x": lambda: novakchoose_x, "y": novakchoose_y}
]
class Player(charachter): 
    def __init__(self, pos_x, pos_y): 
        

def draw_start_menu():
    screen.blit(start_menu_image, (0, 0))
    pygame.display.update()

def slideon(image, current_x, target_x, y, speed):
    if current_x < target_x:
        current_x += speed
        if current_x > target_x:
            current_x = target_x
    screen.blit(image, (current_x, y))
    return current_x
def gameplay(): 
    screen.fill((0,0,0))
    screen.blit(pygame.image.load("images/gamebackground.png"), (0,0))
    pygame.display.update()

def draw_choose_menu():
    screen.fill((195, 230, 158))
    text_surface = font.render("CHOOSE YOUR CHARACHTER", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(600 // 2, 30))
    screen.blit(text_surface, text_rect)

    
    global fedchoose_x, rafachoose_x, novakchoose_x
    fedchoose_x = slideon(fedimage, fedchoose_x, fedchooseslide_target_x, fedchoose_y, 5)
    
    rafachoose_x = slideon(rafaimage, rafachoose_x, rafachooseslide_target_x, rafachoose_y, slide_speed)
    novakchoose_x = slideon(novakimage, novakchoose_x, novakchooseslide_target_x,novakchoose_y, 5)
    sel = characters[selected_index]
    sel_rect = pygame.Rect(sel["x"](), sel["y"], 128, 128)
    pygame.draw.rect(screen, (255, 255, 0), sel_rect.inflate(10, 10), 4)
    pygame.display.update()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "start_menu":
            draw_start_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_state = "choose_menu"
        

    if game_state == "choose_menu":
        
        draw_choose_menu()
        if event.type == pygame.KEYDOWN:
            current_time = pygame.time.get_ticks()

            if current_time - last_move_time > move_delay:
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(characters)
                    last_move_time = current_time
                elif event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(characters)
                    last_move_time = current_time
                elif event.key == pygame.K_RETURN:
                    print(f"You selected character #{selected_index}") 
                    game_state = "gameplay"

    if game_state == "gameplay":
        gameplay()

    clock.tick(45)

pygame.quit()
