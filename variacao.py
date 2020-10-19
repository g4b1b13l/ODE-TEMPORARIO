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

####################
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'font-size': '70%',
    'padding': '6px'
}

tab_style = { #Estilos das Tabs
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-size': '75%',
    'fontWeight': 'bold',
    'fontSize' : '13'
}
##################################

ListaCentros_variacao = ['Todos os centros', 'CCS -','CEAR -','CCEN -','CT -','CCM -','CBIOTEC -','CTDR -','CCHLA -','CCTA -','CCHSA -','CCSA -','CI -','CCAE -','CCJ -','CCA -','CE -']
Lista_Centros = ['CCS','CEAR','CCEN','CT','CCM','CBIOTEC','CTDR','CCHLA','CCTA','CCHSA','CCSA','CI','CCAE','CCJ','CCA','CE']
anos = ['Todos os anos','2017','2018','2019']
nav = Navbar()    
venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
card_content = [
    dbc.CardHeader("Entendendo o gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.P(
                className="card-text",id='relatorio_estudo_vocabular',style={'text-align':'justify'}
            ),
        ]
    ),
]



jumbotron = dbc.Card(card_content,  outline=True)

card_content_2 = [
    dbc.CardHeader("Opções de Filtro",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [

        ##################################
        dcc.Tabs(id='tab_escolha_grafico', value='variabilidade_vocabular',children=[
                 dcc.Tab(label= 'Variabilidade Vocabular', value='variabilidade_vocabular',children=[
                 	html.Div(html.Br()),
                
        #############################################



				        html.H4("Escolha os anos que deseja analisar:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_anos_variacao',  
				        options=[{'label': "Todos os anos", 'value': 'todos'},
				            {'label': "2017", 'value': anos[1]},
				            {'label': "2018", 'value': anos[2]},
				            {'label': "2019", 'value': anos[3]},
				            

				                 
				        ],
				        value= None,   
				        multi=True,
				        placeholder = "Selecione os anos",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				   

				        ),  
				        dcc.Checklist(
						options=[
						    {'label': 'Selecionar Todos os Anos', 'value': 'ta'}, #ta = todos os anos
						],
						id = 'checklist_anos_variacao',
						labelStyle={'display': 'none'}
						),
						html.Br(),
						  
				        html.H4("Escolha os centros desejados:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_centros_variacao', 
				         
				        options=[{'label': "Todos os Centros", 'value': 'todos'},
				                {'label': "CCS", 'value': ListaCentros_variacao[1]},
				                {'label': "CEAR", 'value': ListaCentros_variacao[2]},
				                {'label': "CCEN", 'value': ListaCentros_variacao[3]},
				                {'label': "CT", 'value': ListaCentros_variacao[4]},
				                {'label': "CCM", 'value': ListaCentros_variacao[5]},
				                {'label': "CBIOTEC", 'value': ListaCentros_variacao[6]},
				                {'label': "CTDR", 'value': ListaCentros_variacao[7]},
				                {'label': "CCHLA", 'value': ListaCentros_variacao[8]},
				                {'label': "CCTA", 'value': ListaCentros_variacao[9]},
				                {'label': "CCHSA", 'value': ListaCentros_variacao[10]},
				                {'label': "CCSA", 'value': ListaCentros_variacao[11]},
				                {'label': "CI", 'value': ListaCentros_variacao[12]},
				                {'label': "CCAE", 'value': ListaCentros_variacao[13]},
				                {'label': "CCJ", 'value': ListaCentros_variacao[14]},
				                {'label': "CCA", 'value': ListaCentros_variacao[15]},
				                {'label': "CE", 'value': ListaCentros_variacao[16]},
				                


				            ], 
				        
				        value=None,   
				        multi=True,
				        placeholder = "Selecione os centros",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				   

				    ),
				    dcc.Checklist(
				    options=[
				        {'label': 'Selecionar Todos os Centros', 'value': 'tc'}, #ta = todos os anos
				    ],
				    id = 'checklist_centros_variacao',
				    labelStyle={'display': 'none'}
					),
					html.Br(),
					html.H4("Escolha o campo desejado:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_modalidades_variacao', 
				         
				        options=[
				                {'label': "Resumo", 'value': "Resumo"},
				                {'label': "Justificativa", 'value': "Justificativa"},
				                {'label': "Metodologia", 'value': "Metodologia"},
				                {'label': "Objetivos", 'value': "Objetivos"},
				                {'label': "Fundamentação Teórica", 'value': "Fundamentacao"},
				                

				            ], 
				        
				        value=None,   
				        multi=False,
				        placeholder = "Selecione a modalidade",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				   

				    ),  


				                 	], 



				                 	style=tab_style, selected_style=tab_selected_style),




                
                dcc.Tab(label= 'Análise Gramatical', value='analise_gramatical',children=[
                html.Div(html.Br()),
		                
		        #############################################



		        html.H4("Escolha as classes gramaticais que deseja analisar:", style={'font-size':18}),
		        dcc.Dropdown(
		        id = 'dropdown_classes_analise',  
		        options=[{'label': "Todos as classes", 'value': 'todos'},
		            {'label': "Substantivos", 'value': "Substantivos"},
		            {'label': "Adjetivos", 'value': "Adjetivos"},
		            {'label': "Verbos", 'value': "Verbos"},
		            

		                 
		        ],
		        value= None,   
		        multi=True,
		        placeholder = "Selecione as classes",
		    	searchable=False,
		        style={'margin-bottom':'10px'}
		   

		        ),  
		        dcc.Checklist(
				options=[
				    {'label': 'Selecionar Todas as classes', 'value': 'tc'}, #ta = todos os anos
				],
				id = 'checklist_classes_analise',
				labelStyle={'display': 'none'}
				),
				html.Br(),
				  
		        html.H4("Escolha os centros desejados:", style={'font-size':19}),
		        dcc.Dropdown(
		        id = 'dropdown_centros_analise', 
		         
		        options=[{'label': "Todos os Centros", 'value': 'todos'},
		                {'label': "CCS", 'value': ListaCentros_variacao[1]},
		                {'label': "CEAR", 'value': ListaCentros_variacao[2]},
		                {'label': "CCEN", 'value': ListaCentros_variacao[3]},
		                {'label': "CT", 'value': ListaCentros_variacao[4]},
		                {'label': "CCM", 'value': ListaCentros_variacao[5]},
		                {'label': "CBIOTEC", 'value': ListaCentros_variacao[6]},
		                {'label': "CTDR", 'value': ListaCentros_variacao[7]},
		                {'label': "CCHLA", 'value': ListaCentros_variacao[8]},
		                {'label': "CCTA", 'value': ListaCentros_variacao[9]},
		                {'label': "CCHSA", 'value': ListaCentros_variacao[10]},
		                {'label': "CCSA", 'value': ListaCentros_variacao[11]},
		                {'label': "CI", 'value': ListaCentros_variacao[12]},
		                {'label': "CCAE", 'value': ListaCentros_variacao[13]},
		                {'label': "CCJ", 'value': ListaCentros_variacao[14]},
		                {'label': "CCA", 'value': ListaCentros_variacao[15]},
		                {'label': "CE", 'value': ListaCentros_variacao[16]}, 
		                


		            ], 
		        
		        value=None,   
		        multi=True,
		        placeholder = "Selecione os centros",
		    	searchable=False,
		        style={'margin-bottom':'10px'}
		   

		    ),
		    dcc.Checklist(
		    options=[
		        {'label': 'Selecionar Todos os Centros', 'value': 'tc'}, #ta = todos os anos
		    ],
		    id = 'checklist_centros_analise',
		    labelStyle={'display': 'none'}
			),
			html.Br(),
			html.H4("Escolha o campo desejado:", style={'font-size':19}),
		        dcc.Dropdown(
		        id = 'dropdown_modalidades_analise', 
		         
		        options=[
		                {'label': "Resumo", 'value': "Resumo"},
		                {'label': "Justificativa", 'value': "Justificativa"},
		                {'label': "Metodologia", 'value': "Metodologia"},
		                {'label': "Objetivos", 'value': "Objetivos"},
		                {'label': "Fundamentação Teórica", 'value': "Fundamentacao"},
		                

		            ], 
		        
		        value=None,   
		        multi=False,
		        placeholder = "Selecione o campo",
		    	searchable=False,
		        style={'margin-bottom':'10px'}
		   

		    ),  



                ], style=tab_style, selected_style=tab_selected_style),  
                dcc.Tab(label= 'Nuvem de Palavras', value='nuvem_palavras',children=[
                		html.Div(html.Br()),
        
				        html.H4("Escolha os anos que deseja analisar:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_anos_nuvem',  
				        options=[{'label': "Todos os Anos", 'value': 'todos'},
				            {'label': "2017", 'value': anos[1]},
				            {'label': "2018", 'value': anos[2]},
				            {'label': "2019", 'value': anos[3]},
				            

				                 
				        ],
				        value= None,   
				        multi=True,
				        placeholder = "Selecione os anos",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				        ),
				        dcc.Checklist(
						options=[
						    {'label': 'Selecionar Todos os Anos', 'value': 'ta'}, #ta = todos os anos
						],
						id = 'checklist_anos_nuvem',
						labelStyle={'display': 'none'}
						),
						html.Br(),
				   
						  
				        html.H4("Escolha os centros desejados:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_centros_nuvem', 
				         
				        options=[{'label': "Todos os Centros", 'value': 'todos'},
				                {'label': "CCS", 'value': ListaCentros_variacao[1]},
				                {'label': "CEAR", 'value': ListaCentros_variacao[2]},
				                {'label': "CCEN", 'value': ListaCentros_variacao[3]},
				                {'label': "CT", 'value': ListaCentros_variacao[4]},
				                {'label': "CCM", 'value': ListaCentros_variacao[5]},
				                {'label': "CBIOTEC", 'value': ListaCentros_variacao[6]},
				                {'label': "CTDR", 'value': ListaCentros_variacao[7]},
				                {'label': "CCHLA", 'value': ListaCentros_variacao[8]},
				                {'label': "CCTA", 'value': ListaCentros_variacao[9]},
				                {'label': "CCHSA", 'value': ListaCentros_variacao[10]},
				                {'label': "CCSA", 'value': ListaCentros_variacao[11]},
				                {'label': "CI", 'value': ListaCentros_variacao[12]},
				                {'label': "CCAE", 'value': ListaCentros_variacao[13]},
				                {'label': "CCJ", 'value': ListaCentros_variacao[14]},
				                {'label': "CCA", 'value': ListaCentros_variacao[15]},
				                {'label': "CE", 'value': ListaCentros_variacao[16]},
				                


				            ], 
				        
				        value=None,   
				        multi=True,
				        placeholder = "Selecione o centro",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				   

				    ),
				    dcc.Checklist(
				    options=[
				        {'label': 'Selecionar Todos os Centros', 'value': 'tc'}, #ta = todos os anos
				    ],
				    id = 'checklist_centros_nuvem',
				    labelStyle={'display': 'none'}
					),
				    html.Br(),
				    html.H4("Escolha o campo desejado:", style={'font-size':19}),
				    dcc.Dropdown(
				        id = 'dropdown_modalidades_nuvem', 
				         
				        options=[
				                {'label': "Resumo", 'value': "Resumo"},
				                {'label': "Justificativa", 'value': "Justificativa"},
				                {'label': "Metodologia", 'value': "Metodologia"},
				                {'label': "Objetivos", 'value': "Objetivos"},
				                {'label': "Fundamentação Teórica", 'value': "Fundamentacao"},
				               
				            ], 
				        
				        value=None,   
				        multi=False,
				        placeholder = "Selecione a modalidade",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				   

				    ),
			
                ], style=tab_style, selected_style=tab_selected_style), 
		
		
		
                dcc.Tab(label= 'Contagem de Palavras', value='contagem_palavras',children=[
                html.Div(html.Br()),
				html.H4("Escolha os anos que deseja analisar:", style={'font-size':19}),
				dcc.Dropdown(
				id = 'dropdown_anos_contagem',  
				options=[{'label': "Todos os anos", 'value': 'todos'},
				    {'label': "2017", 'value': anos[1]},
				    {'label': "2018", 'value': anos[2]},
				    {'label': "2019", 'value': anos[3]},
				    

				                 
				],
		        value= None,   
				multi=True,
		        placeholder = "Selecione os anos",
		    	searchable=False,
				style={'margin-bottom':'10px'}
                ),
				dcc.Checklist(
				    options=[
				        {'label': 'Selecionar Todos Anos', 'value': 'ta'}, #ta = todos os anos
				    ],
				    id = 'checklist_anos_contagem',
				    labelStyle={'display': 'none'}
					),
				html.Br(),  
		        html.H4("Escolha os centros desejados:", style={'font-size':19}),
		        dcc.Dropdown(
		        id = 'dropdown_centros_contagem', 
		         
		        options=[{'label': "Todos os Centros", 'value': 'todos'},
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
		    dcc.Checklist(
		    options=[
		        {'label': 'Selecionar Todos os Centros', 'value': 'tc'}, #ta = todos os anos
		    ],
		    id = 'checklist_centros_contagem',
		    labelStyle={'display': 'none'}
			),
			html.Br(),
			html.H4("Digite a(s) palavra(s) que deseja contar\nseparadas por vírgula:", style={'font-size':19}),
                html.H4("Para plurais com o mesmo radical da palavra no singular exemplo 'pesquisa - pesquisas' deve ser considerada apenas a versão da palavra no singular, caso contrário o plural será contabilizado duas vezes", style={'font-size':13}),
                dcc.Input(
                    id='palavra_contagem',
                    placeholder='Escreva a(s) palavra(s)',
                    type='text',
                    value = '',
                    style={'margin-bottom':'10px'}
                ),
                
                        
            ], style=tab_style, selected_style=tab_selected_style),



                ]),

        
        ]
    ),
]

jumbotron_2 = dbc.Card(card_content_2,  outline=True)
card_content_3 = [
	############
    dbc.CardHeader(id='texto_grafico_nuvem',style={'font-size':24, 'textAlign':'center'}),
    ############
    dbc.CardBody(
        [
            #html.Div(id='grafico_variacao_vocabular',
            #style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            html.Div(id='grafico_variacao_vocabular'),
            html.Div(id='grafico_analise_gramatical'),
			html.Div(id='grafico_contagem_palavras'),
            html.Img(id='grafico_nuvem_palavras', style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto','width':'90%','height':'90%'})
            
            
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



def variacao():
    layout = html.Div([
    nav,
	body_1,
	modal,
	modal_2
	])
    return layout
