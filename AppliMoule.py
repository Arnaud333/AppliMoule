
import streamlit as st

import sqlite3

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

if 'ID' not in st.session_state:
    st.session_state.ID=''
if 'LOC' not in st.session_state:
    st.session_state.LOC=''
if 'av' not in st.session_state:
    st.session_state.av=0


st.header('AppliMoules')
st.write('démo pour JMT')

if st.session_state.av==0:
    ID=st.text_input("Scannez le moule à traiter :",value='',key='input_ID')
    st.session_state.ID=ID

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
                st.session_state.av=1
        with cold:
            non=st.button('Non')
            

    else:
        
        con = sqlite3.connect("Moules.db")
        cur = con.cursor()
        cur.execute("SELECT Emplacement FROM moules WHERE Moule_ID = ?", (st.session_state.ID,))
        result = cur.fetchone()
        con.close()
        st.session_state.LOC=result[0]
        st.session_state.av=1


if st.session_state.av>0:
    st.write('moule selectionné',st.session_state.ID)
    st.write(f'Emplacement actuel du moule {st.session_state.ID} :',st.session_state.LOC)
    LOC=st.text_input("Scannez le nouvel emplacement du moule :")

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
                st.session_state.av=2                
                
                
        with cold2:
            non2=st.button('Non')
            if non2:
                st.session_state.av=3
def rerun():
        st.session_state.ID=''
        st.session_state.LOC=''
        st.session_state.av=0        
        # st.experimental_rerun()
    
if st.session_state.av==2:   
    st.write(f"Moule {st.session_state.ID} transféré à l'emplacement {LOC}")
    suivant=st.button('Cliquez pour passer au scan suivant',on_click=rerun)


if st.session_state.av==3: 
    st.write('transfert annulé')
    suivant2=st.button('Cliquez pour passer au scan suivant',on_click=rerun)