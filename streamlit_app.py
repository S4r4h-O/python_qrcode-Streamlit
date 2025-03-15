import streamlit as st
from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask, RadialGradiantColorMask, SquareGradiantColorMask, HorizontalGradiantColorMask, VerticalGradiantColorMask, ImageColorMask
import io

# Mode selector (single or multi)
quant = st.selectbox("Mode", ("Single", "Multi"))
if quant == "Single":
    data = st.text_input("QR Code Content")
   
# Mask and style selectors
colum1, colum2 = st.columns(2)
with colum1:
    style = st.selectbox(
        "Style",
        ("SquareModuleDrawer", "GappedSquareModuleDrawer", "CircleModuleDrawer", "RoundedModuleDrawer", "VerticalBarsDrawer", "HorizontalBarsDrawer")
    )
   
with colum2:
    colorMask = st.selectbox(
        "Color Mask",
        ("SolidFillColorMask", "RadialGradiantColorMask", "SquareGradiantColorMask", "HorizontalGradiantColorMask", "VerticalGradiantColorMask", "ImageColorMask"),
        index=0
    )
   
MODULE_CLASSES = {
    "SquareModuleDrawer": SquareModuleDrawer,
    "GappedSquareModuleDrawer": GappedSquareModuleDrawer,
    "CircleModuleDrawer": CircleModuleDrawer,
    "RoundedModuleDrawer": RoundedModuleDrawer,
    "VerticalBarsDrawer": VerticalBarsDrawer,
    "HorizontalBarsDrawer": HorizontalBarsDrawer
}
COLOR_MASK_CLASSES = {
    "SolidFillColorMask": SolidFillColorMask,
    "RadialGradiantColorMask": RadialGradiantColorMask,
    "SquareGradiantColorMask": SquareGradiantColorMask,
    "HorizontalGradiantColorMask": HorizontalGradiantColorMask,
    "VerticalGradiantColorMask": VerticalGradiantColorMask,
    "ImageColorMask": ImageColorMask
}
   
def convert_to_bytes(img, format="PNG"):
    if img is None:
        return None
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format)
    img_bytes.seek(0)
    return img_bytes.getvalue()    
   
def generator():
    if not data:
        return
   
    # Create QR code
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
   
    selected_module = MODULE_CLASSES.get(style, SquareModuleDrawer)
    selected_color_mask = COLOR_MASK_CLASSES.get(colorMask, SolidFillColorMask)
    
    try:
        # Generate QR code based on selected color mask
        if colorMask == "SolidFillColorMask":
            # SolidFillColorMask uses front_color and back_color
            color_mask_instance = selected_color_mask(
                front_color=(0, 0, 0),
                back_color=(255, 255, 255)
            )
        elif colorMask in ["RadialGradiantColorMask", "SquareGradiantColorMask", 
                          "HorizontalGradiantColorMask", "VerticalGradiantColorMask"]:
            # Gradient masks use center_color and edge_color
            color_mask_instance = selected_color_mask(
                center_color=(0, 0, 0),
                edge_color=(100, 100, 100)
            )
        elif colorMask == "ImageColorMask":
            # For ImageColorMask, we need an actual image
            gradient_img = Image.new('RGB', (100, 100), color=(255, 255, 255))
            for x in range(100):
                for y in range(100):
                    # Create a simple gradient
                    r = int(255 * (1 - x/100))
                    g = int(255 * (1 - y/100))
                    b = int(255 * (1 - (x+y)/200))
                    gradient_img.putpixel((x, y), (r, g, b))
            
            color_mask_instance = selected_color_mask(
                back_color=(255, 255, 255),
                color_mask_image=gradient_img
            )
        else:
            # Default to SolidFillColorMask if none of the above
            color_mask_instance = SolidFillColorMask(
                front_color=(0, 0, 0),
                back_color=(255, 255, 255)
            )
        
        # Generate QR code with the properly configured color mask
        qr_image = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=selected_module(),
            color_mask=color_mask_instance
        )
        
        # Convert to bytes for display
        img_bytes = io.BytesIO()
        qr_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        # Display the QR code using bytes
        st.image(img_bytes)
        
        # Reset the bytes for download
        img_bytes.seek(0)
        
        # Add download button with the proper bytes data
        st.download_button(
            label="Download QR", 
            data=img_bytes.getvalue(),
            file_name="qrcode.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"Error generating QR code: {e}")
        st.error("Try another color mask or style combination.")
       
if st.button("Generate"):
    generator()
    
###

style_drawer_png = "https://raw.githubusercontent.com/lincolnloop/python-qrcode/main/doc/module_drawers.png"
color_mask_png = "https://raw.githubusercontent.com/lincolnloop/python-qrcode/main/doc/color_masks.png"

with st.sidebar:
    
    st.title("Available styles and color masks")
    st.image(style_drawer_png, caption="QR Code Styles")
    st.image(color_mask_png, caption="QR Code Color Masks")
