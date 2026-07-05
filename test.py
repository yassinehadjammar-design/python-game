import pygame
# initialisation of the library
pygame.init()

# init of the window and setting the size of it
window = pygame.display.set_mode((500 , 480)) 

# title that appears on top of the game
pygame.display.set_caption("First Game")

# loading pictures for animation 
# This goes outside the while loop, near the top of the program
walk_right = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
walk_left = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]
background_image = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')
player_gun = [pygame.image.load('images/left_gun.png'),pygame.image.load('images/right_gun.png')] 

# game clock 
clock = pygame.time.Clock()

jumpDelay = 1
def parabolic_tween(t: float) -> float:
    """
    Parabolic function mapping progress `t` (0 to 1):
    - t = 0.0 -> returns 0.0
    - t = 0.5 -> returns 1.0
    - t = 1.0 -> returns -1.0
    """
    return -12.0 * (t ** 2) + 8.0 * t
def lerp(start: float, end: float, alpha: float) -> float:
    """Linearly interpolates between start and end based on alpha (0.0 to 1.0)."""
    return start + (end - start) * alpha

class player(object):
    def __init__(self,x,y,width,height) :
        self.x = x
        self.y = y
        self.width = width
        self.height = height 

        self.velocity = 5
        self.is_jump = False 
        self.jump_count = 0
        
        self.left = False 
        self.right = False 
        self.walk_count = 0

        self.standing = True

        self.last_shot = 0

    def draw(self,window):
        # drawing the caracter
        # if you want to draw an image pygame.draw.rect(window ,(255,0,0), (x,y,width,height))

        if self.walk_count +1 >= 27 :
            self.walk_count = 0

        if self.right or self.left :
            if self.right :
                window.blit(player_gun[1] , (self.x-253,self.y-160))
            else :
                window.blit(player_gun[0] , (self.x-285,self.y-160))

        if not(self.standing) :
            if self.left :
                window.blit(walk_left[self.walk_count//3],(self.x,self.y))
                self.walk_count += 1
            elif self.right :
                window.blit(walk_right[self.walk_count//3],(self.x,self.y))
                self.walk_count += 1
        else :
            if self.right and not self.left:
                window.blit(walk_right[0], (self.x,self.y))
            elif self.left and not self.right :
                window.blit(walk_left[0], (self.x,self.y))
            else :
                window.blit(char,(self.x,self.y))


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius 
        self.color = color
        self.facing = facing 
        self.velocity = 8 * facing

    def draw(self,window):
        pygame.draw.circle(window,self.color,(self.x,self.y),self.radius)


def redraw_game_window():
    # need to fill the screen unless the square is drawn
    # if you wanna fill the screen with a color : window.fill((0,0,0))
    window.blit(background_image , (0,0))

    # drawing the caracter 
    man.draw(window)

    # drawing the bullets

    for bullet in bullets :
        bullet.draw(window)

    # refreshing the game
    pygame.display.update()

# every game has a while loop that checks for collision and movment and verything , this loop is essential

man = player(300,410,64,64)
bullets = []

run = True
while run :
    # game clock ( fps )
    clock.tick(27)

    # cheking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            run = False

    # bullets code 

    for bullet in bullets :
        if bullet.x < 500 and bullet.x > 0 :
            bullet.x += bullet.velocity 
        else :
            bullets.pop(bullets.index(bullet))

    # player movment
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and ( man.left or man.right ):
        if man.left :
            facing = -1 
        else :
            facing = 1
        if len(bullets) < 10 :
            if man.last_shot >=  10 :
                if man.right and not man.left :
                    bullets.append(projectile(round(man.x + 65) ,round( man.y + 37) , 3 , (184,134,11) , facing ))
                else :
                    bullets.append(projectile(round(man.x ) ,round( man.y + 37) , 3 , (184,134,11) , facing ))
                man.last_shot = 0 
    
    if man.last_shot <= 10 :
        man.last_shot += 1

    if keys[pygame.K_LEFT] and man.x > 0 :
        man.x -= man.velocity
        man.left = True
        man.right = False
        man.standing = False 
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width :
        man.x+= man.velocity
        man.right = True
        man.left = False
        man.standing = False
    else :
        man.standing = True
        man.walk_count = 0

    # when the player jumps
    if not(man.is_jump) :
        if keys[pygame.K_UP]:
            man.is_jump = True
            man.walk_count = 0

    else :
        man.y -= (parabolic_tween(man.jump_count) * 20)
        man.jump_count = min(1,man.jump_count+ (1/(27*jumpDelay)))
        print(f"jump value is {man.jump_count}->{parabolic_tween(man.jump_count)}")
        if (man.jump_count==1):
            man.is_jump = False
            man.jump_count = 0


    redraw_game_window() 


# quitting the game
pygame.quit()




