# Import Python libraries
import warnings

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
from collections import namedtuple
from functions import (
    qo,
    qo_standing,
    qo_darcy,
    qo_vogel,
    qo_ipr_compuesto,
    aof,
    j,
    j_darcy,
    Qb,
)
warnings.filterwarnings('ignore')
from IPR_curves import IPR_Curve, IPR_curve, IPR_curve_methods
from nodal_analysis import sg_avg, sg_oil, pwf_vogel, pwf_darcy, f_darcy, gradient_avg

# Icon
icon = Image.open("Resources/PetroGraphix.png")

# App configuration
st.set_page_config(page_title="PetroGraphix", page_icon=icon)

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
st.title("PetroGraphix App®")

st.write("----")

# App's description
st.markdown(
    """This app helps you visualise production curves by year, IPR curves, 
perform calculations, among other things.
"""
)

# Add aditional info
expander = st.expander("Information about Productions Engineering:")
expander.write(
    "The objective of systems analysis is to combine the various components of the \
    production system for an individual well to estimate production rates and optimize \
    the components of the production system. (PetroWiki)"
)

# Add subheader
st.subheader("**What's IPR?**")
IPR_ = st.expander("IPR is...")
IPR_.write(
    "A mathematical tool used in production engineering to assess well \
performance by plotting the well production rate against the flowing bottomhole \
pressure (BHP). The data required to create the IPR are obtained by measuring the \
production rates under various drawdown pressures. The reservoir fluid composition and \
behavior of the fluid phases under flowing conditions determine the shape of the \
curve. (SLB Glossary)"
)

# Add image
image = Image.open("Resources/IPR.png")
st.image(image, width=100, use_column_width=True)

# Descrption
st.caption("*Image of a IPR curve using Vogel's method.*")

# Sidebar
logo = Image.open("Resources/PetroGraphix.png")
st.sidebar.image(logo)

# Sidebar's title
st.sidebar.title("Navigation Menu")

# Upload file
file = st.sidebar.file_uploader("Upload your xlsx file")

with st.sidebar:
    options = option_menu(
        menu_title="Navigate",
        options=["Home", "Data", "Curves", "Calculations", "Nodal Analysis"],
        icons=["house", "tv-fill", "file-bar-graph-fill", "file-check"],
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

    elif options == "Curves":
        st.subheader("**Select an option to visualise the graphic**")
        if st.checkbox("Qo vs t(years)"):
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df["date"], df["oil_rate"], c="brown")
            plt.xlabel("t (years)", fontsize=16,c='white')
            plt.ylabel("Qo (bpd)", fontsize=16,c='white')
            plt.title("Qo vs t(years)", fontsize=18,c='white')
            plt.grid()
            st.plotly_chart(fig)
        elif st.checkbox("Qw vs t(years)"):
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.plot(df["date"], df["water_rate"], c="blue")
            plt.xlabel("t (years)", fontsize=16,c='white')
            plt.ylabel("Qw (bpd)", fontsize=16,c='white')
            plt.title("Qw vs t(years)", fontsize=18,c='white')
            plt.grid()
            st.plotly_chart(fig1)
        elif st.checkbox("Qt vs t(years)"):
            dataq = df["oil_rate"] + df["water_rate"]
            data4 = dataq, df["date"]
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            # Customizing the curve
            ax2.plot(df["date"], dataq, c="green")
            plt.xlabel("t (years)", fontsize=16,c='white')
            plt.ylabel("Qt (bpd)", fontsize=16,c='white')
            plt.title("Qt vs t(years)", fontsize=18,c='white')
            plt.grid()
            st.plotly_chart(fig2)
        elif st.checkbox("Qo per well"):
            fig3,ax3 = plt.subplots(figsize=(10,10))
            ax3.bar(x=df['well_name'], height=df["oil_rate"])
            ax3.set_xlabel("Well_name",fontsize=16,c='white')
            ax3.set_ylabel("Oil_rate",fontsize=16,c='white')
            st.pyplot(fig3)

    elif options == "Calculations":
        st.subheader("**Enter input values**")
        q_test = st.number_input("Enter the flow rate (q_test) value: ")
        pwf_test = st.number_input("Enter the bottom hole pressure (pwf_test) value: ")
        pr = st.number_input("Enter the reservoir pressure (pr) value: ")
        pwf = st.number_input("Enter the bottom hole pressure value (pwf) to analize: ")
        pb = st.number_input("Enter the buble point pressure (pb) value: ")
        ef = st.number_input("Enter the value of ef: ")
        ef2 = st.number_input("Enter the value of ef2: ")
        st.subheader("**Select an option**")
        data = namedtuple("Input", "q_test pwf_test pr pwf pb ef ef2")
        if st.checkbox("J"):
            st.subheader("**Show results**")
            ind = j(q_test, pwf_test, pr, pb, ef=1, ef2=None)
            st.success(f"{'J is'} -> {ind:.2f} stb/psi")
        elif st.checkbox("AOF"):
            st.subheader("**Show results**")
            qmax = aof(q_test, pwf_test, pr, pb, ef=1, ef2=None)
            st.success(f"{'AOF is'} -> {qmax:.2f} stb/d")
        elif st.checkbox("Qo"):
            st.subheader("**Show results**")
            qo = qo(q_test, pwf_test, pr, pwf, pb, ef=1, ef2=None)
            st.success(f"{'Qo is'} -> {qo:.2f} stb/d")
        elif st.checkbox("Qb"):
            st.subheader("**Show results**")
            qb = Qb(q_test, pwf_test, pr, pb, ef=1, ef2=None)
            st.success(f"{'Qb is'} -> {qb:.2f} stb/d")

        st.subheader("**Select this options if you want to visualise the IPR curves**")
        if st.checkbox("IPR Curves"):
            st.subheader("**Select method**")
            method = st.selectbox("Method", ("Darcy", "Vogel", "IPR Compuesto"))
            Data = namedtuple("Input", "qtest pwftest pre pwfl Pb Ef Ef2")
            st.subheader("**Enter input values**")
            qtest = st.number_input("Enter the flow rate (qtest) value: ")
            pwftest = st.number_input(
                "Enter the bottom hole pressure (pwftest) value: ")
            pre = st.number_input("Enter the reservoir pressure (pre) value: ")
            Pb = st.number_input("Enter the buble point pressure (Pb) value: ")

            pwf_l = []
            for i in range(0, int((pre + 100)), 100):
                pwf_l.append(i)
            pwf_l.reverse()
            pwf_a = np.array(pwf_l, dtype=int)
            ipr_ = IPR_curve_methods(
                qtest, pwftest, pre, pwf_a, Pb, method, ef=1, ef2=None
            )
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(ipr_)

    elif options == "Nodal Analysis":
        st.subheader("**Enter input values**")
        API = st.number_input("Enter the API of the fluid: ")
        pr = st.number_input("Enter the reservoir pressure (pr) value: ")
        pb = st.number_input("Enter the buble point pressure (pb) value: ")
        q_test = st.number_input("Enter the maximum value of the flow rate: ")
        pfwt = st.number_input("Enter the value of the total bottom hole pressure: ")
        THP = st.number_input("Enter the value of THP: ")
        wc = st.number_input("Enter the value of the water saturation: ")
        SGh2o = st.number_input("Enter the value of the specific weight of the water: ")
        ID = st.number_input("Enter the value of the internal diameter: ")
        TVD = st.number_input("Enter the value of the True Vertical Depth (TVD): ")
        MD = st.number_input("Enter the value of the Measured Depth: ")

        q = [0, 750, 1400, 2250, 3000, 3750, 4500, 5250, 6000]

        df = pd.DataFrame()
        data = namedtuple("Input", "API pr pb qt pwft THP wc SGh2o ID TVD MD")
        for t in q:
            pwf = pwf_darcy(q_test, pfwt, t, pr, pb)
            Ind = j(q_test, pfwt, pr, pb, ef=1, ef2=None)
            qmax = Ind * pr
            sva = sg_avg(API, wc, SGh2o)
            grad = gradient_avg(API, wc, SGh2o)
            pgrad = TVD * grad
            f = f_darcy(t, ID, C=120)
            F = f * MD
            pf = F * grad
            Po = THP + pgrad + pf
            psys = Po - pwf

            tabla = pd.DataFrame(
                {
                    "Q (bpd)": [t],
                    "Pwf (psia)": [pwf],
                    "THP (psia)": [THP],
                    "PGravedad (psia)": [pgrad],
                    "f": [f],
                    "F": [F],
                    "Pf (psia)": [pf],
                    "Po (psia)": [Po],
                    "Psys (psia)": [psys],
                }
            )
            df = pd.concat([df, tabla], ignore_index=True)

        st.success(df.to_markdown())
