#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer


font.init()
font1=font.Font(None,36)

lose=font1.render('Проиграл',True,(150,50,250))
win=font1.render('molodec ti pobedil!!!',True,(150,200,44))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y



    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_d] and self.rect.x < 600 :
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0 :
            self.rect.x -= self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,self.speed)
        bullets.add(bullet)
lost=0
chetki=0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>500:
            self.rect.y=0
            self.rect.x=randint(150,625)
            lost = lost + 1
        

    
window_size = [700, 500]
window = display.set_mode(window_size)
display.set_caption("shuter")

clock = time.Clock()
FPS = 60


background = transform.scale(image.load("galaxy.jpg"), window_size)

#фоновая музыка
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()



bullets = sprite.Group()
metiors = sprite.Group()

player = Player("rocket.png", 10 ,400 , 5)

monsters=sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png",randint(0,600),7, randint(1,2))  
    monsters.add(monster)

for metior in range(1,4):
    metior = Enemy('asteroid.png',randint(0,600),7,randint(1,2))
    metiors.add(metior)

game = True
finish = False

fires = 0
rel_time = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:

                if fires < 5 and rel_time == False:
                    player.fire()
                    fires += 1
                if fires >= 5 and rel_time == False:
                    first = timer()
                    rel_time = True


    if finish != True:
        window.blit(background, (0,0))

        player.update()
        monsters.update()
        bullets.update()
        metiors.update()


        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        metiors.draw(window)

        if rel_time == True:
            second = timer()

            if second - first < 3:
                reload = font1.render('Reloading...', 1, (255, 0, 0))
                window.blit(reload, (250, 450))
            else:
                fires = 0
                rel_time = False
        
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)

        for collide in sprites_list:
            chetki=chetki+1    
            monster = Enemy("ufo.png",randint(0,600),7, randint(1,10))  
            monsters.add(monster)

        if chetki>=10:
            finish = True
            window.blit(win, (259,250))
        if lost >=10:
            finish = True
            window.blit(lose, (250,250))   

        text_lose=font1.render('Пропущено'+ str(lost),1,(255,255,255))
        anton=font1.render('Счёт'+ str(chetki),1,(255,255,255))

        window.blit(text_lose,(5,10))
        window.blit(anton,(10,35))

        
         

    display.update()
    clock.tick(FPS)