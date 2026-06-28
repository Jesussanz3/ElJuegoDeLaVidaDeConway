import numpy as np ##Para trabajar más fácilmente con matrices
import time ##Para poder usar la función time.sleep para que haya una pausa entre cada iteración del juego de la vida
import pygame ##Para usar la pantalla en la que se verá el juego de la vida en funcionamiento
##pip install pygame   ##Para instalarlo: pip install pygame --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org

##"filas" y "columnas" tienen que ser enteros mayores que 0
filas=20
columnas=20
juego=np.zeros((filas, columnas)) ##Aquí decidimos el tamaño del plano

##Aquí decidimos qué células empiezan vivas. Valor 0: la célula está muerta. Valor 1: la célula está viva. 
#Pongo el ejemplo de la nave que se mueve diagonalmente siempre.

pygame.init()
anchura=800 ##Dimensiones de la pantalla
altura=700
screen = pygame.display.set_mode((anchura, altura)) ##El programá hará una pantalla del tamaño adecuado
#screen.fill((25, 25, 25)) 
dimCW = anchura / filas    ##Las dimensiones de la pantalla se reparten entre todas las células
dimCH = altura / columnas

#c=0 ##Este número será el contador de las iteraciones
#print("Iteración ", c,": ") ##Esto imprimiría en la terminar los valores de las células (0: muerta. 1: viva)
#print(juego)

juegocopia=juego.copy()
pausa=True ##Esta variable guardará si el juego está o no en pausa
while True:
    screen.fill((25, 25, 25)) ##El color por defecto es gris muy oscuro ##Las células tendran un color gris muy oscuro al estar muertas
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT: ##Esto da un pequeño error al cerrar, pero no creo que sea relevante
            pygame.quit()
        if ev.type==pygame.KEYDOWN: ##Al pulsar una tecla, el juego se pausa o continúa
            #if ev.key==pygame.K_SPACE: ##Podemos hacer que el juego pause o continue cuando se pulse una tecla concreta.
            pausa = not pausa 
        if ev.type==pygame.MOUSEBUTTONDOWN: ##Este código es para cambiar el estado de la célula que estés seleccionando (de vivo a muerto, y viceversa)
            posX, posY = pygame.mouse.get_pos() ##Estas variables guardan la posición del cursor cuando pulsamos el ratón
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH)) ##Con las dimensiones de la pantalla y la cantidad de células, calculamos en qué célula hemos pulsado.
            juegocopia[celX, celY] = not juegocopia[celX, celY] ##Cuando pulsemos en una célula, cambiaremos su estado (de viva a muerta y viceversa)
    #c=c+1
    for i in range(0, filas):
        for j in range(0, columnas):
            if not pausa:
                if filas%2==0:
                    vecinosvivos=juego[(i-1)%filas, (j-1)%columnas] + juego[(i-1)%filas, j] + juego[i, (j-1)%columnas] + juego[i, (j+1)%columnas] +  juego[(i+1)%filas, (j-1)%columnas] + juego[(i+1)%filas, j] ##Esta variable calcula el número de vecinos vivos de cada célula
                else:
                    vecinosvivos=juego[(i-1)%filas, j] + juego[(i-1)%filas, (j+1)%columnas] +  juego[i, (j-1)%columnas] + juego[i, (j+1)%columnas] + juego[(i+1)%filas, j] + juego[(i+1)%filas, (j+1)%columnas]
                if juego[i, j]==0: ##Si la célula estaba muerta
                    if  vecinosvivos== 3.0:
                        juegocopia[i, j]=1 #Si una célula muerta tiene exactamente 3 células vecinas vivas, revive
                else: ##Si la célula estaba viva
                    if vecinosvivos<2 or vecinosvivos>3:
                        juegocopia[i, j]=0 #Si una célula viva tiene menos de 2 o más de 3 células vecinas vivas, muere por soledad o por sobrepoblación
            poly=[((i) * dimCW+2, j * dimCH+2), ##Aquí se calculan los límites del cuadrado de la célula con la que estamos tratando. Esquina superior izquierda
                ((i+1) * dimCW-2, j * dimCH+2), #Esquina inferior izquierda
                ((i+1) * dimCW-2, (j+1) * dimCH-2), #Esquina superior derecha
                ((i) * dimCW+2, (j+1) * dimCH-2)]  #Esquina inferior derecha
            if juegocopia[i, j] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1) ##Si la célula está muerta, los bordes del cuadrado de esa célula se mantendrán de color gris oscuro (el cuadrado de la célula se pinta de blanco)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0) ##Si la célula está viva, el cuadrado de la célula se pinta de blanco
    juego=juegocopia.copy() ##Actualizamos los datos del juego de la vida
    #print("Iteración ", c,": ") ##Esto imprimiría en la terminar los valores de las células (0: muerta. 1: viva)
    #print(juego)
    pygame.display.flip() ##Se dibujan los cuadrados de la última iteración
    time.sleep(0.1) ##Esperamos un tiempo hasta la siguiente iteración. El juego no termina a menos que pulsemos Ctrl+C para parar el programa.
