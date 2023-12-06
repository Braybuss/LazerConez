import pygame
from network import Network
import math
from gameover import Gameover

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("LazerConez")
pygame.font.init()

clientNumber = 0


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.mx = 0
        self.my = 0
        self.width = 10
        self.height = height
        self.color = color
        self.theta = 0
        self.vel = 3
        self.hp = 250
        self.vision = 100
        self.energy = 100
        self.upper = [0,0] #cone upper coordinate
        self.lower = [0,0] #cone lower coordinate
        #vision, damage, speed, hp, (dash or invis?), maybe invest 3 points to get one of the two, space to activate dash, invis auto(? maybe keypress),
        #another idea is cone width. COuld have an energy bar that is used to use damaging cone, two more stats(consumption rate, energy level)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y),self.width)#character
        pygame.draw.polygon(win,(0,0,0),[[self.x,self.y],self.upper,self.lower])#vision cone triangle
        #pygame.draw.ellipse(win,(0,0,0))#vision code ellipse at end for rounding
        rect = pygame.Rect(self.x-25,self.y,50,10)
        pygame.draw.rect(win,(250,0,0), rect)
        offset = self.hp/5-25
        rect = pygame.Rect(self.x-25,self.y,25+offset,10)
        pygame.draw.rect(win,(0,250,0), rect)
        offset = self.energy/2-25
        rect = pygame.Rect(self.x-25,self.y+11,25+offset,3)
        pygame.draw.rect(win,(0,0,250), rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.cone()
    def cone(self):
        xdif = self.x-self.mx
        ydif = self.y-self.my
        if xdif == 0:
            if ydif > 0:
                self.theta = 90
            else:
                self.theta = 270
        else:
            self.theta = 180 - math.degrees(math.atan2(ydif,xdif))
        self.upper = [self.x+math.sin((self.theta+15+90)*math.pi/180)*self.vision,self.y+math.cos((self.theta+15+90)*math.pi/180)*self.vision]
        self.lower = [self.x+math.sin((self.theta-15+90)*math.pi/180)*self.vision,self.y+math.cos((self.theta-15+90)*math.pi/180)*self.vision]
    def damagecheq(self,p,p2):
        #calculating the area of 4 triangles, the vision cone, and then from the player to all points inside the cone piont a is player2.pos, point b is upper and c is lower, point p is current characters point
        if self.color == (0,255,0):
            other = p2
        else:
            other = p
        x1 = other.x
        y1 = other.y
        x2, y2 = other.upper
        x3, y3 = other.lower
        x4 = self.x
        y4 = self.y
        values = [x1,y1,x2,y2,x3,y3,x4,y4]
        for value in values:
            if value == 0:
                value = 1
        if (y2-y1)*(x3-x1) - (x2-x1)*(y3-y1) == 0:
            bonus = 1
        else:
            bonus = 0
        w1 = (x1*(y3-y1) + (y4-y1)*(x3-x1)-x4*(y3-y1))/((y2-y1)*(x3-x1) - (x2-x1)*(y3-y1)+bonus)
        if y3-y1 == 0:
            bonus = 1
        else:
            bonus = 0
        w2 = ((y4-y1-w1*(y2-y1))/((y3-y1)+bonus))

        if w1 >= 0 and w2 >= 0 and w1+w2 <= 1:
            self.hp -= 1
        else:
            pass




def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]),int(str[2]), int(str[3]), int(str[4])

def start_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + ',' + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4])

def Start_Stats():
    print("Wow")

def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

def connect():
    ipnums = []
    join_code = input("Enter join code")
    join_code = join_code.upper()
    split_JoinCode = list(map(str,join_code))
    print(split_JoinCode)
    for Y in range(0,len(split_JoinCode)):
        split_JoinCode[Y] = alphabet.index(split_JoinCode[Y])
    for var in range(0,4):
        x=var*2
        split_JoinCode[x] = split_JoinCode[x]*16
        total = split_JoinCode[x]+split_JoinCode[x+1]
        ipnums.append(total)
        print(total)
    ip = str(ipnums[0])
    for i in range(0,3):
        ip+= '.'
        ip += str(ipnums[i+1])
    print(ipnums)
    print(ip)
    return ip

def main():
    run = True
    ip = connect()
    n = Network(ip)
    startPos = start_pos(n.getPos())
    p = Player(startPos[0],startPos[1],100,100,(0,255,0))
    p2 = Player(0,0,100,100,(255,0,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()
        p.mx = mx
        p.my = my
        p2Pos = read_pos(n.send(make_pos((p.x, p.y, mx, my,p.hp))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.mx = p2Pos[2]
        p2.my = p2Pos[3]
        p2.hp = p2Pos[4]
        p.damagecheq(p,p2)
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        if p.hp <= 0:
            p2Pos = read_pos(n.send(make_pos((p.x, p.y, mx, my,p.hp))))
            Gameover(False,win)
            run = False
        elif p2.hp <= 0:
            Gameover(True,win)
            run = False
        redrawWindow(win, p, p2)
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
main()