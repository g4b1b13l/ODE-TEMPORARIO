import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output
import plotly.offline as py
from plotly.graph_objs import *   
import plotly.graph_objs as go 
import dash_bootstrap_components as dbc
import folium  
from folium import IFrame, FeatureGroup 
from plotly.subplots import make_subplots     
import os  
import glob  
import pandas as pd 
from folium.plugins import MarkerCluster   



### Data
import pandas as pd
import pickle
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
## Navbar
from navbar import Navbar
import base64

ano = [2017,2018,2019,2020,'Todos os anos']
centro = ['Todos os centros','CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ']
nav = Navbar()    
graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Professores'],  shared_yaxes=True)
##########
tab_selected_style = {
    'font-size': '70%',
    'padding': '6px'
}

tab_style = { #Estilos das Tabs
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-size': '75%',
    'fontSize' : '13'
    }
#####
tabs = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-2', children=[
        #dcc.Tab(label='Relação Discente/Docente', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Evolutivo', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Gráfico da Media de Discentes', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        #dcc.Tab(label='Relação Discente/Projeto', value='tab-4', style=tab_style, selected_style=tab_selected_style),
])
    ,html.Br()])

####
card_content = [
    dbc.CardHeader("Entendendo o gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.P(
                children=f'''O gráfico analisado é a relação entre Discentes/Docentes, a fim de visualizar o envolvimento dos discentes 
                em projetos de extensão nos anos de 2017, 2018, 2019, 2020. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                os centros: CEAR para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                analisar os centros que possuem mais docentes que discentes, quando os valores obtidos forem menores que 1, e os que possuem 
                mais alunos que professores, para valores maiores que 1.''',
                className="card-text",id='relatorio_discentes',style={'text-align':'justify'}
            ),
        ]
    ),
]



jumbotron = dbc.Card(card_content,  outline=True)

card_content_2 = [
    dbc.CardHeader("Parâmetros do Gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        tabs,
        html.H4("Escolha os anos que deseja analisar", style={'font-size':19}),
        dcc.Dropdown(
        id = 'ano',  
        options=[
            {'label': j, 'value': j} for j in ano  
        ],
        value=[2017,2018,2019,2020],   
        multi=True,
    searchable=False,
         style={'margin-bottom':'10px'}
   

        ),        
        html.H4("Escolha os centros desejados", style={'font-size':19}),
        dcc.Dropdown(
        id = 'centro',  
        options=[
            {'label': j, 'value': j} for j in centro  
        ],
        value=['CEAR'],   
        multi=True,
    searchable=True,
         style={'margin-bottom':'10px'}
   

    ),
        ]
    ),
]

jumbotron_2 = dbc.Card(card_content_2,  outline=True)
card_content_3 = [
    dbc.CardHeader(id='card',style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.Div(id='graph_discentes',
            style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            )
        ]
    ),
]

jumbotron_3 = dbc.Card(card_content_3,  outline=True)



body_rel =html.Div([  

    

        dbc.Row(
           [
               dbc.Col(
                  [jumbotron_2,
                        jumbotron]

        , md=4

               ),
              dbc.Col([
						jumbotron_3
                #html.Iframe(id='mapa', srcDoc=open('Apoio/venn.svg', 'r').read(),width='100%',height='500px'),  

                    ], md=8 ),

                ],no_gutters=True
            ),
              
])

modal_3 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um centro como parâmetro de entrada de centros"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_3", className="ml-auto")
                ),
            ],
            id="modal_3",
        ),
    ]
)

modal_4 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um ano como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_4", className="ml-auto")
                ),
            ],
            id="modal_4",
        ),
    ]
)



def discente():
    layout = html.Div([
    nav,
	body_rel,
	modal_3,
	modal_4

     #html.Iframe(id='mapa', srcDoc=open('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  

     #html.Iframe(id='mapa', srcDoc=open('Apoio/mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  
    ])
    return layout


