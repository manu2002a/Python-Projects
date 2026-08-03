# Tracker de Finanzas Personales

Aplicación desarrollada en Python utilizando Streamlit y Pandas para llevar un control sencillo de ingresos y gastos.

## Descripción

Esta aplicación permite registrar ingresos y gastos, visualizar todas las transacciones en una tabla y consultar un resumen con diferentes métricas. Además, es posible importar un archivo CSV con transacciones y mostrar un gráfico de los gastos por categorías.

## Funcionalidades

- Registrar ingresos y gastos.
- Seleccionar la categoría de cada transacción.
- Mostrar todas las transacciones registradas.
- Importar transacciones desde un archivo CSV.
- Consultar el total de ingresos, gastos y balance.
- Visualizar un gráfico de gastos por categoría.

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas

## Ejecutar la aplicación

1. Abre una terminal y accede a la carpeta del proyecto. Por ejemplo en mi caso:

cd C:\Users\Manu\Desktop\Tracker-Finanzas

2. Crea un entorno virtual:

python -m venv venv

3. Activa el entorno virtual:

venv\Scripts\activate

4. Instala las dependencias del proyecto:

pip install -r requirements.txt

5. Inicia la aplicación:

python -m streamlit run app.py

Una vez ejecutado el comando, Streamlit abrirá automáticamente la aplicación en el navegador. Si no ocurre, copia la dirección que aparece en la terminal (normalmente http://localhost:8501) y pégala en tu navegador.

6. Para salir de streamlit en al terminal pulse:



7. Para desactivar el entorno virtual usamos este comando:

deactivate

## Estructura del proyecto

Tracker-Finanzas/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore

## Posibles mejoras

- Guardar las transacciones en una base de datos.
- Editar y eliminar transacciones.
- Añadir autenticación de usuarios.
- Incorporar más gráficos y estadísticas.

## Autor

Manuel Ferrez Garcia