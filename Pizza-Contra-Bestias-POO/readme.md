# Pizza contra Bestias (Versión POO)

Juego desarrollado en Python utilizando Pygame y Programación Orientada a Objetos (POO).

## Descripción

Esta versión del juego utiliza Programación Orientada a Objetos para organizar mejor el código, separando la lógica en distintas clases y haciendo el proyecto más fácil de mantener y ampliar.

Controla a un repartidor de pizzas y sobrevive al ataque de diferentes animales. Las pizzas se lanzan automáticamente al enemigo más cercano mientras intentas aguantar el mayor tiempo posible.

## Características

- Programación Orientada a Objetos (POO).
- Movimiento con teclado.
- Enemigos que persiguen al jugador.
- Disparo automático.
- Animales aleatorios.
- Sistema de vidas.
- Sonidos.
- Pantallas de victoria y derrota.
- Contador de tiempo.

## Controles

↑ Mover arriba

↓ Mover abajo

← Mover izquierda

→ Mover derecha

## Tecnologías utilizadas

- Python
- Pygame

## Ejecutar el juego

1. Abre una terminal y accede a la carpeta del proyecto. Por ejemplo en mi caso:

cd C:\Users\Manu\Desktop\Pizza-Contra-Bestias-POO

2. Crea un entorno virtual:

py -3.11 -m venv venv

3. Activa el entorno virtual:

venv\Scripts\activate

4. Instala las dependencias del proyecto:

pip install -r requirements.txt

5. Inicia el juego:

python juego.py

6. Para desactivar el entorno virtual usamos este comando:

deactivate

## Estructura del proyecto

Pizza-Contra-Bestias-POO/
├── juego.py
├── requirements.txt
├── README.md
├── .gitignore
└── recursos_juego/
    ├── fondo.png
    ├── pizza.png
    ├── repartidor.png
    ├── gato.png
    ├── perro.png
    ├── leon.png
    ├── toro.png
    ├── corazon.png
    ├── disparo.mp3
    ├── victoria.mp3
    ├── derrota.mp3
    ├── victoria.png
    └── derrota.png

## Posibles mejoras

- Menú principal.
- Selector de dificultad.
- Sistema de puntuación.
- Animaciones.
- Más enemigos.
- Nuevas armas.

## Autor

Manuel Ferrez Garcia