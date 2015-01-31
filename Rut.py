import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Declaramos las constantes de la simulación
m = 6.68 * (10 ** -27)
qe = 1.6 * (10 ** -19)
q = 2 * qe
M = 2.822 * (10 ** -25)
Q = 79 * qe
K = 8.98755 * (10 ** 9)
v = 1.5 * (10 ** 7)
a = abs(q * Q * K) / (m * (v ** 2))
En = 0.5 * m * (v**2)

# Declaramos las listas que vamos a usar, y el número de iteraciones
i_deflex = float(input('Cual es la precision de la deflexion? (En grados) '))
n_intervalos = int(180/i_deflex)
deflex_caja = list()
ang_deflex = list()
sigma = list()
sigma_t = list()
deg_to_rad = math.pi/180

# Llenamos las listas de variables independientes
for cont in range(0,n_intervalos):
    ang_deflex.insert(cont,(i_deflex/2) + (i_deflex * cont))
    deflex_caja.insert(cont,0)

# Introducimos los parámetros de la simulación
n_sucesos = int(input('Cuanto sucesos? '))
b_max = float(input('Introduzca el radio en Amstrong del orificio de salida '))
b_max = b_max * (10 ** -10)
random.seed()
max_angle = 2 * np.pi
coordinates = []
print('Inicializando...')

# En este bucle generamos las coordenadas que vamos a usar multiplicando el radio del orificio de salida y el ángulo máximo
# por un aleatorio entre 0 y 1, así obtenemos coordenadas polares que después pasaremos a cartesianas
for cont in range(n_sucesos):
    r = random.random() * b_max
    angle = random.random() * max_angle
    x,y = np.cos(angle) * r,np.sin(angle) * r
    coordinates.append([x,y])

porcentaje_completado = 0

for variable_que_no_volvera_a_ser_usada in range(0,n_sucesos):
    pprov = variable_que_no_volvera_a_ser_usada * (100/n_sucesos)
    if int(pprov) != porcentaje_completado:
        print(int(pprov), '% completado...')
        porcentaje_completado = int(pprov)
    x,y = coordinates[variable_que_no_volvera_a_ser_usada][0],coordinates[variable_que_no_volvera_a_ser_usada][1]
    b = ((x ** 2) + (y ** 2)) ** 0.5
    E = (((b/a)**2)+1)**0.5
    alfa = math.atan(math.sqrt((E ** 2) - 1))
    deflex = (math.pi - (2*alfa)) * (180/math.pi)
    for cont in range(0,n_intervalos):
        if ((deflex >= (ang_deflex[cont] - (i_deflex/2))) & (deflex < (ang_deflex[cont] + (i_deflex/2)))):
            deflex_caja[cont] = deflex_caja[cont] + 1
        if deflex == 180:
            print('b era igual a 0!')

F = n_sucesos / (b_max ** 2) * np.pi 

for cont in range(n_intervalos):
    sigma.insert(cont,deflex_caja[cont]/(F* (2*math.pi) * math.sin(ang_deflex[cont]*deg_to_rad) * (i_deflex*deg_to_rad)))
    sigma_t.insert(cont,((((q*Q*K)/(2*En)))**2)*(1/((math.sin((ang_deflex[cont]*deg_to_rad)/2))**4))*0.25)
    
for cont in range(n_intervalos):
    print (ang_deflex[cont], '+-' + str(i_deflex/2),'//',deflex_caja[cont],'//',sigma[cont],'//',sigma_t[cont])

plt.close()
plt.plot(ang_deflex,sigma,'g-',ang_deflex,sigma_t,'r-',ang_deflex,sigma,'y^')
plt.title('Sección eficaz frente al ángulo de deflexión')
plt.xlabel('Ángulo de deflexión')
plt.ylabel('Sección eficaz')
plt.axis([0,180,0,max(sigma)])
plt.show()
