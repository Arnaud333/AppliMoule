import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import csv
# import os
import sqlite3
# from st_aggrid import AgGrid
from streamlit_modal import Modal
from Class_Moule import Moule
from Class_Moule import get_values_to_df
from Class_Moule import table_to_df

### Constantes:
db_file='Moules.db'
### parametre pandas pour afficher du multiligne:
pd.set_option('display.max_colwidth',None)
pd.options.display.max_colwidth=200

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
                    padding-bottom: 0,5rem;
                    padding-left: 0,5rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)


selected = option_menu(
    menu_title='Application de gestion des moules               (démo pour JMT)',
    options=["Gestion Moules", "Export Table","Suivi des Moules"],
    icons=['boxes', 'download','gear'],
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
if 'moule' not in st.session_state:
    st.session_state.moule=''
if 'desc' not in st.session_state:
    st.session_state.desc=''
if 'text_desc_suivi' not in st.session_state:
    st.session_state.text_desc_suivi=''
if 'text_user_suivi' not in st.session_state:
    st.session_state.text_user_suivi=''
if 'modif_suivi' not in st.session_state:
    st.session_state.modif_suivi=''
# if 'valider_nouvelle_des' not in st.session_state:
#     st.session_state.valider_nouvelle_des=''
valider_nouvelle_des=''
def change():
    st.session_state.av=1

if selected=="Gestion Moules":   

    if st.session_state.av<2:

        ID=st.text_input("Scannez ou saisissez l'ID moule à traiter :",value='',on_change=change,key='input_ID')
        st.session_state.ID=ID
        if ID!='':
            st.session_state.av=1


    if st.session_state.ID !='':
        
        moule=Moule(st.session_state.ID)
        st.session_state.moule=moule
        if not moule.exist:
            st.write(f"Nouveau Moule {ID} saisissez une description et confirmez la création?")
            colg, cold =st.columns([1,1])
            with colg:
                desc=st.text_input('Description du moule :')
                st.session_state.desc=desc
                oui=st.button('Confirmer création')
                if oui:
                    moule.valid_new_mold(desc)
                    st.session_state.ID=ID
                    st.session_state.LOC=''
                    st.session_state.moule=moule
                    st.session_state.av=2
                    
            # with cold:
            #     non=st.button('Non')                

        else:
            
            st.session_state.LOC=moule.loc
            st.session_state.moule=moule
            st.session_state.desc=moule.desc
            
            st.session_state.av=2


    if st.session_state.av>1:
        moule=st.session_state.moule
       
        st.write('moule selectionné',st.session_state.ID)
        st.write(f'Description du moule : ',moule.desc)
        st.write(f'Emplacement actuel du moule {st.session_state.ID} :',st.session_state.LOC)
        LOC=st.text_input("Scannez ou saisissez le nouvel emplacement du moule :")

        if LOC!='':
            st.session_state.LOC=LOC
            st.write('Confirmez le transfert du moule')
            colg2, cold2 =st.columns([1,1])
            with colg2:
                oui2=st.button('Oui')
                if oui2:
                    moule.Update_loc(LOC)
                    st.session_state.av=3
                    st.session_state.moule=moule               
                                        
            with cold2:
                non2=st.button('Non')
                if non2:
                    st.session_state.av=4
                    st.session_state.moule=moule
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

def export_table(table, file, key_col):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(f'SELECT * FROM {table}')
    rows = cur.fetchall()
    fichier=file #nom du fichier de sortie
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
    df=df.set_index(key_col)
    # df=df.reset_index(drop=True)
    st.write(df)
    csv_file=df.to_csv().encode('utf-8')
    st.download_button('Télécharger la table',csv_file,file)


if selected=="Export Table":
    Exp=st.container()
    with Exp:
        col1, col2, col3 = st.columns([3,90,3])
        with col1:
            pass
        with col2:
            choix_table=st.selectbox('Choisissez la table à exporter',['Aucun','Table Moules', 'Table Mouvements', 'Table suivi des moules'],index=0 )
            # validation_export_moules=st.button("Exporter la table des moules")
            if choix_table=='Table Moules':   
                df=table_to_df('Moules')
                st.write(df)
                csv_file=df.to_csv().encode('utf-8')
                st.download_button('**Télécharger la table**',csv_file,'table_moules.csv')
                
            if choix_table=='Table Mouvements':  
                df=table_to_df('Mouvements')
                st.write(df)
                csv_file=df.to_csv().encode('utf-8')
                st.download_button('**Télécharger la table**',csv_file,'Table_Mouvements.csv')  

            if choix_table=='Table suivi des moules':   
                df=table_to_df('Moule_Suivi')
                st.write(df)
                csv_file=df.to_csv().encode('utf-8')
                st.download_button('**Télécharger la table**',csv_file,'Table_Suivi_Moule.csv',)   
                            

        with col3:
            pass
        
if selected=="Suivi des Moules":
    # modal=Modal('test','m')
    # modal.open()
    def local_css(file_name):   
        with open(file_name) as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    
    def update_suivi(i,id,moule):
        # st.write('compteur ',i)
        test_data=False
        values={}
        if st.session_state.text_desc_suivi!='':
            values={'Description_Action': st.session_state.text_desc_suivi}
            test_data=True
        if st.session_state.text_user_suivi!='':
            values.update({'Intervenant':st.session_state.text_user_suivi})
            test_data=True
        # st.write('id',id)
        if test_data:
            moule.Update_mold_follow_up(id,values)
            st.experimental_rerun()
        

    def generate_html_tab(List_Col,df,moule):
        con={}  #dictionnaire des conteneurs
        col={} #dictionnaire des colonnes
        check={}
        id={}
        nb_col=df.shape[1]+1
        nb_row = df.shape[0]
        for i in range(nb_row):
            con[i]=st.container()
            
            with con[i]:
                # col_row={str(i)+str(j) : st.columns(List_Col[j]) for j in range(nb_col)}
                # col.update(col_row)
                col[str(i)+'1'],col[str(i)+'2'],col[str(i)+'3'],col[str(i)+'4']=st.columns(List_Col)

                for j in range(1,nb_col):
                    
                    with col[str(i)+str(j)]:
                        if j<4:
                           st.write(df.iloc[i,j])
                        else:
                            if st.session_state.modif_suivi:
                                id[i]=df.iloc[i,0]
                                # check[i]=st.button('Modifier',on_click=update_suivi(i,id[i],moule),key='check_suivi'+str(i))
                                check[i]=st.button('Modifier',key='check_suivi'+str(i))
                                if check[i]:
                                    update_suivi(i,id[i],moule)

    

    ID=st.text_input("Scannez ou saisissez l'ID moule à traiter :",value='')

    if ID != '':
        moule=Moule(ID)
        if moule.exist :

            st.write(f"Le moule {moule.id} {moule.desc} est séléctionné")
            modif_des=st.expander("Souhaitez vous modifier la description du moule?")
            with modif_des:
                new_des=st.text_input("Veuillez saisir la nouvelle description")
                valider_nouvelle_des=st.button('Valider')
                if valider_nouvelle_des:
                    moule.Update_Desc(new_des)
                    st.experimental_rerun()
                
                    
            # gridOptions = {defaultColDef: {
            #                 resizable: true,
            #                 initialWidth: 200,
            #                 wrapHeaderText: true,
            #                 autoHeaderHeight: true,
            #             },
            #             columnDefs: columnDefs,
            #             }

            local_css("style.css")        
            # cont1=st.expander('',expanded=True)
            
            cont1=st.container()
            with cont1:
                col1,col2,col3,col4=st.columns([2,8,2,2])
                with col1:
                    st.markdown('**Date**')
                with col2:
                    st.markdown('**Action**')
                with col3:
                    st.markdown('**Auteur**')
                with col4:
                    st.write('')
            
            df=get_values_to_df('Moule_Suivi',['id','Date','Description_Action','Intervenant'],'Moule_ID',ID)
            generate_html_tab([2,8,2,2],df,moule)

            # AgGrid(moule.Display_mold_follow_up()) 
            # st.table(moule.Display_mold_follow_up())
            # df = pd.DataFrame({'Date': ['S5'], 'Actions': ['                   '], 'Auteur':['  ']})
            # grid_return = AgGrid(df, editable=True)
            # new_df = grid_return['data']

            modif_suivi=st.checkbox('Voulez modifier des infos de suivi déjà renseignées?',value=False, key='modif_suivi')

            desc=st.text_area('Veuillez saisir le nouveau suivi du moule',key='text_desc_suivi')
            user=st.text_input("Veuillez indiquer l'auteur",key='text_user_suivi')
            valid_ajout=st.button("Valider l'ajout de suivi moule")
            if valid_ajout:
                moule.Add_mold_follow_up(desc,user)
                st.experimental_rerun()

            
        else:
            st.write(f"Le moule {ID} n'existe pas")

