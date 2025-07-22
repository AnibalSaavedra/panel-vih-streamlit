from PIL import Image
import os
import streamlit as st

# Carga de imagen desde la raíz del repositorio
image = Image.open(os.path.join("logo.png"))
st.image(image, use_column_width=False, width=290)

import streamlit as st
from fpdf import FPDF
import datetime

# Configuración de la página
st.set_page_config(
    page_title="Informe VIH - Clínica Río Blanco",
    page_icon="🧬",
    layout="centered"
)

# Logo e introducción
st.image("https://imgur.com/a/oeYkCVb", width=100)
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Informe VIH - Clínica Río Blanco</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sección de ingreso de datos
st.subheader("📝 Datos del paciente")
nombre = st.text_input("Nombre completo")
rut = st.text_input("RUT")
fecha_muestra = st.date_input("Fecha de toma de muestra", format="DD/MM/YYYY")
hora_muestra = st.time_input("Hora de toma de muestra")
laboratorio = st.text_input("Nombre del laboratorio o centro")
validador = st.text_input("Validador (nombre y cargo)")

st.subheader("🧪 Datos del examen VIH")
tipo_prueba = st.selectbox("Tipo de prueba", ["ELISA", "Test rápido", "Antígeno", "Otro"])
resultado_bruto = st.text_input("Resultado cuantitativo (ej: 0.12, 0.98, 2.5)")
fecha_exposicion = st.date_input("Fecha estimada de exposición (opcional)", format="DD/MM/YYYY")

# Interpretación
def interpretar_vih(valor):
    try:
        valor = float(valor.replace(",", "."))
        if valor >= 0.5:
            interpretacion = "REACTIVO"
            recomendacion = "Muestra sometida a confirmación en Instituto de Salud Pública de Chile."
        else:
            interpretacion = "NO REACTIVO"
            dias_diff = (datetime.date.today() - fecha_exposicion).days
            if dias_diff < 28:
                recomendacion = "Examen realizado antes de los 28 días desde la exposición: debe repetirse al cumplir 28 días."
            else:
                recomendacion = "Resultado con alta confiabilidad (>99%) por haberse realizado después de los 28 días desde exposición."
        return interpretacion, recomendacion
    except:
        return None, "Valor inválido"

# PDF
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "INFORME DE RESULTADO VIH", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Nombre paciente: {nombre}", ln=True)
    pdf.cell(0, 10, f"RUT: {rut}", ln=True)
    pdf.cell(0, 10, f"Fecha muestra: {fecha_muestra.strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 10, f"Hora muestra: {hora_muestra.strftime('%H:%M')}", ln=True)
    pdf.cell(0, 10, f"Laboratorio: {laboratorio}", ln=True)
    pdf.cell(0, 10, f"Tipo de prueba: {tipo_prueba}", ln=True)
    pdf.cell(0, 10, f"Resultado cuantitativo: {resultado_bruto}", ln=True)
    pdf.cell(0, 10, f"Interpretación: {interpretacion}", ln=True)
    pdf.multi_cell(0, 10, f"Recomendación: {recomendacion}")
    pdf.ln(5)
    pdf.cell(0, 10, f"Validador: {validador}", ln=True)
    pdf.cell(0, 10, f"Fecha emisión: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)

    filename = f"Informe_VIH_{nombre.replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename

# Botón generar informe
if st.button("📄 Generar Informe PDF"):
    if not (nombre and rut and resultado_bruto and laboratorio and validador):
        st.error("Por favor completa todos los campos obligatorios.")
    else:
        interpretacion, recomendacion = interpretar_vih(resultado_bruto)
        if interpretacion is None:
            st.error("El valor ingresado no es válido.")
        else:
            archivo = generar_pdf()
            with open(archivo, "rb") as f:
                st.download_button("⬇️ Descargar Informe PDF", f, file_name=archivo, mime="application/pdf")
