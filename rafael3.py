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
     
import os  
import base64 
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
import matplotlib
matplotlib.use('Agg')
anos = ['Todos os anos',2017,2018,2019,2020]
centros = ['Todos os centros','CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ']
area = ['Todos as áreas', 'Ciências Agrárias', 'Ciências Biológicas', 'Ciências Exatas e da Terra', 'Ciências Humanas', 'Ciências Sociais Aplicadas', 'Ciências da Saúde', 'Engenharias', 'Lingüística, Letras e Artes', 'Multidisciplinar']

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

abas = html.Div([
    dcc.Tabs(id='aba-example3', value='aba3-1', children=[
        dcc.Tab(label='Diagrama de Venn', value='aba3-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Evolução docentes', value='aba3-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Relação da Média de Docentes', value='aba3-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Relação Docente/Projeto', value='aba3-4', style=tab_style, selected_style=tab_selected_style),
])
    ,html.Br()])




nav = Navbar()    
venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
card_content = [
    dbc.CardHeader("Entendendo o gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.P(
                children=f'''O gráfico analisado é uma análise de variabilidade, a fim de visualizar a quantidade de professores e alunos que 
                trabalharam em projetos de extensão apenas no ano de 2017, 2018 ou 2019, bem como suas respectivas intersecções. Podemos
                analisar que, como escolhido, está sendo filtrado em apenas os centros: CEAR para serem visualizados. Esses dados foram representados pelo diagrama de Venn.''',
                className="card-text",id='relatorio_docentes3',style={'text-align':'justify'}
            ),
        ]
    ),
]



jumbotron = dbc.Card(card_content,  outline=True)

card_content_2 = [
    dbc.CardHeader("Filtros do Gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        abas,
        html.H4("Escolha os anos que deseja analisar", style={'font-size':19}),
        dcc.Dropdown(
        id = 'anos3',  
        options=[
            {'label': j, 'value': j} for j in anos  
        ],
        value=[2017,2018,2019],   
        multi=True,
    searchable=False,
         style={'margin-bottom':'10px'}
   

        ),        
        html.H4("Escolha os centros desejados", style={'font-size':19}),
        dcc.Dropdown(
        id = 'centros3',  
        options=[
            {'label': j, 'value': j} for j in centros  
        ],
        value=['CEAR'],   
        multi=True,
    searchable=False,
         style={'margin-bottom':'10px'}
   

    ),
        html.H4("Escolha as áreas desejadas:", style={'font-size':19}),
        dcc.Dropdown(
        id = 'area3',  
        options=[
            {'label': j, 'value': j} for j in area  
        ],
        value=['Engenharias','Multidisciplinar','Ciências Exatas e da Terra'],   
        multi=True,
    searchable=True,
         style={'margin-bottom':'10px'}
   

    ),
        ]
    ),
]

jumbotron_2 = dbc.Card(card_content_2,  outline=True)
card_content_3 = [
    dbc.CardHeader(id='card_doc3',style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.Img(id='graph_docentes3',
            style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            ,src='data:image/png;base64,{}'.format(venn.decode())
                ),

            html.Div(id='graph_docentes_23',
            style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            )
        ]
    ),
]

jumbotron_3 = dbc.Card(card_content_3,  outline=True)

body_1 =html.Div([  

    

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

modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um centro como parâmetro de entrada de centros"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close3", className="ml-auto")
                ),
            ],
            id="modal3",
        ),
    ]
)

modal_2 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos dois anos como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_23", className="ml-auto")
                ),
            ],
            id="modal_23",
        ),
    ]
)

modal_3a = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha no máximo três anos como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_3a3", className="ml-auto")
                ),
            ],
            id="modal_3a3",
        ),
    ]
)
modal_53 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos uma área como parâmetro de entrada de áreas"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_53", className="ml-auto")
                ),
            ],
            id="modal_53",
        ),
    ]
)


def rafael3():
    layout = html.Div([
    nav,
	body_1,
	modal,
	modal_2,
    modal_3a,
    modal_53,
    html.Div([], id='rafa3', style={'display': 'none'})

     #html.Iframe(id='mapa', srcDoc=open('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  

     #html.Iframe(id='mapa', srcDoc=open('Apoio/mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  
    ])
    return layout

    



