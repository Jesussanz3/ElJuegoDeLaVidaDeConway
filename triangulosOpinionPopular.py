import math
import pygame
import sys
import numpy as np
import time

def obtener_esquinas_triangulo(cx, cy, tamaño, apuntando_arriba=True):
    """
    Calcula las 3 coordenadas (x, y) de un triángulo equilátero
    basándose en su centro geométrico (baricentro).
    """
    esquinas = []
    # El ángulo inicial cambia 180 grados si el triángulo apunta hacia abajo
    angulo_base = 90 if apuntando_arriba else 270
    
    for i in range(3):
        # 120 grados de separación entre vértices (360 / 3)
        angulo_deg = angulo_base + i * 120
        angulo_rad = math.radians(angulo_deg)
        
        # Nota: En Pygame la Y crece hacia abajo, por lo que restamos para 'arriba'
        x = cx + tamaño * math.cos(angulo_rad)
        y = cy - tamaño * math.sin(angulo_rad)
        esquinas.append((x, y))
        
    return esquinas

def generar_cuadricula_triangular(filas, columnas, tamaño):
    """
    Genera los centros, esquinas y orientación de una matriz de triángulos.
    """
    # Altura de un triángulo equilátero usando el tamaño (radio al vértice)
    # El lado del triángulo es tamaño * sqrt(3)
    ancho_base = tamaño * math.sqrt(3)
    
    # Distancia horizontal entre un triángulo que apunta hacia arriba y el siguiente hacia abajo
    distancia_x = ancho_base / 2
    # Distancia vertical entre filas de triángulos
    distancia_y = tamaño * 1.5

    matriz = []
    
    for fila in range(filas):
        for col in range(columnas):
            # Calcular el centro (cx, cy)
            cx = col * distancia_x
            
            # Si la fila es impar, desplazamos horizontalmente para encajar los huecos
            #if fila % 2 != 0:
            #    cx += distancia_x / 2
                
            cy = fila * distancia_y
            
            # Alternar la orientación (hacia arriba o hacia abajo)
            # Depende de si la suma de la fila y la columna es par o impar
            apuntando_arriba = (fila + col) % 2 == 0
            
            # Corregir levemente la altura del centro para los invertidos para que encajen perfectos
            cy_corregido = cy
            if not apuntando_arriba:
            #    # Ajuste geométrico para el baricentro invertido
                cy_corregido = cy - (tamaño / 2)
            #else:
            #    cy_corregido = cy - (tamaño / 6)

            esquinas = obtener_esquinas_triangulo(cx, cy_corregido, tamaño, apuntando_arriba)
            
            matriz.append({
                'fila': fila,
                'columna': col,
                'centro': (cx, cy_corregido),
                'esquinas': esquinas
            })
            
    return matriz

def detectar_triangulo_clickeado(pos_raton, cuadricula, offset_x, offset_y, tamaño):
    """
    Encuentra el triángulo más cercano al click del ratón.
    """
    mx, my = pos_raton
    triangulo_seleccionado = None
    distancia_minima = float('inf')

    for tri_data in cuadricula:
        cx_pantalla = tri_data['centro'][0] + offset_x
        cy_pantalla = tri_data['centro'][1] + offset_y

        distancia = math.hypot(mx - cx_pantalla, my - cy_pantalla)

        # Usamos un radio de colisión un poco menor que el tamaño del vértice
        if distancia < distancia_minima and distancia < (tamaño * 0.7):
            distancia_minima = distancia
            triangulo_seleccionado = tri_data

    return triangulo_seleccionado

# --- LÓGICA DE PYGAME ---
if __name__ == "__main__":
    pygame.init()

    pantalla = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("")

    # Colores
    COLOR_FONDO = (240, 240, 240)
    COLOR_BORDE = (50, 50, 50)
    COLOR_RELLENO = (0, 0, 255) # Rojo para el clickeado

    # Parámetros geométricos
    TAMAÑO_TRIANGULO = 40  # Distancia del centro a sus vértices
    FILAS = 7
    COLUMNAS = 10
    OFFSET_X = 80
    OFFSET_Y = 80

    mi_cuadricula = generar_cuadricula_triangular(FILAS, COLUMNAS, TAMAÑO_TRIANGULO)
    juego=np.zeros((FILAS, COLUMNAS))
    #juego[0, 1]=1.0
    #juego[2, 1]=1.0
    #juego[1, 0]=1.0

    tri_activo = None
    juegocopia=np.zeros((FILAS, COLUMNAS))
    for i in range(0, FILAS):
        for j in range(0, COLUMNAS):
            juegocopia[i, j]=juego[i, j]
    pausa=True
    pantalla.fill(COLOR_FONDO)
    for tri_data in mi_cuadricula:
        esquinas_desplazadas = [(x + OFFSET_X, y + OFFSET_Y) for x, y in tri_data['esquinas']]
    
    # Determinar color

    # Dibujar Triángulo
        f=tri_data['fila']
        c=tri_data['columna']
        if juegocopia[f, c]==1:
            pygame.draw.polygon(pantalla, COLOR_RELLENO, esquinas_desplazadas)
        else:
            pygame.draw.polygon(pantalla, (255, 0, 0), esquinas_desplazadas)
        pygame.draw.polygon(pantalla, COLOR_BORDE, esquinas_desplazadas, 2)
    pygame.display.flip()
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type==pygame.KEYDOWN:
                if evento.key==pygame.K_SPACE: ##Podemos hacer que el juego pause o continue cuando se pulse una tecla concreta.
                    pausa = not pausa
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    pos_raton = pygame.mouse.get_pos()
                    tri_activo = detectar_triangulo_clickeado(pos_raton, mi_cuadricula, OFFSET_X, OFFSET_Y, TAMAÑO_TRIANGULO)
                    if tri_activo:
                        f=tri_activo['fila']
                        c=tri_activo['columna']
                        esquinas=tri_activo['esquinas']
                        esquinas_desplazadas = [(x + OFFSET_X, y + OFFSET_Y) for x, y in esquinas]
                        if juegocopia[f, c]==0:
                            juego[f, c]=1
                            juegocopia[f, c]=1
                            pygame.draw.polygon(pantalla, COLOR_RELLENO, esquinas_desplazadas)
                        else:
                            juego[f, c]=0
                            juegocopia[f, c]=0
                            pygame.draw.polygon(pantalla, (255, 0, 0), esquinas_desplazadas)
                        pygame.draw.polygon(pantalla, COLOR_BORDE, esquinas_desplazadas, 2)
                        pygame.display.flip()

            if evento.type == pygame.QUIT:
                corriendo = False

        if not pausa:
            for i in range(0, FILAS):
                for j in range(0, COLUMNAS):
                    if (i+j)%2==0:
                        vecinosvivos=juego[(i+1)%FILAS, j] + juego[i, (j-1)%COLUMNAS] + juego[i, (j+1)%COLUMNAS]
                    else:
                        vecinosvivos=juego[(i-1)%FILAS, j] + juego[i, (j-1)%COLUMNAS] + juego[i, (j+1)%COLUMNAS]
                    if vecinosvivos>1:
                        juegocopia[i, j]=1
                    if vecinosvivos<=1:
                        juegocopia[i, j]=0
            # Renderizado
            pantalla.fill(COLOR_FONDO)

            for tri_data in mi_cuadricula:
                esquinas_desplazadas = [(x + OFFSET_X, y + OFFSET_Y) for x, y in tri_data['esquinas']]
                
                # Determinar color
                f=tri_data['fila']
                c=tri_data['columna']
                if juegocopia[f, c]==1:
                    color_actual = COLOR_RELLENO
                else:
                    color_actual = (255, 0, 0)

                # Dibujar Triángulo
                pygame.draw.polygon(pantalla, color_actual, esquinas_desplazadas)
                pygame.draw.polygon(pantalla, COLOR_BORDE, esquinas_desplazadas, 2)

            pygame.display.flip()
                        #for ev in pygame.event.get():
            for i in range(0, FILAS):
                for j in range(0, COLUMNAS):
                    juego[i, j]=juegocopia[i, j]
            time.sleep(1)


    pygame.quit()
    sys.exit()