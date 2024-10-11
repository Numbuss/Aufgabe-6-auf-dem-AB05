import os
import random
from typing import Any
import pygame
class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 600, 400)
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")
    rect   = pygame.sprite.collide_rect
    round  = pygame.sprite.collide_circle
    mask   = pygame.sprite.collide_mask


class obstical(pygame.sprite.Sprite):

    def __init__(self,posx:int,posy:int,width:int,height:int,file_name:str,collison_type:int):
        self.posx          = posx
        self.posy          = posy
        self.width         = width
        self.height        = height
        self.file_name     = file_name
        self.collison_type = collison_type
        super().__init__()
        self.obstical_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, self.file_name)).convert()
        self.obstical_image = pygame.transform.scale(self.obstical_image, (self.width, self.height))
        self.rect: pygame.rect.Rect = self.obstical_image.get_rect()
        self.radius = self.rect.centerx   
        self.rect.centery = Settings.WINDOW.centery
        self.mask = pygame.mask.from_surface(self.obstical_image) 
        self.obstical_rect = self.obstical_image.get_rect()
        self.obstical_rect.topleft = (self.posx, self.posy)





class rechanging(pygame.sprite.Sprite):
     def __init__(self,file_name:str,width:int,height:int):
         self.width     = width
         self.height    = height
         self.file_name = file_name
         self.posy      = random.randint(0,400)
         self.posx      = random.randint(0,600)
         super().__init__()
         self.rech_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, self.file_name)).convert()
         self.rech_image = pygame.transform.scale(self.rech_image, (self.width, self.height))
         self.rech_rect = self.rech_image.get_rect()
         self.rech_rect.topleft = (self.posx, self.posy)
     def update(self):
         
         pygame.transform.scale_by(self.rech_rect, (1.1 , 1.1 ))
     def oncrash(self, *args: Any, **kwargs: Any) -> None :
        if self.collison_type ==1:
         if "hit" in kwargs.keys():
            self.hitr = kwargs["hit"]
            self.posx = random.randint(0,400)
            self.posy = random.randint(0,600)
            self.width = 40
            self.height= 40
        elif self.collison_type ==2:
         if "hit" in kwargs.keys():
            self.hitc = kwargs["hit"]
            self.posx = random.randint(0,400)
            self.posy = random.randint(0,600)
            self.width = 40
            self.height= 40
        elif self.collison_type ==3:
         if "hit" in kwargs.keys():
            self.hitm = kwargs["hit"]
            self.posx = random.randint(0,400)
            self.posy = random.randint(0,600)
            self.width = 40
            self.height= 40

class Game(object):
        def __init__(self) -> None:
               super().__init__()
               os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"
               pygame.init()     
            
               self.surface = pygame.display.set_mode(Settings.WINDOW.size)
               pygame.display.set_caption("mask test")
               self.clock = pygame.time.Clock()      


               self.brick1 = obstical(300,150,40,40,"wall.png",1)   
               self.brick2 = obstical(75,80,40,40,"wall.png",1)
               self.round1 = obstical(50,290,40,40,"ball.png",2)   
               self.round2 = obstical(200,300,40,40,"ball.png",2)  
               self.unatural1 = obstical(85,150,40,40,"unregelmasig.png",3)   
               self.unatural2 = obstical(250,90,40,40,"unregelmasig 2.png",3)
              
               
               self.grow = rechanging("ball.png",40,40)
               self.rec_sprites = pygame.sprite.Group()
               self.round_sprites = pygame.sprite.Group()
               self.mask_sprites = pygame.sprite.Group()
               self.rec_sprites.add(self.brick1)
               self.rec_sprites.add(self.brick2)
               self.round_sprites.add(self.round1)
               self.round_sprites.add(self.round2)
               self.mask_sprites.add(self.unatural1)
               self.mask_sprites.add(self.unatural2)
               self.all_ob = pygame.sprite.Group()
               self.all_ob.add(self.brick1)
               self.all_ob.add(self.brick2)
               self.all_ob.add(self.round1)
               self.all_ob.add(self.round2)
               self.all_ob.add(self.unatural1)
               self.all_ob.add(self.unatural2)
               self.growing = pygame.sprite.GroupSingle(self.grow)
               
               self.running = True

        def run (self):
                

            while self.running:
            # Event-Handling
             self.watch_for_events()

            # Spiellogik
             self.update()
             self.all_ob.update()

            # Objekte zeichnen
             self.draw()

             self.clock.tick(Settings.FPS)
             self.grow.update

             
            pygame.quit()

             


        def watch_for_events(self) -> None:
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        def update(self) -> None:
         self.check_for_collision()

        def draw(self) -> None:
         self.surface.fill("white")
         self.rec_sprites.draw(self.surface)
         self.round_sprites.draw(self.surface)
         self.mask_sprites.draw(self.surface)
         self.growing.draw(self.surface)
         pygame.display.flip()
         

        def check_for_collision(self) -> None:
            hitrec  = pygame.sprite.spritecollide(self.growing.sprite, self.rec_sprites, False, Settings.rect)
            hitcy   = pygame.sprite.spritecollide(self.growing.sprite, self.round_sprites, False, Settings.round)
            hitmask = pygame.sprite.spritecollide(self.growing.sprite, self.mask_sprites, False, Settings.mask)
            for r in self.rec_sprites:
                r.update(hitr=r in hitrec)
            for c in self.round_sprites:
                c.update(hitc=c in hitcy)
            for m in self.mask_sprites:
                m.update(hitm=m in hitmask)


                 #self.grow.posx = random.randint(0,400)
                 #self.grow.posy = random.randint(0,600)
                 #self.grow.width = 40
                 #self.grow.height= 40
            
def main ():
    game = Game()
    game.run()


    


if __name__ == "__main__":
  main()