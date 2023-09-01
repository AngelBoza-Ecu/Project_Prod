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
icon = Image.open("Resources/PetroGraphix.png")

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
st.title('PetroGraphix App®')

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
curve. (SLB Glossary)")

# Add image
image =Image.open('Resources/IPR.png')
st.image(image, width=100, use_column_width=True)

# Descrption
st.caption("*Image of a IPR curve using Vogel's method.*")

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


if file:
    df = pd.read_excel(file)

    if options == "Data":
        data(df)

    elif options == 'Curves':
        st.subheader("**Select an option to visualise the graphic**")
        if st.checkbox("Qo vs t(years)"):
            fig, ax = plt.subplots(figsize=(15, 10))
            ax.plot(df["date"], df["oil_rate"], c='brown')
            plt.xlabel('t (years)', fontsize=16)
            plt.ylabel('Qo (bpd)', fontsize=16)
            plt.title('Qo vs t(years)', fontsize=18)
            st.pyplot(fig)
        elif st.checkbox("Qw vs t(years)"):
            fig1, ax1 = plt.subplots(figsize=(15, 10))
            ax1.plot(df["date"], df["water_rate"], c='brown')
            plt.xlabel('t (years)', fontsize=16)
            plt.ylabel('Qw (bpd)', fontsize=16)
            plt.title('Qw vs t(years)', fontsize=18)
            st.pyplot(fig1)
        elif st.checkbox("Qt vs t(years)"):
            dataq = (df["oil_rate"] + df["water_rate"])
            data4 = dataq, df["date"]
            fig2, ax2 = plt.subplots(figsize=(15, 10))
            # Customizing the curve
            ax2.plot(df["date"], dataq, c='green')
            plt.xlabel('t (years)', fontsize=16)
            plt.ylabel('Qt (bpd)', fontsize=16)
            plt.title('Qt vs t(years)', fontsize=18)
            st.pyplot(fig2)

    elif options == "Calculations":
        st.subheader("**Select an option**")
        if st.checkbox("J"):
            data = namedtuple("Input","q_test pr pwf_test")
            st.subheader("**Enter input values**")
            pr = st.number_input("**Enter the reservoir pressure value: **")
            pwf_test = st.number_input("**Enter the bottom hole pressure value: **")
            q_test = st.number_input("**Enter the flow rate value value: **")
            pb = st.subheader("**Enter the buble point preassure value: **")
            st.subheader("**Show results**")
            #j(q_test,pwf_test,pr,pb,ef=1,ef2=None)

        #elif st.checkbox("AOF"):

    #elif options == "Nodal Analysis":


