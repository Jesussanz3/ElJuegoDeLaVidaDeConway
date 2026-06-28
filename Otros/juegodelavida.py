import pygame ##pip install pygame   ##Para instalarlo: pip install pygame --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org
import numpy as np ##Para instalarlo: pip install numpy --trusted-host pypi.org --trusted-host files.pythonhosted.org
##Desde visual studio code, ctrl + shift + p. -->  Python: select environment --> Python 3.13   . Instrucciones dadas por Gemini
import time
pygame.init()
width, height = 750, 750 #TENGO QUE LIMITAR LA PANTALLA PARA QUE VEAMOS TODOS LOS BORDES
screen = pygame.display.set_mode((height, width))
##HACER QUE SI PULSAS EN UNA CELDA VIVA PASE A MUERTA, Y VER SI SEGUIR POR EL OTRO LADO HACE QUE ALGUNOS AUTÓMATAS NO SALEN COMO ESPERÁBAMOS
bg = 25, 25, 25
screen.fill(bg) ##El color por defecto es negro

nxC, nyC = 50, 50 ##Tenemos 50x50 celdas
dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC)) ##Las células todas están muertas al principio

#gameState[5, 3] = 1
#gameState[5, 4] = 1
#gameState[5, 5] = 1

#gameState[21, 21] = 1
#gameState[22, 22] = 1
#gameState[23, 23] = 1
#gameState[21, 23] = 1
#gameState[20, 23] = 1

pauseExect = False

while True: ##Para que la pantalla se muestre indefinidamente
    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)
    ev = pygame.event.get()
    for event in ev: ##¿PODRÍA HACER QUE CADA ITERACIÓN SE HAGA AL CLICKAR?
        if event.type == pygame.KEYDOWN: ##Si pulsamos la tecla de la flecha de abajo, pausamos y seguimos con el juego de la vida, respectivamente
            pauseExect = not pauseExect
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]
    for y in range (0, nxC):
        for x in range (0, nyC): ##SI NOS PASAMOS, VAMOS AL MÓDULO. CAMBIAR ESTO LUEGO POR SIMPLEMENTE NO CAMBIARLO
            if not pauseExect:
                n_heigh = gameState[(x-1) % nxC,(y-1) % nyC] + gameState[(x-1) % nxC,(y) % nyC] + gameState[(x-1) % nxC,(y+1) % nyC] + gameState[(x) % nxC,(y-1) % nyC] + gameState[(x) % nxC,(y+1) % nyC] + gameState[(x+1) % nxC,(y-1) % nyC] + gameState[(x+1) % nxC,(y) % nyC] + gameState[(x+1) % nxC,(y+1) % nyC]
                
                if gameState[x, y] == 0 and n_heigh == 3:
                    newGameState[x, y] = 1
                if gameState[x, y] == 1 and (n_heigh < 2 or n_heigh > 3):
                    newGameState[x, y] = 0
            poly=[((x) * dimCW, y * dimCH),
                ((x+1) * dimCW, y * dimCH),
                ((x+1) * dimCW, (y+1) * dimCH),
                ((x) * dimCW, (y+1) * dimCH)]
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    gameState = np.copy(newGameState)
    pygame.display.flip()