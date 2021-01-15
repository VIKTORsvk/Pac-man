import pygame
pygame.init()

#################################SOUND###################################
pygame.mixer.init()

start =pygame.mixer.Sound("pacman_beginning.wav")
eating =pygame.mixer.Sound("pacman_chomp.wav")
i_am_speed = pygame.mixer.Sound("i_am_speed.wav")
i_am_speed.set_volume(0.25)
start.set_volume(0.009)
eating.set_volume(0.008)
###Uncomment for chill music###
##pygame.mixer.music.set_volume(0.06)
##hudba =pygame.mixer.music.load("song.mp3")
##pygame.mixer.music.play(-1, 0.0)

start.play()
###################################SETTINGS###############################
game_width = 960
game_height = 640
clock = pygame.time.Clock()
pygame.display.set_caption("pacman!")
screen = pygame.display.set_mode((game_width,game_height ))
pismo = pygame.font.SysFont("arial", 25)
pismo2 = pygame.font.SysFont("arial", 80)
speed = 2
end_of_the_game = False
u_won = False
text2 = 'GAME OVER'
text3 = 'IZI PIZI'
walls=[]
food = []
superpower =[]
food_points = 0

###################################IMAGE########################################################
char = pygame.image.load('pacmanN.png')
goRight = [pygame.image.load('pacmanR.png'),pygame.image.load('pacmanN.png')]
goLeft = [pygame.image.load('pacmanL.png'),pygame.image.load('pacmanN.png')]
goUp= [pygame.image.load('pacmanU.png'),pygame.image.load('pacmanN.png')]
goDown= [pygame.image.load('pacmanD.png'), pygame.image.load('pacmanN.png')]
pacman_logo = pygame.image.load('pacmanaLogo.png')
win_pic = pygame.image.load('win_pic.jpg')





########################################CLASS####################################################

class Player(object):
    
    def __init__(self,x,y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.hitbox = (self.rect.x, self.rect.y, 30, 30)
        

    def move(self, dx, dy):
        if dx != 0:
            self.move_coll(dx, 0)
        if dy != 0:
            self.move_coll(0, dy)
        
    def move_coll(self, dx, dy):
        global food_points, speed
        self.rect.x += dx
        self.rect.y += dy
        self.hitbox = (self.rect.x, self.rect.y, 25, 25)

        for power in superpower:
            if self.rect.colliderect(power.rect):
                superpower.remove(power)
                speed +=1
                if speed == 6:
                    i_am_speed.play()
        
        for snack in food:
            if self.rect.colliderect(snack.rect):
                food_points +=1
                food.remove(snack)
                eating.play()
                
            
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: 
                    self.rect.right = wall.rect.left
                if dx < 0:  
                    self.rect.left = wall.rect.right
                if dy > 0:  
                    self.rect.bottom = wall.rect.top
                if dy < 0: 
                    self.rect.top = wall.rect.bottom
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 200, 0), self.rect)
        if self.walkCount + 1 >= 30:
            self.walkCount = 0
        
        if self.left:  
            screen.blit(goLeft[self.walkCount//15], self.rect)
            self.walkCount += 1                          
        elif self.right:
            screen.blit(goRight[self.walkCount//15], self.rect)
            self.walkCount += 1
        elif self.up:
            screen.blit(goUp[self.walkCount//15], self.rect)
            self.walkCount += 1
        elif self.down:
            screen.blit(goDown[self.walkCount//15], self.rect)
            self.walkCount += 1
        else:
            screen.blit(char, self.rect)
            self.walkCount = 0
        self.hitbox = (self.rect.x, self.rect.y, 25, 25)
        ###### Hitbox pac-man
        #pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        

class enemy(object):
    ghost1Right = [pygame.image.load('ghostR.png')]
    ghost1Left =  [pygame.image.load('ghostL.png')]
    ghost2Right = [pygame.image.load('ghost2R.png')]
    ghost2Left =  [pygame.image.load('ghost2L.png')]
    ghost3Up = [pygame.image.load('ghost3U.png')]
    ghost3Down =  [pygame.image.load('ghost3D.png')]
    ghost4Up = [pygame.image.load('ghost4U.png')]
    ghost4Down =  [pygame.image.load('ghost4D.png')]
    ghost5Right = [pygame.image.load('ghost5R.png')]
    ghost5Left =  [pygame.image.load('ghost5L.png')]
    
   
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end, self.y]  
        self.walkCount = 0
        self.vel = 4
        self.hitbox = (self.x , self.y , 50, 50)

        
    def draw(self, screen, pohyb):
        if pohyb == 1:
            self.move()
            if self.walkCount +1 <= 2:
                self.walkCount = 0
            if self.vel > 0 :
                screen.blit(self.ghost1Right[self.walkCount], (self.x, self.y))
                self.walkCount +=1
            else:
                screen.blit(self.ghost1Left[self.walkCount], (self.x, self.y))
                self.walkCount +=1
            
        if pohyb == 2:
            self.move2()
            if self.walkCount +1 <= 2:
                self.walkCount = 0
            if self.vel > 0 :
                screen.blit(self.ghost3Down[self.walkCount], (self.x, self.y))
                self.walkCount +=1
            else:
                screen.blit(self.ghost3Up[self.walkCount], (self.x, self.y))
                self.walkCount +=1            
        if pohyb == 3:
            self.move3()
            if self.walkCount +1 <= 2:
                self.walkCount = 0
            if self.vel > 0 :
                screen.blit(self.ghost4Down[self.walkCount], (self.x, self.y))
                self.walkCount +=1
            else:
                screen.blit(self.ghost4Up[self.walkCount], (self.x, self.y))
                self.walkCount +=1            
        if pohyb == 4:
            self.move4()
            if self.walkCount +1 <= 2:
                self.walkCount = 0
            if self.vel > 0 :
                screen.blit(self.ghost2Right[self.walkCount], (self.x, self.y))
                self.walkCount +=1
            else:
                screen.blit(self.ghost2Left[self.walkCount], (self.x, self.y))
                self.walkCount +=1
        if pohyb == 5:
            self.move5()
            if self.walkCount +1 <= 2:
                self.walkCount = 0
            if self.vel > 0 :
                screen.blit(self.ghost5Right[self.walkCount], (self.x, self.y))
                self.walkCount +=1
            else:
                screen.blit(self.ghost5Left[self.walkCount], (self.x, self.y))
                self.walkCount +=1
        self.hitbox = (self.x , self.y-2 , 31, 32)
        #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)
            
    def move(self):
        if self.vel > 0 :
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    def move2(self):
        if self.vel > 0 :
            if self.y + self.vel < self.path[1]:
                self.y += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.y - self.vel > self.path[2]:
                self.y += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    def move3(self):
            if self.vel > 0 :
                if self.y + self.vel < self.path[1]:
                    self.y += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            else:
                if self.y - self.vel > self.path[2]:
                    self.y += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
    def move4(self):
            if self.vel < 0 :
                if self.x + self.vel > self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            else:
                if self.x - self.vel < self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0        
                     
    def move5(self):
            if self.vel > 0 :
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0

class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Food(object):
    
    def __init__(self, pos):
        food.append(self)
        self.rect = pygame.Rect(pos[0]+13, pos[1]+13, 5, 5)
        
class Superpower(object):
    
    def __init__(self, pos):
        superpower.append(self)
        self.rect = pygame.Rect(pos[0]+13, pos[1]+13, 7, 7)

#####################################################MAP#####################################################

level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"WooooooooooooooooooooooooooooW",
"WoWWWoWoWWWWWWWWWWWWWWWoWoWWoW",
"WoWsWoWoWWoooooEoooooWWoWoWWoW",
"WoWoooWoWWoWWWWWWWWWoWWoWooooW",
"WoWoWWWoWWoWWWWWWWWWoWWoWWWWoW",
"WooooooooooooooWoooooooooooooW",
"WoWoWWWWWoWWWWoWoWWWWoWWWWWWoW",
"WoWooooWWoWWWWoWoWWWWoWWoooooW",
"WoWoWWoWWoooooooooooooWWoWoWoW",
"WoWoWWoWWoWWWWWWWWWWWoWWoWsWoW",
"WoWoWWoooooooooooooooooooWWWoW",
"WoWoWWWWWWWWWWWoWWWWWWWWWWWWoW",
"WoooooooooooooWoWooooooooooooW",
"WoWWWWWoWWoWWsWoWsWWoWWoWWWWoW",
"WoooooWoWWoWWWWoWWWWoWWoWooooW",
"WoWWWoWoWWoooooooooooWWoWoWWoW",
"WoWWWoWoWWWooWWWWWooWWWoWoWWoW",
"WooooooooooooooooooooooooooooW",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]
level2 = [
"WWWWWWWWWWWWWWWEWWWWWWWWWWWWWW",
"W                            W",
"W                            W",
"W                            W",
"W                            W",
"W                            W",
"W            ssss            W",
"W                            W",
"W                            W",
"W    WW     WWWW     WWWWW   W",
"W   W W    W        W        W",
"W  W  W     W       W        W",
"W     W      WW     W   WWW  W",
"W     W        W    W     W  W",
"W     W         W   W     W  W",
"W    WWW    WWWW     WWWWW   W",
"W                            W",
"W                            W",
"W                            W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "o":
            Food((x, y))
        if col == "s":
            Superpower((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 32, 32)
        x += 32
    y += 32
    x = 0


    






##############################################DRAW FUNCTION############################################

def drawALL():
    text = pismo.render(text1, True, (255, 255, 255))
    game_over = pismo2.render(text2, True, (255, 255, 255))
    win = pismo2.render(text3, True, (255, 255, 255))
    screen.fill((0, 0, 0))
    
    x=32
    y =32
    
    for wall in walls:
        pygame.draw.rect(screen, ( 0, 0, 49), wall.rect)
    for snack in food:
        pygame.draw.rect(screen, ( 255, 247, 0), snack.rect)
    for power in superpower:
        pygame.draw.rect(screen, ( 255, 0, 0), power.rect)

    pygame.draw.rect(screen, (0, 0, 0), end_rect)
    ghost.draw(screen, 1)
    ghost2.draw(screen, 2)
    ghost3.draw(screen, 3)
    ghost4.draw(screen, 4)
    ghost5.draw(screen, 5)
    player.draw(screen)
    
    if end_of_the_game == True :
        pygame.draw.rect(screen, (0,0,0), (0,0,960,640),1000)
        screen.blit(game_over, (250, 270) )
        screen.blit(win_pic, (370,400))
    if u_won == True :
        pygame.draw.rect(screen, (0,0,0), (0,0,960,640),1000)
        screen.blit(win, (350, 270) )
    pygame.draw.line(screen, (51, 204, 204), (15,627),(945,627),3)
    pygame.draw.line(screen, (51, 204, 204), (170,15),(945,15),3)
    pygame.draw.line(screen, (51, 204, 204), (15,15),(15,627),3)
    pygame.draw.line(screen, (51, 204, 204), (945,15),(945,627),3)
    screen.blit(text, (20, 5) )    
    screen.blit(pacman_logo, (350,127))
    pygame.display.update()

#####################################################PLAYERS#############################################    
ghost= enemy(200,352,30,30,770)
ghost2= enemy(897,32,30,30,540)
ghost3= enemy(97,100,30,30,420)
ghost4= enemy(900,577,30,30,32)
ghost5= enemy(32,32,30,30,900)
player = Player(488, 100, 26 ,26)


#####################################################MAIN LOOP############################################
running = True
while running:
    
    clock.tick(50)
    
    text1 = ('SCORE: '+ str(food_points))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    if food_points == 271:
        u_won = True
        
    if player.hitbox[1] <= ghost.hitbox[1] + ghost.hitbox[3]  and player.hitbox[1]+player.hitbox[3] >= ghost.hitbox[1]:
        if player.hitbox[0]+ player.hitbox[2] >= ghost.hitbox[0]  and player.hitbox[0]  <= ghost.hitbox[0] + ghost.hitbox[2]:
            end_of_the_game = True
            
            
            
    if player.hitbox[1] <= ghost2.hitbox[1] + ghost2.hitbox[3]  and player.hitbox[1]+player.hitbox[3] >= ghost2.hitbox[1]:
        if player.hitbox[0]+ player.hitbox[2] >= ghost2.hitbox[0]  and player.hitbox[0]  <= ghost2.hitbox[0] + ghost2.hitbox[2]:
            end_of_the_game = True
            
            
    if player.hitbox[1] <= ghost3.hitbox[1] + ghost3.hitbox[3]  and player.hitbox[1]+player.hitbox[3] >= ghost3.hitbox[1]:
        if player.hitbox[0]+ player.hitbox[2] >= ghost3.hitbox[0]  and player.hitbox[0]  <= ghost3.hitbox[0] + ghost3.hitbox[2]:
            end_of_the_game = True
            
            
    if player.hitbox[1] <= ghost4.hitbox[1] + ghost4.hitbox[3]  and player.hitbox[1]+player.hitbox[3] >= ghost4.hitbox[1]:
        if player.hitbox[0]+ player.hitbox[2] >= ghost4.hitbox[0]  and player.hitbox[0]  <= ghost4.hitbox[0] + ghost4.hitbox[2]:
            end_of_the_game = True
            
    if player.hitbox[1] <= ghost5.hitbox[1] + ghost5.hitbox[3]  and player.hitbox[1]+player.hitbox[3] >= ghost5.hitbox[1]:
        if player.hitbox[0]+ player.hitbox[2] >= ghost5.hitbox[0]  and player.hitbox[0]  <= ghost5.hitbox[0] + ghost5.hitbox[2]:
            end_of_the_game = True
            
            
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-speed, 0)
        player.left = True
        player.right = False
        player.down = False
        player.up = False
    elif key[pygame.K_RIGHT]:
        player.move(speed, 0)
        player.left = False
        player.right = True
        player.down = False
        player.up = False
    elif key[pygame.K_UP]:
        player.move(0, -speed)
        player.left = False
        player.right = False
        player.up=True
        player.down = False
    elif key[pygame.K_DOWN]:
        player.move(0, speed)
        player.left = False
        player.right = False
        player.up = False
        player.down = True
    else: 
        player.left = False
        player.right = False
        player.up = False
        player.down = False
        player.walkCount = 0
       
    drawALL()
    pygame.display.flip()
    
pygame.quit()
