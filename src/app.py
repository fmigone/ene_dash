#!/usr/bin/env python
# coding: utf-8

# In[7]:





# In[10]:


import plotly.express  as px
import pandas as pd 
import numpy as np
import requests


import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import dash_table
import dash_bootstrap_components as dbc

import dash 
import dash_core_components as dcc
from jupyter_dash import JupyterDash
import dash_html_components as html

#Ajouter interview_statut à dataTB pour les tests
df = pd.read_excel(r'dataTB.xlsx')


#Instantiation d'un objet Dash dans Jupyter
#app = JupyterDash(__name__)

#Définition de la mise en page de l'appp
#app.layout = dcc.Graph(id = "exemple-graph", figure=bar_fig)

#Exécution de l'application 
#if __name__ == '__main__':
#    app.run_server(debug = True)
containers = {'Equipe':'Equipe','district':'District', 'milieu':'Milieu',
        'departement':'Département','sous prefecture':'Sous préfecture/Commune' }

containers.keys()



# Création de l'application Dash
bootstrap_theme=[dbc.themes.BOOTSTRAP,'https://use.fontawesome.com/releases/v5.9.0/css/all.css']
app = dash.Dash(__name__)
server = app.server

# Styles
styles = {
    'all' :{'background': '#f2f2f2','height':"500px"},
    'logo1': {'float': 'left', 'padding': '10px', 'width': '100px', 'height': '100px'},
    'logo2': {'float': 'right', 'padding': '10px', 'width': '100px', 'height': '100px'},
    'title': {'textAlign': 'center','border': '3px solid #333333', 'padding': '10px', 'color': '#333333',
    'border-radius':'3%', 'backgroundColor':'#7FFF00', 'width':'140%', 'height':'50%'},
    'container': {'backgroundColor': 'lightgreen', 'padding': '5px', 'margin': '5px', 'border-radius':'3%', 'display': 'inline-block',
                  },
    'container-2': {'backgroundColor': 'lightgreen', 'padding': '15px', 'margin': '15px', 'border-radius':'3%', 'display': 'inline-block',
                  'border': '2px solid #333333'}}

containers = {'Equipe':'Equipe','district':'District', 'milieu':'Milieu',
        'departement':'Département','sous prefecture':'Sous préfecture/Commune','ZD':'ZD','segment':'Segment',
        'MODINTR':'Trimestre actuel', 'V1MODINTR':'Trimestre précédent'}

def adjust_label(var,data = containers):
    if var =='sous prefecture':
        return html.Div([html.Strong(html.Label('Sous préfecture/')) , 
                         html.Br(),
                         html.Strong(html.Label('Commune'))], style={'color': 'black', 'textAlign': 'center','border': '1px solid #333333','backgroundColor':'#7FFF00','border-radius':'3%'})
    else:
        return html.Div([html.Strong(html.Label(containers[var])), 
                         html.Br()],  style={'color': 'black', 'textAlign': 'center','border': '1px solid #333333','backgroundColor':'#7FFF00','border-radius':'3%'}) 



def create_container(var):
    style = {**styles['container-2'] }
    container =html.Div([
        adjust_label(var),
        dcc.Checklist(
            id= var,
            options= sorted(df[var].unique()),
            value= []
        )
    ], style=style)

    return container

def create_container_bigger(var):
    style = {'width': '40%', 'height':'40%',**styles['container'],'border-radius':'3%','border': '3px solid #333333'}
    data = {'Mod': ['face', 'pile'],
        'Value': [10, 20]}

    # Créer une figure horizontale avec Plotly Express
    fig = px.bar(data, x='Value', y='Mod', orientation='h', labels={'Mod': 'Modalités'})
    container =html.Div(
        [adjust_label(var),
        dcc.Graph(id= var, figure =fig ) 
            ], style=style)

    return container
# Exemple de données pour la table

def separator(n):
    list = [html.Br()]*n
    return html.Div(list)

def return_initial_table():
    table = df[['Equipe','Nb_ques_complet','Nb_valide_chef','Nb_rejet_chef','Nb_rejet_HQ']].groupby('Equipe').sum()
    table =  table.reset_index()
    table = table.rename(columns={'Equipe':'Equipes',
                        'Nb_ques_complet':'Entretiens mén/ind terminés',
                        'Nb_valide_chef':"Questionnaires validés par le chef d'équipe",
                        'Nb_rejet_chef':"Questionnaires rejetés par le chef d'équipe",
                        'Nb_rejet_HQ':"Questionnaires rejetés par le superviseur"})
    return table

#
def create_figure(data = df, i=1):
    if i ==1:
        list_var = ['Nb_men_complet','Nb_men_partiel','Nb_men_autre']
        titre = 'Répartition des questionnaires ménages par statut'
    elif i ==2:
        list_var =['Nb_ques_complet','Nb_ques_partiel', 'Nb_qes_autre']
        titre = 'Répartition des questionnaires ménages/Individus par statut'
    figure={
        'data': [
            {'x': [1], 'y': [data[list_var[0]].sum()], 'type': 'bar', 'name': 'Ménages totalement administrés', 'text': [data[list_var[0]].sum()]},
            {'x': [2], 'y': [data[list_var[1]].sum()], 'type': 'bar', 'name': 'Ménages partiellement administrés',  'text': [data[list_var[1]].sum()]},
            {'x': [3], 'y': [data[list_var[2]].sum()], 'type': 'bar', 'name': 'Autres ménages',  'text': [data[list_var[2]].sum()]},
        ],
        'layout': {
        'title': titre,
        }
    
            }
    return figure


# Mise en page de l'application
app.layout = html.Div(style= styles['all'], children=[
    separator(1),
    
    html.Div([
        html.Div( html.Img(src=r'D:\personal\INS\enquete menage continue\application Dash\backend\logo_ins.jpeg',
        style=styles['logo1'])),
        html.Div(html.H1('Tableau de suivi de collecte Enquête Ménage', style=styles['title'])),

        html.Div(html.Img(src='logo2.png', style=styles['logo2'])),
           ], 
           style = {'display': 'flex', 'justify-content': 'space-between', 'flex-wrap': 'wrap'}),

     separator(2),

    html.Div(children = [
        create_container('Equipe'),
        create_container('district'),
        create_container('milieu'),
        create_container('departement'),
        create_container('sous prefecture'),
        create_container('ZD'),
        create_container('segment'),

        html.Div([
            html.Strong(html.Div(id = "nombre total d entretien",  children=str(df['Nb_ques_complet'].sum()),
                                  style={'font-size': '24px', 'textAlign': 'center',})),

            html.Strong( html.Label("Nombre total d'entretiens", style={'color': 'black','font-size': '14px', 'textAlign': 'center',})),

        ],style={'backgroundColor': 'lightgreen', **styles['container'], 'width':'14%', 'height':'70px',
               'color': 'black', 'textAlign': 'center','border': '1px solid #333333','backgroundColor':'#7FFF00','border-radius':'3%' })],
        style={'display': 'flex', 'justify-content': 'space-between', 'flex-wrap': 'wrap'}) ,
    
    
        separator(4),
    
        html.Div(children = [
        create_container_bigger('MODINTR'),
        create_container_bigger('V1MODINTR'),], 
        
        style={'display': 'flex','justify-content': 'space-between', 'flex-wrap': 'wrap'}),

        separator(4),
    html.Div(children = [

    # dcc.Graph(
    #    id='bar-chart-2',
    #   figure=px.bar(data, x='sex', y='tip', title='Répartition des questionnaires ménages/individu par statut'),
    #   style={'width': '50%', 'height': '500px'}) ,
        
    dcc.Graph(
            id='graph-1',
            figure=create_figure(data = df, i=1 )
            ), 
            
    dcc.Graph(
            id='graph-2',
            
            figure=create_figure(data = df, i=2 )
            )],
    style={'display': 'flex', 'justify-content': 'space-between', 'flex-wrap': 'wrap',}),
    #'backgroundColor': 'lightgreen'
    
   separator(4),
    
    html.Div(
        children = [
    dash_table.DataTable(
        id='table',
        data=return_initial_table().to_dict('records'),
    )]) 
])


list_var  = ['Equipe','district', 'milieu','departement','sous prefecture']

#{'Equipe':'Equipe','district':'District', 'milieu':'Milieu',
#        'departement':'Département','sous prefecture':'Sous préfecture/Commune' }

#Callback from district to milieu

#Callback from district to milieu
@app.callback(
    Output(component_id= 'Equipe', component_property='options'),
    Output(component_id= 'district', component_property='options'),
    Output(component_id= 'milieu', component_property='options'),
    Output(component_id= 'departement', component_property='options'),
    Output(component_id= 'sous prefecture', component_property='options'),
    Output(component_id= 'ZD', component_property='options'),
    Output(component_id= 'segment', component_property='options'),
    Output(component_id= 'nombre total d entretien', component_property='children'),
    Output(component_id= 'graph-1', component_property='figure'),
    Output(component_id= 'graph-2', component_property='figure'),
    Output(component_id= 'table', component_property='data'),

    Input(component_id= 'Equipe', component_property='value'),
    Input(component_id= 'district', component_property='value'),
    Input(component_id= 'milieu', component_property='value'),
    Input(component_id= 'departement', component_property='value'),
    Input(component_id= 'sous prefecture', component_property='value'),
    Input(component_id= 'ZD', component_property='value'),
    Input(component_id= 'segment', component_property='value'),
    )

def update_output(value_equipe, value_district,value_milieu, value_departement, value_sous_prefecture,value_ZD, value_segment):

    list_var  = ['Equipe','district', 'milieu','departement','sous prefecture','ZD','segment']
    values = {'Equipe': value_equipe,'milieu': value_milieu,'district': value_district,
                    'departement': value_departement, 'sous prefecture': value_sous_prefecture,
                    'ZD':value_ZD,'segment':value_segment}
    for var,value in values.items():
        if len(value)==0:
            values[var] = df[var].unique()
            
    list_not_empty = {var:value for var,value in values.items() if len(value) != 0}

    dff = df.copy()

    def fill_var(var):
        return df[var].isin(values[var])
    
    dff = df[fill_var('milieu')&
    fill_var("Equipe")&
    fill_var("district")&
    fill_var('departement')&
    fill_var('sous prefecture')&
    fill_var('ZD')&
    fill_var('segment')]
    

    nombre_entretien = dff['Nb_ques_complet'].sum() + dff['Nb_ques_partiel'].sum()+dff['Nb_qes_autre'].sum()
    
    figure_1 = create_figure(data = dff, i = 1)
    figure_2 = create_figure(data = dff,i =2)

    table = dff[['Equipe','Nb_ques_complet','Nb_valide_chef','Nb_rejet_chef','Nb_rejet_HQ']].groupby('Equipe').sum()
    table =  table.reset_index()
    table = table.rename(columns={'Equipe':'Equipes',
                        'Nb_ques_complet':'Entretiens mén/ind terminés',
                        'Nb_valide_chef':"Questionnaires validés par le chef d'équipe",
                        'Nb_rejet_chef':"Questionnaires rejetés par le chef d'équipe",
                        'Nb_rejet_HQ':"Questionnaires rejetés par le superviseur"})
    table.loc['Total'] = table.sum()

    #Resultats
    list_result = [ 
        dff['Equipe'],
        dff["district"],
        dff['milieu'],
        dff['departement'],
        dff['sous prefecture'],
        dff['ZD'],
        dff['segment']
        ]
    return [sorted(result.unique()) for result in list_result] + [nombre_entretien, figure_1,figure_2, table.to_dict('records')]
# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True, port = 8049)


# In[ ]:




