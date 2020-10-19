#IMPORTS

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objs as go
import plotly.offline as py
import dash_bootstrap_components as dbc
from navbar import Navbar
import base64

#FUNÇÃO PARA BARRA DE NAVEGAÇÃO
nav = Navbar()

######DEFININDO ESTILOS########
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'font-size': '70%',
    'padding': '6px'
}

tab_style = { 
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-size': '75%',
    'fontWeight': 'bold',
    'fontSize' : '13'
}
##################################


card_content = [
    dbc.CardHeader("Entendendo o gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.P(
                className="card-text",id='relatorio_estudo_notas',style={'text-align':'justify'}
            ),
        ]
    ),
]

jumbotron = dbc.Card(card_content,  outline=True)

Lista_Centros = ['CCS','CEAR','CCEN','CT','CCM','CBIOTEC','CTDR','CCHLA','CCTA','CCHSA','CCSA','CI','CCAE','CCJ','CCA','CE','Todos os centros']
anos = ['Todos os anos','2017','2018','2019','2020']
anos1 = ['Todos os anos',2017,2018,2019,2020]
areas = ['Todas as areas','Ciências da Saúde','Ciências Humanas','Ciências Sociais Aplicadas','Ciências Agrárias','Lingüística, Letras e Artes','Engenharias','Multidisciplinar','Ciências Exatas e da Terra','Ciências Biológicas']
card_content_2 = [
    dbc.CardHeader("Opções de Filtro",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        #######TABS  PARA OPÇÕES DE ANALISE######
        dcc.Tabs(id='tab_escolha_grafico_manu', value='notas_projetos',children=[
                dcc.Tab(label= 'Notas dos Projetos', value='notas_projetos',children=[
                 	html.Div(html.Br()),
                    html.H4("Escolha os anos que deseja analisar:", style={'font-size':19}),
				    dcc.Dropdown(
				    id = 'dropdown_anos_notas',  
				    options=[
                        {'label': "Todos os anos", 'value': anos[0]},
				        {'label': "2017", 'value': anos[1]},
				        {'label': "2018", 'value': anos[2]},
				        {'label': "2019", 'value': anos[3]},
                        {'label': "2020", 'value': anos[4]},
				             
				    ],
				    value= None,   
				    multi=True,
				    placeholder = "Selecione os anos",
				    searchable=False,
				    style={'margin-bottom':'10px'}
				
				    ), 
					html.Br(),
					  
				    html.H4("Escolha os centros desejados:", style={'font-size':19}),
				    dcc.Dropdown(
				    id = 'dropdown_centros_notas',
                    options=[
                        {'label': "Todos os centros", 'value':Lista_Centros[16] },
		                {'label': "CCS", 'value': Lista_Centros[0]},
		                {'label': "CEAR", 'value': Lista_Centros[1]},
		                {'label': "CCEN", 'value': Lista_Centros[2]},
		                {'label': "CT", 'value': Lista_Centros[3]},
		                {'label': "CCM", 'value': Lista_Centros[4]},
		                {'label': "CBIOTEC", 'value': Lista_Centros[5]},
		                {'label': "CTDR", 'value': Lista_Centros[6]},
		                {'label': "CCHLA", 'value': Lista_Centros[7]},
		                {'label': "CCTA", 'value': Lista_Centros[8]},
		                {'label': "CCHSA", 'value': Lista_Centros[9]},
		                {'label': "CCSA", 'value': Lista_Centros[10]},
		                {'label': "CI", 'value': Lista_Centros[11]},
		                {'label': "CCAE", 'value': Lista_Centros[12]},
		                {'label': "CCJ", 'value': Lista_Centros[13]},
		                {'label': "CCA", 'value': Lista_Centros[14]},
		                {'label': "CE", 'value': Lista_Centros[15]},
                    ], 
		        
		            value=None,   
		            multi=True,
		            placeholder = "Selecione os centros",
		    	    searchable=False,
		            style={'margin-bottom':'10px'}
		   

		            ),
                
        

                ],style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label= 'Notas dos Projetos por Área Temática', value='notas_areaTematica',children=[
                 	html.Div(html.Br()),
                    html.H4("Escolha os anos que deseja analisar:", style={'font-size':19}),
				    dcc.Dropdown(
				    id = 'dropdown_anos_areaTematica_notas',  
				    options=[
                        {'label': "Todos os anos", 'value': anos1[0]},
				        {'label': "2017", 'value': anos1[1]},
				        {'label': "2018", 'value': anos1[2]},
				        {'label': "2019", 'value': anos1[3]},
                        {'label': "2020", 'value': anos1[4]},
				             
				    ],
				    value= None,   
				    multi=True,
				    placeholder = "Selecione os anos",
				    searchable=False,
				    style={'margin-bottom':'10px'}
				
				    ), 
					html.Br(),
					  
				    html.H4("Escolha os centros desejados:", style={'font-size':19}),
				    dcc.Dropdown(
				    id = 'dropdown_centros_areaTematica_notas',
                    options=[
                        {'label': 'Todos os centros', 'value':Lista_Centros[16] },
		                {'label': "CCS", 'value': Lista_Centros[0]},
		                {'label': "CEAR", 'value': Lista_Centros[1]},
		                {'label': "CCEN", 'value': Lista_Centros[2]},
		                {'label': "CT", 'value': Lista_Centros[3]},
		                {'label': "CCM", 'value': Lista_Centros[4]},
		                {'label': "CBIOTEC", 'value': Lista_Centros[5]},
		                {'label': "CTDR", 'value': Lista_Centros[6]},
		                {'label': "CCHLA", 'value': Lista_Centros[7]},
		                {'label': "CCTA", 'value': Lista_Centros[8]},
		                {'label': "CCHSA", 'value': Lista_Centros[9]},
		                {'label': "CCSA", 'value': Lista_Centros[10]},
		                {'label': "CI", 'value': Lista_Centros[11]},
		                {'label': "CCAE", 'value': Lista_Centros[12]},
		                {'label': "CCJ", 'value': Lista_Centros[13]},
		                {'label': "CCA", 'value': Lista_Centros[14]},
		                {'label': "CE", 'value': Lista_Centros[15]},
                    ], 
		        
		            value=None,   
		            multi=True,
		            placeholder = "Selecione os centros",
		    	    searchable=False,
		            style={'margin-bottom':'10px'}
		   

		            ),
                    html.Br(),
					  
				    html.H4("Escolha as Áreas temáticas desejadas:", style={'font-size':19}),
				    dcc.Dropdown(
				    id = 'dropdown_areaTematica_notas',
                    options=[
                        {'label':'Todas as Áreas tematicas','value':areas[0]},
		                {'label': "Ciências da Saúde", 'value': areas[1]},
		                {'label': "Ciências Humanas", 'value': areas[2]},
		                {'label': "Ciências Sociais Aplicadas", 'value': [3]},
		                {'label': "Ciências Agrárias", 'value': areas[4]},
		                {'label': "Lingüística, Letras e Artes", 'value': areas[5]},
		                {'label': "Engenharias", 'value': areas[6]},
		                {'label': "Multidisciplinar", 'value': areas[7]},
		                {'label': "Ciências Exatas e da Terra", 'value': areas[8]},
		                {'label': "Ciências Biológicas", 'value': areas[9]},
                    ], 
		        
		            value=None,   
		            multi=True,
		            placeholder = "Selecione as áreas temáticas",
		    	    searchable=False,
		            style={'margin-bottom':'10px'}
		   

		            ),
                ],style=tab_style, selected_style=tab_selected_style),

####
        ]),

        
        ]
    ),
]

jumbotron_2 = dbc.Card(card_content_2,  outline=True)

card_content_3 = [
	############
    dbc.CardHeader(id='grafico_avaliadores',style={'font-size':24, 'textAlign':'center'}),
    ############
    dbc.CardBody([
        
        html.Div(id='grafico_notas')
        
	])
]

jumbotron_3 = dbc.Card(card_content_3,  outline=True)

body_1 =html.Div([  
        dbc.Row(
           [
            dbc.Col(
                [jumbotron_2,
                jumbotron], md=4),
            dbc.Col([
				jumbotron_3], md=8 ),

        ],no_gutters=True),
])

modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um centro como parâmetro de entrada de centros"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
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
                   dbc.Button("Close", id="close_2", className="ml-auto")
                ),
            ],
            id="modal_2",
        ),
    ]
)

def manu():
    layout = html.Div([
    nav,
	body_1,
	modal,
	modal_2
	])
    return layout

