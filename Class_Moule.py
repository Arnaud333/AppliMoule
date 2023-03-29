#### Import des dépendances
import sqlite3
import datetime
import pandas as pd
import streamlit as st

### Constantes:
db_file='Moules.db'

### parametre pandas pour afficher du multiligne:
pd.set_option('display.max_colwidth',None)
pd.options.display.max_colwidth=200

#### Fonctions utiles pour la classe Moule
def update_table(table_name, key_column, key_value, update_values_dict):
    """
    Met à jour une ligne dans une table SQLite.
    :param db_file: Le fichier de la base de données SQLite.
    :param table_name: Le nom de la table à mettre à jour.
    :param key_column: Le nom de la colonne clé.
    :param key_value: La valeur de la clé pour la ligne à modifier.
    :param update_values_dict: Un dictionnaire contenant les noms des colonnes à mettre à jour comme clés, et les nouvelles valeurs comme valeurs.
    """
    # Vérifier que le dictionnaire n'est pas vide
    if not update_values_dict:
        raise ValueError("Le dictionnaire des valeurs à mettre à jour est vide.")

    # Créer une liste des colonnes à mettre à jour et une liste des nouvelles valeurs à partir du dictionnaire

    update_columns = list(update_values_dict.keys())
    update_values = list(update_values_dict.values())
    # st.write('val',update_values)
    # st.write('testval',isinstance(update_values,list))
    # st.write('col',update_columns)
    # Connexion à la base de données
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Mettre à jour les valeurs des colonnes
    set_query = ", ".join([f"{col} = ?" for col in update_columns])
    update_query = f"UPDATE {table_name} SET {set_query} WHERE {key_column} = ?"
    
    c.execute(update_query, update_values + [key_value])
   
    # Enregistrer les modifications et fermer la connexion à la base de données
    conn.commit()
    conn.close()

def insert_row(table_name, row_dict):
    """
    Insère une nouvelle ligne dans une table SQLite.
    :param db_file: Le fichier de la base de données SQLite.
    :param table_name: Le nom de la table dans laquelle insérer la ligne.
    :param row_dict: Un dictionnaire contenant les noms des colonnes comme clés et les valeurs à insérer comme valeurs.
    """
    # Vérifier que le dictionnaire n'est pas vide
    if not row_dict:
        raise ValueError("Le dictionnaire des valeurs à insérer est vide.")

    # Créer une liste des noms de colonnes et une liste des valeurs à insérer à partir du dictionnaire
    columns = list(row_dict.keys())
    values = list(row_dict.values())

    # Construire la requête SQL pour insérer la nouvelle ligne
    column_names = ", ".join(columns)
    value_placeholders = ", ".join(["?" for _ in values])
    insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({value_placeholders})"

    # Connexion à la base de données
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Exécuter la requête d'insertion avec les valeurs appropriées
    c.execute(insert_query, values)

    # Récupérer la clé primaire de la nouvelle ligne insérée
    last_row_id = c.lastrowid

    # Enregistrer les modifications et fermer la connexion à la base de données
    conn.commit()
    conn.close()

    # Retourner la clé primaire de la nouvelle ligne insérée
    return last_row_id

def get_value(table_name,key_column, primary_key, field_name):
    """
    Récupère la valeur d'un champ spécifié pour une ligne donnée, en fonction de sa clé primaire.
    :param db_file: Le fichier de la base de données SQLite.
    :param table_name: Le nom de la table à interroger.
    :key_column : le nom de la colonne de la clé primaire
    :param primary_key: La valeur de la clé primaire de la ligne à interroger.
    :param field_name: Le nom du champ à récupérer.
    :return: La valeur du champ demandé.
    """
    # Construire la requête SQL pour récupérer la valeur du champ spécifié pour la ligne donnée
    query = f"SELECT {field_name} FROM {table_name} WHERE {key_column} = ?"

    # Connexion à la base de données
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Exécuter la requête de sélection avec la clé primaire spécifiée
    c.execute(query, (primary_key,))
    row = c.fetchone()

    # Vérifier si une ligne a été trouvée
    if row is None:
        value=False
    else:    
        # Récupérer la valeur du champ demandé
        value = row[0]

    # Fermer la connexion à la base de données
    conn.close()

    # Retourner la valeur du champ demandé
    return value

def get_values_to_df(table_name, columns, filter_column, filter_value):
    # Ouvrir la connexion à la base de données
    conn = sqlite3.connect(db_file)

    # Préparer la requête SQL pour sélectionner les colonnes spécifiées à partir de la table spécifiée,
    # en filtrant sur la colonne spécifiée avec la valeur spécifiée
    query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE {filter_column} = ?"

    # Récupérer les résultats de la requête sous forme d'un dataframe pandas
    df = pd.read_sql_query(query, conn, params=[filter_value])

    # Fermer la connexion à la base de données
    conn.close()

    # Retourner le dataframe pandas
    return df

def table_to_df(table_name):
    # Ouvrir la connexion à la base de données
    conn = sqlite3.connect(db_file)   

    # Récupérer les résultats de la requête sous forme d'un dataframe pandas
    df = pd.read_sql_query(f"SELECT * from {table_name}", conn)
    # Fermer la connexion à la base de données  
    conn.close()

    # Retourner le dataframe pandas
    return df




class Moule:
    def __init__(self,ID):
            self.id=ID  #Numero de moule = ID
            if get_value('Moules','Moule_ID',ID,'Emplacement') is False:  #on verifie si le moule existe déjà dans la table et stock l'information dans exist
                self.exist=False
            else:
                self.exist=True
            if self.exist:
                self.loc=get_value('Moules','Moule_ID',ID,'Emplacement') #On récupère l'emplacement du moule si une ligne existe sera none si le moule n'existe pas.
            else:
                self.loc=None
            if self.exist:
                self.desc=get_value('Moules','Moule_ID',ID,'Description') #On récupère la description du moule si une ligne existe,sera none si le moule n'existe pas.
            else:
                self.desc=None

    def valid_new_mold(self, desc):
        now = datetime.datetime.now()  
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M")
        insert_row('Moules',{'Moule_ID':self.id,'Description':desc,'Date_creation': date_str + ' ' + time_str})
    
    def Update_Desc(self, new_desc):        
        update_table('Moules','Moule_ID', self.id, {'Description':new_desc})
        self.desc=new_desc

    def Update_loc(self, new_loc):      
        now = datetime.datetime.now()  
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M")
        update_table('Moules','Moule_ID', self.id, {'Emplacement':new_loc})        
        insert_row('Mouvements',{'Moule_ID':self.id,'Prev_loc':self.loc,'Next_loc':new_loc,'Date': date_str + ' ' + time_str})
        self.loc=new_loc

    def Add_mold_follow_up(self, desc, user):
        now = datetime.datetime.now()  
        date_str = now.strftime("%d/%m/%Y")
        insert_row('Moule_Suivi',{'Moule_ID':self.id,'Date':date_str ,'Description_Action':desc,'Intervenant': user})
    
    def Display_mold_follow_up(self):
        df=get_values_to_df('Moule_Suivi',['Date','Description_Action','Intervenant'],'Moule_ID',self.id)
        return df
    
    def Update_mold_follow_up(self,id,values):
        update_table('Moule_Suivi', 'id', int(id), values)

            
            


            
