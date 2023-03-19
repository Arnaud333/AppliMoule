import pandas as pd
import numpy as np
import cv2
import streamlit as st
from streamlit_option_menu import option_menu
# import os
from camera_input_live import camera_input_live
import sqlite3
import csv

from Barecode import decode

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

# con = sqlite3.connect("Moules.db")
# cur = con.cursor()
# cur.execute('''
#             CREATE TABLE Moules(
#             Moule_ID TEXT PRIMARY KEY,
#             Emplacement TXT
#             )
#             ''')
# con.commit()
# con.close()

selected = option_menu(
    menu_title='AppliMoules, (démo pour JMT)',
    options=["Gestion Moules", "Export table","Codebare (test)"],
    icons=['boxes', 'download','upc-scan'],
    default_index=0,
    orientation="horizontal",
)

if 'ID' not in st.session_state:
    st.session_state.ID=''
if 'LOC' not in st.session_state:
    st.session_state.LOC=''
if 'av' not in st.session_state:
    st.session_state.av=0
if 'test' not in st.session_state:
    st.session_state.test=''


def prise_video():
    image = camera_input_live()
    st.image(image)
    if image is not None:
        bytes_data = image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        # st.write('image',cv2_img)
        if cv2_img[0][0][0]!=0:
            # detector = cv2.QRCodeDetector()
            # detector = cv2.barc
            # data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)
            data=decode(cv2_img)
            if data!=False:
                st.session_state.test=data
                st.write("# Found barcode")
                st.write("# Found barcode",st.session_state.test)
                # with st.expander("Show details"):
                #     st.write("BBox:", bbox)
                #     st.write("Straight QR code:", straight_qrcode)



def change():
    st.session_state.av=1

# st.header('AppliMoules')
# st.write('démo pour JMT')
if selected=="Gestion Moules":
    

    if st.session_state.av<2:

        ID=st.text_input("Scannez ou saisissez l'ID moule à traiter :",value='',on_change=change,key='input_ID')
        st.session_state.ID=ID
        if ID!='':
            st.session_state.av=1


    if st.session_state.ID!='':
        
        con = sqlite3.connect("Moules.db")
        cur = con.cursor()
        cur.execute("SELECT Moule_ID FROM moules WHERE Moule_ID = ?", (st.session_state.ID,))
        result = cur.fetchone()
        con.close()
        
        if result is None:
            st.write(f"Nouveau Moule {ID} confirmez vous la création?")
            colg, cold =st.columns([1,1])
            with colg:
                oui=st.button('Oui')
                if oui:
                    con = sqlite3.connect("Moules.db")
                    cur = con.cursor()
                    cur.execute("INSERT INTO moules (Moule_ID, Emplacement) VALUES (?, ?)", (st.session_state.ID, ''))
                    con.commit()
                    con.close()

                    st.session_state.ID=ID
                    st.session_state.LOC=''
                    st.session_state.av=2
            # with cold:
            #     non=st.button('Non')
                

        else:
            
            con = sqlite3.connect("Moules.db")
            cur = con.cursor()
            cur.execute("SELECT Emplacement FROM moules WHERE Moule_ID = ?", (st.session_state.ID,))
            result = cur.fetchone()
            con.close()
            st.session_state.LOC=result[0]
            st.session_state.av=2


    if st.session_state.av>1:
        st.write('moule selectionné',st.session_state.ID)
        st.write(f'Emplacement actuel du moule {st.session_state.ID} :',st.session_state.LOC)
        LOC=st.text_input("Scannez ou saisissez le nouvel emplacement du moule :")

        if LOC!='':
            st.session_state.LOC=LOC
            st.write('Confirmez le transfert du moule')
            colg2, cold2 =st.columns([1,1])
            with colg2:
                oui2=st.button('Oui')
                if oui2:
                    con = sqlite3.connect("Moules.db")
                    cur = con.cursor()
                    cur.execute("UPDATE moules SET Emplacement = ? WHERE Moule_ID = ?", (st.session_state.LOC,st.session_state.ID))
                    con.commit()
                    con.close()
                    st.session_state.av=3                
                    
                    
            with cold2:
                non2=st.button('Non')
                if non2:
                    st.session_state.av=4
    def rerun():
            st.session_state.ID=''
            st.session_state.LOC=''
            st.session_state.av=0        
            # st.experimental_rerun()
        
    if st.session_state.av==3:   
        st.write(f"Moule {st.session_state.ID} transféré à l'emplacement {LOC}")
        suivant=st.button('Cliquez pour passer au scan suivant',on_click=rerun)


    if st.session_state.av==4: 
        st.write('transfert annulé')
        suivant2=st.button('Cliquez pour passer au scan suivant',on_click=rerun)

if selected=="Export table":

    validation_export=st.button("Exporter la table des moules")
    if validation_export:                            
        con = sqlite3.connect("Moules.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM Moules')
        rows = cur.fetchall()
        fichier='table_moule.csv'
        with open(fichier, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Écriture de l'en-tête
            writer.writerow([i[0] for i in cur.description])
            # Écriture des données
            for row in rows:
                writer.writerow(row)
            # Fermeture de la connexion à la base de données SQLite3
        cur.close()
        con.close()
        df = pd.read_csv(fichier)
        df=df.set_index('Moule_ID')
        # df=df.reset_index(drop=True)
        st.write(df)
        csv=df.to_csv().encode('utf-8')
        
if selected=="Codebare (test)":
    prise_video()
