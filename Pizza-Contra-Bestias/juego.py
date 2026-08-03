from random import randint

import pygame
import random
# Inicializamos la liberia pygame, junto a sus modulos y algunos de dichos modulos inician sdl
# que es una libreria de c que va a hacer que nuestro jugeo funcione
pygame.init()
# Ademas inicializamos el modulo que le permite a pygame reoproducir audio
pygame.mixer.init()

# creamos la pantalla con unas dimensiones de 1280x720 y le ponemos de titulo Pizza contra Bestias
pantalla = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont(None, 40)
pygame.display.set_caption("Pizza contra Bestias")

imagen = pygame.image.load("recursos_juego/pizza.png")
pygame.display.set_icon(imagen)

# Pizza disparada
ancho_pizza = 32
largo_pizza = 32
pizza_imagen = pygame.image.load("recursos_juego/pizza.png")
pizza_imagen = pygame.transform.scale(pizza_imagen, (ancho_pizza, largo_pizza))

datos_pizza = {}
inicio_contador = 0
tiempo_entre_disparos = 2400
velocidad_pizza = 1

# Fondo del Juego
fondo = pygame.image.load("recursos_juego/fondo.png")
fondo = pygame.transform.scale(fondo, (1280, 720))

# Repartidor
ancho_personaje = 75
largo_personaje = 150
repartidor_imagen = pygame.image.load("recursos_juego/repartidor.png")
repartidor_imagen = pygame.transform.scale(repartidor_imagen, (ancho_personaje, largo_personaje))
repartidor_x = (1280 - ancho_personaje) / 2
repartidor_y = (720 - largo_personaje) / 2 + 235

# Sonidos Juego
sonido_disparo = pygame.mixer.Sound("recursos_juego/disparo.mp3")
sonido_victoria = pygame.mixer.Sound("recursos_juego/victoria.mp3")
sonido_derrota = pygame.mixer.Sound("recursos_juego/derrota.mp3")

# Animal
# Funciones para elegir un animal entre 5 y cargar las imagenes las unicas funciones que no estan en las funciones del juego porque no la peudo crear en la seccion del resto de funcione porque necesito usarla antes
def elegir_animal(lista_animales):
    animal_elegido = random.choice(lista_animales)
    return animal_elegido

def cargar_imagen_animal():
    animal_elegido = elegir_animal(lista_animales)
    imagen_animal = pygame.image.load(f"recursos_juego/{animal_elegido}")
    imagen_animal = pygame.transform.scale(imagen_animal, (ancho_animal, largo_animal))
    return imagen_animal

lista_animales = ["gato.png", "leon.png", "toro.png", "perro.png"]

ancho_animal = 60
largo_animal = 120
animal_x = randint(0, 1280 - ancho_animal)
animal_y = 0
animales = {
    0: {
        "x": animal_x,
        "y": animal_y,
        "imagen": cargar_imagen_animal()
    }
}
velocidad_animal = 0.2
contador_animales = 0
cantidad_animales = 1
tiempo_entre_animales = 2200

# Vidas del repartidor
lista_corazones = ["corazon.png", "corazon.png", "corazon.png"]
corazon_x = 15
corazon_y = 15
ultimo_golpe = 0
tiempo_invulnerabilidad = 1500
# Funciones del juego
def cargar_imagen_corazon(lista_corazones):
    lista_surface_corazones = []
    for corazon in lista_corazones:
        imagen_corazon = pygame.image.load(f"recursos_juego/{corazon}")
        imagen_corazon = pygame.transform.scale(imagen_corazon, (30, 30))
        lista_surface_corazones.append(imagen_corazon)
    return lista_surface_corazones

def pizzero(x, y):
    pantalla.blit(repartidor_imagen, (x, y))

def animal(obj_animal):
    pantalla.blit(obj_animal["imagen"], (obj_animal["x"], obj_animal["y"]))

def pizza(obj_pizza):
    pantalla.blit(pizza_imagen, (obj_pizza["x"], obj_pizza["y"]))

def derrota(imagen_derrota):
    pantalla.blit(imagen_derrota, (0, 0))

def victoria(imagen_victoria):
    pantalla.blit(imagen_victoria, (0, 0))

def cargar_imagen_derrota():
    imagen_derrota = pygame.image.load("recursos_juego/derrota.png")
    imagen_derrota = pygame.transform.scale(imagen_derrota, (1280, 720))
    return imagen_derrota

def cargar_imagen_victoria():
    imagen_victoria = pygame.image.load("recursos_juego/victoria.png")
    imagen_victoria = pygame.transform.scale(imagen_victoria, (1280, 720))
    return imagen_victoria

def corazon(lista_corazones):
   sumar_eje_x = 0
   for corazon in lista_corazones:
       pantalla.blit(corazon, (corazon_x + sumar_eje_x, corazon_y))
       sumar_eje_x += 35

def crear_animal():
    lado = randint(0, 3)

    if lado == 0:
        animal_x = randint(0, 1280 - ancho_animal)
        animal_y = 0 - largo_animal

    if lado == 1:
        animal_x = randint(0, 1280 - ancho_animal)
        animal_y = 720 + largo_animal

    if lado == 2:
        animal_x = 0 - ancho_animal
        animal_y = randint(0, 720 - largo_animal)

    if lado == 3:
        animal_x = 1280 + ancho_animal
        animal_y = randint(0, 720 - largo_animal)

    return {
        "x": animal_x,
        "y": animal_y,
        "imagen": cargar_imagen_animal()
    }

def mover_animales():
    for clave in animales:
        animal_actual = animales[clave]

        dx = repartidor_x - animal_actual["x"]
        dy = repartidor_y - animal_actual["y"]
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia > 0:
            animal_actual["x"] += (dx / distancia) * velocidad_animal
            animal_actual["y"] += (dy / distancia) * velocidad_animal

def comprobar_colision_pizza_animales():
    if datos_pizza != {}:
        rect_pizza = pygame.Rect(datos_pizza["x"], datos_pizza["y"], ancho_pizza, largo_pizza)
        animal_a_eliminar = None

        for aninal in animales:
            animal_actual = animales[aninal]
            rect_animal = pygame.Rect(animal_actual["x"], animal_actual["y"], ancho_animal, largo_animal)

            if rect_pizza.colliderect(rect_animal):
                animal_a_eliminar = aninal
                datos_pizza.clear()

        if animal_a_eliminar != None:
            del animales[animal_a_eliminar]

def comprobar_colision_animales_repartidor(lista_corazones):
    global ultimo_golpe
    tiempo_actual = pygame.time.get_ticks()
    rect_repartidor = pygame.Rect(repartidor_x, repartidor_y, ancho_personaje, largo_personaje)
    for aninal in animales:
        animal_actual = animales[aninal]
        rect_animal = pygame.Rect(animal_actual["x"], animal_actual["y"], ancho_animal, largo_animal)

        if rect_repartidor.colliderect(rect_animal):
            if tiempo_actual - ultimo_golpe >= tiempo_invulnerabilidad:
                ultimo_golpe = tiempo_actual
                if len(lista_corazones) > 0:
                    lista_corazones.pop()
            break


def buscar_animal_mas_cercano(repartidor_x, repartidor_y, animales):
    animal_mas_cercano = None
    distancia_mas_cercana = None

    centro_repartidor_x = repartidor_x + ancho_personaje / 2
    centro_repartidor_y = repartidor_y + largo_personaje / 2

    for clave in animales:
        animal_actual = animales[clave]

        centro_animal_x = animal_actual["x"] + ancho_animal / 2
        centro_animal_y = animal_actual["y"] + largo_animal / 2

        dx = centro_animal_x - centro_repartidor_x
        dy = centro_animal_y - centro_repartidor_y
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia_mas_cercana == None or distancia < distancia_mas_cercana:
            distancia_mas_cercana = distancia
            animal_mas_cercano = {
                "centro_x": centro_animal_x,
                "centro_y": centro_animal_y
            }

    return animal_mas_cercano

def disparar_pizza(repartidor_x, repartidor_y):
    animal_objetivo = buscar_animal_mas_cercano(repartidor_x, repartidor_y, animales)
    obj_pizza = {}

    if animal_objetivo != None:
        pizza_x = repartidor_x + ancho_personaje / 2 - ancho_pizza / 2
        pizza_y = repartidor_y + largo_personaje / 2 - largo_pizza / 2

        centro_pizza_x = pizza_x + ancho_pizza / 2
        centro_pizza_y = pizza_y + largo_pizza / 2

        dx = animal_objetivo["centro_x"] - centro_pizza_x
        dy = animal_objetivo["centro_y"] - centro_pizza_y
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia > 0:
            direccion_x = dx / distancia * velocidad_pizza
            direccion_y = dy / distancia * velocidad_pizza

            obj_pizza = {
                "x": pizza_x,
                "y": pizza_y,
                "direccion_x": direccion_x,
                "direccion_y": direccion_y
            }
    return obj_pizza

def contador_juego():
    segundos = pygame.time.get_ticks() // 1000
    minutos = segundos // 60
    tiempo = f"{minutos:02}:{segundos:02}"
    texto = font.render(f"Tiempo: {tiempo}", True, (179, 54, 54))
    ancho = texto.get_width()
    pantalla.blit(texto, ((1280 - ancho) / 2, 30))

# Creamos el bucle principal del juego que en el pues validaremos eventos,
# le diremos a pygame que tiene que dibujar y donde, etc.
maximo_x = 1280 - ancho_personaje
maximo_y = 720 - largo_personaje
velocidad = 0.7
correr = True

# Vamos a añadir los corazones ya cargados en memoria para poder dibujarlos, lo pinemos antes de while para evitar sobrecargar la memoria
lista_surface_corazones = cargar_imagen_corazon(lista_corazones)
imagen_derrota = cargar_imagen_derrota()
imagen_victoria = cargar_imagen_victoria()
while correr:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            correr = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        repartidor_y -= velocidad
        if repartidor_y <= 0:
            repartidor_y = 0
    if keys[pygame.K_DOWN]:
        repartidor_y += velocidad
        if repartidor_y >= maximo_y:
            repartidor_y = maximo_y
    if keys[pygame.K_LEFT]:
        repartidor_x -= velocidad
        if repartidor_x <= 0:
            repartidor_x = 0
    if keys[pygame.K_RIGHT]:
        repartidor_x += velocidad
        if repartidor_x >= maximo_x:
            repartidor_x = maximo_x


    # esto se hara si solo queremos que se mueva cuando pulses la tecla pero lo que queremos es que se mueva cuando mantegamos pulsado una tecla
    # if evento.key == pygame.K_UP:
    #     repartidor_y -= 5
    # if evento.key == pygame.K_DOWN:
    #     repartidor_y += 5
    # if evento.key == pygame.K_LEFT:
    #     repartidor_x -= 5
    # if evento.key == pygame.K_RIGHT:
    #     repartidor_x += 5


    comprobar_colision_animales_repartidor(lista_surface_corazones)
    tiempo_actual_animales = pygame.time.get_ticks()

    if tiempo_actual_animales - contador_animales >= tiempo_entre_animales and cantidad_animales < 12:
        animales[cantidad_animales] = crear_animal()
        cantidad_animales += 1
        contador_animales = tiempo_actual_animales
    mover_animales()

    tiempo_actual = pygame.time.get_ticks()

    if animales != {}:
        if tiempo_actual - inicio_contador >= tiempo_entre_disparos and datos_pizza == {}:
            datos_pizza = disparar_pizza(repartidor_x, repartidor_y)
            inicio_contador = tiempo_actual
            sonido_disparo.play()

    if datos_pizza != {}:
        datos_pizza["x"] += datos_pizza["direccion_x"]
        datos_pizza["y"] += datos_pizza["direccion_y"]

        comprobar_colision_pizza_animales()

        if datos_pizza != {}:
            if datos_pizza["x"] > 1280 + ancho_pizza or datos_pizza["y"] > 720 + largo_pizza or datos_pizza["x"] < 0 - ancho_pizza or datos_pizza["y"] < 0 - largo_pizza:
                datos_pizza.clear()

    if len(lista_surface_corazones) > 0:
        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo, (0, 0))
        contador_juego()
        corazon(lista_surface_corazones)
        pizzero(repartidor_x, repartidor_y)
        for clave in animales:
            animal_actual = animales[clave]
            animal(animales[clave])
        if datos_pizza != {}:
            pizza(datos_pizza)
    else:
        pantalla.fill((0, 0, 0))
        derrota(imagen_derrota)
        sonido_derrota.play()

    if animales == {}:
        pantalla.fill((0, 0, 0))
        victoria(imagen_victoria)
        sonido_victoria.play()

    pygame.display.flip()

pygame.quit()