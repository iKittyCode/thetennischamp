import pygame
import random
import time
import globalvars

class Enemy:
     def __init__(self, frames, x, y, serve_frames):
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
         self.serve_frames = serve_frames
         self.serving = False
         self.serve_index = 0
         self.serve_timer = 0
         self.serve_delay = 60
         self.currentsidedeuce = True
         self.isfirstserve = True

     def update(self, ball, screen):
         if self.serving:
             now = pygame.time.get_ticks()
             if now - self.serve_timer >= self.serve_delay:
                 self.serve_timer = now
                 if self.serve_index < len(self.serve_frames):
                     self.image = self.serve_frames[self.serve_index]
                     self.serve_index += 1
                 else:
                     self.serving = False
                     self.image = self.frames[0]

         if ball and ball.served:
             threshold = 30
             if ball.rect.centerx < self.rect.centerx - threshold:
                 self.rect.x -= self.speed
             elif ball.rect.centerx > self.rect.centerx + threshold:
                 self.rect.x += self.speed

             now = pygame.time.get_ticks()
             self.image = self.frames[1] if self.rect.x > 230 else self.frames[0]

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

             dx = target_x - ball.rect.centerx
             dy = target_y - ball.rect.centery
             direction = pygame.Vector2(dx, dy).normalize() * 5
             ball.velocity = direction
             self.return_direction_toggle = not self.return_direction_toggle
         elif ball.rect.y < 10 and not globalvars.point_over:
             globalvars.scoring("player")
             globalvars.point_over = True

     def draw(self, surface):
         surface.blit(self.image, self.rect.topleft)

     def serve(self):
         if not self.serving:
             self.serving = True
             self.serve_index = 0
             self.serve_timer = pygame.time.get_ticks()
