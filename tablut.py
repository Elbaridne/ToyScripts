import sys

import pygame

special_sq = [[0, 0], [0, 8], [8, 0], [8, 8], [4, 4]]

#Expresiones Lambda
nueva_ubicacion = lambda x,y : True if (x,y) not in [pieza.get_pos() for pieza in piezas] else False
pared = lambda x, y: True if x == 0 or x == 8 or y==0 or y==8 else False
territorio_x = lambda x,y,n: True if [x + n, y] in special_sq else False
territorio_y = lambda x,y,n: True if [x, y + n] in special_sq else False

# Inicio de Pygame
pygame.init()
screen = pygame.display.set_mode((458,458 + 50))
pygame.display.set_caption('Tablut')
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 30)
turno = 0


#Tablero
width, height = 9,9


def crear_tablero():
    x, y = 0, 0
    color = (125,87,46)
    tablero = list()
    for i in range(width):
        x = 0
        fila = list()
        for j in range(height):
            casilla = [x,y,color]
            x += 51
            fila.append(casilla)
        y += 51
        tablero.append(fila)
    return tablero
tablero = crear_tablero()

def dibujar_tablero():
    for row in tablero:
        for casilla in row:
            pygame.draw.rect(screen, casilla[2], (casilla[0],casilla[1],50,50))
    pygame.draw.circle(screen, (183,136,60), (tablero[0][0][0]+25, tablero[0][0][1]+25),25,20)
    pygame.draw.circle(screen, (183, 136, 60), (tablero[len(tablero)-1][0][0] + 25, tablero[len(tablero)-1][0][1] + 25), 25, 20)
    pygame.draw.circle(screen, (183, 136, 60), (tablero[0][len(tablero)-1][0] + 25, tablero[0][len(tablero)-1][1] + 25), 25, 20)
    pygame.draw.circle(screen, (183, 136, 60), (tablero[len(tablero)-1][len(tablero)-1][0] + 25, tablero[len(tablero)-1][len(tablero)-1][1] + 25), 25, 20)
    pygame.draw.circle(screen, (183, 136, 60), (tablero[4][4][0] + 25, tablero[4][4][1] + 25), 25, 20)

    tablero[0][0][2] = (105,77,36)
    tablero[4][4][2] = (105,77,36)
    tablero[len(tablero)-1][0][2] = (105,77,36)
    tablero[0][len(tablero)-1][2] = (105,77,36)
    tablero[len(tablero)-1][len(tablero)-1][2] = (105,77,36)

sueco_img = pygame.image.load('Sueco.png')
mosco_img = pygame.image.load('Mosco.bmp')



class Pieza:

    def __init__(self,x,y,sueco,rey=False):
        self.x , self.y = x , y
        self.rey = rey
        self.movimientos = list()
        if sueco :
            self.equipo = 'Sueco'
            self.color = (20,220,220)
        else:
            self.equipo = 'Moscovita'
            self.color = (120,0,60)

    def get_pos(self):
        return (self.x, self.y)

    def draw(self):
        global screen
        if self.equipo == 'Sueco':
            screen.blit(sueco_img, (self.x * 51,self.y * 51))
        else:
            screen.blit(mosco_img, (self.x * 51, self.y * 51))

        if self.rey:
            pygame.draw.rect(screen, (255,255,0),
                             (self.x * 51 + 15, self.y * 51, 20, 20))
        if len(self.movimientos) > 0:
            for mov in self.movimientos:
                pygame.draw.rect(screen, (40,40,40), (mov[0]*51, mov[1] * 51,50,50))

    def move(self):
        x, y = self.x, self.y

        x1 = x
        while x1 < 8:
            x1 += 1
            if nueva_ubicacion(x1, y) is False: break
            else: self.movimientos.append([x1,y])

        x1 = x
        while x1 > 0:
            x1 -= 1
            if nueva_ubicacion(x1, y) is False: break
            else: self.movimientos.append([x1,y])
        y1 = y
        while y1 < 8:
            y1 += 1
            if nueva_ubicacion(x, y1) is False: break
            else: self.movimientos.append([x,y1])
        y1 = y
        while y1 > 0:
            y1 -= 1
            if nueva_ubicacion(x, y1) is False: break
            else: self.movimientos.append([x, y1])
        if not self.rey:
            for esquina in special_sq:
                if esquina in self.movimientos:
                    self.movimientos.remove(esquina)

    def __str__(self):
        return f'{self.equipo} [{self.x},{self.y}]'

    def __repr__(self):
        return f'{self.equipo} [{self.x},{self.y}]'

    def colindantes(self, n) -> list:
        der,izq,arr,aba,wall = (list() for _ in range(5))
        for pieza in piezas:
            if pieza.x == self.x + n and pieza.y == self.y:
                der.append(pieza)
            if pieza.x == self.x - n and pieza.y == self.y:
                izq.append(pieza)
            if pieza.y == self.y + n and pieza.x == self.x:
                aba.append(pieza)
            if pieza.y == self.y - n and pieza.x == self.x:
                arr.append(pieza)
        if territorio_x(self.x,self.y,n): der.append('ESPQ')
        if territorio_x(self.x,self.y,-n): izq.append('ESPQ')
        if territorio_y(self.x,self.y,n): aba.append('ESPQ')
        if territorio_y(self.x,self.y,-n):arr.append('ESPQ')
        if pared(self.x,self.y): wall.append(True)

        return der,izq,arr,aba,wall




def select():
    global turno
    pos = pygame.mouse.get_pos()
    x, y = map(lambda x: (x - (x % 50)) // 50, pos)
    for pieza in piezas:
        if pieza.x == x and pieza.y == y:
            if turno == 0 and pieza.equipo == 'Sueco':
                pieza.move()
                return pieza

            if turno == 1 and pieza.equipo == 'Moscovita':
                pieza.move()
                return pieza





def check_movement():
    global turno, pieza_seleccionada
    pos = pygame.mouse.get_pos()
    x, y = map(lambda x: (x - (x % 50)) // 50, pos)
    if nueva_ubicacion(x, y) and pieza_seleccionada is not None:

        if [x, y] in pieza_seleccionada.movimientos:
            pieza_seleccionada.x = x
            pieza_seleccionada.y = y
            pieza_seleccionada.movimientos = []

            if pieza_seleccionada.rey and [x, y] in special_sq:
                print('Los Suecos ganan')
                turno = 2
                return

            colin = list(zip(pieza_seleccionada.colindantes(1), pieza_seleccionada.colindantes(2)))
            print(colin)

            def comprobar(lado: list):
                if len(lado[0]) > 0:
                    first = lado[0][0]
                    if type(first) is Pieza:
                        if first.rey:
                            print('Es rey!')
                            print(first.colindantes(1))
                            # 1 ESPQ, 3 Moscovitas
                            # 1 ESPQ, 2 Moscovitas, Pared
                            # 4 Moscovitas
                        elif first.equipo != pieza_seleccionada.equipo:
                            if len(lado[1]) > 0:
                                second = lado[1][0]
                                if second is not None and type(second) is Pieza:
                                    print(lado[1][0], '2')
                                    if lado[1][0].equipo == pieza_seleccionada.equipo:
                                        piezas.remove(first)
                                if lado[1][0] is not None and type(lado[1][0]) is str:
                                    piezas.remove(first)

            list(map(comprobar,colin))



            turno = 0 if pieza_seleccionada.equipo == 'Moscovita' else 1



            pieza_seleccionada = None



'''Constructor de piezas y posicionamiento'''
def set_up():
    rey = Pieza(4,4,True,rey=True)
    mosco1 = Pieza(3,0,False)
    mosco2 = Pieza(4,0,False)
    mosco3 = Pieza(5, 0, False)
    mosco4 = Pieza(4, 1, False)
    sueco1 = Pieza(4,2,True)
    sueco2 = Pieza(4,3,True)
    sueco3 = Pieza(2, 4, True)
    sueco4 = Pieza(3, 4, True)
    sueco5 = Pieza(5, 4, True)
    sueco6 = Pieza(6, 4, True)
    sueco7 = Pieza(4, 5, True)
    sueco8 = Pieza(4, 6, True)
    mosco6 = Pieza(8, 3, False)
    mosco7 = Pieza(8, 4, False)
    mosco8 = Pieza(8, 5, False)
    mosco9 = Pieza(7, 4, False)
    mosco10 = Pieza(4, 7, False)
    mosco11 = Pieza(5, 8, False)
    mosco12 = Pieza(4, 8, False)
    mosco13 = Pieza(3, 8, False)
    mosco5 = Pieza(0, 3, False)
    mosco14 = Pieza(0, 4, False)
    mosco15 = Pieza(0, 5, False)
    mosco16 = Pieza(1, 4, False)
    piezas = [rey,mosco1,mosco2,mosco3,mosco4,sueco1,sueco2,mosco6,mosco7,mosco8,mosco9,mosco5,
              mosco14,mosco15,mosco16,mosco13,mosco12,mosco11,mosco10,sueco3,sueco4,sueco5,sueco6,sueco7,sueco8]
    return piezas


# Configuración del Juego
piezas = set_up()
x, y = 0,0
pieza_seleccionada = None

white_text = myfont.render('Turno de Moscovitas', False, (255, 255, 255))
black_text = myfont.render('Turno de Suecos', False, (255,255,255))
sueco_win = myfont.render('GANAN los Suecos', False, (255,255,255))
mosco_win = myfont.render('GANAN los Moscovitas', False, (255,255,255))

#Bucle principal de Juego
while 1:

    clock.tick(50)
    screen.fill((180, 180, 180))
    dibujar_tablero()
    if turno == 0:
        screen.blit(black_text, (51*2 , 51*9))
    if turno == 1:
        screen.blit(white_text, (51*2, 51*9))
    if turno == 2:
        screen.blit(sueco_win, (51*2, 51*9))
    if turno == 3:
        screen.blit(mosco_win, (51*2, 51*9))
    for pieza in piezas:
        pieza.draw()

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit(0)

        #Right arrow -> Reset Game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                piezas = set_up()
                turno = 0

        #Right Click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pieza_seleccionada is None:
                pieza_seleccionada = select()

        #Left Click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if pieza_seleccionada is not None:
                pieza_seleccionada.movimientos = []
                pieza_seleccionada = None


        if event.type == pygame.MOUSEBUTTONUP:
            check_movement()

