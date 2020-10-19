import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import cufflinks as cf
init_notebook_mode(connected=True)
cf.go_offline()



import dash
import dash_core_components as dcc
import dash_html_components as html
from navbar import Navbar


nav = Navbar()

df_2017 = pd.read_csv('Apoio/df_2017.csv',index_col=0)
df_2018 = pd.read_csv('Apoio/df_2018.csv',index_col=0)

pio.templates.default = "plotly_white"

fig1 = make_subplots(rows=1, cols=1,row_titles = ['Quantidade de Projetos'],  shared_yaxes=True)

fig1.add_trace(go.Bar(x=df_2017.columns.to_list(), y=df_2017.loc['QUANTIDADE'], name='2017'),1,1)
fig1.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=False)
fig1.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
fig1.update_layout(title_text='Projetos de Extensão Divididos por Centro', title_x=0.5)

fig1.add_trace(go.Bar(x=df_2018.columns.to_list(), y=df_2018.loc['QUANTIDADE'], name='2018'),1,1)
fig1.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
fig1.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))

fig1.update_layout(
    autosize=False,
    width=700,
    height=600,
)


fig2 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]], subplot_titles=['2017', '2018'])
fig2.update_layout(
    autosize=False,
    width=750,
    height=380,
)

fig2.update_traces(textposition='inside')
fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig2.add_trace(go.Pie(labels=df_2017.columns.to_list(), values=df_2017.loc['QUANTIDADE'], scalegroup='one', textinfo='percent', name='2017'),1, 1)
fig2.add_trace(go.Pie(labels=df_2018.columns.to_list(), values=df_2018.loc['QUANTIDADE'], scalegroup='one', textinfo='percent', name='2018'),1, 2)
fig2.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
fig2.update_layout(title_text='Projetos de Extensão Divididos por Centro em Porcentagem', title_x=0.5)


import plotly.graph_objects as go  
import dash
import dash_core_components as dcc
import dash_html_components as html
import io
import flask
from flask import send_file
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #Importando um estilo de css desse link



body = html.Div([
    html.Div(children=[
        html.Div('Informações de Pessoal', className="app-header--title"),
        html.Hr(style={'backgroundColor':'gray','width':'100%','height':'1px'}),
        html.Hr(style={'backgroundColor':'gray', 'width':'2px','height':'110%', 'position':'absolute','left':'31%','top':'15%'})
    ],className='app-header'),
    
    html.Div(html.Br()), #Pulei linha com html mesmo heheh
    html.Div(html.Br()),
    
    
    html.Div(className='lado_esquerdo', children=[
        html.Div(html.Br()),
        html.H4("Informações de Pessoal", style={'font-size':24, 'textAlign':'center'}),
        html.Div(html.Br()),
        html.H4("Selecione o tipo de Informação que deseja visualizar:", style={'font-size':19, 'textAlign':'center'}),
        dcc.Dropdown(
        id='escolherGrafico_dropdown1',
        options=[{'label': i, 'value': i} for i in ['Quantitativo de Projetos de Extensão por Centro', 'Porcentagem de Projetos de Extensão por Centro']], #cria um dropdown (caixa de seleção) com os elementos passados na lista
        placeholder="Selecione",
        searchable=False,
        style={'font-size':'100%', 'min-height':'3px'},
        ),
        html.Div(id='texto_graficos'),
    ]), 
        #O gráfico saira aqui
    html.Div(className="lado_direito", children=[
        html.Div(id='output_dropdown1'),
    ]),
         
], className='margens')


def joao():
    layout = html.Div([
    nav,
    body,
    ])
    return layout

