import streamlit as st
import qrcode
import io
from PIL import Image

# Función para generar una vCard en formato de texto con dirección, sitio web y puesto en la empresa
def generar_vcard(nombre, apellido, telefono, correo, web, empresa, direccion, puesto):
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{nombre} {apellido}\nTEL:{telefono}\nEMAIL:{correo}\n"
    if direccion:
        vcard += f"ADR;TYPE=HOME,POSTAL:{direccion}\n"  # Agregar dirección (uso TYPE=HOME,POSTAL para dirección personal)
    if web:
        if not web.startswith("http://") and not web.startswith("https://"):
            web = "http://" + web  # Agregar el prefijo "http://" si no está presente
        vcard += f"URL:{web}\n"
    if empresa:
        vcard += f"ORG:{empresa}\n"
    if puesto:
        vcard += f"TITLE:{puesto}\n"  # Agregar el puesto en la empresa
    vcard += "END:VCARD"
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
direccion = st.text_input("Dirección:")
empresa = st.text_input("Empresa:")
puesto = st.text_input("Puesto:")

# Selector para ajustar el tamaño de los cuadrados interiores
box_size = st.slider("Tamaño de los cuadrados interiores", min_value=1, max_value=20, value=10)

# Selector para ajustar el ancho del borde
border = st.slider("Ancho del borde", min_value=1, max_value=10, value=4)

# Botón para generar el código QR de la vCard
if st.button("Generar Código QR"):
    if nombre and apellido and telefono and correo:
        vcard_text = generar_vcard(nombre, apellido, telefono, correo, web, empresa, direccion, puesto)

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
    if nombre and apellido and telefono:
        vcard_text = generar_vcard(nombre, apellido, telefono, correo, web, empresa, direccion, puesto)
        qr_img = generar_qr_vcard(vcard_text)
        qr_img_bytes = io.BytesIO()
        qr_img.save(qr_img_bytes, format="PNG")
        st.download_button(
            label="Descargar QR",
            data=qr_img_bytes.getvalue(),
            file_name="qr_vcard.png",
            mime="image/png",
        )

