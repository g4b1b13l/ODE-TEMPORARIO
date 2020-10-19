'''import pandas as pd
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
init_notebook_mode(connected=True)
import dash_bootstrap_components as dbc

import dash
import dash_core_components as dcc
import dash_html_components as html


from navbar import Navbar



nav = Navbar()

#dados = pd.read_csv('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\Atividade Rafael\\contagem')    
#dados2 = pd.read_csv('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\Atividade Rafael\\relacao') 

dados = pd.read_csv('Apoio/contagem.csv')
dados2 = pd.read_csv('Apoio/relacao')

fig_1 = make_subplots(rows=1, cols=1,row_titles = ['Quantidade de Membros'],  shared_yaxes=True)

fig_1.add_trace(go.Bar(x=['2017','2018','2019'], y=dados[dados['a']=='DISCENTE']['descricao'].to_list(), name='DISCENTE'),1,1)
fig_1.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
fig_1.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
fig_1.update_layout(title_text='Elvolvimento com Extensão por Ano', title_x=0.5)

fig_1.add_trace(go.Bar(x=['2017','2018','2019'], y=dados[dados['a']=='DOCENTE']['descricao'].to_list(), name='DOCENTE'),1,1)
fig_1.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
fig_1.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))

fig_1.add_trace(go.Bar(x=['2017','2018','2019'], y=dados[dados['a']=='SERVIDOR']['descricao'].to_list(), name='SERVIDOR'),1,1)
fig_1.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
fig_1.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))







fig_2 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'}]], subplot_titles=['2017', '2018','2019'])

fig_2.update_layout(autosize=True)#,width=990,height=400)
fig_2.update_traces(textposition='inside')
fig_2.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
fig_2.add_trace(go.Pie(labels=['DISCENTE','DOCENTE','SERVIDOR'], values=dados['descricao'].loc[:2], textinfo='percent', name='2017'),1, 1)
fig_2.add_trace(go.Pie(labels=['DISCENTE','DOCENTE','SERVIDOR'], values=dados['descricao'].loc[3:5], textinfo='percent', name='2018'),1, 2)
fig_2.add_trace(go.Pie(labels=['DISCENTE','DOCENTE','SERVIDOR'], values=dados['descricao'].loc[6:], textinfo='percent', name='2019'),1, 3)
fig_2.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
fig_2.update_layout(title_text='Percentual de Envolvimento por Ano', title_x=0.5)




dados2[['2017','2018','2019']] = dados2[['2017','2018','2019']].applymap(lambda x : "%.2f" % x)

fig_3 = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Professores'],  shared_yaxes=True)

fig_3.add_trace(go.Bar(x=dados2['centro'].to_list(), y= dados2['2017'].to_list(), name='2017',text=dados2['2017'].to_list(), textposition='auto',),1,1)
fig_3.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=False)
fig_3.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
fig_3.update_layout(title_text='Razão entre Discentes e Docentes por Centro nos Anos de 2017, 2018 e 2019', title_x=0.5)

fig_3.add_trace(go.Bar(x=dados2['centro'], y=dados2['2018'].to_list(), name='2018',text=dados2['2018'].to_list(), textposition='auto',),1,1)
fig_3.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
fig_3.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))

fig_3.add_trace(go.Bar(x=dados2['centro'], y=dados2['2019'].to_list(), name='2019',text=dados2['2019'].to_list(), textposition='auto',),1,1)
fig_3.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
fig_3.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
fig_3.update_layout(yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 0.5)) 

body = html.Div([
    html.Div(children=[
        html.Div('Dados dos participantes de projetos de extensão', className="app-header--title"),
        html.Hr(),
    ],className='app-header'),
    html.Div(html.Br()),
    html.Div(html.Br()), 
    html.Div(html.Br()),
    dbc.Row(
           [
               dbc.Col(
                  [
        html.H4("Paramêtros para o gráfico", style={'font-size':24, 'textAlign':'center'}),
        html.H4("Escolha abaixo qual gráfico você quer exibir:", style={'font-size':19}),
        dcc.Dropdown(
        id='demo-dropdown',
        options=[{'label': i, 'value': i} for i in ['Quantitativo do Envolvimento com projetos por Ano', 'Porcentagem do Envolvimento com projetos por Ano','Relação de Discentes/Docentes por Centro']],
        placeholder="Selecione",
        searchable=False,
        style={'margin-bottom':'10px'}
        ),
        html.Div(id='teste2'),

     
    ],md=4),

    dbc.Col([
    
    html.Div(id='teste')
    ],md=8),
    ]),
    ])
def rafael():
    layout = html.Div([
    nav,
    body,
    ])
    return layout'''

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

sano = [2017,2018,2019,2020,'Todos os anos']
scentro = ['Todos os centros','CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ']
nav = Navbar()    
sgraf = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Professores'],  shared_yaxes=True)
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
    dcc.Tabs(id='stabs-example', value='stab-1', children=[
        dcc.Tab(label='Area Tematica por Centro', value='stab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Area Geral %', value='stab-2', style=tab_style, selected_style=tab_selected_style),
])
    ,html.Br()])

####
card_content = [
    dbc.CardHeader("Entendendo o gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.P(
                children=f'''...''',
                className="card-text",id='srelatorio_discentes',style={'text-align':'justify'}
            ),
        ]
    ),
]



sjumbotron = dbc.Card(card_content,  outline=True)

scard_content_2 = [
    dbc.CardHeader("Parâmetros do Gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        tabs,
        html.H4("Escolha os anos que deseja analisar", style={'font-size':19}),
        dcc.Dropdown(
        id = 'sano',  
        options=[
            {'label': j, 'value': j} for j in sano  
        ],
        value=[2017,2018,2019,2020],   
        multi=True,
    searchable=False,
         style={'margin-bottom':'10px'}
   

        ),        
        html.H4("Escolha os centros desejados", style={'font-size':19}),
        dcc.Dropdown(
        id = 'scentro',  
        options=[
            {'label': j, 'value': j} for j in scentro  
        ],
        value=['CEAR'],   
        multi=True,
    searchable=True,
         style={'margin-bottom':'10px'}
   

    ),
        ]
    ),
]

sjumbotron_2 = dbc.Card(scard_content_2,  outline=True)
scard_content_3 = [
    dbc.CardHeader(id='scard',style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.Div(id='sgraph_discentes',
            style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            )
        ]
    ),
]

sjumbotron_3 = dbc.Card(scard_content_3,  outline=True)



sbody_rel =html.Div([  

    

        dbc.Row(
           [
               dbc.Col(
                  [sjumbotron_2,
                        sjumbotron]

        , md=4

               ),
              dbc.Col([
						sjumbotron_3
                #html.Iframe(id='mapa', srcDoc=open('Apoio/venn.svg', 'r').read(),width='100%',height='500px'),  

                    ], md=8 ),

                ],no_gutters=True
            ),
              
])

smodal_3 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um centro como parâmetro de entrada de centros"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="sclose_3", className="ml-auto")
                ),
            ],
            id="smodal_3",
        ),
    ]
)

smodal_4 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um ano como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="sclose_4", className="ml-auto")
                ),
            ],
            id="smodal_4",
        ),
    ]
)



def rafael():
    layout = html.Div([
    nav,
	sbody_rel,
	smodal_3,
	smodal_4

     #html.Iframe(id='mapa', srcDoc=open('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  

     #html.Iframe(id='mapa', srcDoc=open('Apoio/mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  
    ])
    return layout




