import streamlit as st
from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import io

# Perguntar se deseja inserir imagem embutida
img_embed = st.file_uploader("Select a file", type=["png", "jpg", "jpeg"])

# Perguntar os dados do qr
data = st.text_input("Digite os dados para o QR Code:")

# Função para converter imagem em bytes

def convertTobytes(img, format="PNG"):
    if img is None:
        return None
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format)
    return img_bytes.getvalue()

def st_qr():
    if not data:
        return
    
    # Criando o QR Code com correção de erro alta
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)    

    # Gerando as imagens com diferentes estilos
    img_1 = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    img_2 = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())

    # Carregando a imagem embutida
    if img_embed is not None:
        embedded_img = Image.open(img_embed)
        img_3 = qr.make_image(image_factory=StyledPilImage, embedded_image=embedded_img)
    else:
        img_3 = None
    
    # Converter imagem para bytes para download
    img_1_bytes = convertTobytes(img_1)
    img_2_bytes = convertTobytes(img_2)
    img_3_bytes = convertTobytes(img_3)

    # Criando colunas para exibição
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Imagem 1")
        qr1 = st.image(img_1_bytes)
        st.download_button(label="Download 1", data=img_1_bytes, file_name="QR 1.png")

    with col2:
        st.header("Imagem 2")
        qr2 = st.image(img_2_bytes)
        st.download_button(label="Download 2", data=img_2_bytes, file_name="QR 2.png")

    with col3:
        st.header("Imagem 3")
        if img_3:
            qr3 = st.image(img_3_bytes)
            st.download_button(label="Download 3", data=img_3_bytes, file_name="QR 3.png")
            

if st.button("Generate"):
    st_qr()
