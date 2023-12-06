import pygame

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Over")
pygame.font.init()

def Gameover(bool,win):
    running = True
    if bool:
        result = "Win!"
        color = (0,250,0)
    else:
        result = "Loose :(("
        color = (250,0,0)
    my_font = pygame.font.SysFont('Times New Roman', 45)
    text = my_font.render("Game over, You {0}".format(result), True, (250, 250, 250))
    win.fill(color)
    win.blit(text,(width/20,height/2-height/10))
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False