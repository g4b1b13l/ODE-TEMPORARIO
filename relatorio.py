import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar


nav = Navbar()

#df_2017 = pd.read_csv('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\Atividade JOao\\Atividade4\\df_2017.csv',index_col=0)
#df_2018 = pd.read_csv('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\Atividade JOao\\Atividade4\\df_2018.csv',index_col=0)

tab_style = { #Estilos das Tabs
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

all_options = {
    'João Guilherme e Emmanuela': ['Abril', 'Maio', 'Junho', 'Julho'],
    'Gabriel': ['Abril', 'Maio', 'Junho', 'Julho'],
    'Rafael': ['Abril', 'Maio', 'Junho', 'Julho'], 
}

body = html.Div([
    html.Div(children=[
        html.Div('Página das Reuniões', className="app-header--title"),
        html.Hr(style={'backgroundColor':'gray','width':'100%','height':'1px'}),
        html.Hr(style={'backgroundColor':'gray', 'width':'2px','height':'110%', 'position':'absolute','left':'31%','top':'15%'})
    ],className='app-header'),
    
    html.Div(html.Br()), #Pulei linha com html mesmo heheh
    html.Div(html.Br()),
    
    html.Div(className='lado_esquerdo', children=[
        html.Div(html.Br()),
        html.Div(html.Br()),
        html.Div(html.Br()),
        html.H4("Lista de Tarefas Desenvolvidas", style={'font-size':24, 'textAlign':'center'}),
        html.Div(html.Br()),
        html.H4("Selecione o Discente:", style={'font-size':19, 'textAlign':'left'}),
                                                
                                                
        dcc.Dropdown(
        id='countries-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value= 'João Guilherme e Emmanuela',
        searchable=False,
        ),
        
        
        html.Div(html.P(html.Br())), #Pula uma linha
        html.H4("Selecione o Mês de Trabalho:", style={'font-size':19, 'textAlign':'left'}), 
        
         dcc.Dropdown(id='cities-dropdown'),
        
    ]), 
    
    html.Div(className="lado_direito", children=[
        html.Div(html.Br()),
        html.Div(id='display-selected-values'),
    ]),
  
],className='margens')


def relatorio():
    layout = html.Div([
    nav,
    body
    ])
    return layout


