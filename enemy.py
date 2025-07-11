import pygame
import random
class Enemy:
    def __init__(self, frames, x, y):
        self.frames = frames
        self.frame_index = 0
        self.image = frames[0]
        self.rect = pygame.Rect(x, y, frames[0].get_width(), frames[0].get_height())
        self.speed = 3
        self.anim_timer = 0
        self.anim_delay = 300
        self.return_cooldown = 1200
        self.last_return_time = 0
        self.return_direction_toggle = True  

    def update(self, ball, screen):
        
        if ball and ball.served:
            
            threshold = 30
            if ball.rect.centerx < self.rect.centerx - threshold:
                self.rect.x -= self.speed
            elif ball.rect.centerx > self.rect.centerx + threshold:
                self.rect.x += self.speed
            
            now = pygame.time.get_ticks()
            if self.rect.x > 230: 
                self.image = self.frames[1]
            else:
                self.image = self.frames[0]
            

            if ball.landed_in:

           
                self.try_return(ball, screen)

    def try_return(self, ball, screen):
        now = pygame.time.get_ticks()
        if now - self.last_return_time < self.return_cooldown:
            return

        if self.rect.colliderect(ball.rect) or abs(ball.rect.centery - self.rect.centery) < 3:
            self.last_return_time = now
            target_x = (screen.get_width() // 2) + random.uniform(-100, 100)
            target_y = 370 + random.uniform(-10, 10)

        
            dx = (target_x - ball.rect.centerx)
            dy = target_y - ball.rect.centery  
            direction = pygame.Vector2(dx, dy).normalize() * 5  # Speed = 5
            ball.velocity = direction
            self.return_direction_toggle = not self.return_direction_toggle
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
