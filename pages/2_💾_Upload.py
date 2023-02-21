# calculation will be do here direct when files uploaded
# error should be shown when data format is not satisfied requirements
# afterwards, the dataset will be saved as dataframe in parquet file format contains all columns *old columns and filtered data
import streamlit as st
import pandas as pd
import seaborn as sns
import math
import os
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("Neu CSV Dateien hochladen")

uploaded_files = st.file_uploader(
    "Bitte stellen Sie sicher, dass Ihre Beschleunigungs-CSV-Dateien diese Form von Headern haben: (x, y, z) mit den entsprechenden Werten. \n Wenn keine Headern vorhanden sind, müssen die Wertspalten die Form (x, y, z) oder (time_stamp, x, y, z) haben.",
    type="csv",
    accept_multiple_files=True,
)

cutoff = 1  # desired cutoff frequency of the filter, Hz
threshold = 5
fs = 8  # sample rate, Hz
order = 2  # sin wave can be approx represented as quadratic


def butter_lowpass_filter(data, cutoff, fs, order):
    # Nyquist Frequency
    nyq = 0.5 * fs  # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    y = filtfilt(b, a, data)
    return y


for uploaded_file in uploaded_files:
    df = pd.read_csv(uploaded_file)
    st.write("#### " + uploaded_file.name)
    # df.columns = df.columns.str.replace("Unnamed: 0", "index")
    try:
        print(type(float(list(df.columns)[-1])))
        print("CSV has no header")
        if len(df.columns) == 3:
            df.columns = ["x", "y", "z"]
        if len(df.columns) == 4:
            df.columns = ["time_stamp", "x", "y", "z"]
    except ValueError:
        print("CSV has headers")
        pass

    df.dropna(subset=['x'], inplace=True)
    df["norm"] = df.apply(
        lambda row: math.sqrt(row.x * row.x + row.y * row.y + row.z * row.z), axis=1
    )
    # df = df.drop(columns=["x", "y", "z"], axis=1)
    df["lowpass_filter"] = butter_lowpass_filter(df["norm"], cutoff, fs, order)
    last_val = df["norm"].iloc[0]
    df["threshold_filter"] = df["norm"]
    for i, row in df.iterrows():
        if abs(row["norm"] - last_val) > threshold:
            df.loc[i, "threshold_filter"] = None
        last_val = row["norm"]
    df["moving_average"] = df["norm"].rolling(5).mean()
    df = df.reset_index()
    df.to_parquet(
        "save/" + uploaded_file.name[:-4] + ".parquet.gzip", compression="gzip"
    )
    # st.dataframe(df)
    df.to_csv("save/" + uploaded_file.name.split('.')[0] + '_result.csv', index=False)

    # Figure 1
    fig1 = plt.figure(figsize=(12, 6), dpi=300)
    sns.lineplot(
        x="index",
        y="norm",
        data=df,
        color="#94a3b8",
        lw=1,
        label="normierte Beschleunigung",
    )
    sns.lineplot(
        x="index",
        y="moving_average",
        data=df,
        color="#881337",
        lw=1,
        label="gleitende Durchschnitt über 5-Werten",
    )
    plt.ylabel("accerelation")
    plt.xlabel("index")
    plt.savefig("save/" + uploaded_file.name[:-4] + "gleitende_Dschn.png", dpi=300)
    # Figure 2
    fig2 = plt.figure(figsize=(12, 6), dpi=300)
    sns.lineplot(
        x="index",
        y="norm",
        data=df,
        color="#94a3b8",
        lw=1,
        label="normierte Beschleunigung",
    )
    sns.lineplot(
        x="index",
        y="lowpass_filter",
        data=df,
        color="#064e3b",
        lw=1,
        label="Tiefpassfilter",
    )
    plt.ylabel("accerelation")
    plt.xlabel("index")
    plt.savefig("save/" + uploaded_file.name[:-4] + "_low_pass.png", dpi=300)
    # Figure 3
    fig3 = plt.figure(figsize=(12, 6), dpi=300)
    sns.lineplot(
        x="index",
        y="norm",
        data=df,
        color="#94a3b8",
        lw=1,
        label="normierte Beschleunigung",
    )
    sns.lineplot(
        x="index",
        y="threshold_filter",
        data=df,
        color="#701a75",
        lw=1,
        label="Schwellenwertfilter",
    )
    plt.xlabel("index")
    plt.ylabel("accerelation")
    plt.savefig("save/" + uploaded_file.name[:-4] + "_threshold.png", dpi=300)
    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)
else:
    st.write("Bitte laden Sie die CSV Dateien hoch")
