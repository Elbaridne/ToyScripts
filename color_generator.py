import random
import pygame, sys

pygame.init()
screen = pygame.display.set_mode((410,100))
pygame.display.set_caption("Color Picker for IA")
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 30)

def generator_rgb():
    red = random.randint(0,255)
    green = random.randint(0,255)
    blue = random.randint(0,255)
    return red,green,blue


color = generator_rgb()
white_text = myfont.render('Some Text', False, (255, 255, 255))
black_text = myfont.render('Some Text', False, (0,0,0))
colors = []

while 1:
    clock.tick(50)
    screen.fill((125,125,125))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(colors)
            with open('colors.csv', 'w') as csv:
                for color in colors:
                    csv.write(str(color[0])+";"+color[1]+'\n')
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                print('Right value')
                colors.append([color,'black'])
                color = generator_rgb()
            if event.key == pygame.K_LEFT:
                print('Left value')
                colors.append([color,'white'])
                color = generator_rgb()


    pygame.draw.rect(screen, color, (10, 10, 190, 80))
    pygame.draw.rect(screen, color, (210,10,190,80))
    screen.blit(white_text, (20, 20))
    screen.blit(black_text, (220, 20))
    pygame.display.flip()




