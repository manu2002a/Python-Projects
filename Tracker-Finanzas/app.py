import streamlit as st
import pandas as pd

# st.title("Texto Prueba")
# st.write("Esto es un parrafo de ejemplo")
#
# st.markdown("**Esto es texto en negrita** y *esto es texto en cursiva*")
#
# st.header("Cabecera")
# st.subheader("Subcabecera")
# st.success("Esto es texto en negrita")
# st.caption("Mensaje pequeno")

categorias_gastos = ["Vivienda", "Servicios", "Alimentacion", "Transporte", "Salud", "Educacion", "Ocio", "Ropa y calzado", "Cuidado personal", "Seguros", "Deudas y prestamos", "Ahorro e inversion", "Mascotas", "Regalos y donaciones", "Impuestos y tramites", "Suscripciones", "Gastos familiares", "Emergencias o imprevistos"]


def inicializar_session_state_transacciones():
    if "transacciones" not in st.session_state:
        st.session_state["transacciones"] = []


def mostrar_formulario():
    with st.form("Formulario"):
        descripcion = st.text_input("Descripcion del gasto o ingreso", placeholder="Haz una descripcion del gasto o ingreso")
        dinero = st.number_input("Dinero", step=1.0, min_value=0.0, format="%0.2f", placeholder="Dinero")
        fecha = st.date_input("Fecha")
        categoria = st.selectbox("Categoria", categorias_gastos)
        tipo = st.radio("Tipo", ["Ingreso", "Gasto"], horizontal=True)
        boton = st.form_submit_button("Enviar")

    return boton, descripcion, dinero, fecha, categoria, tipo


def guardar_transaccion(descripcion, dinero, fecha, categoria, tipo):
    st.session_state["transacciones"].append({"descripcion": descripcion, "dinero": dinero, "fecha": fecha, "categoria": categoria, "tipo": tipo})
    st.success("Transaccion enviada con exito")


def mostrar_transacciones():
    if st.session_state["transacciones"]:
        data = pd.DataFrame(st.session_state["transacciones"])
        st.dataframe(data)

def subir_csv():
    archivo = st.file_uploader("Subir CSV", type="csv")

    if archivo is not None:
        data = pd.read_csv(archivo)
        lista_diccionarios = data.to_dict("records")
        boton_csv = st.button("Guardar CSV")
        if boton_csv:
            st.session_state["transacciones"].extend(lista_diccionarios)
            st.success("CSV guardado en session_state")

def calcular_ingreso():
    ingreso_total = 0
    if st.session_state["transacciones"]:
        for transaccion in st.session_state["transacciones"]:
            if transaccion["tipo"] == "Ingreso":
                ingreso_total += transaccion["dinero"]
    return ingreso_total


def calcular_gasto():
    gasto_total = 0
    contador = 0
    if st.session_state["transacciones"]:
        for transaccion in st.session_state["transacciones"]:
            if transaccion["tipo"] == "Gasto":
                gasto_total += transaccion["dinero"]
                contador += 1
    return gasto_total, contador


def seleccionar_datos_para_grafico():
    categorias_seleccionadas = st.multiselect(
        "Selecciona las categorias de tus gastos mensuales:",
        options=categorias_gastos,
        placeholder="Elige una o mas categorias...",
    )
    return categorias_seleccionadas


def mostrar_grafico(categorias_seleccionadas):
    datos_graficos = []

    for transaccion in st.session_state["transacciones"]:
        if transaccion["categoria"] in categorias_seleccionadas:
            datos_graficos.append({
                "dinero": transaccion["dinero"],
                "categoria": transaccion["categoria"]
            })

    if datos_graficos:
        data = pd.DataFrame(datos_graficos)
        st.bar_chart(data, x="categoria", y="dinero")
    else:
        st.info("No hay datos para las categorias seleccionadas")


st.title("Tracker de Finanzas Personales")
subir_csv()
inicializar_session_state_transacciones()

with st.sidebar:
    boton, descripcion, dinero, fecha, categoria, tipo = mostrar_formulario()
    categorias_seleccionadas = seleccionar_datos_para_grafico()

if boton == True:
    guardar_transaccion(descripcion, dinero, fecha, categoria, tipo)


tab1, tab2, tab3 = st.tabs(["Resumen", "Movimientos", "Analisis"])

ingreso = calcular_ingreso()
gasto, contador = calcular_gasto()


with tab1:
    column1, column2, column3, column4 = st.columns(4)
    column1.metric("Ingreso", value=ingreso)
    column2.metric("Gasto", value=gasto)
    column3.metric("Balance", value=ingreso-gasto)
    if contador > 0:
        column4.metric("Gastos Media", value=gasto / contador)
with tab2:
    mostrar_transacciones()
with tab3:
    mostrar_grafico(categorias_seleccionadas)