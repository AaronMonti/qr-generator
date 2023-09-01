import streamlit as st
import qrcode
import io
from PIL import Image

# Función para generar una vCard en formato de texto
def generar_vcard(nombre, apellido, telefono, correo):
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{nombre} {apellido}\nTEL:{telefono}\nEMAIL:{correo}\nEND:VCARD"
    return vcard

# Función para generar un código QR a partir de una vCard
def generar_qr_vcard(vcard_text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(vcard_text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Título de la aplicación
st.title("Generador de Código QR para vCard")

# Entradas de texto para ingresar los datos de la vCard
nombre = st.text_input("Nombre:")
apellido = st.text_input("Apellido:")
telefono = st.text_input("Teléfono:")
correo = st.text_input("Correo electrónico:")
web = st.text_input("Web:")
empresa = st.text_input("Empresa:")

# Selector para ajustar el tamaño de los cuadrados interiores
box_size = st.slider("Tamaño de los cuadrados interiores", min_value=1, max_value=20, value=10)

# Selector para ajustar el ancho del borde
border = st.slider("Ancho del borde", min_value=1, max_value=10, value=4)

# Botón para generar el código QR de la vCard
if st.button("Generar Código QR"):
    if nombre and apellido and telefono and correo:
        vcard_text = generar_vcard(nombre, apellido, telefono, correo)
        qr_img = generar_qr_vcard(vcard_text)
        
        # Convertir la imagen PIL a un formato que Streamlit pueda mostrar
        img_byte_array = io.BytesIO()
        qr_img.save(img_byte_array, format='PNG')
        
        # Mostrar la imagen en Streamlit
        st.image(img_byte_array, use_column_width=True, caption="Código QR de la vCard")

# Nota para el usuario
st.info("Complete los campos y haga clic en 'Generar Código QR' para generar la vCard como un código QR.")

# Verificación para abrir el QR en una ventana emergente
if st.button("Abrir QR en una ventana emergente"):
    if nombre and apellido and telefono and correo:
        vcard_text = generar_vcard(nombre, apellido, telefono, correo)
        qr_img = generar_qr_vcard(vcard_text)
        qr_img_bytes = io.BytesIO()
        qr_img.save(qr_img_bytes, format="PNG")
        st.download_button(
            label="Descargar QR",
            data=qr_img_bytes.getvalue(),
            file_name="qr_vcard.png",
            mime="image/png",
        )

