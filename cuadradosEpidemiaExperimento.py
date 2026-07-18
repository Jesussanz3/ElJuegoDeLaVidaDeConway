import numpy as np ##Para trabajar más fácilmente con matrices
import time ##Para poder usar la función time.sleep para que haya una pausa entre cada iteración del juego de la vida
import pygame ##Para usar la pantalla en la que se verá el juego de la vida en funcionamiento
##pip install pygame   ##Para instalarlo: pip install pygame --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org
import random

##"filas" y "columnas" tienen que ser enteros mayores que 0
filas=20
columnas=20
juego=np.zeros((filas, columnas)) ##Aquí decidimos el tamaño del plano

##Aquí decidimos qué células empiezan vivas. Valor 0: la célula está muerta. Valor 1: la célula está viva. 
#Pongo el ejemplo de la nave que se mueve diagonalmente siempre.
#juego[4, 6]=0
#print("Juego: ", juego[4, 6])
#juego[4, 6]=1  
#print("Juego: ", juego[4, 6])
#juego[4, 6]=-1  
#print("Juego: ", juego[4, 6])

#juego[5, 4]=1 
#juego[5, 6]=1 
#juego[6, 5]=1 
#juego[6, 6]=1 

pygame.init()
anchura=800 ##Dimensiones de la pantalla
altura=700
screen = pygame.display.set_mode((anchura, altura)) ##El programá hará una pantalla del tamaño adecuado
pygame.display.set_caption("")
#screen.fill((25, 25, 25)) 
dimCW = anchura / filas    ##Las dimensiones de la pantalla se reparten entre todas las células
dimCH = altura / columnas

#c=0 ##Este número será el contador de las iteraciones
#print("Iteración ", c,": ") ##Esto imprimiría en la terminar los valores de las células (0: muerta. 1: viva)
#print(juego)

celdasvivasjovenes=0
celdasvivasmaduras=0
for i in range (0, filas):
    for j in range (0, columnas):
        prob=random.random()
        #print("prob: ", prob)
        if prob<0.75:
            prob2=random.random()
            if prob2<0.5:
                juego[i,j]=1
                celdasvivasjovenes=celdasvivasjovenes+1
            else:
                juego[i,j]=2
                celdasvivasmaduras=celdasvivasmaduras+1
        #print("juego[",i,", ",j,"]: ",juego[i,j])
celdasmuertas=filas*columnas-celdasvivasjovenes-celdasvivasmaduras
print("Iteración 0. Celdas vivas: ", (celdasvivasjovenes+celdasvivasmaduras)/(filas*columnas),". Celdas vivas jóvenes: ",celdasvivasjovenes/(filas*columnas),". Celdas vivas maduras: ",celdasvivasmaduras/(filas*columnas),". Celdas muertas: ",celdasmuertas/(filas*columnas))
entropia=0-(celdasvivasjovenes/(filas*columnas))*np.log(celdasvivasjovenes/(filas*columnas))-(celdasvivasmaduras/(filas*columnas))*np.log(celdasvivasmaduras/(filas*columnas))-(celdasmuertas/(filas*columnas))*np.log(celdasmuertas/(filas*columnas))
entropia=entropia/np.log(3)
print("Entropía: ", entropia)
juegocopia=juego.copy()
screen.fill((25, 25, 25)) ##El color por defecto es gris muy oscuro ##Las células tendran un color gris muy oscuro al estar muertas
dia=0

for celX in range(0, filas):
    for celY in range(0, columnas):
        poly=[((celX) * dimCW+2, celY * dimCH+2), ##Aquí se calculan los límites del cuadrado de la célula con la que estamos tratando. Esquina superior izquierda
        ((celX+1) * dimCW-2, celY * dimCH+2), #Esquina inferior izquierda
        ((celX+1) * dimCW-2, (celY+1) * dimCH-2), #Esquina superior derecha
        ((celX) * dimCW+2, (celY+1) * dimCH-2)]  #Esquina inferior derecha
        if juegocopia[celX, celY]==1:
            pygame.draw.polygon(screen, (0, 128, 0), poly, 0)
        else:
            if juegocopia[celX, celY]==0:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
            else:
                pygame.draw.polygon(screen, (0, 255, 0), poly, 0)
pygame.display.flip()
pausa=True ##Esta variable guardará si el juego está o no en pausa
corriendo=True
while corriendo:
    for ev in pygame.event.get():
        if ev.type==pygame.KEYDOWN: ##Al pulsar una tecla, el juego se pausa o continúa
            if ev.key==pygame.K_SPACE: ##Podemos hacer que el juego pause o continue cuando se pulse una tecla concreta.
                pausa = not pausa 
        if ev.type==pygame.MOUSEBUTTONDOWN: ##Este código es para cambiar el estado de la célula que estés seleccionando (de vivo a muerto, y viceversa)
            posX, posY = pygame.mouse.get_pos() ##Estas variables guardan la posición del cursor cuando pulsamos el ratón
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH)) ##Con las dimensiones de la pantalla y la cantidad de células, calculamos en qué célula hemos pulsado.
            poly=[((celX) * dimCW+2, celY * dimCH+2), ##Aquí se calculan los límites del cuadrado de la célula con la que estamos tratando. Esquina superior izquierda
            ((celX+1) * dimCW-2, celY * dimCH+2), #Esquina inferior izquierda
            ((celX+1) * dimCW-2, (celY+1) * dimCH-2), #Esquina superior derecha
            ((celX) * dimCW+2, (celY+1) * dimCH-2)]  #Esquina inferior derecha
            if juegocopia[celX, celY]==1:
                juego[celX, celY]=0
                juegocopia[celX, celY]=0
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
            else:
                if juegocopia[celX, celY]==0:
                    juego[celX, celY]=2
                    juegocopia[celX, celY]=2
                    pygame.draw.polygon(screen, (0, 255, 0), poly, 0)
                else:
                    juego[celX, celY]=1
                    juegocopia[celX, celY]=1
                    pygame.draw.polygon(screen, (0, 128, 0), poly, 0)
            pygame.display.flip()
        if ev.type==pygame.QUIT: ##Esto da un pequeño error al cerrar, pero no creo que sea relevante
            corriendo=False
    #c=c+1
    if not pausa:
        celdasvivasjovenes=0
        celdasvivasmaduras=0
        actividad=0
        screen.fill((25, 25, 25))
        for i in range(0, filas):
            for j in range(0, columnas):
                vecinosvivos=0
                for k in range (-1, 2):
                    for l in range (-1, 2):
                        if not (k==0 and l==0):
                            if juego[(i+k)%filas, (j+l)%columnas]>0:
                                vecinosvivos=vecinosvivos+1
                if juego[i, j]==0:
                    if vecinosvivos==3:
                        juegocopia[i, j]=1
                        celdasvivasjovenes=celdasvivasjovenes+1
                        actividad=actividad+1
                else:
                    if vecinosvivos==2 or vecinosvivos==3:
                        juegocopia[i, j]=2
                        celdasvivasmaduras=celdasvivasmaduras+1
                        if juego[i,j]==1:
                            actividad=actividad+1
                    else:
                        juegocopia[i, j]=0       
                        actividad=actividad+1                 
                poly=[((i) * dimCW+2, j * dimCH+2), ##Aquí se calculan los límites del cuadrado de la célula con la que estamos tratando. Esquina superior izquierda
                    ((i+1) * dimCW-2, j * dimCH+2), #Esquina inferior izquierda
                    ((i+1) * dimCW-2, (j+1) * dimCH-2), #Esquina superior derecha
                    ((i) * dimCW+2, (j+1) * dimCH-2)]  #Esquina inferior derecha
                if juegocopia[i, j] == 1:
                    pygame.draw.polygon(screen, (0, 128, 0), poly, 0) ##Si la célula está muerta, los bordes del cuadrado de esa célula se mantendrán de color gris oscuro (el cuadrado de la célula se pinta de blanco)
                else:
                    if juegocopia[i, j] == 0:
                        pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
                    else:
                        pygame.draw.polygon(screen, (0, 255, 0), poly, 0) ##Si la célula está viva, el cuadrado de la célula se pinta de blanco
        juego=juegocopia.copy() ##Actualizamos los datos del juego de la vida
        dia=dia+1
        celdasmuertas=(filas*columnas)-celdasvivasjovenes-celdasvivasmaduras
        print("Iteración ", dia,". Celdas vivas: ", (celdasvivasjovenes+celdasvivasmaduras)/(filas*columnas),". Celdas vivas jóvenes: ",celdasvivasjovenes/(filas*columnas),". Celdas vivas maduras: ",celdasvivasmaduras/(filas*columnas),". Celdas muertas: ",celdasmuertas/(filas*columnas),". Actividad: ", actividad/(filas*columnas))
        entropia=0-(celdasvivasjovenes/(filas*columnas))*np.log(celdasvivasjovenes/(filas*columnas))-(celdasvivasmaduras/(filas*columnas))*np.log(celdasvivasmaduras/(filas*columnas))-(celdasmuertas/(filas*columnas))*np.log(celdasmuertas/(filas*columnas))
        entropia=entropia/np.log(3)
        print("Entropía: ", entropia)
        pygame.display.flip() ##Se dibujan los cuadrados de la última iteración
        if dia==9 or dia==10 or dia==49 or dia ==50 or dia==99 or dia==100:
            time.sleep(0.5)
        else:
            time.sleep(0.1) ##Esperamos un tiempo hasta la siguiente iteración. El juego no termina a menos que pulsemos Ctrl+C para parar el programa.
pygame.quit()
