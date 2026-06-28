import math
import pygame
import sys
import numpy as np

def obtener_esquinas_hexagono(cx, cy, tamaño, orientacion='puntiagudo'):
    """Calcula las 6 coordenadas (x, y) de las esquinas de un hexágono."""
    esquinas = []
    for i in range(6):
        if orientacion == 'puntiagudo':
            angulo_deg = 60 * i - 30
        else: # plano
            angulo_deg = 60 * i
            
        angulo_rad = math.radians(angulo_deg)
        x = cx + tamaño * math.cos(angulo_rad)
        y = cy + tamaño * math.sin(angulo_rad)
        esquinas.append((x, y))
        
    return esquinas

def generar_cuadricula_hexagonal(filas, columnas, tamaño):
    """Genera los centros y las esquinas para una matriz de hexágonos (odd-r)."""
    ancho = math.sqrt(3) * tamaño
    altura = 2 * tamaño
    distancia_x = ancho
    distancia_y = 3/4 * altura
    matriz = []
    
    for fila in range(filas):
        for col in range(columnas):
            offset_x = (ancho / 2) if fila % 2 != 0 else 0
            cx = col * distancia_x + offset_x
            cy = fila * distancia_y
            esquinas = obtener_esquinas_hexagono(cx, cy, tamaño)
            
            matriz.append({
                'fila': fila,
                'columna': col,
                'centro': (cx, cy),
                'esquinas': esquinas
            })
            
    return matriz

# --- LÓGICA DE PYGAME ---
if __name__ == "__main__":
    # 1. Inicializar Pygame
    pygame.init()

    # 2. Configurar la ventana
    ANCHO_PANTALLA = 800
    ALTO_PANTALLA = 600
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Mi Cuadrícula Hexagonal")

    # 3. Definir Colores (RGB)
    COLOR_FONDO = (240, 240, 240)  # Gris muy claro
    COLOR_BORDE = (50, 50, 50)     # Gris oscuro
    COLOR_RELLENO = (100, 200, 150) # Verde azulado

    # 4. Parámetros de la cuadrícula
    RADIO = 40
    FILAS = 6
    COLUMNAS = 8
    
    # Desplazamiento inicial para que la cuadrícula no se corte en el borde superior izquierdo
    OFFSET_X = 60
    OFFSET_Y = 60

    # Generamos la información matemática
    mi_cuadricula = generar_cuadricula_hexagonal(FILAS, COLUMNAS, RADIO)
    for i in mi_cuadricula:
        print("Fila de hexágono: ",i['fila'] , ". Columna de hexágono: ", i['columna'],". Centro de hexágono: ", (i['centro'][0]+OFFSET_X, i['centro'][1]+OFFSET_Y))
    juego=np.zeros((FILAS, COLUMNAS))

    # 5. Bucle principal de la aplicación
    corriendo = True
    while corriendo:
        # Control de eventos (como cerrar la ventana)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Rellenar el fondo
        pantalla.fill(COLOR_FONDO)

        # Dibujar cada hexágono de la cuadrícula
        for hex_data in mi_cuadricula:
            # Extraemos las esquinas y aplicamos el desplazamiento (offset)
            esquinas_originales = hex_data['esquinas']
            esquinas_desplazadas = [(x + OFFSET_X, y + OFFSET_Y) for x, y in esquinas_originales]
            
            # Dibujar el relleno del hexágono
            pygame.draw.polygon(pantalla, COLOR_RELLENO, esquinas_desplazadas)
            
            # Dibujar el borde del hexágono (el grosor '2' al final indica que es solo el borde)
            pygame.draw.polygon(pantalla, COLOR_BORDE, esquinas_desplazadas, 2)

        # Actualizar la pantalla
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type==pygame.MOUSEBUTTONDOWN: ##Este código es para cambiar el estado de la célula que estés seleccionando (de vivo a muerto, y viceversa)
                posX, posY = pygame.mouse.get_pos() ##Estas variables guardan la posición del cursor cuando pulsamos el ratón
                print("posX: ",posX,". posY: ",posY)
                """
                Calcula qué hexágono está más cerca de la posición del ratón.
                """
                hexagono_seleccionado = None
                distancia_minima = float('inf')

                for hex_data in mi_cuadricula:
                    # IMPORTANTE: Los centros matemáticos no tienen el offset de la pantalla.
                    # Tenemos que sumar el offset para que coincida con lo que vemos en Pygame.
                    cx_pantalla = hex_data['centro'][0] + OFFSET_X
                    cy_pantalla = hex_data['centro'][1] + OFFSET_Y

                    # Calculamos la distancia euclidiana entre el ratón y el centro del hexágono
                    distancia = math.hypot(posX - cx_pantalla, posY - cy_pantalla)

                    # Si la distancia es menor que el radio (aproximadamente) y es la más corta encontrada
                    if distancia < distancia_minima and distancia < (RADIO * 0.9): 
                        distancia_minima = distancia
                        hexagono_seleccionado = hex_data
                if hexagono_seleccionado:
                    print("hexágono [",hexagono_seleccionado['fila'],"][",hexagono_seleccionado['columna'],"]")
                else:
                    print("Has clickeado fuera de los hexágonos")

    # Salir de forma limpia
    pygame.quit()
    sys.exit()