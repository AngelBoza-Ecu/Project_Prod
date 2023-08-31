# Import Python libraries

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
from collections import namedtuple

# Icon
icon =Image.open("Resources/PetroGraphix.png")

# App configuration
st.set_page_config(page_title='PetroGraphix', page_icon=icon)

st.markdown(
    """
<style>
h1 {text-align: center;
}
body {background-color: #DCE3D5;
      width: 1400px;
      margin: 15px auto;
}
footer {
  display: none;
}
</style>""",
    unsafe_allow_html=True,
)


# App's title
st.title('PetroGraphix')

st.write('----')

# App's description
st.markdown("""This app helps you visualise production curves by year, IPR curves, 
perform calculations, among other things.
""")

# Add aditional info
expander = st.expander('Information about Productions Engineering:')
expander.write(
    "The objective of systems analysis is to combine the various components of the \
    production system for an individual well to estimate production rates and optimize \
    the components of the production system. (PetroWiki)"
)

# Add subheader
st.subheader("**What's IPR?**")
IPR_ = st.expander("IPR is...")
IPR_.write("A mathematical tool used in production engineering to assess well \
performance by plotting the well production rate against the flowing bottomhole \
pressure (BHP). The data required to create the IPR are obtained by measuring the \
production rates under various drawdown pressures. The reservoir fluid composition and \
behavior of the fluid phases under flowing conditions determine the shape of the \
curve.")

# Add image
image =Image.open('Resources/IPR.png')
st.image(image, width=100, use_column_width=True)