# This app will show gallery of imported dataset as charts with names
# Each chart on click will show up its details, which was described when data imported
# User can also edit the notes for each dataset
# Button export saved dataframe *parquet* to csv file

import streamlit as st
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt

st.title("Gallery")
st.write("Diese Seite enthält alle hochgeladenen Daten und das gefilterte Ergebnis. Bitte überprüfen Sie den /save-Ordner, um die exportierten Diagramme anzuzeigen")

path_of_the_directory = "save"
object = os.scandir(path_of_the_directory)
lof = []
for n in object:
    if n.is_file() and "parquet" in n.name:
        lof.append(n.name)

object.close()

if 'option' not in st.session_state:
    if len(lof) != 0:
        st.session_state.option = lof[0] 

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

def show_chart(file):
    df = pd.read_parquet('save/' + file)
    st.write('#### ' + file.split('.')[0])
    csv = convert_df(df)
    st.download_button(
        label="Ergebnis als csv Datei speichern",
        data=csv,
        file_name = file.split('.')[0] + '_result.csv',
        mime='text/csv',
    )
    # Figure 1
    fig1 = plt.figure(figsize=(12, 6), dpi=300)
    sns.lineplot( x="index", y="norm", data=df, color="#94a3b8", lw=1, label="normierte Beschleunigung")
    sns.lineplot( x="index", y="moving_average", data=df, color="#881337", lw=1, label="gleitende Durchschnitt über 5-Werten")
    plt.ylabel("accerelation")
    plt.xlabel("index")
    # Figure 2
    fig2 = plt.figure(figsize=(12, 6), dpi=300)
    sns.lineplot(x = 'index', y = 'norm', data=df, color='#94a3b8', lw=1, label='normierte Beschleunigung')
    sns.lineplot(x = 'index', y = 'lowpass_filter', data=df, color='#064e3b', lw=1, label='Tiefpassfilter')
    plt.ylabel("accerelation")
    plt.xlabel("index")
    # Figure 3
    fig3 = plt.figure(figsize=(12, 6), dpi=300)
    sns.lineplot(x = 'index', y = 'norm', data=df, color='#94a3b8', lw=1, label='normierte Beschleunigung')
    sns.lineplot(x = 'index', y = 'threshold_filter', data=df, color='#701a75', lw=1, label='Schwellenwertfilter')
    plt.xlabel("index")
    plt.ylabel("accerelation")
    st.pyplot(fig1)
    st.write("Abbildung 1. gleitende Durchschnitt über 5-Werten")
    st.pyplot(fig2)
    st.write("Abbildung 2. Tiefpassfilter")
    st.pyplot(fig3)
    st.write("Abbildung 3. Schwellenwertfilter")
    fig4 = plt.figure(figsize=(12, 12))
    plt.subplot(311)
    sns.lineplot(x = 'index', y = 'norm', data=df, color='#94a3b8', lw=1, label='normierte Beschleunigung')
    sns.lineplot(x = 'index', y = 'moving_average', data=df, color='#881337', lw=1, label='gleitende Durchschnitt über 5-Werten')
    plt.ylabel("accerelation")
    plt.subplot(312)
    sns.lineplot(x = 'index', y = 'norm', data=df, color='#94a3b8', lw=1, label='normierte Beschleunigung')
    sns.lineplot(x = 'index', y = 'lowpass_filter', data=df, color='#064e3b', lw=1, label='Tiefpassfilter')
    plt.ylabel("accerelation")
    plt.subplot(313)
    sns.lineplot(x = 'index', y = 'norm', data=df, color='#94a3b8', lw=1, label='normierte Beschleunigung')
    sns.lineplot(x = 'index', y = 'threshold_filter', data=df, color='#701a75', lw=1, label='Schwellenwertfilter')
    plt.xlabel("index")
    plt.ylabel("accerelation")
    plt.savefig('save/' + file.split('.')[0] + '_combined.png', dpi=300)
    st.pyplot(fig4)
    st.write("Abbildung 4. Vergleich Filtermethoden")

if len(lof) != 0:
    option = st.selectbox('Bitte wählen Sie den Datensatz', lof, key='option')
    show_chart(option)
else:
    st.markdown(":red[Es gibt keine gespeicherte Daten]")

