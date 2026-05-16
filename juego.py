import pygame
import sys

#Inicializar a pygame

pygame.init()

#Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Future Pizza")
icono = pygame.image.load("./Recursos/Piz.png")
pygame.display.set_icon(icono)


#Fondo
fondo = pygame.image.load("./Recursos/FONDO.png")
fondo = pygame.transform.scale(fondo, (860, 600))

#Repartidor
repartidor_img = pygame.image.load("./Recursos/Reparte.png")
repartidor_img = repartidor_img.subsurface((179, 25, 221, 374))
repartidor_img = pygame.transform.scale(repartidor_img, (64, 108))
repartidor_x = 368
repartidor_y = 450
repartidor_cambio_x = 0
repartidor_cambio_y = 0
velocidad_repartidor = 3


def repartidor(x, y):
    pantalla.blit(repartidor_img,(x, y))

# Loop del juego
se_ejecuta = True

while se_ejecuta: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            se_ejecuta = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                repartidor_cambio_x = -velocidad_repartidor
            if event.key == pygame.K_RIGHT:
                repartidor_cambio_x = velocidad_repartidor
            if event.key == pygame.K_UP:
                repartidor_cambio_y = -velocidad_repartidor
            if event.key == pygame.K_DOWN: 
                repartidor_cambio_y = velocidad_repartidor
        if event.type == pygame.KEYUP: 
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                repartidor_cambio_x = 0                   
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                repartidor_cambio_y = 0 

    repartidor_x += repartidor_cambio_x
    repartidor_y += repartidor_cambio_y

    if repartidor_x < 0:
        repartidor_x = 0            
    elif repartidor_x > 736: 
        repartidor_x = 736
    if repartidor_y < 0:
        repartidor_y = 0            
    elif repartidor_y > 492: 
        repartidor_y = 492
        
    pantalla.blit(fondo, (0, 0))
    repartidor(repartidor_x, repartidor_y)
    pygame.display.update()   
    



pygame.quit()
sys.exit()