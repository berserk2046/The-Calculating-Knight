import random
import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()

# Global variables
s_w = 800
s_h = 600

# Fondo
bg = pygame.image.load("fondo.png")

# Imagenes de los sprites
caballero = pygame.image.load("caballero.png")
dragon = pygame.image.load("dragon.png")

# triangulos
tri_image = pygame.image.load("triangle.png")

#petty solution
rand_txt = ''

# Sprites, son objetos.
class player(pygame.sprite.Sprite):
    # self es el sprite en si, head es la imagen.
    def __init__(self, caballero):
        super(player, self).__init__() # no se jaja
        # carga la imagenk
        self.image = caballero
        # Pone las coordenadas en las que aparece la cabeza y el tamano de la imagen.
        self.rect = self.image.get_rect(topleft=(s_w/2, s_h/1.5)) # gets the rectangle to print it on screen

    # Movimiento, chequea las teclas y luego refresca el progrma para registrarlas
    def update(self, keys):
        if keys[pygame.K_w]:
            self.rect.move_ip(0, -1)
        if keys[pygame.K_s]:
            self.rect.move_ip(0, 1)
        if keys[pygame.K_a]:
            self.rect.move_ip(-1, 0)
        if keys[pygame.K_d]:
            self.rect.move_ip(1, 0)

        # Restricciones de movimiento (no peude salir de la pantalla)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > s_w:
            self.rect.right  = s_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > s_h: 
            self.rect.bottom = s_h


class enemy(pygame.sprite.Sprite):
    # self es el sprite en si, head es la imagen.
    def __init__(self, dragon):
        super(enemy, self).__init__() # no se jaja
        # carga la imagenk
        self.image = dragon
        # Pone las coordenadas en las que aparece la cabeza y el tamano de la imagen.
        self.rect = self.image.get_rect(topleft=(s_w/1.5, s_h/1.5)) # gets the rectangle to print it on screen


class triangle(pygame.sprite.Sprite):
    def __init__(self,tri_image):
        super(triangle, self).__init__()
        self.image = tri_image
        self.rect = self.image.get_rect(topleft=(s_w/6, s_h/2))

def rand_election():
    # Elecciones, solo hay una por falta de problemas.
    election = [0] # 0 trigonometry, 2, 3 to add more things
    rand_txt = ''
    # Escoge una variable random de la lista de elecciones
    ran_election = random.choice(election)
    if ran_election == 0:
        rand_txt = "triangle"
    return rand_txt


# Main, declaraciones.
screen = pygame.display.set_mode((s_w, s_h))
clock = pygame.time.Clock() # Reloj del juego, para que funcione la pausa, por ejemplo
start_time = pygame.time.get_ticks()




# Caja de texto
input_box = pygame.Rect(20, s_h/6, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False

# Texto
font = pygame.font.Font(None, 18)
font_timer = pygame.font.Font(None, 25)
font_dead = pygame.font.Font(None, 32)
txt = font.render(rand_election(), False, (0,0,0))

# Pantalla de muerte
deadline = pygame.Surface((s_w, s_h/3))
deadline.set_alpha(180)
deadline.fill("red")



# main loop
running = True
paused = False

#caja  de la izquierda
aside_pos = pygame.Rect(0, 0, s_w/3.2, s_h)
aside_color = "gray"

# personajes :)
Player = player(caballero)
Enemy = enemy(dragon)

# run loop
while running:
    #event loop
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False

        # hace que la caja se active cuando se presiona click encima de ella
        if event.type == pygame.MOUSEBUTTONDOWN:
            # cambia el color de la caja
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False

            color = color_active if active else color_inactive

        # Si se recibe una tecla entonces la caja la reconoce y cuando se presiona enter se almacena en text, luego se borra.
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                    text = ''
                # Elimina una tecla con backspace
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode



    #Counting time
    if not paused:
        counting_time = pygame.time.get_ticks() - start_time
        counting_min = str(counting_time//60000).zfill(2) # estos minutos son para mostrar
        counting_sec = str( (counting_time%60000)//1000).zfill(2)
        counting_mil = str(counting_time%1000).zfill(3)
        
        counting_string = "%s:%s:%s" % (counting_min, counting_sec, counting_mil)
        counting_txt = font_timer.render(str(counting_string), 1, "black")
        counting_rect = counting_txt.get_rect(topleft=(s_w/9, s_h/8))

        counting_minutes = counting_time//60000 # Estos minutos es para regular tiempo

    # Refresca las teclas, osea, llama la funcion del sprite de las teclas para que funcionen
    keys = pygame.key.get_pressed()
    Player.update(keys)

    # refreshing
    # Basicamente carga los sprites y las cajas.
    screen.blit(bg, (0,0))


    # Screen
    pygame.draw.rect(screen, aside_color, aside_pos, 0 )
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)

    # Elementos dentro de la caja gris
    pygame.draw.polygon(screen, "black", [[30,20], [40,60], [70,10]])

    # Aca va donde se muestran los triangulos y las elecciones.
    triangulo = triangle(tri_image)
    screen.blit(triangulo.image, triangulo.rect)
    screen.blit(txt, (25, s_h/2.5))
    screen.blit(counting_txt, counting_rect)

    # Labels
    label_timer = font.render("Cuando el Reloj llegue a 1 minuto pierdes.",1,"black")
    screen.blit(label_timer, (10, s_h/10))

    # Carga los personajes
    screen.blit(Player.image, Player.rect) 
    screen.blit(Enemy.image, Enemy.rect)

    #Pantalla de Muerte
    dead_label = font_dead.render("Perdiste", 1, "black")
    dead_labelrect = dead_label.get_rect(topleft=(s_w/2-50, s_h/3+80))
    if counting_minutes >= 1:
        screen.blit(deadline, (0, s_h/3))
        screen.blit(dead_label, dead_labelrect)
        paused = True

    # para mostrar las cosas en la pantalla
    pygame.display.flip()
    pygame.display.update()
    clock.tick(25)
