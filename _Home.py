import streamlit as st
from PIL import Image

image = Image.open('GRS_logo.png')
st.set_page_config(page_title="Home", page_icon="🛖", layout="wide")
st.image(image, width=300)

st.write("# Welcome to Dr. Shirley monitoring system! v1.1 🙌")

st.sidebar.success("Let's go.")

st.markdown(
    """
    #### *Dieses App ist für Anwendung Filtermethoden der Beschleunigungsdaten gemessen mit ADXL345 3-Axen Beschleunigungssensor*

    ---
    ### Wollen Sie die importierte Daten sehen?
    Checkout [Gallery](Gallery)
    ### Wollen Sie die neue csv-Dateien hochladen?
    Checkout [Upload](Upload)
    """
)
