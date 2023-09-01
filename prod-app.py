# Import Python libraries
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
from collections import namedtuple
from utilities import j

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

# Sidebar
logo =Image.open("Resources/PetroGraphix.png")
st.sidebar.image(logo)

# Sidebar's title
st.sidebar.title('Navigation Menu')

# Upload file
file = st.sidebar.file_uploader("Upload your xlsx file")

with st.sidebar:
    options = option_menu(
        menu_title="Navigate",
        options=['Home','Data','Curves','Calculations','Nodal Analysis'],
        icons=['house','tv-fill','file-bar-graph-fill','file-check'],
    )


# Functions to use
def data(field):
    st.subheader("**View DataFrame**")
    st.write(field.head())
    st.subheader("**Statistical Summary**")
    st.write(field.describe())

def plots(field):
    st.subheader("Visualise curves")
    x = st.selectbox("Choose Date", field.columns)
    y = st.selectbox("Choose between Oil_rate or Water_rate", field.columns)
    st.subheader("**The curve is: **")
    fig,ax = plt.subplots()
    ax.plot(x,y)
    plt.title("Flow rate")
    plt.xlabel('Years')
    plt.ylabel('Barrels per day')
    st.pyplot(fig)


if file:
    df = pd.read_excel(file)

    if options == "Data":
        data(df)

    elif options == 'Curves':
        qvt = st.selectbox("***Qo vs t(años)***")
        wvt = st.selectbox("***Qw vs t(años)***")

        plots(df)

    elif options == "Calculations":
        if st.checkbox("J"):
            data = namedtuple("Input","Qo Pr Pwf")
            st.subheader("**Enter input values**")
            pr = st.number_input("**Enter the reservoir pressure value: **")
            pwf_test = st.number_input("**Enter the bottom hole pressure value: **")
            q_test = st.number_input("**Enter the flow rate value value: **")
            pb = st.subheader("**Enter the buble point preassure value: **")
            st.subheader("**Show results**")
            j(q_test,pwf_test,pr,pb,ef=1,ef2=None)
