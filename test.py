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

# game clock 
clock = pygame.time.Clock()

def ease_out_quad(t):
    return t * (2 - t)
def tween_next_value_step(current_val, start_val, end_val,dt, smooth_func):
    """
    Calculates the exact next value step dynamically.
    Works frame-by-frame using only the current value.
    """
    # 1. Prevent division by zero
    if start_val == end_val:
        return end_val

    # 2. Find current linear progress (0.0 to 1.0)
    t = (current_val - start_val) / (end_val - start_val)
    t = max(0.0, min(t, 1.0))

    # 3. Use an incredibly tiny time step (dt) to find the slope/velocity of your easing curve
    
    # Calculate the rate of change (how fast the curve is moving right now)
    current_speed = smooth_func(t)
    next_speed = smooth_func(min(t + dt, 1.0))
    curve_slope = next_speed - current_speed

    # 4. If the slope is zero (stuck at start), force a baseline starting step to kickstart movement
    if curve_slope <= 0:
        curve_slope = dt * 1.5 

    # 5. Calculate the next physical step size based on that curve speed
    step = (end_val - start_val) * curve_slope

    # 6. Apply step and return the next value
    next_val = current_val + step
    
    # Don't overshoot the final target range
    if start_val < end_val:
        return max(start_val, min(next_val, end_val))
    else:
        return min(start_val, max(next_val, end_val))

class player(object):
    def __init__(self,x,y,width,height) :
        self.x = x
        self.y = y
        self.width = width
        self.height = height 

        self.velocity = 5
        self.is_jump = False 
        self.jump_count = 10
        
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
                bullets.append(projectile(round(man.x + man.width // 2) ,round( man.y + man.height // 2) , 6 , (0,0,0) , facing ))
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
        if man.jump_count >= -10 :
            neg = 1
            if man.jump_count < 0 :
                neg = -1 
            man.y -= (man.jump_count ** 2) * 0.5 * neg
            man.jump_count = tween_next_value_step(man.jump_count,10,-10,1/27,ease_out_quad)
            print(f"jump value is {man.jump_count}")
        else :
            man.is_jump = False 
            man.jump_count = 10

    redraw_game_window() 


# quitting the game
pygame.quit()




