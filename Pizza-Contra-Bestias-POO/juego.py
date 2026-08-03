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

class Animal():
    def __init__(self):
        self.ancho = 60
        self.largo = 120

        self.x = randint(0, 1280 - self.ancho)
        self.y = 0

        self.imagen = self.cargar_imagen_animal()
        self.velocidad = 0.2
        self.animales = {
            0: {
                "x": self.x,
                "y": self.y,
                "imagen": self.cargar_imagen_animal()
            }
        }


    lista_animales = ["gato.png", "leon.png", "toro.png", "perro.png"]

    velocidad_animal = 0.2
    contador_animales = 0
    cantidad_animales = 1
    tiempo_entre_animales = 2200

    def animal(self, obj_animal):
        pantalla.blit(obj_animal["imagen"], (obj_animal["x"], obj_animal["y"]))

    def mover_animales(self, repartidor):
        for clave in self.animales:
            animal_actual = self.animales[clave]

            dx = repartidor.repartidor_x - animal_actual["x"]
            dy = repartidor.repartidor_y - animal_actual["y"]
            distancia = (dx ** 2 + dy ** 2) ** 0.5

            if distancia > 0:
                animal_actual["x"] += (dx / distancia) * self.velocidad_animal
                animal_actual["y"] += (dy / distancia) * self.velocidad_animal

    def elegir_animal(self):
        animal_elegido = random.choice(self.lista_animales)
        return animal_elegido

    def cargar_imagen_animal(self):
        animal_elegido = self.elegir_animal()
        imagen_animal = pygame.image.load(f"recursos_juego/{animal_elegido}")
        imagen_animal = pygame.transform.scale(imagen_animal, (self.ancho, self.largo))
        return imagen_animal

    def crear_animal(self):
        lado = randint(0, 3)

        if lado == 0:
            animal_x = randint(0, 1280 - self.ancho)
            animal_y = 0 - self.largo

        if lado == 1:
            animal_x = randint(0, 1280 - self.ancho)
            animal_y = 720 + self.largo

        if lado == 2:
            animal_x = 0 - self.ancho
            animal_y = randint(0, 720 - self.largo)

        if lado == 3:
            animal_x = 1280 + self.ancho
            animal_y = randint(0, 720 - self.largo)

        return {
            "x": animal_x,
            "y": animal_y,
            "imagen": self.cargar_imagen_animal()
        }

    def buscar_animal_mas_cercano(self, repartidor):
        animal_mas_cercano = None
        distancia_mas_cercana = None

        centro_repartidor_x = repartidor.repartidor_x + repartidor.ancho_personaje / 2
        centro_repartidor_y = repartidor.repartidor_y + repartidor.largo_personaje / 2

        for clave in self.animales:
            animal_actual = self.animales[clave]

            centro_animal_x = animal_actual["x"] + self.ancho / 2
            centro_animal_y = animal_actual["y"] + self.largo / 2

            dx = centro_animal_x - centro_repartidor_x
            dy = centro_animal_y - centro_repartidor_y
            distancia = (dx ** 2 + dy ** 2) ** 0.5

            if distancia_mas_cercana == None or distancia < distancia_mas_cercana:
                distancia_mas_cercana = distancia
                animal_mas_cercano = {
                    "centro_x": centro_animal_x,
                    "centro_y": centro_animal_y
                }

        return animal_mas_cercano

class Repartidor():
    def __init__(self):
        self.ancho_personaje = 75
        self.largo_personaje = 150
        self.repartidor_imagen = pygame.image.load("recursos_juego/repartidor.png")
        self.repartidor_imagen = pygame.transform.scale(self.repartidor_imagen, (self.ancho_personaje, self.largo_personaje))
        self.repartidor_x = (1280 - self.ancho_personaje) / 2
        self.repartidor_y = (720 - self.largo_personaje) / 2 + 235
        self.ultimo_golpe = 0
        self.tiempo_invulnerabilidad = 1500

    def repartidor(self):
        pantalla.blit(self.repartidor_imagen, (self.repartidor_x, self.repartidor_y))

    def comprobar_colision_animales_repartidor(self, lista_corazones, perro):
        tiempo_actual = pygame.time.get_ticks()
        rect_repartidor = pygame.Rect(self.repartidor_x, self.repartidor_y, self.ancho_personaje, self.largo_personaje)
        for aninal in perro.animales:
            animal_actual = perro.animales[aninal]
            rect_animal = pygame.Rect(animal_actual["x"], animal_actual["y"], perro.ancho, perro.largo)

            if rect_repartidor.colliderect(rect_animal):
                if tiempo_actual - self.ultimo_golpe >= self.tiempo_invulnerabilidad:
                    self.ultimo_golpe = tiempo_actual
                    if len(lista_corazones) > 0:
                        lista_corazones.pop()
                break

class Pizza():
    def __init__(self):
        self.ancho_pizza = 32
        self.largo_pizza = 32

        self.pizza_imagen = pygame.image.load("recursos_juego/pizza.png")
        self.pizza_imagen = pygame.transform.scale(self.pizza_imagen,(self.ancho_pizza, self.largo_pizza))

        self.datos_pizza = {}
        self.inicio_contador = 0
        self.tiempo_entre_disparos = 2400
        self.velocidad_pizza = 1

    def pizza(self, obj_pizza):
        pantalla.blit(self.pizza_imagen, (obj_pizza["x"], obj_pizza["y"]))

    def disparar_pizza(self, animal, repartidor):
        animal_objetivo = animal.buscar_animal_mas_cercano(repartidor)
        obj_pizza = {}

        if animal_objetivo != None:
            pizza_x = repartidor.repartidor_x + repartidor.ancho_personaje / 2 - self.ancho_pizza / 2
            pizza_y = repartidor.repartidor_y + repartidor.largo_personaje / 2 - self.largo_pizza / 2

            centro_pizza_x = pizza_x + self.ancho_pizza / 2
            centro_pizza_y = pizza_y + self.largo_pizza / 2

            dx = animal_objetivo["centro_x"] - centro_pizza_x
            dy = animal_objetivo["centro_y"] - centro_pizza_y
            distancia = (dx ** 2 + dy ** 2) ** 0.5

            if distancia > 0:
                direccion_x = dx / distancia * self.velocidad_pizza
                direccion_y = dy / distancia * self.velocidad_pizza

                obj_pizza = {
                    "x": pizza_x,
                    "y": pizza_y,
                    "direccion_x": direccion_x,
                    "direccion_y": direccion_y
                }
        return obj_pizza

    def comprobar_colision_pizza_animales(self, perro):
        if self.datos_pizza != {}:
            rect_pizza = pygame.Rect(self.datos_pizza["x"], self.datos_pizza["y"], self.ancho_pizza, self.largo_pizza)
            animal_a_eliminar = None

            for animal in perro.animales:
                animal_actual = perro.animales[animal]
                rect_animal = pygame.Rect(animal_actual["x"], animal_actual["y"], perro.ancho, perro.largo)

                if rect_pizza.colliderect(rect_animal):
                    animal_a_eliminar = animal
                    self.datos_pizza.clear()

            if animal_a_eliminar != None:
                del perro.animales[animal_a_eliminar]

class Corazon():
    def __init__(self):
        self.lista_corazones = ["corazon.png", "corazon.png", "corazon.png"]
        self.corazon_x = 15
        self.corazon_y = 15
        self.ultimo_golpe = 0

    def cargar_imagen_corazon(self):
        lista_surface_corazones = []
        for corazon in self.lista_corazones:
            imagen_corazon = pygame.image.load(f"recursos_juego/{corazon}")
            imagen_corazon = pygame.transform.scale(imagen_corazon, (30, 30))
            lista_surface_corazones.append(imagen_corazon)
        return lista_surface_corazones

    def corazon(self, lista_corazones):
        sumar_eje_x = 0
        for corazon in lista_corazones:
            pantalla.blit(corazon, (self.corazon_x + sumar_eje_x, self.corazon_y))
            sumar_eje_x += 35

class Derrota():
    def cargar_imagen_derrota(self):
        imagen_derrota = pygame.image.load("recursos_juego/derrota.png")
        imagen_derrota = pygame.transform.scale(imagen_derrota, (1280, 720))
        return imagen_derrota

    def derrota(self, imagen_derrota):
        pantalla.blit(imagen_derrota, (0, 0))

class Victoria():
    def cargar_imagen_victoria(self):
        imagen_victoria = pygame.image.load("recursos_juego/victoria.png")
        imagen_victoria = pygame.transform.scale(imagen_victoria, (1280, 720))
        return imagen_victoria

    def victoria(self, imagen_victoria):
        pantalla.blit(imagen_victoria, (0, 0))

class Tiempo():
    def contador_juego(self):
        segundos = pygame.time.get_ticks() // 1000
        minutos = segundos // 60
        tiempo = f"{minutos:02}:{segundos:02}"
        texto = font.render(f"Tiempo: {tiempo}", True, (179, 54, 54))
        ancho = texto.get_width()
        pantalla.blit(texto, ((1280 - ancho) / 2, 30))


# Fondo del Juego
fondo = pygame.image.load("recursos_juego/fondo.png")
fondo = pygame.transform.scale(fondo, (1280, 720))

# Sonidos Juego
sonido_disparo = pygame.mixer.Sound("recursos_juego/disparo.mp3")
sonido_victoria = pygame.mixer.Sound("recursos_juego/victoria.mp3")
sonido_derrota = pygame.mixer.Sound("recursos_juego/derrota.mp3")

# Instancias de las clases
animal = Animal()
repartidor = Repartidor()
pizza = Pizza()
victoria = Victoria()
derrota = Derrota()
tiempo = Tiempo()
corazon = Corazon()

# Creamos el bucle principal del juego que en el pues validaremos eventos,
# le diremos a pygame que tiene que dibujar y donde, etc.
maximo_x = 1280 - repartidor.ancho_personaje
maximo_y = 720 - repartidor.largo_personaje
velocidad = 0.7
correr = True

# Vamos a añadir los corazones ya cargados en memoria para poder dibujarlos, lo pinemos antes de while para evitar sobrecargar la memoria
lista_surface_corazones = corazon.cargar_imagen_corazon()
imagen_derrota = derrota.cargar_imagen_derrota()
imagen_victoria = victoria.cargar_imagen_victoria()
while correr:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            correr = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        repartidor.repartidor_y -= velocidad
        if repartidor.repartidor_y <= 0:
            repartidor.repartidor_y = 0
    if keys[pygame.K_DOWN]:
        repartidor.repartidor_y += velocidad
        if repartidor.repartidor_y >= maximo_y:
            repartidor.repartidor_y = maximo_y
    if keys[pygame.K_LEFT]:
        repartidor.repartidor_x -= velocidad
        if repartidor.repartidor_x <= 0:
            repartidor.repartidor_x = 0
    if keys[pygame.K_RIGHT]:
        repartidor.repartidor_x += velocidad
        if repartidor.repartidor_x >= maximo_x:
            repartidor.repartidor_x = maximo_x


    # esto se hara si solo queremos que se mueva cuando pulses la tecla pero lo que queremos es que se mueva cuando mantegamos pulsado una tecla
    # if evento.key == pygame.K_UP:
    #     repartidor_y -= 5
    # if evento.key == pygame.K_DOWN:
    #     repartidor_y += 5
    # if evento.key == pygame.K_LEFT:
    #     repartidor_x -= 5
    # if evento.key == pygame.K_RIGHT:
    #     repartidor_x += 5


    repartidor.comprobar_colision_animales_repartidor(lista_surface_corazones, animal)
    tiempo_actual_animales = pygame.time.get_ticks()

    if tiempo_actual_animales - animal.contador_animales >= animal.tiempo_entre_animales and animal.cantidad_animales < 12:
        animal.animales[animal.cantidad_animales] = animal.crear_animal()
        animal.cantidad_animales += 1
        animal.contador_animales = tiempo_actual_animales
    animal.mover_animales(repartidor)

    tiempo_actual = pygame.time.get_ticks()

    if animal.animales != {}:
        if tiempo_actual - pizza.inicio_contador >= pizza.tiempo_entre_disparos and pizza.datos_pizza == {}:
            pizza.datos_pizza = pizza.disparar_pizza(animal, repartidor)
            pizza.inicio_contador = tiempo_actual
            sonido_disparo.play()

    if pizza.datos_pizza != {}:
        pizza.datos_pizza["x"] += pizza.datos_pizza["direccion_x"]
        pizza.datos_pizza["y"] += pizza.datos_pizza["direccion_y"]

        pizza.comprobar_colision_pizza_animales(animal)

        if pizza.datos_pizza != {}:
            if pizza.datos_pizza["x"] > 1280 + pizza.ancho_pizza or pizza.datos_pizza["y"] > 720 + pizza.largo_pizza or pizza.datos_pizza["x"] < 0 - pizza.ancho_pizza or pizza.datos_pizza["y"] < 0 - pizza.largo_pizza:
                pizza.datos_pizza.clear()

    if len(lista_surface_corazones) > 0:
        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo, (0, 0))
        tiempo.contador_juego()
        corazon.corazon(lista_surface_corazones)
        repartidor.repartidor()
        for clave in animal.animales:
            animal_actual = animal.animales[clave]
            animal.animal(animal.animales[clave])
        if pizza.datos_pizza != {}:
            pizza.pizza(pizza.datos_pizza)
    else:
        pantalla.fill((0, 0, 0))
        derrota.derrota(imagen_derrota)
        sonido_derrota.play()

    if animal.animales == {}:
        pantalla.fill((0, 0, 0))
        victoria.victoria(imagen_victoria)
        sonido_victoria.play()

    pygame.display.flip()

pygame.quit()