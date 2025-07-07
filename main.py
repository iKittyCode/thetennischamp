import pygame
import time
pygame.init()
paused = False 
choosen = None
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("The Championships")
clock = pygame.time.Clock()
running = True
player = None
enemy = None
ball = None


playerframes = []
playerframes.append(pygame.transform.scale_by(pygame.image.load("images/mainchar1/tile012.png").convert_alpha(), 1.5))

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

player_bounds =  pygame.Rect(0, screen.get_height() // 2, screen.get_width(), screen.get_height() // 2)
server_frames = []
# for i in range(5):  # Adjust number to match your actual frames
#     frame = pygame.image.load(f"images/serve/serve{i}.png").convert_alpha()
#     frame = pygame.transform.scale(frame, (128, 128))
#     serve_frames.append(frame)
server_frames.append(pygame.transform.scale_by(pygame.image.load("images/mainchar1/tile002.png"), 1.5))
server_frames.append(pygame.transform.scale_by(pygame.image.load("images/mainchar1/tile001.png"), 1.5))
server_frames.append(pygame.transform.scale_by(pygame.image.load("images/mainchar1/tile008.png"), 1.5))
server_frames.append(pygame.transform.scale_by(pygame.image.load("images/mainchar1/tile003.png"), 1.5))
server_frames.append(pygame.transform.scale_by(pygame.image.load("images/mainchar1/tile007.png"), 1.5))
# class Enemy(pygame.sprite.Sprite): 
#     def __init__(self, frames, x, y, serve_frames):
        
class Ball:
    def __init__(self, x, y):
        self.image =  pygame.image.load("images/tennisball.png").convert_alpha()  # Make sure you have this
        self.image = pygame.transform.scale(self.image, (12, 12))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.Vector2(0, 0)
        self.served = False

    def serve(self, direction):
        if not self.served:
            self.velocity = pygame.Vector2(direction)
            self.served = True

    def update(self, player):
        if self.served:
            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y
        else: 
            self.x = player.rect.x

    def reset(self, x, y):
        self.rect.center = (x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.served = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        
    def followplayer(self, player):
        self.rect.centerx = player.rect.centerx + 30
        self.rect.centery = player.rect.centery -10


class Player:
    def __init__(self, frames, x, y, serve_frames):
        self.frames = frames
        self.frame_index = 0
        self.image = frames[0]
        self.rect = pygame.Rect(x, y, frames[0].get_width(), frames[0].get_height())
        self.speed = 5
        self.currentsidedeuce = True
        self.isfirstserve = True

        # Animation timing
        self.anim_timer = 0
        self.anim_delay = 100

        # Serve animation
        self.serve_frames = serve_frames
        self.serving = False
        self.serve_index = 0
        self.serve_timer = 0
        self.serve_delay = 60

    def move(self, keys):
        if self.serving:
            return  # No movement during serve

        moved = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            moved = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            moved = True
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            moved = True
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            moved = True

        if moved:
            now = pygame.time.get_ticks()
            if now - self.anim_timer > self.anim_delay:
                self.anim_timer = now
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
        else:
            self.frame_index = 0
            self.image = self.frames[0]

        self.rect.clamp_ip(player_bounds)

    def serve(self):
        if not self.serving:
            self.serving = True
            self.serve_index = 0
            self.serve_timer = pygame.time.get_ticks()

    def update(self):
        
        if self.serving:
            now = pygame.time.get_ticks()

            if now - self.serve_timer >= self.serve_delay:
                self.serve_timer = now

                if self.serve_index < len(self.serve_frames):
                    self.image = self.serve_frames[self.serve_index]
                    self.serve_index += 1
                else:
                # Serve finished
                    self.serving = False
                    self.image = self.frames[0]  # Return to idle

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)



                  


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
    
    keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    screen.blit(pygame.image.load("images/gamebackground.png"), (0, 0))

    if not paused:
        if ball and not ball.served:
            ball.followplayer(player)
        if keys[pygame.K_r]:
            if not player.isfirstserve:
                player.currentsidedeuce = not player.currentsidedeuce
            player.isfirstserve = not player.isfirstserve
            
            
            time.sleep(0.3)
            
            if ball and not ball.served:

                player.serve()
                
                if player.rect.x < 310:

                    ball.serve((3, -4))
                else: 
                    ball.serve((-3, -4))

        if not ball.served: 
            if player.currentsidedeuce and player.isfirstserve: 
                player.rect.x = 360
            elif not player.currentsidedeuce and player.isfirstserve: 
                player.rect.x = 220


        if ball and ball.served:
            ball.draw(screen)
        if ball:
            ball.update(player)
            # Reset ball if it goes out of bounds
            if ball.rect.left > screen.get_width() or \
                ball.rect.right < 0 or \
                ball.rect.top > screen.get_height() or \
                ball.rect.bottom < 0:
                ball.reset(player.rect.centerx + 30, player.rect.centery - 10)
    player.update()
    player.move(keys)

    
    player.draw(screen)


    if paused:
        pause_text = font.render("PAUSED", True, (255, 0, 0))
        pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(pause_text, pause_rect)

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
                    player = Player(playerframes, 360, 370, server_frames)
                    ball = Ball(player.rect.centerx + 30, player.rect.centery - 10)
                    game_state = "gameplay"

    if game_state == "gameplay":
        gameplay()

    # Check pause toggle separately (outside event loop)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        if not paused:
            paused = True
            pygame.time.wait(200)  # Small delay to avoid instant unpause
        else:
            paused = False
            pygame.time.wait(200)

    clock.tick(45)

pygame.quit()
