import unidecode as und
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from mapa import grupos,dados,dict_csv,state_data,geo_data,dict_coordenadas,folder, extension, separator,files_logos, folder_1,files_json,folder_2,files_dados,tooltip,html1,limpa_nome_arquivo_json,limpa_nome_arquivo,gera_cloropleth,gera_camadas_ufpb,gera_icones_da_ufpb,mapa_da_ufpb,mapa
from joao import fig1, fig2, joao
#from rafael import fig_1,fig_2,fig_3,rafael
from rafael import rafael
from manu import manu,Lista_Centros,areas
from discentes import discente, graf_rel
from rafael2 import rafael2, graf_rel
from relatorio import all_options, relatorio, tab_style, tab_selected_style
from homepage import Homepage
from quem_somos import quem_somos
import folium  
from folium import IFrame, FeatureGroup 
from flask import Flask,flash
from login import app as server
import os
import re
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from variacao import variacao, ListaCentros_variacao, Lista_Centros
from docentes import docente, venn
from rafael3 import rafael3, venn
import pandas as pd
import base64 
import matplotlib_venn as vplt
from matplotlib import pyplot as plt
import matplotlib
from operator import itemgetter #Lembrar de Acrescentar
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import io
matplotlib.use('Agg')


from logging import FileHandler, WARNING



app =  dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED],     
        meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}         
    ])
server = app.server
      
app.config.suppress_callback_exceptions = True   

app.layout = html.Div([ 
dcc.Location(id = 'url', refresh = False),      
html.Div(id = 'page-content')
])




@app.callback(Output('page-content', 'children'),     
			[Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/mapa-ufpb':
		return mapa()
	if pathname == '/joao':
		return joao()
	if pathname == '/rafael':
		return rafael()            
	if pathname == '/emmanuela':       
		return manu() 
	if pathname == '/relatorio':       
		return relatorio()
	if pathname == '/quemsomos':       
		return quem_somos()
	if pathname=='/estudo-vocabular':
		return variacao()
	if pathname=='/docente':
		return docente()
	if pathname=='/discente':
		return discente()
	if pathname=='/rafael2':
		return rafael2()
	if pathname=='/rafael3':
		return rafael3()
	return Homepage()

@app.callback(
   dash.dependencies.Output('choropleth', 'style'),
	[dash.dependencies.Input('flag', 'value')])             

def some_o_grafico_para_aparecer_os_outros(valor):
	if valor == 'nao':
		return {'display': 'none'}
	if valor == 'sim':
		return {'display': 'block'} 
	else:
		return {'display': 'none'}         

@app.callback(
   dash.dependencies.Output('dados', 'value'),
	[dash.dependencies.Input('flag', 'value')])             

def some_o_grafico_para_aparecer_os_outros(valor):
	if valor == 'nao':
		return 0
	else:
		return dash.no_update


@app.callback(
   dash.dependencies.Output('value-container', 'style'),
	[dash.dependencies.Input('grupos', 'value')])

def some_o_grafico_para_aparecer_os_outros(grupos):
	return {'display': 'none'}



@app.callback(
   dash.dependencies.Output('grupos', 'value'),
	[dash.dependencies.Input('tabs', 'value'),dash.dependencies.Input('value-container', 'style')],[dash.dependencies.State('grupos', 'value')])             

def some_o_grafico_para_aparecer_os_outros(tabs,flag,grupos):
	if 'Todos os centros' in grupos:
		valor = True
	else:
		valor = False
	if valor == False or tabs == 'tab-1' or tabs == 'tab-2' or tabs == 'tab-4':
		return grupos
	if valor == True and tabs =='tab-3':
		print('cheguei de novo aqui')
		return ['CCHLA','CEAR','CCSA','CE','CCJ','CT','CBIOTEC','CCTA','CCEN','CCS','CCM']
	if valor == True and tabs =='tab-5':
		return ['CI','CTDR']           



@app.callback(
   dash.dependencies.Output('grupos', 'options'),
	[dash.dependencies.Input('tabs', 'value')])             

def ajeita_entrada_valores(tabs):
	if tabs == 'tab-1':
		return [{'label': j, 'value': j} for j in ['CCA']]
	if tabs == 'tab-2':
		return [{'label': j, 'value': j} for j in ['CCHSA']]
	if tabs == 'tab-3':
		return [{'label': j, 'value': j} for j in ['Todos os centros','CCHLA','CEAR','CCSA','CE','CCJ','CT','CBIOTEC','CCTA','CCEN','CCS','CCM']]
	if tabs == 'tab-4':
		return [{'label': j, 'value': j} for j in ['CCAE']]
	if tabs == 'tab-5':
		return [{'label': j, 'value': j} for j in ['Todos os centros','CI','CTDR']]

@app.callback(
	dash.dependencies.Output('mapa', 'srcDoc'),
	[dash.dependencies.Input('grupos', 'value'),
	dash.dependencies.Input('dados', 'value'),
	dash.dependencies.Input('flag', 'value'),
	dash.dependencies.Input('tabs', 'value')])

def update_map(grupos,dado,flag,tabs):
	print(tabs)
	if tabs == 'tab-5':
		base = os.path.join('Apoio/base_mangabeira.json')
		mapa_ = folium.Map(location= [-7.162806, -34.817641], zoom_start=15,tiles='cartodbpositron')    
	if tabs == 'tab-3':
		base = os.path.join('Apoio/base_ufpb.json')
		mapa_ = folium.Map(location= [-7.1385,-34.8464], zoom_start=15,tiles='cartodbpositron')
	if tabs == 'tab-1':
		base = os.path.join('Apoio/base_areia.json')
		mapa_ = folium.Map(location= [-6.973741,-35.716276], zoom_start=15,tiles='cartodbpositron')
	if tabs == 'tab-2':
		base = os.path.join('Apoio/base_bananeiras.json')
		mapa_ = folium.Map(location= [-6.751973,-35.647689], zoom_start=15,tiles='cartodbpositron')
	if tabs == 'tab-4':
		base = os.path.join('Apoio/base_mamanguape.json')
		mapa_ = folium.Map(location= [-6.829537,-35.118103], zoom_start=15,tiles='cartodbpositron')
	folium.GeoJson(base, name='base').add_to(mapa_)

	mapa_da_ufpb(tooltip, files_logos,dict_coordenadas,files_json,geo_data,state_data, files_dados,mapa_,flag,grupos,dado)  
	#return open('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\mapa_ufpb_centros.html', 'r').read()
	return open('Apoio/mapa_ufpb_centros.html', 'r').read()   

####################mapa###########
@app.callback(dash.dependencies.Output('output_dropdown1', 'children'), #Recupea o dropdown informado
			  [dash.dependencies.Input('escolherGrafico_dropdown1', 'value')])


def mostrar_graficos(value): #Faz a operação de 'Mostrar' a imagem dependendo do dropdown selecionado
	if value == 'Quantitativo de Projetos de Extensão por Centro':
		return dcc.Graph(figure=fig1)
	  
	
	
	elif value == 'Porcentagem de Projetos de Extensão por Centro':
		return html.Div([
			html.Div(html.Br()),
			html.Div(html.Br()),
			html.Div(html.Br()),
			html.Div(html.Br()),
			html.Div(html.Br()),
			dcc.Graph(figure=fig2)
		])


@app.callback(dash.dependencies.Output('texto_graficos', 'children'), #Recupea o dropdown informado
			[dash.dependencies.Input('escolherGrafico_dropdown1', 'value')])

def mostrar_textos(value): #Faz a operação de 'Mostrar' a imagem dependendo do dropdown selecionado
	if value == 'Quantitativo de Projetos de Extensão por Centro':
		return html.Div([
					html.Div(html.Br()),
					dcc.Markdown('''
					##### Informações Relevantes sobre o Gráfico
					Durante o ano de 2017, foram 485 projetos de extensão concluídos ao todo, percebe-se
					que há uma desproprocionalidade no número de projetos por centro, já que alguns centros
					concluíram muitos mais projetos do que outros. o Centro de Ciências da Saúde(CCS), por exemplo
					concluiu muito mais projetos do que os demais centros tendo mais do que o dobro de projetos
					do que o segundo da lista. Nesse sentido, o ano de 2018 segue a mesma tendência mesmo com um aumento
					de projetos (de 485 para 513).
					
					Para obter mais informações acerca desses dados, você pode baixar um relatório completo através do botão abaixo.
					''', style={'textAlign':'justify', 'font-size':16}),
					html.Div(className='centralizar', children= [html.A(html.Button('Baixar informações', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,'height':40,'font-size':16,'backgroundColor':'007FFF', 'fontWeight':'bold','borderRadius':8}),  href='https://docs.google.com/document/u/1/export?format=pdf&id=1g60AAai8RQH5-YI6sJkgx1eh7WsSpmGCgyhXtRzxxW8&token=AC4w5VgQfRwUncRUP5k12pyAxE_DjD2GRQ%3A1592677938489&includes_info_params=true')]),
			]) 
	
	
	elif value == 'Porcentagem de Projetos de Extensão por Centro':
		 return html.Div([
					html.Div(html.Br()),
					dcc.Markdown('''
					##### Informações Relevantes sobre o Gráfico
					Durante o ano de 2017, foram 485 projetos de extensão concluídos ao todo, percebe-se que nesse ano
					existe uma densidade muito grande de projetos por alguns centros, com os 5 primeiros contendo mais do
					que 50% do total de projetos de extensão, sendo que são 16 centros consultados, ou seja, a maioria dos
					projetos está concentrada em 31,25% dos centros consultados. No ano de 2018, com 513 projetos concluídos, a mesma tendência
					foi seguida.
	
					Para obter mais informações acerca desses dados, você pode baixar um relatório completo através do botão abaixo.
					''', style={'textAlign':'justify', 'font-size':17}),
					html.Div(className='centralizar', children= [html.A(html.Button('Baixar informações', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,'height':40,'font-size':16,'backgroundColor':'007FFF', 'fontWeight':'bold','borderRadius':8}),  href='https://docs.google.com/document/u/1/export?format=pdf&id=1g60AAai8RQH5-YI6sJkgx1eh7WsSpmGCgyhXtRzxxW8&token=AC4w5VgQfRwUncRUP5k12pyAxE_DjD2GRQ%3A1592677938489&includes_info_params=true')]),
			]) 
		

  

##########joao##############

#@app.callback(
#	dash.dependencies.Output('teste', 'children'),
#	[dash.dependencies.Input('demo-dropdown', 'value')])
#def update_output(value):
#	if value == 'Quantitativo do Envolvimento com projetos por Ano':
#		return dcc.Graph(figure=fig_1)
#	elif value == 'Porcentagem do Envolvimento com projetos por Ano':
#		return dcc.Graph(figure=fig_2)
#	elif value == 'Relação de Discentes/Docentes por Centro':
#		return dcc.Graph(figure=fig_3)  
	#html.Div([
  #      dcc.Graph(figure=fig3),
  #     dcc.Markdown(###### **Sobre o Grafico:** Esse Grafico mostra a relação aluno/professor, tal dado mostra os centros que possuem a quantidade de professores maiores que alunos quando os valores obtidos forem menores que 1, e quantidades de alunos maiores que professores para valores maiores que 1.
#Tais dados foram obtidos por meio de um banco de disponibilizado pela SUPERINTENDÊNCIA DE TECNOLOGIA DA INFORMAÇÃO (STI) e manipulados utilizando a linguagem de programção Python., 
		  #           style={'horizontal-Align':'left', 'textAlign':'left'})
	#    ])
	
#@app.callback(
#	dash.dependencies.Output('teste2', 'children'),
#	[dash.dependencies.Input('demo-dropdown', 'value')])
#def update_output2(value):
#	if value == 'Quantitativo do Envolvimento com projetos por Ano':
#		return html.Div([
#			dcc.Markdown('#### **Informações Relevantes sobre o Gráfico**'),
#			html.P('Ao se  comparar os anos de 2017 e 2018 pecebe-se um aumento significativo no número de discentes, mas ao comparar os anos de 2018 e 2019 observa-se um redução significativa nesse valor. Já o número de docentes e servidores nota-se que os valores se mantiveram constantes no decorrer dos anos. Com esses resultados consegue-se analisar o envolvimento do corpo estudantil com os projetos de extensão e varificar a evolução dessa atividade.',
#				  style={'font-size':16,'textAlign': 'left'})
#		])
#	elif value == 'Porcentagem do Envolvimento com projetos por Ano':
#		return html.Div([
#			dcc.Markdown('#### **Informações Relevantes sobre o Gráfico**'),
#			html.P('Ao se  comparar os anos de 2017 e 2018 pecebe-se um aumento significativo no número de discentes e isso causou uma redução percentual no número de docente e discente, mas ao comparar os anos de 2018 e 2019 percebe-se o efeito contrário, pois como o número de discente cai temos um aumento percentual no número de docente e discente. Com esses resulados pode-se comparar o envolvimento do corpo estudantil e com isso criar medidas para incentivar o aumento desse envolvimento bem como verificar os impactos das medidas adotadas.',
#				  style={'font-size':16,'textAlign': 'left'})
#		])
#	elif value == 'Relação de Discentes/Docentes por Centro':
#		return html.Div([
#			dcc.Markdown('#### **Informações Relevantes sobre o Gráfico**'),
#			html.P('Com esses resultados pode-se analisar os centros que possuem mais docentes que discentes, quando os valores obtidos forem menores que 1, e os que possuem mais alunos que professores, para valores maiores que 1.',
#				  style={'font-size':16,'textAlign': 'left'})
#		])
#


@app.callback(
	Output("sgraph_discentes", "children"),
	[Input("scentro", "value"),
	Input("sano", "value"), Input("stabs-example","value")],
)
def update_graph_discentes(centro, ano, tab):
    if tab == 'stab-1':        
        df_rel = pd.read_csv("Apoio/area-centro.csv")
        agraf_rel = make_subplots(rows=1, cols=1,  shared_yaxes=True)
        for an in ano:
            z = df_rel[(df_rel['centro'].isin(centro))].groupby(['area'])[str(an)].sum().reset_index(level=0)
            agraf_rel.add_trace(go.Bar(x=z.drop(z[z[str(an)]==0].index)['area'], y=z.drop(z[z[str(an)]==0].index)[str(an)], name=str(an)),1,1)
            agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
        agraf_rel.update_layout(go.Layout(yaxis={'title':'Numero de Projetos'},xaxis={'title': 'Area'}))
        return dcc.Graph(figure=agraf_rel)
    if tab == 'stab-2':
        df_rel = pd.read_csv("Apoio/area-centro.csv")
        if len(ano) == 1:
                agraf_rel = make_subplots(rows=1, cols=1, specs=[[{"type": "pie"}]],subplot_titles=sorted(ano))
        elif len(ano) == 2:
                agraf_rel = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],subplot_titles=sorted(ano))
        elif len(ano) == 3:
                agraf_rel = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"},{"type": "pie"}]],subplot_titles=sorted(ano))
        elif len(ano) == 4:
                agraf_rel = make_subplots(rows=1, cols=4, specs=[[{"type": "pie"}, {"type": "pie"},{"type": "pie"},{"type": "pie"}]],subplot_titles=sorted(ano))
        i = 0
        for an in sorted(ano):
                i += 1
                z = df_rel[(df_rel['centro'].isin(centro))].groupby(['area'])[str(an)].sum().reset_index(level=0)
                agraf_rel.add_trace(go.Pie(labels=z.drop(z[z[str(an)]==0].index)['area'], values=z.drop(z[z[str(an)]==0].index)[str(an)], name=str(an)),1,i)
                agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                agraf_rel.update_traces(hoverinfo='label+percent', textinfo='percent',
                marker=dict(line=dict(color='#000000', width=0.5)))
                agraf_rel.update_traces(textposition='inside')
                agraf_rel.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        return dcc.Graph(figure=agraf_rel)


            
	 
@app.callback(
	[Output("scentro", "value"),Output("smodal_3", "is_open")],
	[Input("sano", "value"), Input("sclose_3", "n_clicks")],
	[State("scentro", "value"),State("smodal_3", "is_open")],

)
def limite_centros(ano,n_rel, centro,is_open_rel):
	if 'Todos os centros' in centro:
		return [['CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ'],is_open_rel]
	if len(centro) == 0:
		return [['CEAR'], not is_open_rel]
	else:
		if n_rel:
			if is_open_rel == True:
				return [centro, not is_open_rel]
			return [centro, is_open_rel]
		return [centro, is_open_rel]



@app.callback(
	[Output("sano", "value"),Output("smodal_4", "is_open")],
	[Input("scentro", "value"),Input("sclose_4", "n_clicks")],
	[State("sano", "value"),State("smodal_4", "is_open")],

)

def flag(centro,n_rel, ano, is_open_rel):
        if 'Todos os anos' in ano:
                return [[2017,2018,2019,2020],is_open_rel]
        if len(ano) == 0:
                return [[2020], not is_open_rel]
        else:
                if n_rel:
                        if is_open_rel == True:
                                return [ano, not is_open_rel]
                        return [ano, is_open_rel]
                return [ano, is_open_rel]




        
        

@app.callback(
	Output("scard", "children"),
	[Input("stabs-example","value")]
)

def graf_tit(tab):
        if tab == 'stab-1':
                return 'Gráfico da Relação de Discentes/Docentes por Centro'
        elif tab == 'stab-2':
                return 'Gráfico Evolutivo de Discentes por Centro'
 
##########rafael##############


@app.callback([dash.dependencies.Output('bar_graph','figure'),
			   dash.dependencies.Output('pie_graph','figure')],
			   [dash.dependencies.Input('years','value')])


def update_graph(values):
	datas = []
	layouts=[]
	if '17' ==values:
		return figa,pie1

	elif '18' == values :
		return fig2a,pie2
		
	elif '19'== values:
		return fig3a,pie3



##########manu##############     
@app.callback(
	Output("grafico_avaliadores", "children"),
	[Input("tab_escolha_grafico_manu","value")]
)

def graf_titulo(tab):
        if tab == 'notas_projetos':
          return 'Média das notas dos projetos por Centro'

        elif tab == 'notas_areaTematica':
          return 'Média das notas dos projetos por Centro e Área Temática'

@app.callback(
	Output('relatorio_estudo_notas','children'),
	[Input('dropdown_anos_notas','value'),
	Input('dropdown_centros_notas','value'),
	Input('dropdown_anos_areaTematica_notas','value'),
	Input('dropdown_centros_areaTematica_notas','value'),
	Input('dropdown_areaTematica_notas','value'),
	Input('tab_escolha_grafico_manu','value')]
)

def formatar_relatorio(dropdown_anos_notas,dropdown_centros_notas,dropdown_anos_areaTematica_notas,dropdown_centros_areaTematica_notas,dropdown_areaTematica_notas,tab):
		if tab == 'notas_projetos':
			anos0 =", ".join(str(x) for x in dropdown_anos_notas)
			centros0 =", ".join(str(x) for x in dropdown_centros_notas)
			return f'''Este gráfico mostra a média, e seu respectivo desvio padrão, encontrados para as notas recebidas por todos projetos do(s) Centro(s): {centros0}, no(s) Ano(s) {anos0}, sendo as notas de cada um calculadas de acordo com o método usado pela PROEX: para projetos com até 4 avaliações sua nota é a média comum entre estas, para projetos com 6-7 avaliações sua nota é a média comun entre as três últimas.'''
		if tab == 'notas_areaTematica':
			anos1 =", ".join(str(x) for x in dropdown_anos_areaTematica_notas)
			centros1 =", ".join(str(x) for x in dropdown_centros_areaTematica_notas) 
			area =", ".join(str(x) for x in dropdown_areaTematica_notas)
			return f'''Este gráfico mostra a média, e seu respectivo desvio padrão, encontrados para as notas recebidas por todos os projetos contidos na(s) Área(s) Temática(s): {area} do(s) Centro(s): {centros1}, no(s) Ano(s) {anos1}, sendo as notas de cada um calculadas de acordo com o método usado pela PROEX: para projetos com até 4 avaliações sua nota é a média comum entre estas, para projetos com 6-7 avaliações sua nota é a média comun entre as três últimas.'''					


@app.callback(
	Output("grafico_notas", "children"),
	[Input("dropdown_anos_notas", "value"),
	Input("dropdown_centros_notas", "value"),
	Input("dropdown_anos_areaTematica_notas","value"),
	Input("dropdown_centros_areaTematica_notas","value"),
	Input("dropdown_areaTematica_notas", "value"),
	Input("tab_escolha_grafico_manu","value")]
)
def grafico_notas(dropdown_anos_notas,dropdown_centros_notas,dropdown_anos_areaTematica_notas,dropdown_centros_areaTematica_notas,dropdown_areaTematica_notas,tab_escolha_grafico):
	if (tab_escolha_grafico == 'notas_projetos'):
		centros_selecionados = []
		medias = pd.read_csv('Apoio/media_notas.csv')
		desvios = pd.read_csv('Apoio/desvio_media_notas.csv')
		lista_anos = []
		lista_anos = dropdown_anos_notas

		for i in dropdown_centros_notas :
			if (i in Lista_Centros[0:]):
				centros_selecionados.append(i)
			else:
				None
		lista_anos_texto =", ".join(str(x) for x in lista_anos)
		if (len(lista_anos) == 1):
			#medias.sort_values(by = [lista_anos[0]],inplace = True)
			error = []
			ordem = []
			for j in centros_selecionados:
				indice = list(medias[medias['Centros']== j].index)
				ordem.append(indice[0])
			ordem = sorted(ordem)
			dt = medias.loc[ordem,:]
			for i in list(dt['Centros']):
				a = list(desvios[desvios['Centros'] == i][lista_anos[0]])
				error.append(a[0])
			dt.sort_values(by =[lista_anos[0]],inplace = True )
			x = list(dt['Centros'])
			y = list(dt.loc[:,lista_anos[0]])
			
			fig = go.Figure()
			fig.add_trace(go.Bar(
    			name=lista_anos[0],
    			x=x, y=y,
    			error_y=dict(type='data', array=np.array(error))
			))
			fig . update_layout ( 
				title = 'Média das notas dos projetos por Centro no(s) ano(s) : {}'.format(lista_anos_texto),
    			yaxis  =  dict ( 
        		tickmode  =  'linear' , 
        		tick0  =  0 , 
        		dtick  =  (1) 
    			) 
			)
			lista_anos = []
			return dcc.Graph(
							id='grafico',
							figure = fig)
				
		elif (len(lista_anos) == 2):
			error = []
			error_1 = []
			ordem = []
			for j in centros_selecionados:
				indice = list(medias[medias['Centros']== j].index)
				ordem.append(indice[0])
			ordem = sorted(ordem)
			dt = medias.loc[ordem,:]
			for i in list(dt['Centros']):
				a = list(desvios[desvios['Centros'] == i][lista_anos[0]])
				error.append(a[0])
				b = list(desvios[desvios['Centros'] == i][lista_anos[1]])
				error_1.append(b[0])
			
			data = dt.sort_values(by =[lista_anos[0]])
			x = list(data['Centros'])
			y = list(data.loc[:,lista_anos[0]])

			data1 = dt.sort_values(by =[lista_anos[1]])
			x1 = list(data1['Centros'])
			y1 = list(data1.loc[:,lista_anos[1]])
			
			fig = go.Figure()
			fig.add_trace(go.Bar(
    			name=lista_anos[0],
    			x=x, y=y,
    			error_y=dict(type='data', array=np.array(error))
			))
			fig.add_trace(go.Bar(
    			name=lista_anos[1],
    			x=x1, y=y1,
    			error_y=dict(type='data', array=np.array(error_1))
			))
			fig . update_layout ( 
				title = 'Média das notas dos projetos por Centro no(s) ano(s) : {}'.format(lista_anos_texto),
    			yaxis  =  dict ( 
        		tickmode  =  'linear' , 
        		tick0  =  0 , 
        		dtick  =  (1) 
    			) 
			)
			lista_anos = []
			return dcc.Graph(
							id='grafico',
							figure = fig)

		elif (len(lista_anos) == 3):
			error = []
			error_1 = []
			error_2 = []
			ordem = []
			for j in centros_selecionados:
				indice = list(medias[medias['Centros']== j].index)
				ordem.append(indice[0])
			ordem = sorted(ordem)
			dt = medias.loc[ordem,:]
			for i in list(dt['Centros']):
				a = list(desvios[desvios['Centros'] == i][lista_anos[0]])
				error.append(a[0])
				b = list(desvios[desvios['Centros'] == i][lista_anos[1]])
				error_1.append(b[0])
				c = list(desvios[desvios['Centros'] == i][lista_anos[2]])
				error_2.append(c[0])
			
			data = dt.sort_values(by =[lista_anos[0]])
			x = list(data['Centros'])
			y = list(data.loc[:,lista_anos[0]])

			data1 = dt.sort_values(by =[lista_anos[1]])
			x1 = list(data1['Centros'])
			y1 = list(data1.loc[:,lista_anos[1]])

			data2 = dt.sort_values(by =[lista_anos[2]])
			x2 = list(data2['Centros'])
			y2 = list(data2.loc[:,lista_anos[2]])
			
			fig = go.Figure()
			fig.add_trace(go.Bar(
    			name=lista_anos[0],
    			x=x, y=y,
    			error_y=dict(type='data', array=np.array(error))
			))
			fig.add_trace(go.Bar(
    			name=lista_anos[1],
    			x=x1, y=y1,
    			error_y=dict(type='data', array=np.array(error_1))
			))
			fig.add_trace(go.Bar(
    			name=lista_anos[2],
    			x=x2, y=y2,
    			error_y=dict(type='data', array=np.array(error_2))
			))
			fig . update_layout ( 
				title = 'Média das notas dos projetos por Centro no(s) ano(s) : {}'.format(lista_anos_texto),
    			yaxis  =  dict ( 
        		tickmode  =  'linear' , 
        		tick0  =  0 , 
        		dtick  =  (1) 
    			) 
			)
			lista_anos = []
			return dcc.Graph(
							id='grafico',
							figure = fig)

		elif (len(lista_anos) == 4):
			error = []
			error_1 = []
			error_2 = []
			error_3 = []
			ordem = []
			for j in centros_selecionados:
				indice = list(medias[medias['Centros']== j].index)
				ordem.append(indice[0])
			ordem = sorted(ordem)
			dt = medias.loc[ordem,:]
			for i in list(dt['Centros']):
				a = list(desvios[desvios['Centros'] == i][lista_anos[0]])
				error.append(a[0])
				b = list(desvios[desvios['Centros'] == i][lista_anos[1]])
				error_1.append(b[0])
				c = list(desvios[desvios['Centros'] == i][lista_anos[2]])
				error_2.append(c[0])
				d = list(desvios[desvios['Centros'] == i][lista_anos[3]])
				error_3.append(d[0])
			
			data = dt.sort_values(by =[lista_anos[0]])
			x = list(data['Centros'])
			y = list(data.loc[:,lista_anos[0]])

			data1 = dt.sort_values(by =[lista_anos[1]])
			x1 = list(data1['Centros'])
			y1 = list(data1.loc[:,lista_anos[1]])

			data2 = dt.sort_values(by =[lista_anos[2]])
			x2 = list(data2['Centros'])
			y2 = list(data2.loc[:,lista_anos[2]])

			data3 = dt.sort_values(by =[lista_anos[3]])
			x3 = list(data3['Centros'])
			y3 = list(data3.loc[:,lista_anos[3]])
			
			fig = go.Figure()
			fig.add_trace(go.Bar(
    			name=lista_anos[0],
    			x=x, y=y,
    			error_y=dict(type='data', array=np.array(error))
			))
			fig.add_trace(go.Bar(
    			name=lista_anos[1],
    			x=x1, y=y1,
    			error_y=dict(type='data', array=np.array(error_1))
			))
			fig.add_trace(go.Bar(
    			name=lista_anos[2],
    			x=x2, y=y2,
    			error_y=dict(type='data', array=np.array(error_2))
			))
			fig.add_trace(go.Bar(
    			name=lista_anos[3],
    			x=x3, y=y3,
    			error_y=dict(type='data', array=np.array(error_3))
			))
			fig . update_layout ( 
				title = 'Média das notas dos projetos por Centro no(s) ano(s) : {}'.format(lista_anos_texto),
    			yaxis  =  dict ( 
        		tickmode  =  'linear' , 
        		tick0  =  0 , 
        		dtick  =  (1) 
    			) 
			)
			lista_anos = []
			return dcc.Graph(
							id='grafico',
							figure = fig)

	if (tab_escolha_grafico == 'notas_areaTematica'):
		centros_selecionados = []
		areas_selecionadas = []
		amostras = pd.read_csv('Apoio/amostras_dos_projetos_por_areatematica.csv')
		amostras.drop('Unnamed: 0',axis = 1,inplace = True)
		amostras.drop('Unnamed: 1',axis = 1,inplace = True)

		out = ['CCS','CCS','CCS','CCS','CEAR','CEAR','CEAR','CEAR','CCEN','CCEN','CCEN','CCEN','CT','CT','CT','CT','CCM','CCM','CCM','CCM','CBIOTEC','CBIOTEC','CBIOTEC','CBIOTEC','CTDR','CTDR','CTDR','CTDR','CCHLA','CCHLA','CCHLA','CCHLA','CCTA','CCTA','CCTA','CCTA','CCHSA','CCHSA','CCHSA','CCHSA','CCSA','CCSA','CCSA','CCSA','CI','CI','CI','CI','CCAE','CCAE','CCAE','CCAE','CCJ','CCJ','CCJ','CCJ','CCA','CCA','CCA','CCA','CE','CE','CE','CE']
		inter = [2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020,2017,2018,2019,2020]
		multi = list(zip(out,inter))
		multi = pd.MultiIndex.from_tuples(multi)

		amostras.index = multi
		amostras.index.names = ['Centro','Ano']

		lista_anos = []
		lista_anos = dropdown_anos_areaTematica_notas

		for i in dropdown_centros_areaTematica_notas :
			if (i in Lista_Centros[0:]):
				centros_selecionados.append(i)
			else:
				None

		for i in dropdown_areaTematica_notas :
			if (i in areas[0:]):
				areas_selecionadas.append(i)
			else:
				None
		if (len(lista_anos) == 1):
			dataAmostra = amostras.loc[(centros_selecionados,lista_anos),areas_selecionadas]
			##-----------------------------------##
			dataAmostra0 = dataAmostra.xs(lista_anos[0],level='Ano')
			print(dataAmostra0)
			amostraStr = []
			desvios0 = []
			medias0 = []
			areasAcessadas0 = []
			dataCentros0 = list(dataAmostra0.index)
			regex = re.compile(r'''(
				\d+
				\.?
				\d*
				)''',re.VERBOSE)
			for i in range(0,len(dataAmostra0)):
				geral = dataAmostra0.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas0.append(list(resultado.index))
				Am = list(dataAmostra0.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios0.append(0.0)
					medias0.append(0.0)
				if valor > 0:
					medias0.append(valor/tamanhoTotal)
					desvios0.append(np.std(amostraCentro))
			dicioM0 = dict(zip(dataCentros0,medias0))
			dicioD0 =dict(zip(dataCentros0,desvios0))
			dicioM0 = dict(sorted(dicioM0.items(),key = itemgetter(1)))
			print(dicioM0)
			print(dicioD0)

			error0 = []
			for i in dicioM0.keys():
				error0.append(dicioD0[i])
			##-----------------------------------##
			
			fig = go.Figure()
			fig.add_trace(go.Bar(
			x = list(dicioM0.keys()),
			y = list(dicioM0.values()),
			name = lista_anos[0],
			text = areasAcessadas0,
			error_y=dict(type='data', array=np.array(error0))
			))
			print(list(dicioM0.keys()))
			print(list(dicioM0.values()))
			print(error0)
			fig.update_traces(hovertemplate='Centro: %{x} <br>Nota: %{y} <br>Áreas: %{text}')
			fig.update_layout (
				yaxis  =  dict ( 
        		tickmode  =  'linear' , 
        		tick0  =  0 , 
        		dtick  =  (1) 
    			) 
			)
			return dcc.Graph(
							id='grafico_area',
							figure = fig)

		if (len(lista_anos) == 2):
			dataAmostra = amostras.loc[(centros_selecionados,lista_anos),areas_selecionadas]
			regex = re.compile(r'''(
				\d+
				\.?
				\d*
				)''',re.VERBOSE)
			##-----------------------------------##
			dataAmostra0 = dataAmostra.xs(lista_anos[0],level='Ano')
			amostraStr = []
			desvios0 = []
			medias0 = []
			dataCentros0 = list(dataAmostra0.index)
			areasAcessadas0 = []
			for i in range(0,len(dataAmostra0)):
				geral = dataAmostra0.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas0.append(list(resultado.index))
				Am = list(dataAmostra0.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios0.append(0.0)
					medias0.append(0.0)
				if valor > 0:
					medias0.append(valor/tamanhoTotal)
					desvios0.append(np.std(amostraCentro))
			dicioM0 = dict(zip(dataCentros0,medias0))
			dicioD0 =dict(zip(dataCentros0,desvios0))
			dicioM0 = dict(sorted(dicioM0.items(),key = itemgetter(1)))

			error0 = []
			for i in dicioM0.keys():
				error0.append(dicioD0[i])
			##-----------------------------------##
			dataAmostra1 = dataAmostra.xs(lista_anos[1],level='Ano')
			amostraStr = []
			desvios1 = []
			medias1 = []
			areasAcessadas1 = []
			dataCentros1 = list(dataAmostra1.index)
			for i in range(0,len(dataAmostra1)):
				geral = dataAmostra1.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas1.append(list(resultado.index))
				Am = list(dataAmostra1.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios1.append(0.0)
					medias1.append(0.0)
				if valor > 0:
					medias1.append(valor/tamanhoTotal)
					desvios1.append(np.std(amostraCentro))
			dicioM1 = dict(zip(dataCentros1,medias1))
			dicioD1 =dict(zip(dataCentros1,desvios1))
			dicioM1 = dict(sorted(dicioM1.items(),key = itemgetter(1)))

			error1 = []
			for i in dicioM1.keys():
				error1.append(dicioD1[i])
			##-----------------------------------##
			fig = go.Figure()
			fig.add_trace(go.Bar(
			x = list(dicioM0.keys()),
			y = list(dicioM0.values()),
			name = lista_anos[0],
			text = areasAcessadas0,
			error_y=dict(type='data', array=np.array(error0))
			))

			fig.add_trace(go.Bar(
			x = list(dicioM1.keys()),
			y = list(dicioM1.values()),
			name = lista_anos[1],
			text = areasAcessadas1,
			error_y=dict(type='data', array=np.array(error1))
			))

			fig.update_traces(hovertemplate='Centro: %{x} <br>Nota: %{y} <br>Áreas: %{text}')
			fig.update_layout ( 
				yaxis  =  dict ( 
        		tickmode  =  'linear' , 
        		tick0  =  0 , 
        		dtick  =  (1) 
    			) 
			)
			return dcc.Graph(
							id='grafico_area',
							figure = fig)

		if (len(lista_anos) == 3):
			dataAmostra = amostras.loc[(centros_selecionados,lista_anos),areas_selecionadas]
			regex = re.compile(r'''(
				\d+
				\.?
				\d*
				)''',re.VERBOSE)
			##-----------------------------------##	
			dataAmostra0 = dataAmostra.xs(lista_anos[0],level='Ano')
			amostraStr = []
			desvios0 = []
			medias0 = []
			areasAcessadas0 = []
			dataCentros0 = list(dataAmostra0.index)
			for i in range(0,len(dataAmostra0)):
				geral = dataAmostra0.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas0.append(list(resultado.index))
				Am = list(dataAmostra0.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios0.append(0.0)
					medias0.append(0.0)
				if valor > 0:
					medias0.append(valor/tamanhoTotal)
					desvios0.append(np.std(amostraCentro))
			dicioM0 = dict(zip(dataCentros0,medias0))
			dicioD0 =dict(zip(dataCentros0,desvios0))
			dicioM0 = dict(sorted(dicioM0.items(),key = itemgetter(1)))

			error0 = []
			for i in dicioM0.keys():
				error0.append(dicioD0[i])
			##-----------------------------------##
			dataAmostra1 = dataAmostra.xs(lista_anos[1],level='Ano')
			amostraStr = []
			desvios1 = []
			medias1 = []
			areasAcessadas1 = []
			dataCentros1 = list(dataAmostra1.index)
			for i in range(0,len(dataAmostra1)):
				geral = dataAmostra1.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas1.append(list(resultado.index))
				Am = list(dataAmostra1.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios1.append(0.0)
					medias1.append(0.0)
				if valor > 0:
					medias1.append(valor/tamanhoTotal)
					desvios1.append(np.std(amostraCentro))
			dicioM1 = dict(zip(dataCentros1,medias1))
			dicioD1 =dict(zip(dataCentros1,desvios1))
			dicioM1 = dict(sorted(dicioM1.items(),key = itemgetter(1)))

			error1 = []
			for i in dicioM1.keys():
				error1.append(dicioD1[i])
			##-----------------------------------##
			dataAmostra2 = dataAmostra.xs(lista_anos[2],level='Ano')
			amostraStr = []
			desvios2 = []
			medias2 = []
			areasAcessadas2 = []
			dataCentros2 = list(dataAmostra2.index)
			for i in range(0,len(dataAmostra2)):
				geral = dataAmostra2.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas2.append(list(resultado.index))
				Am = list(dataAmostra2.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios2.append(0.0)
					medias2.append(0.0)
				if valor > 0:
					medias2.append(valor/tamanhoTotal)
					desvios2.append(np.std(amostraCentro))
			dicioM2 = dict(zip(dataCentros2,medias2))
			dicioD2 =dict(zip(dataCentros2,desvios2))
			dicioM2 = dict(sorted(dicioM2.items(),key = itemgetter(1)))

			error2 = []
			for i in dicioM2.keys():
				error2.append(dicioD2[i])
			##-----------------------------------##
			fig = go.Figure()
			fig.add_trace(go.Bar(
			x = list(dicioM0.keys()),
			y = list(dicioM0.values()),
			text = areasAcessadas0,
			name = lista_anos[0],
			error_y=dict(type='data', array=np.array(error0))
			))

			fig.add_trace(go.Bar(
			x = list(dicioM1.keys()),
			y = list(dicioM1.values()),
			text = areasAcessadas1,
			name = lista_anos[1],
			error_y=dict(type='data', array=np.array(error1))
			))

			fig.add_trace(go.Bar(
			x = list(dicioM2.keys()),
			y = list(dicioM2.values()),
			text = areasAcessadas2,
			name = lista_anos[2],
			error_y=dict(type='data', array=np.array(error2))
			))

			fig.update_traces(hovertemplate='Centro: %{x} <br>Nota: %{y} <br>Áreas: %{text}')
			fig.update_layout ( 
				yaxis  =  dict ( 
        		tickmode  =  'linear' , 
        		tick0  =  0 , 
        		dtick  =  (1) 
    			) 
			)
			return dcc.Graph(
							id='grafico_area',
							figure = fig)

		if (len(lista_anos) == 4):
			dataAmostra = amostras.loc[(centros_selecionados,lista_anos),areas_selecionadas]
			regex = re.compile(r'''(
				\d+
				\.?
				\d*
				)''',re.VERBOSE)
			##-----------------------------------##	
			dataAmostra0 = dataAmostra.xs(lista_anos[0],level='Ano')
			
			amostraStr = []
			desvios0 = []
			medias0 = []
			areasAcessadas0 = []
			dataCentros0 = list(dataAmostra0.index)
			for i in range(0,len(dataAmostra0)):
				geral = dataAmostra0.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas0.append(list(resultado.index))
				Am = list(dataAmostra0.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios0.append(0.0)
					medias0.append(0.0)
				if valor > 0:
					medias0.append(valor/tamanhoTotal)
					desvios0.append(np.std(amostraCentro))
			dicioM0 = dict(zip(dataCentros0,medias0))
			dicioD0 =dict(zip(dataCentros0,desvios0))
			dicioM0 = dict(sorted(dicioM0.items(),key = itemgetter(1)))

			error0 = []
			for i in dicioM0.keys():
				error0.append(dicioD0[i])
			##-----------------------------------##
			
			dataAmostra1 = dataAmostra.xs(lista_anos[1],level='Ano')
			
			amostraStr = []
			desvios1 = []
			medias1 = []
			areasAcessadas1 =[]
			dataCentros1 = list(dataAmostra1.index)
			for i in range(0,len(dataAmostra1)):
				geral = dataAmostra1.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas1.append(list(resultado.index))
				Am = list(dataAmostra1.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios1.append(0.0)
					medias1.append(0.0)
				if valor > 0:
					medias1.append(valor/tamanhoTotal)
					desvios1.append(np.std(amostraCentro))
			dicioM1 = dict(zip(dataCentros1,medias1))
			dicioD1 =dict(zip(dataCentros1,desvios1))
			dicioM1 = dict(sorted(dicioM1.items(),key = itemgetter(1)))

			error1 = []
			for i in dicioM1.keys():
				
				error1.append(dicioD1[i])
			##-----------------------------------##
			dataAmostra2 = dataAmostra.xs(lista_anos[2],level='Ano')
			amostraStr = []
			desvios2 = []
			medias2 = []
			areasAcessadas2 = []
			dataCentros2 = list(dataAmostra2.index)
			for i in range(0,len(dataAmostra2)):
				geral = dataAmostra2.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas2.append(list(resultado.index))
				Am = list(dataAmostra2.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios2.append(0.0)
					medias2.append(0.0)
				if valor > 0:
					medias2.append(valor/tamanhoTotal)
					desvios2.append(np.std(amostraCentro))
			dicioM2 = dict(zip(dataCentros2,medias2))
			dicioD2 =dict(zip(dataCentros2,desvios2))
			dicioM2 = dict(sorted(dicioM2.items(),key = itemgetter(1)))

			error2 = []
			
			for i in dicioM2.keys():
				error2.append(dicioD2[i])
			##-----------------------------------##
			dataAmostra3 = dataAmostra.xs(lista_anos[3],level='Ano')
			amostraStr = []
			desvios3 = []
			medias3 = []
			areasAcessadas3 = []
			dataCentros3 = list(dataAmostra3.index)
			for i in range(0,len(dataAmostra3)):
				geral = dataAmostra3.iloc[i,:]
				condicao = geral == '0.0'
				resultado = geral.mask(condicao)
				resultado.dropna(inplace = True)
				areasAcessadas3.append(list(resultado.index))
				Am = list(dataAmostra3.iloc[i,:])
				amostraStr.append(Am)
			for j in range(0,len(amostraStr)):
				amostraCentro=[]
				tamanhoTotal = 0
				for k in range(0,len(amostraStr[j])):
					find = regex.findall(amostraStr[j][k])
					tamanho = len(find)
					if tamanho == 1 and find[0] == '0.0':
						tamanho = 0
					tamanhoTotal = tamanhoTotal + tamanho
					for m in find:
						m = float(m)
						if m != 0.0:
							amostraCentro.append(m)
				valor = sum(amostraCentro)
				if valor == 0:
					desvios3.append(0.0)
					medias3.append(0.0)
				if valor > 0:
					medias3.append(valor/tamanhoTotal)
					desvios3.append(np.std(amostraCentro))
			dicioM3 = dict(zip(dataCentros3,medias2))
			dicioD3 =dict(zip(dataCentros3,desvios2))
			dicioM3 = dict(sorted(dicioM3.items(),key = itemgetter(1)))

			error3 = []
			for i in dicioM3.keys():
				error3.append(dicioD3[i])
			##-----------------------------------##
			fig = go.Figure()
			fig.add_trace(go.Bar(
			x = list(dicioM0.keys()),
			y = list(dicioM0.values()),
			text = areasAcessadas0,
			name = lista_anos[0],
			error_y=dict(type='data', array=np.array(error0))
			))

			fig.add_trace(go.Bar(
			x = list(dicioM1.keys()),
			y = list(dicioM1.values()),
			name = lista_anos[1],
			text = areasAcessadas1,
			error_y=dict(type='data', array=np.array(error1))
			))

			fig.add_trace(go.Bar(
			x = list(dicioM2.keys()),
			y = list(dicioM2.values()),
			name = lista_anos[2],
			text = areasAcessadas2,
			error_y=dict(type='data', array=np.array(error2))
			))

			fig.add_trace(go.Bar(
			x = list(dicioM3.keys()),
			y = list(dicioM3.values()),
			name = lista_anos[3],
			text = areasAcessadas3,
			error_y=dict(type='data', array=np.array(error3))
			))

			fig.update_traces(hovertemplate='Centro: %{x} <br>Nota: %{y} <br>Áreas: %{text}')
			fig.update_layout ( 
				yaxis  =  dict ( 
        		tickmode  =  'linear' , 
        		tick0  =  0 , 
        		dtick  =  (1) 
    			) 
			)
			return dcc.Graph(
							id='grafico_area',
							figure = fig)
			




####exibirnotecomeça######
@app.callback(
	dash.dependencies.Output('cities-dropdown', 'options'),
	[dash.dependencies.Input('countries-dropdown', 'value')])
def set_cities_options(selected_country):
	return [{'label': i, 'value': i} for i in all_options[selected_country]]

@app.callback(
	dash.dependencies.Output('cities-dropdown', 'value'),
	[dash.dependencies.Input('cities-dropdown', 'options')])
def set_cities_value(available_options):
	return available_options[0]['value']

@app.callback(
	dash.dependencies.Output('display-selected-values', 'children'),
	[dash.dependencies.Input('countries-dropdown', 'value'),
	 dash.dependencies.Input('cities-dropdown', 'value')])


def set_display_children(selected_country, selected_city):
	
	 #João e emmanuela
	if ((selected_country == 'João Guilherme e Emmanuela' or selected_country == 'Rafael' or selected_country == 'Gabriel')  and selected_city=='Abril'):
		return html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 10/04/2020 - 11/05/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Familiarização com Python+biblioteca grafica
								- Familiarização com Edital Probex,
							   ''', style={'horizontal-Align':'left', 'textAlign':'left', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
					
				])
		])
		
	
	   
	elif selected_country == 'João Guilherme e Emmanuela' and selected_city=='Maio':
		return  html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 12/05/2020 - 19/05/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Criar um Jupyter Notebook para totalizar o número de projetos por ano
								- Ler Arquivos de Dados
								- Fazer a Correção dos caracteres indesejados
								- Eliminar as Duplicidades dos projetos existentes
								- Levantar os quantitativos dos projetos por ano (2017, 2018, 2019)(Situação em 2017 e 2018: Concluido / em 2019: Em execução
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
		
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 2: 19/05/2020 - 25/05/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Levantar todos os tipos de situação que um projeto pode assumir
								- Quantas são as ocorrências por situação(2017,2018,2019)
								- Quantitativos dos Projetos por Unidade Proponente
								- Contagem de projetos com situação CONCLUÍDA em 2017 e 2018 separado por Centro
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 3: 25/05/2020 - 01/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Apresentar os dados obtidos anteriormente usando graficos (Pizza e Barra)
								- Ordenar do menor para o maior numero de ocorrências
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
					
				])
		])
			
	
	elif selected_country == 'João Guilherme e Emmanuela' and selected_city=='Junho':
		return  html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 01/06/2020 - 08/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Criar uma page com os gráficos gerados
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
		
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 2: 09/06/2020 - 15/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Criar uma Page de reuniões(Atividades+Resultados)
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 3: 15/06/2020 - 22/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Descrever os Gráficos que estão sendo Exibidos
								- Colocar o Pdf do tutorial no Github
								- Atualizar a proposta da page das atividades
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 4: 22/06/2020 - 30/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Apresentação sobre a Biblioteca NLTK + Testes (João)
								- Contagem de Palvras(Metodologia, Justificativa e Resumo) - (Emmanuela)
								- Separar as ocorrências destas palavras por Centro (Emmanuela)
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
				])
		])
	
	elif selected_country == 'João Guilherme e Emmanuela' and selected_city=='Julho':
		return  html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 30/06/2020 - 04/07/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Atualizar o site (joão)
								- Aplicar o nltk para ver a variabilidade vocabular dos centros (usando resumo, justificativa e metodologia)
								- Gerar um gráfico de barras e colocar no site(joão)
								- Separar os dados por anos (Emmanuela)
								- Normalizar de acordo com a quantidade de projetos de cada centro (Emmanuela)
								- Deixar Genérica a Quantidade de Palavras (Emmanuela)
								- Remover os projetos com status não desejado (Emmanuela)
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
		
								], style=tab_style, selected_style=tab_selected_style),
				
				
				])
		])
	
	
	
	
   
	
	
	
	#Gabriel
	
	elif selected_country == 'Gabriel' and selected_city=='Maio':
		return  html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 12/05/2020 - 19/05/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Cria um jupyter notebook para gerar um mapa com os centros da UFPB
								- Gerar um json com a delimitação dos centros
								- Construir o mapa baseado no folium com uma camada paracada centro
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
		
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 2: 19/05/2020 - 25/05/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Colorir o mapa de acordo com o dado
								- Adicionar o eventro click (Revelar a lista de centros presente no poligono)
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 3: 25/05/2020 - 01/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Introduzir o conveito de filtro no mapa
								- dividir o conjunto de centros em 3 grupos
								- cada grupo pode ser escolhido individualmente em um listbox
								- uma vez escolhido o grupo, o grafico deve fazer o highlight apenas nos centros do grupo escolhido
								Criar pastas compartilhadas
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),       
				])
		])
   
	
	
	elif selected_country == 'Gabriel' and selected_city=='Junho':
		return  html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 01/06/2020 - 08/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Unir todas as páginas em um Dash Multipage 
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
		
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 2: 09/06/2020 - 15/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Gerenciar as seguintes plataformas:
								- Heroku  
								- Github 
									-Pasta de Apoio -Root
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 3: 15/06/2020 - 22/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Atualizar o texto do que é ODE
								- Atualizar o modo choropleth (Escala de cores)
								- Atualizar a divisão dos centros
								- Checar o controle de acesso ao site
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 4: 22/06/2020 - 30/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Personalizar a tela de login
								- Fazer o vídeo intro da apresentação.
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
				
				
				])
		])
	
	
	elif selected_country == 'Gabriel' and selected_city=='Julho':
		return  html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 30/06/2020 - 04/07/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Colocar link nas imagens
								- Alterar o mapa
								- Alterar o layout do site para o modo duas colunas 
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
		
								], style=tab_style, selected_style=tab_selected_style),
				
				
				])
		])
	
	
	
	
	
	#Rafael
	
	elif selected_country == 'Rafael' and selected_city=='Maio':
		 return  html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 12/05/2020 - 19/05/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Criar um jupyter notebook para totalizar o numero de participantes
								- Ler arquivo dos dados
								- Fazer a correção dos caracteres indesejados
								- Eliminar, eventual, duplicidade de docentes e discentes existentes / id_projeto
								- Levantar os quantitativos dos docentes e discentes por ano (2017, 2018, 2019)
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
		
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 2: 19/05/2020 - 25/05/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Criar um jupyter notebook para totalizar o numero de participantes
								- Quais são as ocorrências por categoria de aluno?
								- Quantitativos dos alunos por Curso? (2017, 2018, 2019)
								- Quais são as ocorrências por categoria de docente?
								- Quantitativos dos docentes por departamento (2017, 2018, 2019)
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 3: 25/05/2020 - 01/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Criar um jupyter notebook para totalizar o numero de participantes
								- Corrigir os comentarios das celulas nos notebooks
								- Listar projetos que possuem apenas docentes (2017/2018 Concluídos, 2019 Em Execução)(2017, 2018, 2019)
								- Calcular a relação alunos/professor para cada centro (2017, 2018, 2019)
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),       
				])
		])
   
	
	elif selected_country == 'Rafael' and selected_city=='Junho':
		return  html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 01/06/2020 - 08/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Gerar o gráfico de pizza e barra com os resultados
								- Criar Page com os graficos gerados
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
		
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 2: 09/06/2020 - 15/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								Apresentação Extensão
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar apresentação', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste'),
								
								], style=tab_style, selected_style=tab_selected_style),
				
				dcc.Tab(label= 'ATIVIDADE 3: 15/06/2020 - 22/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Descrever os gráficos que estão sendo exibidos
								- Atualizar a Apresentação
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar apresentação', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),  
				
				dcc.Tab(label= 'ATIVIDADE 4: 22/06/2020 - 30/06/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Atualizar gráficos (layout)
								- Atualizar o texto dos gráficos
								- Colocar os dados referentes aos servidores
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
								
								], style=tab_style, selected_style=tab_selected_style),
				])
		])
	
	
	elif selected_country == 'Rafael' and selected_city=='Julho':
		return  html.Div([
			dcc.Tabs([
				dcc.Tab(label= 'ATIVIDADE 1: 30/06/2020 - 04/07/2020',children=[
					html.Div(html.Br()),
					dcc.Markdown('''
								- Dados para a página do Cear, projetos probex, fluex, ufpb no seu município e proext
							   ''', style={'horizontal-Align':'left', 'textAlign':'justify', 'font-size':16}),
								html.A(html.Button('Baixar notebook', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,  'height':40, 'font-size':14, 'textAlign':'center',  'color':'blue'}),  href='teste')
		
								], style=tab_style, selected_style=tab_selected_style),
				
				
				])
		])
	



####exibir note_termina####


###variacao###

@app.callback(
	dash.dependencies.Output('graficos_variabilidade', 'children'),
	[dash.dependencies.Input('seletor_variabilidade_vocabular', 'value')])

def retornar_variabilidade(value):
	if(value == 'vr'):
		return dcc.Graph(figure=fig1aa)
	
	elif(value == 'vj'):
		return dcc.Graph(figure=fig2aa)

	elif(value == 'vm'):
		return dcc.Graph(figure=fig3aa)
	
	
@app.callback(
	dash.dependencies.Output('texto_graficos_variabilidade', 'children'),
	[dash.dependencies.Input('seletor_variabilidade_vocabular', 'value')])


def retornar_variabilidade(value):
	
	if(value=='vr'):
		return html.Div([
			html.Div(html.Br()),
			html.H4("Descrição do Gráfico:", style={'font-size':19, 'textAlign':'left'}),
			dcc.Markdown('''
						Nesse gráfico, podemos observar o número de palavras médio diferentes em cada "Resumo" dos projetos de extensão centros da UFPB.
						Observando esses dados, observamos que há uma tendência nos centros de ciências humanas em ter mais palavras,algo já 
						esperado já que esses centros trabalham diretamente com a linguagem. Além dos centros de saúde, que normalmente exigem
						maior grau de linguagem por possuírem um vestibular mais competitivo.
						''', style={'horizontal-Align':'cenetr', 'textAlign':'justify', 'font-size':16}),
						html.Div(className='centralizar', children= [html.A(html.Button('Baixar informações', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,'height':40,'font-size':16,'backgroundColor':'007FFF', 'fontWeight':'bold','borderRadius':8}),  href='https://docs.google.com/document/u/1/export?format=pdf&id=11MWRa0afaZ9COa9VUr_YZfTVPcJkAsi9mSuAvH2n6ck&token=AC4w5ViuO5UKGXN4CssKTVS-XL0w47FJOg%3A1594066993067&includes_info_params=true')]),
								
		]) 
			
	
	elif(value == 'vj'):
		return html.Div([
			html.Div(html.Br()),
			html.H4("Descrição do Gráfico:", style={'font-size':19, 'textAlign':'left'}),
			dcc.Markdown('''
						Nesse gráfico, podemos observar o número de palavras médio diferentes em cada "Justificativa" dos projetos de extensão dos centros da UFPB.
						Observando esses dados, observamos que há uma tendência nos centros de ciências humanas em ter mais palavras,algo já 
						esperado já que esses centros trabalham diretamente com a linguagem. Além dos centros de saúde, que normalmente exigem
						maior grau de linguagem por possuírem um vestibular mais competitivo.
						''', style={'horizontal-Align':'cenetr', 'textAlign':'justify', 'font-size':16}),
						html.Div(className='centralizar', children= [html.A(html.Button('Baixar informações', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,'height':40,'font-size':16,'backgroundColor':'007FFF', 'fontWeight':'bold','borderRadius':8}),  href='https://doc-00-24-docstext.googleusercontent.com/export/kq4mtetp1ihn1m4d7shunh4ngg/bd76gicbdgi68qc1okoiu909c4/1594067380000/111158653440589959688/111158653440589959688/1ryverwoc2qio7bng-5k8bhG0GXh9s9tUVh8ZDx5xCFk?format=pdf&id=1ryverwoc2qio7bng-5k8bhG0GXh9s9tUVh8ZDx5xCFk&token=AC4w5VhL5yobIZifume_kohdrYzv1545tQ:1594067272165&includes_info_params=true&dat=AJ7Y-hQ3dSY3d16uTDaVc3j5BCHQzIEgD_uymszL7nSnuBaTv0iIwEhSN-VVb98qbaMvPlcOH0lHoWeawxpOKTiaMZIxZA3EvEvHH6S_liKgQVwQi6Ly6ks17YJIxGnCrKBtn-xxVss9wnJg47SWwlaRhYkIbKaTuaau5nhNAa5ZCHlllR54PvLysVoHvqGbrkwwKB2JgtqiI0g08D0lSLD79otIJMod_iTJ5a6Y6gugAX3oYMThmsVXfWlgMAhwMSnZwo1B6UJ3Ih1bujSpX-50RXN_GI554J8UWD37PeBlo-7qMMPAYGeilKLCUd1kSs8f6UTYLOGigoIGurKrZdGQptvVlN3DffKuyWWNfpFmp1XQ-a5C-teDxQu_DWEDYWNKjNU-nH53G6u0c0SZ7pUFSwvV_BSXU3HKxxt9A3_RKxuEYwR-GLi6PAU2zxTHxPEH8MdYboWSOe6vPcRb74JztHw07DKmd0GPSLYpnKej_apYlo86lhpjGe4aJ9z6g0ep-ikNUsoW8EVJmIZpT1TXzKaJeCfB5GoMMh97NqYwyKU1F-mLuCxfGGbk7Q3xzEKX1Nr5xitcQ_7012wvlF6uNi21--EmYNwHV2dyuubCesBoKGQaFE1AEWpQwd7_GOm7OTqPj_K_orq-3hwmYWHg7pG8MeX6OsdbBDaAsXM')]),
								
		]) 

	elif(value == 'vm'):
		return html.Div([
			html.Div(html.Br()),
			html.H4("Descrição do Gráfico:", style={'font-size':19, 'textAlign':'left'}),
			dcc.Markdown('''
						Nesse gráfico, podemos observar o número de palavras médio diferentes em cada "Metodologia" dos projetos de extensão dos centros da UFPB.
						Observando esses dados, observamos que há uma tendência nos centros de ciências humanas em ter mais palavras,algo já 
						esperado já que esses centros trabalham diretamente com a linguagem. Além dos centros de saúde, que normalmente exigem
						maior grau de linguagem por possuírem um vestibular mais competitivo.
						''', style={'horizontal-Align':'cenetr', 'textAlign':'justify', 'font-size':16}),
						html.Div(className='centralizar', children= [html.A(html.Button('Baixar informações', id='btn1', n_clicks=0, autoFocus=True, style={'width':300,'height':40,'font-size':16,'backgroundColor':'007FFF', 'fontWeight':'bold','borderRadius':8}),  href='https://docs.google.com/document/u/1/export?format=pdf&id=1BhoNSAVLpDrlC1HxuSPxtrk8E5AIr7Rva6L7SXLbItA&token=AC4w5VgUwmH64oQ2EDYdQvTocAIXJXj4rw%3A1594067407227&includes_info_params=true')]),
								
		]) 




###variacao###
###DOCENTES###



@app.callback(
	Output("graph_docentes_2", "style"),
	[Input("aba-example","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas == 'aba-1':
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
	else:
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}

@app.callback(
	Output("graph_docentes", "style"),
	[Input("aba-example","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas == 'aba-1':
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
	else:
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}


@app.callback(
        [Output("graph_docentes", "src"),Output("graph_docentes_2", "children")],
        [Input("centros", "value"),
        Input("anos", "value"),Input("aba-example","value")],
)
def update_graph_docentes(centros, anos,abas):
        print(abas,flush=True)
        if abas == 'aba-1':
                df_ = pd.read_csv("Apoio/df_docentes_.csv")

                meio = 0
                sete_oito = 0
                sete_nove = 0
                oito_nove = 0 
                sete_vinte = 0 
                oito_vinte = 0
                nove_vinte = 0    
                result_df_2017 = []
                result_df_2018 = []
                result_df_2019 = []
                result_df_2020 = []

                df_ = df_[df_.a.isin(centros)]

                if 2017 in anos: 
                        df_2017 = df_[df_['ano']==2017] 
                        result_df_2017 = df_2017.drop_duplicates(subset=['id_pessoa'], keep='last') 
                if 2018 in anos:
                        df_2018 = df_[df_['ano']==2018]
                        result_df_2018 = df_2018.drop_duplicates(subset=['id_pessoa'], keep='last')
                if 2019 in anos:
                        df_2019 = df_[df_['ano']==2019]
                        result_df_2019 = df_2019.drop_duplicates(subset=['id_pessoa'], keep='last')
                if 2020 in anos:
                        df_2020 = df_[df_['ano']==2020]
                        result_df_2020 = df_2020.drop_duplicates(subset=['id_pessoa'], keep='last')

                if 2017 in anos and 2018 in anos and 2019 in anos:
                        meio = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2019['id_pessoa']))))
                if 2017 in anos and 2018 in anos and 2020 in anos:
                        meio = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2020['id_pessoa']))))
                if 2018 in anos and 2019 in anos and 2020 in anos:
                        meio = len(list(set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])) & set(list(result_df_2020['id_pessoa']))))
                if 2017 in anos and 2019 in anos and 2020 in anos:
                        meio = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])) & set(list(result_df_2020['id_pessoa']))))

                print(meio)


                if 2017 in anos and 2018 in anos: 
                        sete_oito = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2018['id_pessoa'])))) - meio
                if 2017 in anos and 2019 in anos: 
                        sete_nove = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])))) - meio
                if 2018 in anos and 2019 in anos:
                        oito_nove =  len(list(set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])))) - meio  

                if 2017 in anos and 2020 in anos:
                        sete_vinte =  len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2020['id_pessoa'])))) - meio 
                if 2018 in anos and 2020 in anos:
                        oito_vinte =  len(list(set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2020['id_pessoa'])))) - meio 
                if 2019 in anos and 2020 in anos:
                        nove_vinte =  len(list(set(list(result_df_2019['id_pessoa'])) & set(list(result_df_2020['id_pessoa'])))) - meio 


                if 2017 in anos: 
                        sete = len(set(list(result_df_2017['id_pessoa']))) - meio - sete_oito - sete_nove - sete_vinte
                if 2018 in anos:
                        oito = len(set(list(result_df_2018['id_pessoa']))) - meio - sete_oito - oito_nove - oito_vinte
                if 2019 in anos:
                        nove = len(set(list(result_df_2019['id_pessoa']))) - meio - sete_nove - oito_nove - nove_vinte
                if 2020 in anos:
                        vinte = len(set(list(result_df_2020['id_pessoa']))) - meio - sete_vinte - oito_vinte - nove_vinte

                plt.clf()

                if 2017 in anos and 2018 in anos and 2019 in anos:
                        v = vplt.venn3(subsets=(sete, oito, sete_oito, nove, sete_nove, oito_nove, meio), set_labels = ('2017','2018', '2019'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]

                if 2017 in anos and 2018 in anos and 2020 in anos:
                        v = vplt.venn3(subsets=(sete, oito, sete_oito, vinte, sete_vinte, oito_vinte, meio), set_labels = ('2017','2018', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]

                if 2018 in anos and 2019 in anos and 2020 in anos:
                        v = vplt.venn3(subsets=(oito, nove, oito_nove, vinte, oito_vinte, nove_vinte, meio), set_labels = ('2018','2019', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]

                if 2017 in anos and 2019 in anos and 2020 in anos:
                        v = vplt.venn3(subsets=(sete, nove, sete_nove, vinte, sete_vinte, nove_vinte, meio), set_labels = ('2017','2019', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]


                if 2017 in anos and 2018 in anos:
                        v = vplt.venn2(subsets={'10': sete, '01': oito, '11': sete_oito}, set_labels = ('2017', '2018'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                if 2017 in anos and 2019 in anos:
                        v = vplt.venn2(subsets={'10': sete, '01': nove, '11': sete_nove}, set_labels = ('2017', '2019'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                if 2018 in anos and 2019 in anos:
                        v = vplt.venn2(subsets={'10': oito, '01': nove, '11': oito_nove}, set_labels = ('2018', '2019'))
                        plt.savefig('Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                 
                if 2017 in anos and 2020 in anos:
                        v = vplt.venn2(subsets={'10': sete, '01': vinte, '11': sete_vinte}, set_labels = ('2017', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                 
                 
                if 2018 in anos and 2020 in anos:
                        v = vplt.venn2(subsets={'10': oito, '01': vinte, '11': oito_vinte}, set_labels = ('2018', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                 
                if 2019 in anos and 2020 in anos:
                        v = vplt.venn2(subsets={'10': nove, '01': vinte, '11': nove_vinte}, set_labels = ('2019', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]


        elif abas == 'aba-2':
                df_rel = (pd.read_csv('Apoio/evolucao_docentes.csv').sort_values(by=str(anos[0]))) if len(anos) == 1 else pd.read_csv('Apoio/evolucao_docentes.csv')

                agraf_rel = make_subplots(rows=1, cols=1,row_titles = ['Quantidade de Docentes'],  shared_yaxes=True)
                if 2017 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2017'].to_list(), name='2017', text=df_rel[df_rel['centro'].isin(centros)]['2017'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2018 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2018'].to_list(), name='2018', text=df_rel[df_rel['centro'].isin(centros)]['2018'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2019 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2019'].to_list(), name='2019', text=df_rel[df_rel['centro'].isin(centros)]['2019'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2020 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2020'].to_list(), name='2020', text=df_rel[df_rel['centro'].isin(centros)]['2020'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                agraf_rel.update_layout(height=600)
                return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph(figure=agraf_rel)]
                                    
        elif abas == 'aba-3':
                df_rel = (pd.read_csv('Apoio/relacao_docente_projeto.csv').sort_values(by=str(anos[0]))) if len(anos) == 1 else pd.read_csv('Apoio/relacao_docente_projeto.csv')

                agraf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Docente/Projeto'],  shared_yaxes=True)
                if 2017 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2017'].to_list(), name='2017', text=df_rel[df_rel['centro'].isin(centros)]['2017'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2018 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2018'].to_list(), name='2018', text=df_rel[df_rel['centro'].isin(centros)]['2018'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2019 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2019'].to_list(), name='2019', text=df_rel[df_rel['centro'].isin(centros)]['2019'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2020 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2020'].to_list(), name='2020', text=df_rel[df_rel['centro'].isin(centros)]['2020'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                agraf_rel.update_layout(height=600)
                return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph(figure=agraf_rel)]
        elif abas == 'aba-4':
                df_rel = pd.read_csv('Apoio/doc-pro.csv')
                agraf_rel = make_subplots(rows=1, cols=1,  shared_yaxes=True)
                for an in anos:
                        agraf_rel.add_trace(go.Scatter(x=df_rel[(df_rel['ano']==an)&(df_rel['centros'].isin(centros))].groupby(['projetos'])['docentes'].sum().reset_index(level=0)['projetos'].to_list(), y=df_rel[(df_rel['ano']==an)&(df_rel['centros'].isin(centros))].groupby(['projetos'])['docentes'].sum().reset_index(level=0)['docentes'].to_list(), name=str(an), mode='markers'),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                agraf_rel.update_layout(go.Layout(yaxis={'title':'Numero de Projetos'},xaxis={'title': 'Quantidade de Docentes'}))
                venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                agraf_rel.update_layout(height=600)
                return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph(figure=agraf_rel)]





@app.callback(
	[Output("centros", "value"),Output("modal", "is_open")],
	[Input("anos", "value"), Input("close", "n_clicks")],
	[State("centros", "value"),State("modal", "is_open")],

)
def limite_centros(anos,n2, centros,is_open):
	if 'Todos os centros' in centros:
		return [['CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ'],is_open]
	if len(centros) == 0:
		return [['CEAR'], not is_open]
	else:
		if n2:
			if is_open == True:
				return [centros, not is_open]
			return [centros, is_open]
		return [centros, is_open]


@app.callback(
	[Output("anos", "value"),Output("modal_2", "is_open"),Output("modal_3a", "is_open")],
	[Input("centros", "value"),Input("close_2", "n_clicks"),Input("close_3a", "n_clicks"),Input("aba-example","value")],
	[State("anos", "value"),State("modal_2", "is_open"),State("modal_3a", "is_open")],

)

def flag(centros,n2,n3, abas, anos, is_open,is_open2):
	if len(anos) > 3:
		if abas != 'aba-1':
			return [anos,is_open,is_open2]
		return [[2018,2019,2029],is_open,not is_open2]
	if len(anos) < 2:
		if abas != 'aba-1':
			return [anos,is_open,is_open2]

		return [[2018,2019], not is_open,is_open2]
	else:
		if n3:
			if is_open2 == True:
				return [anos,is_open, not is_open2]
			return [anos, is_open,is_open2]
		if n2:

			if is_open == True:
				return [anos, not is_open,is_open2]
			return [anos, is_open,is_open2]
		return [anos, is_open,is_open2]


@app.callback(
	Output("relatorio_docentes", "children"),
	[Input("centros", "value"),Input("anos", "value"),Input("aba-example","value")]

)
def relatorio_docentes(centros,anos, abas):
	if abas == 'aba-1':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é uma análise de variabilidade, a fim de visualizar a quantidade de professores e alunos que 
		trabalharam em projetos de extensão apenas no ano de {anos}, bem como suas respectivas intersecções. Podemos
		analisar que, como escolhido, está sendo filtrado em apenas os centros: {centros} para serem visualizados.
		Esses dados foram representados pelo diagrama de Venn.'''
	if abas == 'aba-2':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é o evolutivo dos docentes por centro, a fim de visualizar o envolvimento dos docentes 
		em projetos de extensão nos anos de {anos}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
		os centros: {centros} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
		analisar os centros que atraem mais docentes para projetos de estensão e nos permite fazer um comparativo com os outros centros.'''
	if abas == 'aba-3':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é a relação entre Docentes/Projeto, a fim de visualizar o envolvimento dos docentes 
		em projetos de extensão nos anos de {anos}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
		os centros: {centros} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
		analisar os centros que possuem a maior média de docentes por projetos.'''
	if abas == 'aba-4':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é a relação entre Docentes/Projeto, a fim de visualizar a quantidade de projetos que possuem apenas um docente,
                                dois docentes e assim sucessivamente, 
				nos anos de {anos}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
				os centros: {centros} para serem visualizados. Esses dados foram representados em um grafico de dispersão. Com esses resultados pode-se 
				analisar os projetos que possuem mais docentes.'''

        

@app.callback(
	Output("card_doc", "children"),
	[Input("aba-example","value")]
)

def graf_tit(abas):
        if abas == 'aba-1':
                return 'Gráfico de Variabilidade de Docentes'
        elif abas == 'aba-2':
                return 'Gráfico Evolutivo de Docentes por Centro'
        elif abas == 'aba-3':
                return 'Gráfico da Media de Docentes por Centro'
        elif abas == 'aba-4':
                return 'Gráfico da Relação Docente/Projeto'




###DOCENTES###

@app.callback(
	Output("popover", "is_open"),
	[Input("popover_target", "n_clicks")],
	[State("popover", "is_open")],
)
def toggle_popover(n, is_open):
	if n:
		return not is_open
	return is_open


###relacao###
###DISCENTES###
@app.callback(
	Output("graph_discentes", "children"),
	[Input("centro", "value"),
	Input("ano", "value"), Input("tabs-example","value")],
)
def update_graph_discentes(centro, ano, tab):
    if tab == 'tab-1':        
        df_rel = (pd.read_csv("Apoio/relacao_novo.csv").sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv("Apoio/relacao_novo.csv")
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Professores'],  shared_yaxes=True)
        for a in ano: 
            graf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centro)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), name=str(a), text=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), textposition='auto',),1,1)
            graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
            graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        graf_rel.update_layout(yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 0.5))
        return dcc.Graph(figure=graf_rel)
    elif tab == 'tab-2':
        df_rel = (pd.read_csv('Apoio/evo.csv').sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv('Apoio/evo.csv')
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Quantidade de Discentes'],  shared_yaxes=True)
        for a in ano:
                graf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centro)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), name=str(a), text=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), textposition='auto',),1,1)
                graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        return dcc.Graph(figure=graf_rel)
    elif tab == 'tab-3':
        df_rel = (pd.read_csv('Apoio/rel_dis_pro.csv').sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv('Apoio/rel_dis_pro.csv')
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Projeto'],  shared_yaxes=True)
        for a in ano:
                graf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centro)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), name=str(a), text=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), textposition='auto',),1,1)
                graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        return dcc.Graph(figure=graf_rel)
    elif tab == 'tab-4':
        df_rel = pd.read_csv('Apoio/dis-pro.csv')
        graf_rel = make_subplots(rows=1, cols=1,  shared_yaxes=True)
        for a in ano:
                graf_rel.add_trace(go.Scatter(x=df_rel[(df_rel['ano']==a)&(df_rel['centros'].isin(centro))].groupby(['projetos'])['discentes'].sum().reset_index(level=0)['projetos'].to_list(), y=df_rel[(df_rel['ano']==a)&(df_rel['centros'].isin(centro))].groupby(['projetos'])['discentes'].sum().reset_index(level=0)['discentes'].to_list(), name=str(a), mode='markers'),1,1)
                graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
        graf_rel.update_layout(go.Layout(yaxis={'title':'Numero de Projetos'},xaxis={'title': 'Quantidade de discentes'}))
        return dcc.Graph(figure=graf_rel)




            
	 
@app.callback(
	[Output("centro", "value"),Output("modal_3", "is_open")],
	[Input("ano", "value"), Input("close_3", "n_clicks")],
	[State("centro", "value"),State("modal_3", "is_open")],

)
def limite_centros(ano,n_rel, centro,is_open_rel):
	if 'Todos os centros' in centro:
		return [['CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ'],is_open_rel]
	if len(centro) == 0:
		return [['CEAR'], not is_open_rel]
	else:
		if n_rel:
			if is_open_rel == True:
				return [centro, not is_open_rel]
			return [centro, is_open_rel]
		return [centro, is_open_rel]



@app.callback(
	[Output("ano", "value"),Output("modal_4", "is_open")],
	[Input("centro", "value"),Input("close_4", "n_clicks")],
	[State("ano", "value"),State("modal_4", "is_open")],

)

def flag(centro,n_rel, ano, is_open_rel):
        if 'Todos os anos' in ano:
                return [[2017,2018,2019,2020],is_open_rel]
        if len(ano) == 0:
                return [[2020], not is_open_rel]
        else:
                if n_rel:
                        if is_open_rel == True:
                                return [ano, not is_open_rel]
                        return [ano, is_open_rel]
                return [ano, is_open_rel]



@app.callback(
	Output("relatorio_discentes", "children"),
	[Input("centro", "value"),Input("ano", "value"),
         Input("tabs-example","value")]

)

def relatorio_discentes(centro,ano,tab):
        centro=", ".join(str(x) for x in centro)
        ano=", ".join(str(x) for x in sorted(ano))
        if tab == 'tab-1':
                return f'''O gráfico analisado é a relação entre Discentes/Docentes, a fim de visualizar o envolvimento dos discentes 
                                em projetos de extensão nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                                analisar os centros que possuem mais docentes que discentes, quando os valores obtidos forem menores que 1, e os que possuem 
                                mais alunos que professores, para valores maiores que 1.'''
        elif tab == 'tab-2':
                return f'''O gráfico analisado é o evolutivo dos discentes por centro, a fim de visualizar o envolvimento dos discentes 
                                em projetos de extensão nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                                analisar os centros que atraem mais alunos para projetos de estensão e nos permite fazer um comparativo com os outros centros.'''
        elif tab == 'tab-3':
                return f'''O gráfico analisado é a relação entre Discentes/Projeto, a fim de visualizar o envolvimento dos discentes 
                                em projetos de extensão nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                                analisar os centros que possuem a maior média de discentes por projetos.'''
        elif tab == 'tab-4':
                return f'''O gráfico analisado é a relação entre Discentes/Projeto, a fim de visualizar a quantidade de projetos que possuem apenas um discente,
                                dois discentes e assim sucessivamente, 
                                nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de dispersão. Com esses resultados pode-se 
                                analisar os projetos que possuem mais discentes envolvidos.'''

        
        

@app.callback(
	Output("card", "children"),
	[Input("tabs-example","value")]
)

def graf_tit(tab):
        if tab == 'tab-1':
                return 'Gráfico da Relação de Discentes/Docentes por Centro'
        elif tab == 'tab-2':
                return 'Gráfico Evolutivo de Discentes por Centro'
        elif tab == 'tab-3':
                return 'Gráfico da Media de Discentes por Centro'
        elif tab == 'tab-4':
                return 'Gráfico da Relação de Discentes/Projeto por Centro'





####################Variação Vocabular

@app.callback(
	Output("checklist_centros_variacao", "value"),
	[Input("dropdown_centros_variacao","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''

@app.callback(
	Output("checklist_anos_variacao", "value"),
	[Input("dropdown_anos_variacao","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'ta'
	else:
		return ''


@app.callback(
	Output("checklist_classes_analise", "value"),
	[Input("dropdown_classes_analise","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''

@app.callback(
	Output("checklist_centros_analise", "value"),
	[Input("dropdown_centros_analise","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''


@app.callback(
	Output("checklist_anos_nuvem", "value"),
	[Input("dropdown_anos_nuvem","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'ta'
	else:
		return ''




@app.callback(
	Output("checklist_centros_nuvem", "value"),
	[Input("dropdown_centros_nuvem","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''




@app.callback(
	Output("checklist_anos_contagem", "value"),
	[Input("dropdown_anos_contagem","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'ta'
	else:
		return ''

@app.callback(
	Output("checklist_centros_contagem", "value"),
	[Input("dropdown_centros_contagem","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''






@app.callback(
	Output("grafico_variacao_vocabular", "children"),
	[Input("dropdown_anos_variacao", "value"),
	Input("dropdown_centros_variacao", "value"),
	Input("dropdown_modalidades_variacao", "value"),
	Input("tab_escolha_grafico","value")] #######################
)
def update_grafico_variacao_vocabular(dropdown_anos_variacao, dropdown_centros_variacao, dropdown_modalidades_variacao, tab_escolha_grafico):
   
	#return tab_escolha_grafico (variabilidade_vocabular e analise_gramatical)
	if tab_escolha_grafico == "variabilidade_vocabular":

		if('Resumo' in dropdown_modalidades_variacao):
			informacao = "Resumos"
		if('Justificativa' in dropdown_modalidades_variacao):
			informacao = "Justificativas" 
		if('Metodologia' in dropdown_modalidades_variacao):
			informacao = "Metodologias"   

		if('Fundamentacao' in dropdown_modalidades_variacao):
			informacao = "Fundamentacões Teóricas" 

		if('Objetivo' in dropdown_modalidades_variacao):
			informacao = "Objetivos"  

		#########################
		if(tab_escolha_grafico == "variabilidade_vocabular"):
			if(informacao == "Resumos"):    
				df_resumo_2017 = pd.read_csv('Apoio/Dataframes/df_resumo_2017.csv')
				df_resumo_2018 = pd.read_csv('Apoio/Dataframes/df_resumo_2018.csv')
				df_resumo_2019 = pd.read_csv('Apoio/Dataframes/df_resumo_2019.csv')

			elif(informacao == "Justificativas"):   
				df_resumo_2017 = pd.read_csv('Apoio/Dataframes/justificativa_2017.csv')
				df_resumo_2018 = pd.read_csv('Apoio/Dataframes/justificativa_2018.csv')
				df_resumo_2019 = pd.read_csv('Apoio/Dataframes/justificativa_2019.csv')

			elif(informacao == "Metodologias"):
				df_resumo_2017 = pd.read_csv('Apoio/Dataframes/metodologia_2017.csv')
				df_resumo_2018 = pd.read_csv('Apoio/Dataframes/metodologia_2018.csv')
				df_resumo_2019 = pd.read_csv('Apoio/Dataframes/metodologia_2019.csv')

			elif(informacao == "Fundamentacões Teóricas"):   
				df_resumo_2017 = pd.read_csv('Apoio/Dataframes/fundamentacao_2017.csv')
				df_resumo_2018 = pd.read_csv('Apoio/Dataframes/fundamentacao_2018.csv')
				df_resumo_2019 = pd.read_csv('Apoio/Dataframes/fundamentacao_2019.csv')

			elif(informacao == "Objetivos"):
				df_resumo_2017 = pd.read_csv('Apoio/Dataframes/objetivo_2017.csv')
				df_resumo_2018 = pd.read_csv('Apoio/Dataframes/objetivo_2018.csv')
				df_resumo_2019 = pd.read_csv('Apoio/Dataframes/objetivo_2019.csv')

			else:
				informacao = "Resumos"    
				df_resumo_2017 = pd.read_csv('Apoio/Dataframes/df_resumo_2017.csv')
				df_resumo_2018 = pd.read_csv('Apoio/Dataframes/df_resumo_2018.csv')
				df_resumo_2019 = pd.read_csv('Apoio/Dataframes/df_resumo_2019.csv')

		else:
			None
		
		
		tamanho_anos = [0]
		df_resumos = [0,0,0]
		df_resumos[0] = df_resumo_2017
		df_resumos[1] = df_resumo_2018
		df_resumos[2] = df_resumo_2019
		df_consulta = [0,0,0]
		centros_variacao = []
		qtd_palavras_2017 =[]
		qtd_palavras_2018 =[]
		qtd_palavras_2019 =[]
		anos = '0'

		if ('2017' in dropdown_anos_variacao and '2018' in dropdown_anos_variacao and '2019' in dropdown_anos_variacao):
			df_consulta.clear()
			centros_variacao.clear()
			tamanho_anos.clear()
			qtd_palavras_2017.clear()
			qtd_palavras_2018.clear()
			qtd_palavras_2019.clear()
			anos = '2017,2018 e 2019'

			df_consulta.append(df_resumo_2017.loc['PALAVRAS'])
			df_consulta.append(df_resumo_2018.loc['PALAVRAS'])
			df_consulta.append(df_resumo_2019.loc['PALAVRAS'])
			tamanho_anos.append(3)
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)

			####
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2017.append(df_resumo_2017.loc['PALAVRAS'][i])
				
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2018.append(df_resumo_2018.loc['PALAVRAS'][i])
				
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2019.append(df_resumo_2019.loc['PALAVRAS'][i])

			
		elif ('2017' in dropdown_anos_variacao and '2018' in dropdown_anos_variacao):
			df_consulta.clear()
			centros_variacao.clear()
			tamanho_anos.clear()
			qtd_palavras_2017.clear()
			qtd_palavras_2018.clear()
			qtd_palavras_2019.clear()
			anos = '2017 e 2018'

			df_consulta.append(df_resumo_2017.loc['PALAVRAS'])
			df_consulta.append(df_resumo_2018.loc['PALAVRAS'])
			tamanho_anos.append(2)
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)

			####
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2017.append(df_resumo_2017.loc['PALAVRAS'][i])

			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2018.append(df_resumo_2018.loc['PALAVRAS'][i])
					

		elif ('2017' in dropdown_anos_variacao and '2019' in dropdown_anos_variacao):
			df_consulta.clear()
			centros_variacao.clear()
			tamanho_anos.clear()
			qtd_palavras_2017.clear()
			qtd_palavras_2018.clear()
			qtd_palavras_2019.clear()
			anos = '2017 e 2019'
			
			df_consulta.append(df_resumo_2017.loc['PALAVRAS'])
			df_consulta.append(df_resumo_2019.loc['PALAVRAS'])
			tamanho_anos.append(2)
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)

			####
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2017.append(df_resumo_2017.loc['PALAVRAS'][i])

			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2018.append(df_resumo_2019.loc['PALAVRAS'][i])
					
					

		elif ('2018' in dropdown_anos_variacao and '2019' in dropdown_anos_variacao):
			df_consulta.clear()
			centros_variacao.clear()
			tamanho_anos.clear()
			qtd_palavras_2017.clear()
			qtd_palavras_2018.clear()
			qtd_palavras_2019.clear()
			anos = '2018 e 2019'

			df_consulta.append(df_resumo_2018.loc['PALAVRAS'])
			df_consulta.append(df_resumo_2019.loc['PALAVRAS'])
			tamanho_anos.append(2)
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)

			####
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2017.append(df_resumo_2018.loc['PALAVRAS'][i])

			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2018.append(df_resumo_2019.loc['PALAVRAS'][i])
					
			

		elif ('2017' in dropdown_anos_variacao):
			df_consulta.clear()
			centros_variacao.clear()
			tamanho_anos.clear()
			qtd_palavras_2017.clear()
			qtd_palavras_2018.clear()
			qtd_palavras_2019.clear()
			anos = '2017'

			df_consulta.append(df_resumo_2017.loc['PALAVRAS'])
			tamanho_anos.append(1)
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)

			####		
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2017.append(df_resumo_2017.loc['PALAVRAS'][i])

		elif ('2018' in dropdown_anos_variacao):
			df_consulta.clear()
			centros_variacao.clear()
			tamanho_anos.clear()
			qtd_palavras_2017.clear()
			qtd_palavras_2018.clear()
			qtd_palavras_2019.clear()
			anos = '2018'

			df_consulta.append(df_resumo_2017.loc['PALAVRAS'])
			tamanho_anos.append(1)
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)

			####		
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2017.append(df_resumo_2018.loc['PALAVRAS'][i])
			

		elif ('2019' in dropdown_anos_variacao):
			df_consulta.clear()
			centros_variacao.clear()
			tamanho_anos.clear()
			qtd_palavras_2017.clear()
			qtd_palavras_2018.clear()
			qtd_palavras_2019.clear()
			anos = '2019'

			df_consulta.append(df_resumo_2017.loc['PALAVRAS'])
			tamanho_anos.append(1)
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					
			####
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2017.append(df_resumo_2019.loc['PALAVRAS'][i])
					
					
		for j,i in enumerate(centros_variacao):
			centros_variacao[j] = i.split(' -')[0]
			   
		if(tamanho_anos[0] == 1):
			dc_total_2017 = dict(zip(centros_variacao,qtd_palavras_2017)) #Ordena do menor para o maior
			dc_total_2017 = dict(sorted(dc_total_2017.items(), key=itemgetter(1)))
			df_total_2017 = pd.DataFrame(data=dc_total_2017,index=['PALAVRAS'])
			x=df_total_2017.columns.to_list()
			y = df_total_2017.loc['PALAVRAS']
		
		
			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x , 'y': y, 'type': 'bar', 'name': anos},
					],
					'layout': {
						'title': 'Gráfico da Variabilidade Vocabular por Centro - {} - ({})'.format(informacao, anos)
					}
				})
				
		if(tamanho_anos[0] == 2):
			dc_total_2017 = dict(zip(centros_variacao,qtd_palavras_2017)) #Ordena do menor para o maior
			dc_total_2017 = dict(sorted(dc_total_2017.items(), key=itemgetter(1)))
			df_total_2017 = pd.DataFrame(data=dc_total_2017,index=['PALAVRAS'])
			x=df_total_2017.columns.to_list()
			y = df_total_2017.loc['PALAVRAS']

			dc_total_2018 = dict(zip(centros_variacao,qtd_palavras_2018)) #Ordena do menor para o maior
			dc_total_2018 = dict(sorted(dc_total_2018.items(), key=itemgetter(1)))
			df_total_2018 = pd.DataFrame(data=dc_total_2018,index=['PALAVRAS'])
			x_2018=df_total_2018.columns.to_list()
			y_2018 = df_total_2018.loc['PALAVRAS']
		
		
			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x , 'y': y, 'type': 'bar', 'name': anos.split('e')[0]},
						{'x': x_2018 , 'y': y_2018, 'type': 'bar', 'name': str(anos.split('e')[1]).split(" ")[1] }

					],
				'layout': {
					'title': 'Gráfico da Variabilidade Vocabular por Centro - {} - ({})'.format(informacao, anos)
				}
				})
				
				
		if(tamanho_anos[0] == 3):
			dc_total_2017 = dict(zip(centros_variacao,qtd_palavras_2017)) #Ordena do menor para o maior
			dc_total_2017 = dict(sorted(dc_total_2017.items(), key=itemgetter(1)))
			df_total_2017 = pd.DataFrame(data=dc_total_2017,index=['PALAVRAS'])
			x=df_total_2017.columns.to_list()
			y = df_total_2017.loc['PALAVRAS']
			   
			dc_total_2018 = dict(zip(centros_variacao,qtd_palavras_2018)) #Ordena do menor para o maior
			dc_total_2018 = dict(sorted(dc_total_2018.items(), key=itemgetter(1)))
			df_total_2018 = pd.DataFrame(data=dc_total_2018,index=['PALAVRAS'])
			x_2018=df_total_2018.columns.to_list()
			y_2018 = df_total_2018.loc['PALAVRAS']

			dc_total_2019 = dict(zip(centros_variacao,qtd_palavras_2019)) #Ordena do menor para o maior
			dc_total_2019 = dict(sorted(dc_total_2019.items(), key=itemgetter(1)))
			df_total_2019 = pd.DataFrame(data=dc_total_2019,index=['PALAVRAS'])
			x_2019=df_total_2019.columns.to_list()
			y_2019 = df_total_2019.loc['PALAVRAS']
		
			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x , 'y': y, 'type': 'bar', 'name': anos.split(',')[0]},
						{'x': x_2018 , 'y': y_2018, 'type': 'bar', 'name': str(anos.split(',')[1]).split('e')[0]},
						{'x': x_2019 , 'y': y_2019, 'type': 'bar', 'name': str(anos.split('e')[1]).split(" ")[1]}
					],
			'layout': {
				'title': 'Gráfico da Variabilidade Vocabular por Centro - {} - ({})'.format(informacao, anos)
				}
			})

		
			
@app.callback(
	Output("dropdown_anos_variacao","value"),
	[Input("checklist_anos_variacao", "value")],[State("dropdown_anos_variacao", "value")]

)
def retornar_anos_dropdown(value,estado):
	print(value)
	if('ta' in value):
		return ["2017", "2018", "2019"]
	else:
		return estado
		


@app.callback(
	Output("dropdown_centros_variacao","value"),
	[Input("checklist_centros_variacao", "value")],[State("dropdown_centros_variacao", "value")]
)
def retornar_anos_dropdown(value,estado):
	if('tc' in value):
		return ListaCentros_variacao[1:]
	else:
		return estado


########################
######################
#######################
################
#Agora para as classes gramaticais



		
@app.callback(
	Output("grafico_analise_gramatical", "children"), #o gráfico independe dos cards
	[Input("dropdown_classes_analise", "value"),
	Input("dropdown_centros_analise", "value"),
	Input("dropdown_modalidades_analise", "value"),
	Input("tab_escolha_grafico","value")] #######################
)
def update_grafico_analise_vocabular(dropdown_classes_analise, dropdown_centros_analise, dropdown_modalidades_analise, tab_escolha_grafico):
	if tab_escolha_grafico == "analise_gramatical":
		informacao = []
		informacao.clear()
		if('Substantivos' in dropdown_classes_analise):
			informacao.append("Substantivos")
		if('Adjetivos' in dropdown_classes_analise):
			informacao.append("Adjetivos") 
		if('Verbos' in dropdown_classes_analise):
			informacao.append("Verbos")   
		#####Funcionando

		#########################
		if("Substantivos" in informacao and "Adjetivos" in informacao and "Verbos" in informacao):
			cont = 3
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_resumo.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_resumo.csv')
				df3 = pd.read_csv('Apoio/Dataframes/verbos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_justificativa.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_justificativa.csv')
				df3 = pd.read_csv('Apoio/Dataframes/verbos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_metodologia.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_metodologia.csv')
				df3 = pd.read_csv('Apoio/Dataframes/verbos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_fundamentacao.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_fundamentacao.csv')
				df3 = pd.read_csv('Apoio/Dataframes/verbos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_objetivos.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_objetivos.csv')
				df3 = pd.read_csv('Apoio/Dataframes/verbos_objetivos.csv')
				info = "Objetivo"

		elif("Substantivos" in informacao and "Adjetivos" in informacao):
			cont = 2
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_resumo.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_justificativa.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_metodologia.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_fundamentacao.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_objetivos.csv')
				df2 = pd.read_csv('Apoio/Dataframes/adjetivos_objetivos.csv')
				info = "Objetivo"


		elif("Substantivos" in informacao and "Verbos" in informacao):
			cont =2
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_resumo.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_justificativa.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_metodologia.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_fundamentacao.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_objetivos.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_objetivos.csv')
				info = "Objetivo"

		elif("Adjetivos" in informacao and "Verbos" in informacao):
			cont =2
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_resumo.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_justificativa.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_metodologia.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_fundamentacao.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_objetivos.csv')
				df2 = pd.read_csv('Apoio/Dataframes/verbos_objetivos.csv')
				info = "Objetivo"

		elif("Substantivos" in informacao):
			cont = 1
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/substantivos_objetivos.csv')
				info = "Objetivo"

		elif("Adjetivos" in informacao):
			cont = 1
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivos" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/adjetivos_objetivos.csv')
				info = "Objetivo"

		elif("Verbos" in informacao):
			cont = 1
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/verbos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/verbos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/verbos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/verbos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('Apoio/Dataframes/verbos_objetivos.csv')
				info = "Objetivo"	
		#####Tudo ok, agora fazendo os gráficos

		centros_variacao = []
		df_consulta1 = []
		df_consulta2 = []
		df_consulta3 = []

		if(cont==1):
			for i in dropdown_centros_analise: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df1.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_analise:
					del centros_variacao[j]
					del df_consulta1[j]

		elif(cont==2):
			for i in dropdown_centros_analise: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df1.loc['PALAVRAS'][i])
					df_consulta2.append(df2.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_analise:
					del centros_variacao[j]
					del df_consulta1[j]
					del df_consulta2[j]

		elif(cont==3):
			for i in dropdown_centros_analise: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df1.loc['PALAVRAS'][i])
					df_consulta2.append(df2.loc['PALAVRAS'][i])
					df_consulta3.append(df3.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_analise:
					del centros_variacao[j]
					del df_consulta1[j]
					del df_consulta2[j]
					del df_consulta3[j]


		for j,i in enumerate(centros_variacao):
			centros_variacao[j] = i.split(' -')[0]


		if(cont == 1):
			dc_total1 = dict(zip(centros_variacao,df_consulta1)) #Ordena do menor para o maior
			dc_total1 = dict(sorted(dc_total1.items(), key=itemgetter(1)))
			df_total1 = pd.DataFrame(data=dc_total1,index=['PALAVRAS'])
			x1=df_total1.columns.to_list()
			y1 = df_total1.loc['PALAVRAS']
			   
		
			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x1 , 'y': y1, 'type': 'bar', 'name': "Nome qualquer"},
					],
			'layout': {
				'title': 'Gráfico da Análise Gramatical do(a) {} por Centro (média de 2017,2018 e 2019)'.format(info)
				}
			})


		if(cont == 2):
			dc_total1 = dict(zip(centros_variacao,df_consulta1)) #Ordena do menor para o maior
			dc_total1 = dict(sorted(dc_total1.items(), key=itemgetter(1)))
			df_total1 = pd.DataFrame(data=dc_total1,index=['PALAVRAS'])
			x1=df_total1.columns.to_list()
			y1 = df_total1.loc['PALAVRAS']

			dc_total2 = dict(zip(centros_variacao,df_consulta2)) #Ordena do menor para o maior
			dc_total2 = dict(sorted(dc_total2.items(), key=itemgetter(1)))
			df_total2 = pd.DataFrame(data=dc_total2,index=['PALAVRAS'])
			x2=df_total2.columns.to_list()
			y2 = df_total2.loc['PALAVRAS']

			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x1 , 'y': y1, 'type': 'bar', 'name': informacao[0]},
						{'x': x2 , 'y': y2, 'type': 'bar', 'name': informacao[1]},
					],
			'layout': {
				'title': 'Gráfico da Análise Gramatical do(a) {} por Centro (média de 2017,2018 e 2019)'.format(info)
		
				}
			})


		if(cont == 3):
			dc_total1 = dict(zip(centros_variacao,df_consulta1)) #Ordena do menor para o maior
			dc_total1 = dict(sorted(dc_total1.items(), key=itemgetter(1)))
			df_total1 = pd.DataFrame(data=dc_total1,index=['PALAVRAS'])
			x1=df_total1.columns.to_list()
			y1 = df_total1.loc['PALAVRAS']

			dc_total2 = dict(zip(centros_variacao,df_consulta2)) #Ordena do menor para o maior
			dc_total2 = dict(sorted(dc_total2.items(), key=itemgetter(1)))
			df_total2 = pd.DataFrame(data=dc_total2,index=['PALAVRAS'])
			x2=df_total2.columns.to_list()
			y2 = df_total2.loc['PALAVRAS']

			dc_total3 = dict(zip(centros_variacao,df_consulta3)) #Ordena do menor para o maior
			dc_total3 = dict(sorted(dc_total3.items(), key=itemgetter(1)))
			df_total3 = pd.DataFrame(data=dc_total3,index=['PALAVRAS'])
			x3=df_total3.columns.to_list()
			y3 = df_total3.loc['PALAVRAS']

			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x1 , 'y': y1, 'type': 'bar', 'name': informacao[0]},
						{'x': x2 , 'y': y2, 'type': 'bar', 'name': informacao[1]},
						{'x': x3 , 'y': y3, 'type': 'bar', 'name': informacao[2]},
					],
			'layout': {
				'title': 'Gráfico da Análise Gramatical do(a) {} por Centro (média de 2017,2018 e 2019)'.format(info)
				}
			})



@app.callback(
	Output("dropdown_classes_analise","value"),
	[Input("checklist_classes_analise", "value")],[State("dropdown_classes_analise", "value")]

)
def retornar_classes_dropdown(value,estado):
	if('tc' in value):
		return ["Substantivos", "Adjetivos", "Verbos"]
	else:
		return estado 

@app.callback(
	Output("dropdown_centros_analise","value"),
	[Input("checklist_centros_analise", "value")],[State("dropdown_centros_analise", "value")]
)
def retornar_centros_dropdown(value,estado):
	if('tc' in value):
		return ListaCentros_variacao[1:]
	else:
		return estado
	
	
##############Nuvem de Palavras
##############
##############

@app.callback(
	Output("texto_grafico_nuvem", "children"),
	[Input("tab_escolha_grafico","value")]
)

def graf_tit(tipo_grafico):
        if tipo_grafico == 'nuvem_palavras':
          return 'Nuvem de Palavras por Centro, Ano e Campo'

        elif tipo_grafico == 'variabilidade_vocabular':
          return 'Gráfico da Variabilidade Vocabular por Centro e Campo'

        elif tipo_grafico == 'analise_gramatical':
          return 'Gráfico da Análise Gramatical por Classe, Centro e Campo'

        elif tipo_grafico == 'contagem_palavras':
          return 'Contagem de Palavras por Ano'







@app.callback(
	Output("grafico_nuvem_palavras", "src"),
	[Input("dropdown_anos_nuvem", "value"),
	Input("dropdown_centros_nuvem", "value"),
	Input("tab_escolha_grafico","value"),
	Input("dropdown_modalidades_nuvem","value")] #######################
)
def update_grafico_variacao_vocabular(dropdown_anos_nuvem, dropdown_centros_nuvem, tab_escolha_grafico, dropdown_modalidades_nuvem):
	f= io.open("Apoio/stopwords_portugues.txt", "r", encoding="utf8") #Importando as stopwords
	stopwords_portuguese = []
	stopwords_portuguese = f.readlines()
	for j,i in enumerate(stopwords_portuguese):
		if(" \n" in i):
			stopwords_portuguese[j] = stopwords_portuguese[j].split(" \n")[0]
		elif("\n" in i):
			stopwords_portuguese[j] = stopwords_portuguese[j].split("\n")[0]


	if(tab_escolha_grafico == "nuvem_palavras"):
		if( "Resumo" in dropdown_modalidades_nuvem):
			info = "Resumo"
			df_2017 = pd.read_csv("Apoio/Dataframes/lista_palavras_resumo_2017.csv")
			df_2018 = pd.read_csv("Apoio/Dataframes/lista_palavras_resumo_2018.csv")
			df_2019 = pd.read_csv("Apoio/Dataframes/lista_palavras_resumo_2019.csv")

		elif( "Metodologia" in dropdown_modalidades_nuvem):
			info = "Metodologia"
			df_2017 = pd.read_csv("Apoio/Dataframes/lista_palavras_metodologia_2017.csv")
			df_2018 = pd.read_csv("Apoio/Dataframes/lista_palavras_metodologia_2018.csv")
			df_2019 = pd.read_csv("Apoio/Dataframes/lista_palavras_metodologia_2019.csv")

		elif( "Justificativa" in dropdown_modalidades_nuvem):
			info = "Justificativa"
			df_2017 = pd.read_csv("Apoio/Dataframes/lista_palavras_justificativa_2017.csv")
			df_2018 = pd.read_csv("Apoio/Dataframes/lista_palavras_justificativa_2018.csv")
			df_2019 = pd.read_csv("Apoio/Dataframes/lista_palavras_justificativa_2019.csv")

		elif( "Objetivo" in dropdown_modalidades_nuvem):
			info = "Objetivo"
			df_2017 = pd.read_csv("Apoio/Dataframes/lista_palavras_objetivo_2017.csv")
			df_2018 = pd.read_csv("Apoio/Dataframes/lista_palavras_objetivo_2018.csv")
			df_2019 = pd.read_csv("Apoio/Dataframes/lista_palavras_objetivo_2019.csv")

		elif("Fundamentacao" in dropdown_modalidades_nuvem):
			info = "Fundamentacão Teórica"
			df_2017 = pd.read_csv("Apoio/Dataframes/lista_palavras_fundamentacao_2017.csv")
			df_2018 = pd.read_csv("Apoio/Dataframes/lista_palavras_fundamentacao_2018.csv")
			df_2019 = pd.read_csv("Apoio/Dataframes/lista_palavras_fundamentacao_2019.csv")

		

		df_consulta1 = []
		df_consulta2 = []
		df_consulta3 = []
		centros_variacao = []
		texto = ""

		##Pegando os centros desejados
		if('2017' in dropdown_centros_nuvem and '2018' in dropdown_centros_nuvem and '2019' in dropdown_centros_nuvem):
			contador = 3
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df_2017.loc['PALAVRAS'][i])
					df_consulta2.append(df_2018.loc['PALAVRAS'][i])
					df_consulta3.append(df_2019.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_nuvem:
					del centros_variacao[j]
					del df_consulta1[j]
					del df_consulta2[j]
					del df_consulta3[j]


		elif('2017' in dropdown_centros_nuvem and '2018' in dropdown_centros_nuvem):
			contador = 2
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df_2017.loc['PALAVRAS'][i])
					df_consulta2.append(df_2018.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_nuvem:
					del centros_variacao[j]
					del df_consulta1[j]
					del df_consulta2[j]


		elif('2017' in dropdown_centros_nuvem and '2019' in dropdown_centros_nuvem):
			contador = 2
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df_2017.loc['PALAVRAS'][i])
					df_consulta2.append(df_2019.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_nuvem:
					del centros_variacao[j]
					del df_consulta1[j]
					del df_consulta2[j]

		elif('2018' in dropdown_centros_nuvem and '2019' in dropdown_centros_nuvem):
			contador = 2
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df_2018.loc['PALAVRAS'][i])
					df_consulta2.append(df_2019.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_nuvem:
					del centros_variacao[j]
					del df_consulta1[j]
					del df_consulta2[j]


		elif('2017' in dropdown_anos_nuvem):
			contador = 1
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df_2017.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_nuvem:
					del centros_variacao[j]
					del df_consulta1[j]


		elif('2018' in dropdown_anos_nuvem):
			contador  = 1
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df_2018.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_nuvem:
					del centros_variacao[j]
					del df_consulta1[j]


		elif('2019' in dropdown_anos_nuvem):
			contador = 1
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df_2019.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_nuvem:
					del centros_variacao[j]
					del df_consulta1[j]



		if(contador==1):
			texto_nuvem = ""
			for i in df_consulta1:
				texto_nuvem += i
			wordcloud = WordCloud(max_font_size=60, max_words=20, background_color="white", stopwords=stopwords_portuguese).generate(texto_nuvem)
			fig, ax = plt.subplots()
			ax.imshow(wordcloud, interpolation='bilinear')
			ax.set_axis_off()
			plt.savefig('Apoio/nuvem/nuvem.png')
			encoded_image = base64.b64encode(open("Apoio/nuvem/nuvem.png", 'rb').read())
			src='data:image/png;base64,{}'.format(encoded_image.decode())
			return src


		elif(contador==2):
			texto_nuvem = ""
			for i in df_consulta1:
				texto_nuvem += i

			for i in df_consulta2:
				texto_nuvem += i

			wordcloud = WordCloud(max_font_size=60, max_words=20, background_color="white", stopwords=stopwords_portuguese).generate(texto_nuvem)
			fig, ax = plt.subplots()
			ax.imshow(wordcloud, interpolation='bilinear')
			ax.set_axis_off()
			plt.savefig('Apoio/nuvem/nuvem.png')
			encoded_image = base64.b64encode(open("Apoio/nuvem/nuvem.png", 'rb').read())
			src='data:image/png;base64,{}'.format(encoded_image.decode())
			return src


		elif(contador==3):
			texto_nuvem = ""
			for i in df_consulta1:
				texto_nuvem += i

			for i in df_consulta2:
				texto_nuvem += i

			for i in df_consulta3:
				texto_nuvem += i

			wordcloud = WordCloud(max_font_size=60, max_words=20, background_color="white", stopwords=stopwords_portuguese).generate(texto_nuvem)
			fig, ax = plt.subplots()
			ax.imshow(wordcloud, interpolation='bilinear')
			ax.set_axis_off()
			plt.savefig('Apoio/nuvem/nuvem.png')
			encoded_image = base64.b64encode(open("Apoio/nuvem/nuvem.png", 'rb').read())
			src='data:image/png;base64,{}'.format(encoded_image.decode())
			return src

	else:
		image_filename = 'Apoio/nuvem/blank.png'
		encoded_image = base64.b64encode(open(image_filename, 'rb').read())
		src='data:image/png;base64,{}'.format(encoded_image.decode())
		return src



@app.callback(
	Output("dropdown_anos_nuvem","value"),
	[Input("checklist_anos_nuvem", "value")],[State("dropdown_anos_nuvem", "value")]

)
def retornar_anos_dropdown(value,estado):
	if('ta' in value):
		return ["2017", "2018", "2019"]
	else:
		return estado
		


@app.callback(
	Output("dropdown_centros_nuvem","value"),
	[Input("checklist_centros_nuvem", "value")],[State("dropdown_centros_nuvem", "value")]
)
def retornar_anos_dropdown(value,estado):
	if('tc' in value):
		return ListaCentros_variacao[1:]
	else:
		return estado	



 ##########Contagem Palavras
@app.callback(
	dash.dependencies.Output("grafico_contagem_palavras", "children"),
	[dash.dependencies.Input("dropdown_anos_contagem", "value"),
	dash.dependencies.Input("palavra_contagem", "value"),
	dash.dependencies.Input("dropdown_centros_contagem", "value"),
	dash.dependencies.Input("tab_escolha_grafico","value")] #######################
)
def grafico(dropdown_anos_contagem, palavra_contagem,dropdown_centros_contagem,tab_escolha_grafico):
	if tab_escolha_grafico == "contagem_palavras":
			centros_selecionados = []
			tamanho_anos = [0]
			anos = '0'
			palavras_input_ = str(palavra_contagem)
			palavras_input = palavras_input_.lower()
			palavras_input = und.unidecode(palavras_input)
			palavras = palavras_input.split(',')
	

			df_17= pd.read_csv('Apoio/dataset_2017.csv')
			df_18= pd.read_csv('Apoio/dataset_2018.csv')
			df_19= pd.read_csv('Apoio/dataset_2019.csv')


			if ('2017' in dropdown_anos_contagem and '2018' in dropdown_anos_contagem and '2019' in dropdown_anos_contagem):
					tamanho_anos.clear()
					anos = '2017,2018 e 2019'
					tamanho_anos.append(3)
					textos_2017 = pd.read_csv('Apoio/Dataframes/textos_contagem_2017.csv')
					textos_2018 = pd.read_csv('Apoio/Dataframes/textos_contagem_2018.csv')
					textos_2019 = pd.read_csv('Apoio/Dataframes/textos_contagem_2019.csv')

					normalizado_17 = []
					normalizado_18 = []
					normalizado_19 = []
					for i in Lista_Centros:
							text = list(textos_2017[i])
							text = ' '.join(text)
							text1 = list(textos_2018[i])
							text1 = ' '.join(text1)
							text2 = list(textos_2019[i])
							text2 = ' '.join(text2)
							encontrados_17 = []
							encontrados_18 = []
							encontrados_19 = []

							for n in range(0, len(palavras)):
									palavra = re.compile(palavras[n])
									p = palavra.findall(text)
									tam = len(p)
									p1 = palavra.findall(text1)
									tam1 = len(p1)
									p2 = palavra.findall(text2)
									tam2 = len(p2)
									encontrados_17.append(tam)
									encontrados_18.append(tam1)
									encontrados_19.append(tam2)
							total = sum(encontrados_17) # atribui o números de elementos da lista a uma variável
							total1 = sum(encontrados_18)
							total2 = sum(encontrados_19)
							quant = int(df_17[i])
							quant1 = int(df_18[i])
							quant2 = int(df_19[i])
							normalizado_17.append(total/quant)
							normalizado_18.append(total1/quant1)
							normalizado_19.append(total2/quant2)   
				  

			elif ('2017' in dropdown_anos_contagem and '2018' in dropdown_anos_contagem):
					tamanho_anos.clear()
					anos = '2017 e 2018'
					tamanho_anos.append(2)
					textos_2017 = pd.read_csv('Apoio/Dataframes/textos_contagem_2017.csv')
					textos_2018 = pd.read_csv('Apoio/Dataframes/textos_contagem_2018.csv')

					normalizado_17 = []
					normalizado_18 = []
					for i in Lista_Centros:
							text = list(textos_2017[i])
							text = ' '.join(text)
							text1 = list(textos_2018[i])
							text1 = ' '.join(text1)
							encontrados_17 = []
							encontrados_18 = []
							for n in range(0, len(palavras)):
									palavra = re.compile(palavras[n])
									p = palavra.findall(text)
									tam = len(p)
									p1 = palavra.findall(text1)
									tam1 = len(p1)
									encontrados_17.append(tam)
									encontrados_18.append(tam1)
							total = sum(encontrados_17) # atribui o números de elementos da lista a uma variável
							total1 = sum(encontrados_18)
							quant = int(df_17[i])
							quant1 = int(df_18[i])
							normalizado_17.append(total/quant)
							normalizado_18.append(total1/quant1)   
		
			
			elif ('2018' in dropdown_anos_contagem and '2019' in dropdown_anos_contagem):
					tamanho_anos.clear()
					anos = '2018 e 2019'
					tamanho_anos.append(2)
					textos_2018 = pd.read_csv('Apoio/Dataframes/textos_contagem_2018.csv')
					textos_2019 = pd.read_csv('Apoio/Dataframes/textos_contagem_2019.csv')

					normalizado_17 = []
					normalizado_18 = []
					for i in Lista_Centros:
							text = list(textos_2018[i])
							text = ' '.join(text)
							text1 = list(textos_2019[i])
							text1 = ' '.join(text1)
							encontrados_17 = []
							encontrados_18 = []
							for n in range(0, len(palavras)):
									palavra = re.compile(palavras[n])
									p = palavra.findall(text)
									tam = len(p)
									p1 = palavra.findall(text1)
									tam1 = len(p1)
									encontrados_17.append(tam)
									encontrados_18.append(tam1)
							total = sum(encontrados_17) # atribui o números de elementos da lista a uma variável
							total1 = sum(encontrados_18)
							quant = int(df_18[i])
							quant1 = int(df_19[i])
							normalizado_17.append(total/quant)
							normalizado_18.append(total1/quant1)   
			
							   
			
				
			elif ('2017' in dropdown_anos_contagem and '2019' in dropdown_anos_contagem):
					tamanho_anos.clear()
					anos = '2017 e 2019'
					tamanho_anos.append(2)
					textos_2017 = pd.read_csv('Apoio/Dataframes/textos_contagem_2017.csv')
					textos_2019 = pd.read_csv('Apoio/Dataframes/textos_contagem_2019.csv')

					normalizado_17 = []
					normalizado_18 = []
					for i in Lista_Centros:
							text = list(textos_2017[i])
							text = ' '.join(text)
							text1 = list(textos_2019[i])
							text1 = ' '.join(text1)
							encontrados_17 = []
							encontrados_18 = []
							for n in range(0, len(palavras)):
									palavra = re.compile(palavras[n])
									p = palavra.findall(text)
									tam = len(p)
									p1 = palavra.findall(text1)
									tam1 = len(p1)
									encontrados_17.append(tam)
									encontrados_18.append(tam1)
							total = sum(encontrados_17) # atribui o números de elementos da lista a uma variável
							total1 = sum(encontrados_18)
							quant = int(df_17[i])
							quant1 = int(df_19[i])
							normalizado_17.append(total/quant)
							normalizado_18.append(total1/quant1)   
				
				
				
			elif ('2017' in dropdown_anos_contagem ):
					tamanho_anos.clear()
					anos = '2017'
					tamanho_anos.append(1)
					textos_2017 = pd.read_csv('Apoio/Dataframes/textos_contagem_2017.csv')

					normalizado_17 = []
					for i in Lista_Centros:
							text = list(textos_2017[i])
							text = ' '.join(text)
							encontrados_17 = []
							for n in range(0, len(palavras)):
									palavra = re.compile(palavras[n])
									p = palavra.findall(text)
									tam = len(p)
									encontrados_17.append(tam)
							total = sum(encontrados_17)
							quant = int(df_17[i])
							normalizado_17.append(total/quant)    
			
			elif ('2018' in dropdown_anos_contagem ):
					tamanho_anos.clear()
					anos = '2018'
					tamanho_anos.append(1)
					textos_2018 = pd.read_csv('Apoio/Dataframes/textos_contagem_2018.csv')

					normalizado_17 = []
					for i in Lista_Centros:
							text = list(textos_2018[i])
							text = ' '.join(text)
							encontrados_17 = []
							for n in range(0, len(palavras)):
									palavra = re.compile(palavras[n])
									p = palavra.findall(text)
									tam = len(p)
									encontrados_17.append(tam)
							total = sum(encontrados_17)
							quant = int(df_18[i])
							normalizado_17.append(total/quant)    
			
				
			elif ('2019' in dropdown_anos_contagem ):
					tamanho_anos.clear()
					anos = '2019'
					tamanho_anos.append(1)
					textos_2019 = pd.read_csv('Apoio/Dataframes/textos_contagem_2019.csv')

					normalizado_17 = []
					for i in Lista_Centros:
							text = list(textos_2019[i])
							text = ' '.join(text)
							encontrados_17 = []
							for n in range(0, len(palavras)):
									palavra = re.compile(palavras[n])
									p = palavra.findall(text)
									tam = len(p)
									encontrados_17.append(tam)
							total = sum(encontrados_17)
							quant = int(df_19[i])
							normalizado_17.append(total/quant)    
			lista_centros = ['CCS','CEAR','CCEN','CT','CCM','CBIOTEC','CTDR','CCHLA','CCTA','CCHSA','CCSA','CI','CCAE','CCJ','CCA','CE']
			for i in dropdown_centros_contagem :
				if (i in Lista_Centros[0:]):
					centros_selecionados.append(i)
				else:
					None
			'''
			for j,i in enumerate(centros_selecionados):
				if i not in dropdown_centros_contagem :
					del centros_selecionados[j]
			print(centros_selecionados, flush = True)
			'''
			
				
			if(tamanho_anos[0] == 1):
					data = dict(zip(Lista_Centros,normalizado_17))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores = list(dataframe.loc['numero'])
					valores_arredondados = []
		 
					for j in valores:
							val = round(j,2)
							valores_arredondados.append(val)
					x = dataframe.columns.to_list()
					y = valores_arredondados
					return dcc.Graph(
							id='g1_contagem_palavras',
							figure={
									'data': [
											{'x': x , 'y': y, 'type': 'bar', 'name': anos},
											],
									'layout': {
											'title': 'Gráfico da quantidade das palavras - {} normalizadas por Centro - ({})'.format(palavras_input_, anos)
											}
									})
			elif(tamanho_anos[0] == 2):
					data = dict(zip(Lista_Centros,normalizado_17))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores = list(dataframe.loc['numero'])
					valores_arredondados = []
					for j in valores:
							val = round(j,2)
							valores_arredondados.append(val)
					x = dataframe.columns.to_list()
					y = valores_arredondados

					data2 = dict(zip(Lista_Centros,normalizado_18))
					data2 = dict(sorted(data2.items(),key=itemgetter(1)))
					dataframe2_ = pd.DataFrame(data = data2, index = ['numero'])
					dataframe2 = dataframe2_[centros_selecionados]
					valores2 = list(dataframe2.loc['numero'])
					valores_arredondados2 = []
					for j in valores2:
							val = round(j,2)
							valores_arredondados2.append(val)
					x2 = dataframe2.columns.to_list()
					y2 = valores_arredondados2

					return dcc.Graph(
							id='g1_contagem_palavras',
							figure={
									'data': [
											{'x': x , 'y': y, 'type': 'bar', 'name': anos.split('e')[0]},
											{'x': x2 , 'y': y2, 'type': 'bar', 'name':  str(anos.split('e')[1]).split(" ")[1]}
											],
									'layout': {
											'title': 'Gráfico da quantidade das palavras - {} normalizadas por Centro - ({})'.format(palavras_input_, anos)
											}
									})
			
			elif(tamanho_anos[0] == 3):

					data = dict(zip(Lista_Centros,normalizado_17))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores = list(dataframe.loc['numero'])
					valores_arredondados = []
					for j in valores:
							val = round(j,2)
							valores_arredondados.append(val)
					x = dataframe.columns.to_list()
					y = valores_arredondados


					data2 = dict(zip(Lista_Centros,normalizado_18))
					data2 = dict(sorted(data2.items(),key=itemgetter(1)))
					dataframe2_ = pd.DataFrame(data = data2, index = ['numero'])
					dataframe2 = dataframe2_[centros_selecionados]
					valores2 = list(dataframe2.loc['numero'])
					valores_arredondados2 = []
					for j in valores2:
							val = round(j,2)
							valores_arredondados2.append(val)
					x2 = dataframe2.columns.to_list()
					y2 = valores_arredondados2

					data3 = dict(zip(Lista_Centros,normalizado_19))
					data3 = dict(sorted(data3.items(),key=itemgetter(1)))
					dataframe3_ = pd.DataFrame(data = data3, index = ['numero'])
					dataframe3 = dataframe3_[centros_selecionados]
					valores3 = list(dataframe3.loc['numero'])
					valores_arredondados3 = []
					for j in valores3:
							val = round(j,2)
							valores_arredondados3.append(val)
					x3 = dataframe3.columns.to_list()
					y3 = valores_arredondados3

					return dcc.Graph(
							id='g1_contagem_palavras',
							figure={
									'data': [
											{'x': x , 'y': y, 'type': 'bar', 'name': anos.split(',')[0]},
											{'x': x2 , 'y': y2, 'type': 'bar', 'name': str(anos.split(',')[1]).split("e")[0]},
											{'x': x3 , 'y': y3, 'type': 'bar', 'name': str(anos.split('e')[1]).split(" ")[1]}
											],
									'layout': {
											'title': 'Gráfico da quantidade das palavras - {} normalizadas por Centro - ({})'.format(palavras_input_, anos)
											}
									})		
@app.callback(
	Output("dropdown_anos_contagem","value"),
	[Input("checklist_anos_contagem", "value")],[State("dropdown_anos_contagem", "value")]
)
def retornar_anos_dropdown(value,estado):
	if('ta' in value):
		return ["2017","2018","2019"]
	else:
		return estado

@app.callback(
	Output("dropdown_centros_contagem","value"),
	[Input("checklist_centros_contagem", "value")],[State("dropdown_centros_contagem", "value")]
)
def retornar_anos_dropdown(value,estado):
	if('tc' in value):
		return ['CCS','CEAR','CCEN','CT','CCM','CBIOTEC','CTDR','CCHLA','CCTA','CCHSA','CCSA','CI','CCAE','CCJ','CCA','CE']
	else:
		return estado

#Relatório dos Gráficos - Estudo Vocabular
@app.callback(
	Output("relatorio_estudo_vocabular","children"),
	[Input("tab_escolha_grafico", "value"),
	Input("dropdown_anos_variacao","value"),
	Input("dropdown_centros_variacao","value"),
	Input("dropdown_modalidades_variacao","value"),
	Input("dropdown_classes_analise","value"),
	Input("dropdown_centros_analise","value"),
	Input("dropdown_modalidades_analise","value"),
	Input("dropdown_anos_nuvem", "value"),
	Input("dropdown_centros_nuvem", "value"),
	Input("dropdown_modalidades_nuvem","value"),
	Input("dropdown_anos_contagem", "value"),
	Input("dropdown_centros_contagem", "value"),
	Input("palavra_contagem","value")],
)
def relatorio_estudo_vocabular(value, dropdown_anos_variacao, dropdown_centros_variacao, dropdown_modalidades_variacao, dropdown_classes_analise, dropdown_centros_analise,dropdown_modalidades_analise, dropdown_anos_nuvem, dropdown_centros_nuvem,dropdown_modalidades_nuvem,dropdown_anos_contagem,dropdown_centros_contagem, palavra_contagem):
	#######variação vocabular
	try:
		dropdown_anos_variacao = sorted(dropdown_anos_variacao)
		anos_variacao = ""
		for i in dropdown_anos_variacao:
		    if('2017' not in anos_variacao and '2018' not in anos_variacao and '2019' not in anos_variacao):
		        anos_variacao = anos_variacao + str(i)
		    else:
		        anos_variacao = anos_variacao + "," + str(i)

		centros_variacao = ""
		for i in dropdown_centros_variacao:
		    if('C' not in centros_variacao):
		        centros_variacao = centros_variacao + str(i.split(' -')[0])
		    else:
		        centros_variacao = centros_variacao + "," + str(i.split(' -')[0])

		campo_variacao = dropdown_modalidades_variacao
		if(campo_variacao == None):
			campo_variacao = ""
	######Análise Gramatical
	except:
		None

	try:	
		classes_analise = ""

		for i in dropdown_classes_analise:
			if(classes_analise != ''):
				classes_analise = classes_analise + "," +i
			else:
				classes_analise = classes_analise + i


		centros_analise =""
		for i in dropdown_centros_analise:
		    if('C' not in centros_analise):
		        centros_analise = centros_analise + str(i.split(' -')[0])
		    else:
		        centros_analise = centros_analise + "," + str(i.split(' -')[0])

		modalidades_analise = ""
		for i in dropdown_modalidades_analise:
			modalidades_analise += i

		if(modalidades_analise == None):
			modalidades_analise = ""

	except:
		None



	#Nuvem de Palavras
	try:
		anos_nuvem = ""
		for i in dropdown_anos_nuvem:
		    if('2017' not in anos_nuvem and '2018' not in anos_nuvem and '2019' not in anos_nuvem):
		        anos_nuvem = anos_nuvem + str(i)
		    else:
		        anos_nuvem = anos_nuvem + "," + str(i)

		centros_nuvem = ""
		for i in dropdown_centros_nuvem:
		    if('C' not in centros_nuvem):
		        centros_nuvem = centros_nuvem + str(i.split(' -')[0])
		    else:
		        centros_nuvem = centros_nuvem + "," + str(i.split(' -')[0])

		campo_nuvem = ""
		for i in dropdown_modalidades_nuvem:
			campo_nuvem += i

		if(campo_nuvem == None):
			campo_nuvem = ""


	#Contagem de Palavras

	except:
		None

	try:
		anos_contagem = ""
		for i in dropdown_anos_contagem:
		    if('2017' not in anos_contagem and '2018' not in anos_contagem and '2019' not in anos_contagem):
		        anos_contagem = anos_contagem + str(i)
		    else:
		        anos_contagem = anos_contagem + "," + str(i)


		centros_contagem = ""
		for i in dropdown_centros_contagem:
		    if('C' not in centros_contagem):
		        centros_contagem = centros_contagem + str(i.split(' -')[0])
		    else:
		        centros_contagem = centros_contagem + "," + str(i.split(' -')[0])

	except:
		None



			

	if value == 'variabilidade_vocabular':
		try:
			return f'''O Gráfico apresentado mostra a Varibilidade Vocabular dos projetos de extensão da UFPB por Centro(s), Ano(s) e Campo. A variabilidade vocabular consiste na quantidade média de palavras dos projetos dos centros escolhidos, isto é o total de palavras dividido pelo total de projetos considerados daquele centro. Nesse caso em específico, você está observando a Variabilidade Vocabular do(s) Ano(s): {anos_variacao}, no(s) Centro(s): {centros_variacao}, e no Campo {campo_variacao}'''
		except:
			return ""

	elif value == 'analise_gramatical' :
		try:
			return f'''O Gráfico apresentado mostra uma Análise Vocabular dos projetos de extensão da UFPB por Classe(s) de Palavra(s), Centro(s) e Campo. A análise gramatical consiste na quantidade média de elementos de uma determinada classe gramatical (a quantidade total daquela classe naquele centro dividida pela quantidade total de projetos daquele centro). Nesse caso em específico, você está observando uma Análise Gramatical da(s) classe(s): {classes_analise}, no(s) centro(s): {centros_analise}, e no campo {modalidades_analise}, considerando uma média dos anos de 2017, 2018 e 2019.'''
		except:
			return ""

	elif value == 'nuvem_palavras' :
		try:
			return f'''O gráfico apresentado mostra uma Nuvem de Palavras com as palavras mais relevantes de determinado(s) Centro(s) em determinado(s) Ano(s). A nuvem de palavras consiste nas 20 principais palavras dos centros escolhidos nos anos escolhidos, ou seja, se você escolheu mais de um centro em mais de um ano, todas as palavras foram consideradas para a confecção desta nuvem. Nesse caso em específico, você está observando a Nuvem de Palavras do(s) Ano(s): {anos_nuvem}, no(s) Centro(s): {centros_nuvem}, e no campo {campo_nuvem}'''
	
		except:
			return ""

	elif value == 'contagem_palavras':
		try:
			return f'''Este gráfico mostra o número de ocorrências das palavras pesquisadas normalizadas por centro, podendo nos apontar as tendências de área de envolvimento comparadas por centro. Os campos que foram levados em consideração para a contagem foram : Justificativa, Metodologia, Fundamentação Teórica e Objetivos. Nesse caso em específico, você está observando o gráfico referente a contagem da palavra "{palavra_contagem}", no(s) Ano(s) {anos_contagem}, e no(s) Centro(s): {centros_contagem}'''
		except:
			return ""
	else:
		return ""


###RAFAEL2###

def ins (r, s):
    ins_loc = r.index.max()
    if np.isnan(ins_loc):
        r.loc[0] = s
    else:
        r.loc[ins_loc + 1] = s

@app.callback(
        Output("area2", "options"),
        [Input("centro2", "value"), Input("ano2", "value")],
)

def op (centro, ano):
        print(ano)
        mb = pd.read_csv('Apoio/mb_area.csv')
        area = list(set(mb[(mb['a'].isin(centro))&(mb['ano'].isin(ano))]['area'].dropna()))
        area.insert(0, 'Todas as areas')
        if 0 in area:
                area.remove(0)
        area = [{'label': j, 'value': j} for j in area]
        return area



@app.callback(
	Output("graph_discentes2", "children"),
	[Input("centro2", "value"), Input("area2", "value"),
	Input("ano2", "value"), Input("tabs-example2","value"), Input('rafa2','style')],
)
def update_graph_discentes(centro, area, ano, tab, rafa2):
    if tab == 'tab2-1':
        z = pd.DataFrame()
        z2 = pd.DataFrame()
        mb = pd.read_csv('Apoio/mb_area.csv')
        pt = pd.read_csv('Apoio/pt_area.csv')
        for x in sorted(ano):
                z = pd.concat([mb[(mb['ano']==x)&(mb['a'].isin(centro))&(mb['area'].isin(area))].drop_duplicates(subset = ['id_pessoa']), z], ignore_index=True)
                z2 = pd.concat([pt[(pt['ano']==x)&(pt['a'].isin(centro))&(pt['area'].isin(area))].drop_duplicates(subset = ['id_discente_extensao']), z2], ignore_index=True)
        evo = pd.DataFrame(columns=['centro','ano','rel'])
        for i in centro:
                for x in ano:
                        b = []
                        b.append(i)
                        b.append(x)
                        if len(z[(z['ano']==x)&(z['a']==i)&(z['categoria_membro']=='DOCENTE')]['id_pessoa']) != 0:
                                if x == 2020:
                                        b.append(len(z2[(z2['ano']==x)&(z2['a']==i)]['id_discente_extensao'].unique())/len(z[(z['ano']==x)&(z['a']==i)&(z['categoria_membro']=='DOCENTE')]['id_pessoa'].unique()))
                                else:
                                        b.append((len(z[(z['ano']==x)&(z['a']==i)&(z['categoria_membro']=='DISCENTE')]['id_pessoa'].unique()))/len(z[(z['ano']==x)&(z['a']==i)&(z['categoria_membro']=='DOCENTE')]['id_pessoa'].unique()))
                        else:
                                b.append(0)
                        ins(evo, b)
        evo[['rel']] = evo[['rel']].applymap(lambda x : "%.2f" % x)
        evo = evo.sort_values(['ano', 'centro'])
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Professores'],  shared_yaxes=True)
        for a in ano: 
            graf_rel.add_trace(go.Bar(x=evo[evo['centro'].isin(centro)]['centro'].to_list(), y=evo[(evo['centro'].isin(centro))&(evo['ano']==a)]['rel'].to_list(), name=str(a), text=evo[(evo['centro'].isin(centro))&(evo['ano']==a)]['rel'].to_list(), textposition='auto',),1,1)
            graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
            graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        
        return dcc.Graph(figure=graf_rel)
    elif tab == 'tab2-2':
        z = pd.DataFrame()
        z2 = pd.DataFrame()
        mb = pd.read_csv('Apoio/mb_area.csv')
        pt = pd.read_csv('Apoio/pt_area.csv')
        for x in sorted(ano):
                z = pd.concat([mb[(mb['ano']==x)&(mb['a'].isin(centro))&(mb['area'].isin(area))].drop_duplicates(subset = ['id_pessoa']), z], ignore_index=True)
                z2 = pd.concat([pt[(pt['ano']==x)&(pt['a'].isin(centro))&(pt['area'].isin(area))].drop_duplicates(subset = ['id_discente_extensao']), z2], ignore_index=True)
        evo = pd.DataFrame(columns=['centro','ano','quant'])
        for i in centro:
                for x in sorted(ano):
                        b = []
                        b.append(i)
                        b.append(x)
                        if x == 2020:
                                b.append(len(z2[(z2['ano']==x)&(z2['a']==i)]['id_discente_extensao'].unique()))
                        else:
                                b.append((len(z[(z['ano']==x)&(z['a']==i)&(z['categoria_membro']=='DISCENTE')]['id_pessoa'].unique())))
                        ins(evo, b)
        evo = evo.sort_values(['ano', 'centro'])
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Quantidade de Discentes'],  shared_yaxes=True)
        for a in ano:
                graf_rel.add_trace(go.Bar(x=evo[evo['ano']==a]['centro'].to_list(), y=evo[evo['ano']==a]['quant'].to_list(), name=str(a), text=evo[evo['ano']==a]['quant'].to_list(), textposition='auto',),1,1)
                graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        return dcc.Graph(figure=graf_rel)
    elif tab == 'tab2-3':
        z = pd.DataFrame()
        z2 = pd.DataFrame()
        mb = pd.read_csv('Apoio/mb_area.csv')
        pt = pd.read_csv('Apoio/pt_area.csv')
        for x in sorted(ano):
                z = pd.concat([mb[(mb['ano']==x)&(mb['a'].isin(centro))&(mb['area'].isin(area))].drop_duplicates(subset = ['id_pessoa']), z], ignore_index=True)
                z2 = pd.concat([pt[(pt['ano']==x)&(pt['a'].isin(centro))&(pt['area'].isin(area))].drop_duplicates(subset = ['id_discente_extensao']), z2], ignore_index=True)
        evo = pd.DataFrame(columns=['centro','ano','media'])
        for i in centro:
                for x in sorted(ano):
                        b = []
                        b.append(i)
                        b.append(x)
                        if len(z[(z['ano']==x)&(z['a']==i)]['id_projeto'].unique()) != 0:
                                if x == 2020:
                                        b.append(len(z2[(z2['ano']==x)&(z2['a']==i)]['id_discente_extensao'].unique())/len(z[(z['ano']==x)&(z['a']==i)]['id_projeto'].unique()))
                                else:
                                        b.append((len(z[(z['ano']==x)&(z['a']==i)&(z['categoria_membro']=='DISCENTE')]['id_pessoa'].unique()))/len(z[(z['ano']==x)&(z['a']==i)]['id_projeto'].unique()))
                        else:
                                b.append(0)
                        ins(evo, b)
        evo[['media']] = evo[['media']].applymap(lambda x : "%.2f" % x)
        evo = evo.sort_values(['ano','centro'])
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Projeto'],  shared_yaxes=True)
        for a in ano:
                graf_rel.add_trace(go.Bar(x=evo[evo['ano']==a]['centro'].to_list(), y=evo[evo['ano']==a]['media'].to_list(), name=str(a), text=evo[evo['ano']==a]['media'].to_list(), textposition='auto',),1,1)
                graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        return dcc.Graph(figure=graf_rel)
    elif tab == 'tab2-4':
        evo = pd.read_csv('Apoio/dis-pro_area.csv')
        graf_rel = make_subplots(rows=1, cols=1,  shared_yaxes=True)
        for a in ano:
                graf_rel.add_trace(go.Scatter(x=evo[(evo['ano']==a)&(evo['centros'].isin(centro))&(evo['area'].isin(area))].groupby(['projetos'])['discentes'].sum().reset_index(level=0)['projetos'].to_list(), y=evo[(evo['ano']==a)&(evo['centros'].isin(centro))&(evo['area'].isin(area))].groupby(['projetos'])['discentes'].sum().reset_index(level=0)['discentes'].to_list(), name=str(a), mode='markers'),1,1)
                graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
        graf_rel.update_layout(go.Layout(yaxis={'title':'Numero de Projetos'},xaxis={'title': 'Quantidade de discentes'}))
        return dcc.Graph(figure=graf_rel)


@app.callback(
        Output("rafa2", "style"),
        [Input("area2", "value")]
)
def teste(area):
        return {'display':'none'}



@app.callback(
	[Output("area2", "value"),Output("modal_52", "is_open")],
	[Input("centro2", "value"), Input("ano2", "value"), Input('rafa2','style'),Input("close_52", "n_clicks")],
	[State("area2", "value"),State("modal_52", "is_open")],

)
def flag(centro,ano,rafa,n_rel, area, is_open_rel):
        mb = pd.read_csv('Apoio/mb_area.csv')
        a = list(set(mb[(mb['a'].isin(centro))&(mb['ano'].isin(ano))]['area'].dropna()))
        if 'Todas as areas' in area:
                print ('oi')
                return [a,is_open_rel]
        if len(area) == 0:
                print('oi1')
                return [a[0], not is_open_rel]
        else:
                print('oi4')
                if n_rel:
                        print('oi2')
                        if is_open_rel == True:
                                print('oi3')
                                return [area, not is_open_rel]
                        return [area, is_open_rel]
                return [area, is_open_rel]
            
	 
@app.callback(
	[Output("centro2", "value"),Output("modal_32", "is_open")],
	[Input("ano2", "value"), Input("close_32", "n_clicks")],
	[State("centro2", "value"),State("modal_32", "is_open")],

)
def limite_centros(ano,n_rel, centro,is_open_rel):
	if 'Todos os centros' in centro:
		return [['CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ'],is_open_rel]
	if len(centro) == 0:
		return [['CEAR'], not is_open_rel]
	else:
		if n_rel:
			if is_open_rel == True:
				return [centro, not is_open_rel]
			return [centro, is_open_rel]
		return [centro, is_open_rel]



@app.callback(
	[Output("ano2", "value"),Output("modal_42", "is_open")],
	[Input("centro2", "value"),Input("close_42", "n_clicks")],
	[State("ano2", "value"),State("modal_42", "is_open")],

)

def flag(centro,n_rel, ano, is_open_rel):
        if 'Todos os anos' in ano:
                return [[2017,2018,2019,2020],is_open_rel]
        if len(ano) == 0:
                return [[2020], not is_open_rel]
        else:
                if n_rel:
                        if is_open_rel == True:
                                return [ano, not is_open_rel]
                        return [ano, is_open_rel]
                return [ano, is_open_rel]








@app.callback(
	Output("relatorio_discentes2", "children"),
	[Input("centro2", "value"),Input("ano2", "value"),
         Input("tabs-example2","value")]

)

def relatorio_discentes(centro,ano,tab):
        centro=", ".join(str(x) for x in centro)
        ano=", ".join(str(x) for x in sorted(ano))
        if tab == 'tab2-1':
                return f'''O gráfico analisado é a relação entre Discentes/Docentes, a fim de visualizar o envolvimento dos discentes 
                                em projetos de extensão nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                                analisar os centros que possuem mais docentes que discentes, quando os valores obtidos forem menores que 1, e os que possuem 
                                mais alunos que professores, para valores maiores que 1.'''
        elif tab == 'tab2-2':
                return f'''O gráfico analisado é o evolutivo dos discentes por centro, a fim de visualizar o envolvimento dos discentes 
                                em projetos de extensão nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                                analisar os centros que atraem mais alunos para projetos de estensão e nos permite fazer um comparativo com os outros centros.'''
        elif tab == 'tab2-3':
                return f'''O gráfico analisado é a relação entre Discentes/Projeto, a fim de visualizar o envolvimento dos discentes 
                                em projetos de extensão nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                                analisar os centros que possuem a maior média de discentes por projetos.'''
        elif tab == 'tab2-4':
                return f'''O gráfico analisado é a relação entre Discentes/Projeto, a fim de visualizar a quantidade de projetos que possuem apenas um discente,
                                dois discentes e assim sucessivamente, 
                                nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de dispersão. Com esses resultados pode-se 
                                analisar os projetos que possuem mais discentes envolvidos.'''

        
        

@app.callback(
	Output("card2", "children"),
	[Input("tabs-example2","value")]
)

def graf_tit(tab):
        if tab == 'tab2-1':
                return 'Gráfico da Relação de Discentes/Docentes por Centro'
        elif tab == 'tab2-2':
                return 'Gráfico Evolutivo de Discentes por Centro'
        elif tab == 'tab2-3':
                return 'Gráfico da Media de Discentes por Centro'
        elif tab == 'tab2-4':
                return 'Gráfico da Relação de Discentes/Projeto por Centro'


###RAFAEL3###

@app.callback(
	Output("graph_docentes_23", "style"),
	[Input("aba-example3","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas == 'aba3-1':
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
	else:
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}



@app.callback(
	Output("graph_docentes3", "style"),
	[Input("aba-example3","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas == 'aba3-1':
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
	else:
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}


@app.callback(
        [Output("graph_docentes3", "src"),Output("graph_docentes_23", "children")],
        [Input("centros3", "value"), Input('area3','value'),
        Input("anos3", "value"),Input("aba-example3","value"), Input('rafa3','style')],
)
def update_graph_docentes(centros,area , anos,abas,rafa3):
        print(rafa3)
        print(abas,flush=True)
        if abas == 'aba3-1':
                df_ = pd.read_csv("Apoio/mb_area.csv")

                meio = 0
                sete_oito = 0
                sete_nove = 0
                oito_nove = 0 
                sete_vinte = 0 
                oito_vinte = 0
                nove_vinte = 0    
                result_df_2017 = []
                result_df_2018 = []
                result_df_2019 = []
                result_df_2020 = []

                df_ = df_[df_.a.isin(centros)]

                if 2017 in anos: 
                        df_2017 = df_[df_['ano']==2017] 
                        result_df_2017 = df_2017[(df_2017['ano']==2017)&(df_2017['a'].isin(centros))&(df_2017['area'].isin(area))].drop_duplicates(subset = ['id_pessoa']) 
                if 2018 in anos:
                        df_2018 = df_[df_['ano']==2018]
                        result_df_2018 = df_2018[(df_2018['ano']==2018)&(df_2018['a'].isin(centros))&(df_2018['area'].isin(area))].drop_duplicates(subset = ['id_pessoa'])
                if 2019 in anos:
                        df_2019 = df_[df_['ano']==2019]
                        result_df_2019 = df_2019[(df_2019['ano']==2019)&(df_2019['a'].isin(centros))&(df_2019['area'].isin(area))].drop_duplicates(subset = ['id_pessoa'])
                if 2020 in anos:
                        df_2020 = df_[df_['ano']==2020]
                        result_df_2020 = df_2020[(df_2020['ano']==2020)&(df_2020['a'].isin(centros))&(df_2020['area'].isin(area))].drop_duplicates(subset = ['id_pessoa'])

                if 2017 in anos and 2018 in anos and 2019 in anos:
                        meio = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2019['id_pessoa']))))
                if 2017 in anos and 2018 in anos and 2020 in anos:
                        meio = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2020['id_pessoa']))))
                if 2018 in anos and 2019 in anos and 2020 in anos:
                        meio = len(list(set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])) & set(list(result_df_2020['id_pessoa']))))
                if 2017 in anos and 2019 in anos and 2020 in anos:
                        meio = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])) & set(list(result_df_2020['id_pessoa']))))

                print(meio)


                if 2017 in anos and 2018 in anos: 
                        sete_oito = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2018['id_pessoa'])))) - meio
                if 2017 in anos and 2019 in anos: 
                        sete_nove = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])))) - meio
                if 2018 in anos and 2019 in anos:
                        oito_nove =  len(list(set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])))) - meio  

                if 2017 in anos and 2020 in anos:
                        sete_vinte =  len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2020['id_pessoa'])))) - meio 
                if 2018 in anos and 2020 in anos:
                        oito_vinte =  len(list(set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2020['id_pessoa'])))) - meio 
                if 2019 in anos and 2020 in anos:
                        nove_vinte =  len(list(set(list(result_df_2019['id_pessoa'])) & set(list(result_df_2020['id_pessoa'])))) - meio 


                if 2017 in anos: 
                        sete = len(set(list(result_df_2017['id_pessoa']))) - meio - sete_oito - sete_nove - sete_vinte
                if 2018 in anos:
                        oito = len(set(list(result_df_2018['id_pessoa']))) - meio - sete_oito - oito_nove - oito_vinte
                if 2019 in anos:
                        nove = len(set(list(result_df_2019['id_pessoa']))) - meio - sete_nove - oito_nove - nove_vinte
                if 2020 in anos:
                        vinte = len(set(list(result_df_2020['id_pessoa']))) - meio - sete_vinte - oito_vinte - nove_vinte

                plt.clf()

                if 2017 in anos and 2018 in anos and 2019 in anos:
                        v = vplt.venn3(subsets=(sete, oito, sete_oito, nove, sete_nove, oito_nove, meio), set_labels = ('2017','2018', '2019'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]

                if 2017 in anos and 2018 in anos and 2020 in anos:
                        v = vplt.venn3(subsets=(sete, oito, sete_oito, vinte, sete_vinte, oito_vinte, meio), set_labels = ('2017','2018', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]

                if 2018 in anos and 2019 in anos and 2020 in anos:
                        v = vplt.venn3(subsets=(oito, nove, oito_nove, vinte, oito_vinte, nove_vinte, meio), set_labels = ('2018','2019', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]

                if 2017 in anos and 2019 in anos and 2020 in anos:
                        v = vplt.venn3(subsets=(sete, nove, sete_nove, vinte, sete_vinte, nove_vinte, meio), set_labels = ('2017','2019', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]


                if 2017 in anos and 2018 in anos:
                        v = vplt.venn2(subsets={'10': sete, '01': oito, '11': sete_oito}, set_labels = ('2017', '2018'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                if 2017 in anos and 2019 in anos:
                        v = vplt.venn2(subsets={'10': sete, '01': nove, '11': sete_nove}, set_labels = ('2017', '2019'))
                        plt.savefig('Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                if 2018 in anos and 2019 in anos:
                        v = vplt.venn2(subsets={'10': oito, '01': nove, '11': oito_nove}, set_labels = ('2018', '2019'))
                        plt.savefig('Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                 
                if 2017 in anos and 2020 in anos:
                        v = vplt.venn2(subsets={'10': sete, '01': vinte, '11': sete_vinte}, set_labels = ('2017', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                 
                 
                if 2018 in anos and 2020 in anos:
                        v = vplt.venn2(subsets={'10': oito, '01': vinte, '11': oito_vinte}, set_labels = ('2018', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                 
                if 2019 in anos and 2020 in anos:
                        v = vplt.venn2(subsets={'10': nove, '01': vinte, '11': nove_vinte}, set_labels = ('2019', '2020'))
                        plt.savefig('Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]


        elif abas == 'aba3-2':
                z = pd.DataFrame()
                mb = pd.read_csv('Apoio/mb_area.csv')
                for x in sorted(anos):
                        z = pd.concat([mb[(mb['ano']==x)&(mb['a'].isin(centros))&(mb['area'].isin(area))].drop_duplicates(subset = ['id_pessoa']), z], ignore_index=True)
                evo = pd.DataFrame(columns=['centro','ano','quant'])
                for i in centros:
                        for x in sorted(anos):
                                b = []
                                b.append(i)
                                b.append(x)
                                b.append((len(z[(z['ano']==x)&(z['a']==i)&(z['categoria_membro']=='DOCENTE')]['id_pessoa'].unique())))
                                ins(evo, b)
                evo = evo.sort_values(['ano', 'centro'])
                agraf_rel = make_subplots(rows=1, cols=1,row_titles = ['Quantidade de Discentes'],  shared_yaxes=True)
                for a in anos:
                        agraf_rel.add_trace(go.Bar(x=evo[evo['ano']==a]['centro'].to_list(), y=evo[evo['ano']==a]['quant'].to_list(), name=str(a), text=evo[evo['ano']==a]['quant'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                agraf_rel.update_layout(height=600)
                return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph(figure=agraf_rel)]
                                    
        elif abas == 'aba3-3':
                z = pd.DataFrame()
                mb = pd.read_csv('Apoio/mb_area.csv')
                for x in sorted(anos):
                        z = pd.concat([mb[(mb['ano']==x)&(mb['a'].isin(centros))&(mb['area'].isin(area))].drop_duplicates(subset = ['id_pessoa']), z], ignore_index=True)
                evo = pd.DataFrame(columns=['centro','ano','media'])
                for i in centros:
                        for x in sorted(anos):
                                b = []
                                b.append(i)
                                b.append(x)
                                if len(z[(z['ano']==x)&(z['a']==i)]['id_projeto'].unique()) != 0:
                                        b.append((len(z[(z['ano']==x)&(z['a']==i)&(z['categoria_membro']=='DOCENTE')]['id_pessoa'].unique()))/len(z[(z['ano']==x)&(z['a']==i)]['id_projeto'].unique()))
                                else:
                                        b.append(0)
                                ins(evo, b)
                evo[['media']] = evo[['media']].applymap(lambda x : "%.2f" % x)
                evo = evo.sort_values(['ano','centro'])
                agraf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Projeto'],  shared_yaxes=True)
                for a in anos:
                        agraf_rel.add_trace(go.Bar(x=evo[evo['ano']==a]['centro'].to_list(), y=evo[evo['ano']==a]['media'].to_list(), name=str(a), text=evo[evo['ano']==a]['media'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                agraf_rel.update_layout(height=600)
                return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph(figure=agraf_rel)]
        elif abas == 'aba3-4':
                evo = pd.read_csv('Apoio/doc-pro_area.csv')
                agraf_rel = make_subplots(rows=1, cols=1,  shared_yaxes=True)
                for a in anos:
                        agraf_rel.add_trace(go.Scatter(x=evo[(evo['ano']==a)&(evo['centros'].isin(centros))&(evo['area'].isin(area))].groupby(['projetos'])['docentes'].sum().reset_index(level=0)['projetos'].to_list(), y=evo[(evo['ano']==a)&(evo['centros'].isin(centros))&(evo['area'].isin(area))].groupby(['projetos'])['docentes'].sum().reset_index(level=0)['docentes'].to_list(), name=str(a), mode='markers'),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                agraf_rel.update_layout(go.Layout(yaxis={'title':'Numero de Projetos'},xaxis={'title': 'Quantidade de discentes'}))
                venn = base64.b64encode(open('Apoio/venn.png', 'rb').read())
                agraf_rel.update_layout(height=600)
                return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph(figure=agraf_rel)]


@app.callback(
        Output("rafa3", "style"),
        [Input("area3", "value")]
)
def teste(area):
        return {'display':'none'}


@app.callback(
	[Output("area3", "value"),Output("modal_53", "is_open")],
	[Input("centros3", "value"), Input("anos3", "value"), Input('rafa3','style'),Input("close_53", "n_clicks")],
	[State("area3", "value"),State("modal_53", "is_open")],

)
def flag_area3(centro,ano,rafa,n_rel, area, is_open_rel):
	mb = pd.read_csv('Apoio/mb_area.csv')
	a = list(set(mb[(mb['a'].isin(centro))&(mb['ano'].isin(ano))]['area'].dropna()))
	if 'Todos as áreas' in area:
		return [a,is_open_rel]
	if len(area) == 0:
		return [a[0], not is_open_rel]
	else:
		if n_rel:
			if is_open_rel == True:
				return [area, not is_open_rel]
			return [area,is_open_rel]
		return [area, is_open_rel]



@app.callback(
	[Output("centros3", "value"),Output("modal3", "is_open")],
	[Input("anos3", "value"), Input("close3", "n_clicks")],
	[State("centros3", "value"),State("modal3", "is_open")],

)
def limite_centros(anos,n2, centros,is_open):
	if 'Todos os centros' in centros:
		return [['CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ'],is_open]
	if len(centros) == 0:
		return [['CEAR'], not is_open]
	else:
		if n2:
			if is_open == True:
				return [centros, not is_open]
			return [centros, is_open]
		return [centros, is_open]


@app.callback(
	[Output("anos3", "value"),Output("modal_23", "is_open"),Output("modal_3a3", "is_open")],
	[Input("centros3", "value"),Input("close_23", "n_clicks"),Input("close_3a3", "n_clicks"),Input("aba-example3","value")],
	[State("anos3", "value"),State("modal_23", "is_open"),State("modal_3a3", "is_open")],

)

def flag(centros,n2,n3, abas, anos, is_open,is_open2):
	if len(anos) > 3:
		if abas != 'aba3-1':
			return [anos,is_open,is_open2]
		return [[2018,2019,2029],is_open,not is_open2]
	if len(anos) < 2:
		if abas != 'aba3-1':
			return [anos,is_open,is_open2]

		return [[2018,2019], not is_open,is_open2]
	else:
		if n3:
			if is_open2 == True:
				return [anos,is_open, not is_open2]
			return [anos, is_open,is_open2]
		if n2:

			if is_open == True:
				return [anos, not is_open,is_open2]
			return [anos, is_open,is_open2]
		return [anos, is_open,is_open2]


@app.callback(
	Output("relatorio_docentes3", "children"),
	[Input("centros3", "value"),Input("anos3", "value"),Input("aba-example3","value")]

)
def relatorio_docentes(centros,anos, abas):
	if abas == 'aba3-1':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é uma análise de variabilidade, a fim de visualizar a quantidade de professores e alunos que 
		trabalharam em projetos de extensão apenas no ano de {anos}, bem como suas respectivas intersecções. Podemos
		analisar que, como escolhido, está sendo filtrado em apenas os centros: {centros} para serem visualizados.
		Esses dados foram representados pelo diagrama de Venn.'''
	if abas == 'aba3-2':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é o evolutivo dos docentes por centro, a fim de visualizar o envolvimento dos docentes 
		em projetos de extensão nos anos de {anos}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
		os centros: {centros} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
		analisar os centros que atraem mais docentes para projetos de estensão e nos permite fazer um comparativo com os outros centros.'''
	if abas == 'aba3-3':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é a relação entre Docentes/Projeto, a fim de visualizar o envolvimento dos docentes 
		em projetos de extensão nos anos de {anos}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
		os centros: {centros} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
		analisar os centros que possuem a maior média de docentes por projetos.'''
	if abas == 'aba3-4':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é a relação entre Docentes/Projeto, a fim de visualizar a quantidade de projetos que possuem apenas um docente,
                                dois docentes e assim sucessivamente, 
				nos anos de {anos}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
				os centros: {centros} para serem visualizados. Esses dados foram representados em um grafico de dispersão. Com esses resultados pode-se 
				analisar os projetos que possuem mais docentes.'''

        

@app.callback(
	Output("card_doc3", "children"),
	[Input("aba-example3","value")]
)

def graf_tit(abas):
        if abas == 'aba3-1':
                return 'Gráfico de Variabilidade de Docentes'
        elif abas == 'aba3-2':
                return 'Gráfico Evolutivo de Docentes por Centro'
        elif abas == 'aba3-3':
                return 'Gráfico da Media de Docentes por Centro'
        elif abas == 'aba3-4':
                return 'Gráfico da Relação Docente/Projeto'




	



if __name__ == '__main__': 
    app.run_server(port=4062)                            










