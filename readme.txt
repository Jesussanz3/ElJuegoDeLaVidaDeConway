Simulación del Juego de la Vida y sus variantes

 

Este repositorio contiene distintos programas desarrollados en Python para simular el Juego de la Vida de Conway y varias extensiones aplicadas a ejemplos inspirados en procesos reales.

Las simulaciones permiten trabajar con tres tipos de teselaciones:

Cuadrangular.
Hexagonal.
Triangular.
 

Dependencias

 

Los programas utilizan las siguientes bibliotecas:

Pygame, para representar gráficamente la matriz, gestionar la interacción con el usuario y ejecutar la simulación.
NumPy, para almacenar y manipular eficientemente los estados de las células mediante matrices.
Las dependencias pueden instalarse con:

pip install pygame numpy

 

Configuración de la matriz

 

En cada programa, las variables filas y columnas permiten establecer las dimensiones de la matriz utilizada en la simulación.

Cada posición de la matriz almacena un número entero que representa el estado de una célula. El significado de cada estado y su color asociado depende del ejemplo ejecutado.

En cada iteración, el estado de una célula se actualiza de acuerdo con las reglas definidas y con los estados de sus células vecinas.

La definición de vecindad depende de la teselación:

En todas las matrices, se consideran vecinas las células que comparten un lado o un vértice.
Una vez calculados todos los nuevos estados, la representación gráfica de la matriz se actualiza. Cada color corresponde a un estado determinado y los bordes de las células permanecen visibles durante toda la simulación.

 

Teselaciones hexagonales y triangulares

 

La representación de matrices hexagonales y triangulares requiere cálculos geométricos adicionales respecto a la matriz cuadrangular.

En particular, es necesario desplazar algunas filas o figuras para conseguir que las células encajen correctamente y evitar que parte de la teselación quede fuera de la ventana. Además, la posición y orientación de las células deben calcularse de forma específica para cada tipo de teselación.

 

Ejecución

 

Para ejecutar una simulación, puede utilizarse el botón Run Python File del editor o el siguiente comando:

python nombre_del_archivo.py

Al iniciar el programa, la simulación permanece pausada para permitir la edición de la configuración inicial.

Los controles disponibles son:

Clic sobre una célula: cambia su estado.
Barra espaciadora: inicia, pausa o reanuda la simulación.
 

Velocidad de la simulación

 

El tiempo transcurrido entre dos iteraciones consecutivas se controla mediante la función:

time.sleep(valor)

Un valor mayor produce una simulación más lenta, mientras que un valor menor reduce el tiempo de espera entre iteraciones.

Por ejemplo:

time.sleep(0.5)

introduce una pausa de medio segundo entre cada actualización de la matriz.
Por ejemplo:

time.sleep(0.5)

introduce una pausa de medio segundo entre cada actualización de la matriz.
