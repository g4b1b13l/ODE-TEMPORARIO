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
import numpy as np
from PIL import Image
import json
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

style1 = {'fillColor': '#00FFFFFF', 'lineColor': '#00FFFFFF','zoom_on_click':'False'}

nav = Navbar()    

retval = os.getcwd()

grupos = ['CCHLA','CEAR','CCSA','CE','CCJ','CT','CBIOTEC','CCTA','CCEN','CCS','CCM'] 
dados = ['Quantidade de projetos em 2017','Quantidade de projetos em 2018','Quantidade de projetos em 2019','Quantidade de projetos em 2020'] 

dict_csv = { 'Quantidade de projetos em 2017' : 'Apoio/dados/dataset_2017.csv',
            'Quantidade de projetos em 2018' : 'Apoio/dados/dataset_2018.csv',
    		'Quantidade de projetos em 2019' : 'Apoio/dados/dataset_2019.csv',
            'Quantidade de projetos em 2020' : 'Apoio/dados/dataset_2020.csv'
}

def escala_mapa(max):
    step = (max/9)
    myscale=np.arange(1, max, step).tolist()
    myscale.extend([max])
    return myscale

dict_ajeita_ano = {'Quantidade de projetos em 2017': '2017', 'Quantidade de projetos em 2018': '2018', 'Quantidade de projetos em 2019': '2019','Quantidade de projetos em 2020':'2020'}

#state_data=pd.read_csv('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\dados\\projetos_2017.csv', engine='python')
#geo_data = 'C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\ufpb_centros.json'   

state_data=pd.read_csv('Apoio/Projetos_2017.csv', engine='python')
geo_data = 'Apoio/ufpb_centros.json'  


professores_envolvidos ={'CBIOTEC2017': 6,
 'CBIOTEC2018': 9,
 'CBIOTEC2019': 10,
 'CBIOTEC2020': 8,
 'CCA2017': 81,
 'CCA2018': 84,
 'CCA2019': 90,
 'CCA2020': 90,
 'CCAE2017': 76,
 'CCAE2018': 90,
 'CCAE2019': 86,
 'CCAE2020': 85,
 'CCEN2017': 45,
 'CCEN2018': 46,
 'CCEN2019': 45,
 'CCEN2020': 77,
 'CCHLA2017': 78,
 'CCHLA2018': 102,
 'CCHLA2019': 94,
 'CCHLA2020': 160,
 'CCHSA2017': 65,
 'CCHSA2018': 81,
 'CCHSA2019': 74,
 'CCHSA2020': 96,
 'CCJ2017': 40,
 'CCJ2018': 45,
 'CCJ2019': 49,
 'CCJ2020': 46,
 'CCM2017': 56,
 'CCM2018': 83,
 'CCM2019': 85,
 'CCM2020': 93,
 'CCS2017': 246,
 'CCS2018': 281,
 'CCS2019': 266,
 'CCS2020': 332,
 'CCSA2017': 79,
 'CCSA2018': 80,
 'CCSA2019': 43,
 'CCSA2020': 84,
 'CCTA2017': 69,
 'CCTA2018': 69,
 'CCTA2019': 76,
 'CCTA2020': 95,
 'CE2017': 60,
 'CE2018': 53,
 'CE2019': 95,
 'CE2020': 97,
 'CEAR2017': 19,
 'CEAR2018': 21,
 'CEAR2019': 19,
 'CEAR2020': 21,
 'CI2017': 14,
 'CI2018': 25,
 'CI2019': 20,
 'CI2020': 18,
 'CT2017': 86,
 'CT2018': 69,
 'CT2019': 63,
 'CT2020': 91,
 'CTDR2017': 39,
 'CTDR2018': 22,
 'CTDR2019': 26,
 'CTDR2020': 45}

chama_ano_criacao = {   
    'CCHLA': 1949
    ,'CEAR': 2011
    ,'CCSA': 1934
    ,'CE': 1978  
    ,'CCJ':1949
    ,'CT': 1974 
    ,'CBIOTEC':2011
    ,'CCTA':2012
    ,'CCEN': 1974
    ,'CCS': 1974
    ,'CCM': 2007
    ,'CCA': 1936
    ,'CCHSA': 2008
    ,'CCAE': 2006
    ,'CI':2012
    ,'CTDR': 2009
} 

chama_departamentos = {   
    'CCHLA': 11
    ,'CEAR': 2
    ,'CCSA': 6
    ,'CE': 7  
    ,'CCJ':5
    ,'CT': 7 
    ,'CBIOTEC':2
    ,'CCTA': 7
    ,'CCEN':9
    ,'CCS':13
    ,'CCM': 5
    ,'CCA': 7
    ,'CCHSA': 6
    ,'CCAE': 8
    ,'CTDR': 3
    ,'CI': 3
} 
  
chama_cursos = {   
    'CCHLA': ['Ciências Sociais','Comunicação em Mídias Digitais', 'Filosofia', 'História', 'Letras', 'Letras / Ead', 'Letras - Libras', 'Letras(Língua Espanhola)','Letras(Língua Francesa)','Letras(Línguas Clássicas)','Letras(Língua Inglesa)','Línguas Estrangeiras Aplicadas às Negociações Internacionais', 'Psicologia','Serviço Social','Tradução']
    ,'CEAR': ['Engenharia Elétrica', 'Engenharia de Energias Renovaveis']
    ,'CCSA': ['Admnistração', 'Admnistração Pública','Arquivologia','Biblioteconomia', 'Ciências Atuariais','Ciências Contábeis','Ciências Econômicas','Gestão Pública','Relações Internacionais','Tecnologia em Gestão Pública']
    ,'CE': ['Ciências das Religiões','Ciências Naturais','Pedagogia','Pedagogia - EAD', 'Pedagogia(Educação Do Campo)','Pedagogia(MSC)','Psicopedagogia(BACH)']  
    ,'CCJ':['Direito']
    ,'CT': ['Arquitetura e Urbanismo','Engenharia Ambiental','Engenharia Civil','Engenharia De Alimentos','Engenharia De Materiais','Engenharia de Produção','Engenharia de Produção Mecânica','Engenharia Mecânica','Engenharia Química','Química Industrial']
    ,'CBIOTEC':['Biotecnologia']
    ,'CCTA': ['Artes Visuais','Cinema e Audiovisual','Comunicação Social','Dança','Educação Artística','Hotelaria', 'Jornalismo','Música','Música - Bacharelado', 'Música Popular', 'Radialismo','Regência De bandas E Fanfarras','Relações Públicas', 'Teatro(Bacharelado)','Teatro(Licenciatura)','Turismo']
    ,'CCEN':['Ciencias','Ciências Biológicas','Ciências Biológicas - EAD', 'Computação', 'Estatística','Física','Geografia','Matemática','Matemática - EAD', 'Química' ]
    ,'CCS':['Biomedicina','Educação Física','Educação Física - Licenciatura','Enfermagem','Farmácia','Fisioterapia','Fonoaudiologia','Nutrição','Odontologia','Terapia Ocupacional']
    ,'CCM': ['Medicina']
    ,'CCA': ['Agronomia','Ciências biológicas', 'Medicina Veterinaria','Química','Zootecnia']
    ,'CCHSA': ['Admnistração','Agroecologia','Agroindustria','Ciências Agrárias','Curso Superior de Tecnologia em Cooperativismo','Pedagogia']
    ,'CCAE': ['Admnistração','Antropologia','Ciência da Computação','Ciências Contábeis','Design','Ecologia','Hotelaria','Letras','Letras(Espanhol)','Letras(Inglês)','Matemática','Pedagogia','Secretariado Executivo Bilíngue','Sistemas de Informação']
    ,'CTDR': ['Gastronomia','Tecnologia de Alimentos','Tecnologia em Produção Sucroaalcoleira']
    ,'CI': ['Ciência da Computação','Ciência de Dados e Inteligência Artificial','Engenharia da Computação','Matemática Computacional']
}   

chama_assessor = {   
    'CCHLA': 'Nívia Pereira'
    ,'CEAR': 'Jose Mauricio Ramos de Souza Neto'
    ,'CCSA': 'Danielle Vieira'
    ,'CE': 'Quézia Furtado, Mª da Conceição Miranda'
    ,'CCJ':'Ludmila Cerqueira'
    ,'CT': 'Aurélia Idrogo, Luzia Camboim'
    ,'CBIOTEC':'Elisângela A. de Moura Kretzschmar'
    ,'CCTA': 'Luceni Caetano' 
    ,'CCEN':'Jane Torelli'
    ,'CCS': 'Rosenés Lima'
    ,'CCM': 'André Bonifácio'
    ,'CCA': 'Fábio Mielezrsk'  
    ,'CCHSA': 'Catarina de Medeiros'
    ,'CCAE': 'Jocélio de Oliveira'
    ,'CI': 'José Miguel Aroztegui'
    ,'CTDR': 'Ana Braga'
} 



chama_diretor = {   
    'CCHLA': 'Mônica Nóbrega'
    ,'CEAR': 'Zaqueu Ernesto da Silva '
    ,'CCSA': 'Walmir Rufino Da Silva'
    ,'CE': 'Wilson Honorato Aragão'
    ,'CCJ':'Fredys Orlando Souto'
    ,'CT': 'Antônio de Mello Villar'
    ,'CBIOTEC':'Valdir de Andrade Braga'
    ,'CCTA': 'José David Campos Fernandes'
    ,'CCEN':'José Roberto Soares do Nascimento'
    ,'CCS':'João Euclides Fernandes Braga'
    ,'CCM': 'Eduardo Sérgio Moura Souza'
    ,'CCA': 'Manuel Bandeira de Albuquerque'
    ,'CCHSA': 'Terezinha Domiciano Martins'
    ,'CCAE': 'Maria Angeluce Soares Perônico Barbotin'
    ,'CI': 'Hamilton Soares da Silva'
    ,'CTDR': 'José Marcelino Oliveira Cavalheiro'
} 

chama_vice = {   
    'CCHLA': 'Rodrigo Freire de Carvalho e Silva'
    ,'CEAR': 'Euler Cássio Tavares de Macedo'
    ,'CCSA': 'Aldo Leonardo Cunha Callado'
    ,'CE': 'Swamy de Paula Lima Soares'
    ,'CCJ': 'Valfredo de Andrade Aguiar Filho'
    ,'CT': 'Tarciso Cabral da Silva' 
    ,'CBIOTEC': 'Fabíola da Cruz Nunes'
    ,'CCTA': 'Ulisses Carvalho da Silva'
    ,'CCEN': 'Severino Francisco de Oliveira'
    ,'CCS':'Fabiano Gonzaga Rodrigues'
    ,'CCM': 'Eutília Freire'
    ,'CCA': 'Ricardo Romão Guerra'
    ,'CCHSA': 'Pedro Germano Antonio Nunes'
    ,'CCAE': 'Alexandre Scaico'
    ,'CI': 'Lucídio dos Anjos Formiga Cabral'
    ,'CTDR': 'João Andrade da Silva'
} 

centro_extenso = {   
    'CCHLA': 'Centro de Ciências Humanas, Letras e Artes'
    ,'CEAR': 'Centro de Energias Alternativas e Renováveis'
    ,'CCSA': 'Centro de Ciências Sociais Aplicadas'
    ,'CE': 'Centro de Educação'
    ,'CCJ': 'Centro de Ciências Jurídicas'
    ,'CT': 'Centro de Tecnologia' 
    ,'CBIOTEC': 'Centro de Biotecnologia'
    ,'CCTA': 'Centro de Comunicação, Turismo e Artes'
    ,'CCEN': 'Centro de Ciências Exatas e da Natureza'
    ,'CCS':'Centro de Ciências da Saúde'
    ,'CCM': 'Centro de Ciências Médicas'
    ,'CCA': 'Centro de Ciencias Agrárias'
    ,'CCHSA': 'Centro de Ciências Humanas, Sociais e Agrárias'
    ,'CCAE': 'Centro de Ciências Aplicadas e Educação'
    ,'CI': 'Centro de Informática'
    ,'CTDR': 'Centro de Tecnologia e Desenvolvimento Regional'
} 




def chama_projetos(file,dado):
    state_data_1=pd.read_csv(dict_csv[dado], engine='python')
    filtered = [file] 
    print(state_data_1)
    state_data_1 = state_data_1[state_data_1['centros'].isin(filtered)]
    lista= list(state_data_1['qtd_projeto'])
    return lista[0]

dict_coordenadas = {
    'cbiotec' : [-7.140993, -34.846455],
    'ccen'  : [-7.139640, -34.845020],    
    'cchla' : [-7.139370, -34.850374], 
    'ccj' :  [-7.141978, -34.848935], 
    'ccm' : [-7.136423, -34.840567 ],    
    'ccs' :  [-7.135673, -34.841516],  
    'ccsa' :  [-7.141069, -34.849936],   
    'ccta' : [-7.137422, -34.849572],  
    'ce' : [-7.139994, -34.850124],  
    'cear' : [-7.141625, -34.850556],  
    'ct' : [-7.142505, -34.850309],
    'cca'  : [-6.973692, -35.716273],   
    'ccae'  : [-6.829091, -35.118770],
    'cchsa'  : [-6.752077, -35.647532],
    'ci':[-7.162211,-34.817228],
    'ctdr':[-7.163018,-34.817989]
} 

#folder ='C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\logos'    
folder ='Apoio/logos'    

extension = '*'                               
separator = ','                                    
extension = '*.' + extension  
os.chdir(folder)             
files_logos= glob.glob(extension)   

os.chdir(retval)             

#folder_1 ='C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\arquivos_json' 
#folder_1 ='C:Apoio\\arquivos_json' 
folder_1='Apoio/arquivos_json'
os.chdir(folder_1)             
files_json= glob.glob(extension)   
os.chdir(retval)             

#folder_2 ='C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\dados' 
folder_2 ='Apoio/dados' 
os.chdir(folder_2)             
files_dados= glob.glob(extension)   
os.chdir(retval)             

tooltip = "Clique para abrir a imagem"     
html1 = '<img src="data:image/png;base64,{}">'.format  

def limpa_nome_arquivo_json(logo):   
    files=logo.replace('json','')      
    files=files.replace('.','') 
    return files 

def limpa_nome_arquivo(logo):  
    files=logo.replace('jpeg','')      
    files=files.replace('jpg','')  
    files=files.replace('png','')  
    files=files.replace('.','') 
    return files 

def gera_cloropleth(geo_data,state_data,files_dados,mapa_,dado,grupos):

    state_data_1=[] 
    state_data_1=pd.read_csv(dict_csv[dado], engine='python')
    #geo_data = 'C:\\Users\\Pessoal\\Desktop\\ODE\\choropleth\\gp_1.json'      
    #geo_data = 'Apoio/choropleth/json_divisao_centros.json'  
    with open('Apoio/choropleth/json_divisao_centros.json') as jsonfile:
        input_dict = json.load(jsonfile)

    lista_features = [x for x in input_dict['features'] if x['id'] in grupos]

    #geo_data = json.dumps(lista_features)
    geo_data ={'type': 'FeatureCollection','features': lista_features}

    filtered = grupos
    state_data_1 = state_data_1[state_data_1['centros'].isin(filtered)]  

    #myscale = (state_data_1['qtd_projeto'].quantile((0,0.12,0.22,0.32,0.42,0.52,0.72,0.82,0.92,1))).tolist()
    maxi=max(list(state_data_1['qtd_projeto']))
    myscale=escala_mapa(maxi)
    myscale=[float(i) for i in myscale]
    try:
        folium.Choropleth(   
                geo_data = geo_data, 
                name='Choropleth',
                data=state_data_1,    
                columns=['centros', 'qtd_projeto'],   
                key_on='feature.id', 
                fill_color='YlGn',    
                fill_opacity=0.7,   
                line_opacity=0.2,
                legend_name='Quantidade de projetos',   
                threshold_scale=myscale,
                #show=False,
                #overlay=False         
            ).add_to(mapa_) 
    except KeyError:
        pass

  

        
    #folium.LayerControl().add_to(map)
  
  

def gera_camadas_ufpb(arquivo_json,mapa_,logo):    
    #AQUIII
    picture1 = base64.b64encode(open('Apoio/logos/' + logo ,'rb').read()).decode()
    #img = Image.open('Apoio/logos/' + logo)

    iframe1 = IFrame(html1(picture1), width=200+20, height=200+20)   
    #icon1 = folium.features.CustomIcon('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\logos\\' + logo, icon_size=(20,20))
    #camadas_ufpb = os.path.join('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\arquivos_json\\' + arquivo_json)
    camadas_ufpb = os.path.join('Apoio/arquivos_json/' + arquivo_json)

    arquivo_json=limpa_nome_arquivo_json(arquivo_json)

    camada=folium.GeoJson(camadas_ufpb,name=arquivo_json, tooltip='Clique para abrir a imagem',style_function=lambda x:style1).add_to(mapa_)    

    #camada.add_child(folium.Popup(dict_centros[arquivo_json]))
    camada.add_child(folium.Popup(iframe1,width=200+20,height=200+20))
    
    camada.add_to(mapa_)    




def gera_icones_da_ufpb(logo,dict_logo,dict_coordenadas,html1,tooltip,mapa_,arquivo_json,dado): 
    #AQUIII
    #picture1 = base64.b64encode(open('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\logos\\' + logo ,'rb').read()).decode()
    files=limpa_nome_arquivo(logo) 
    file = files.upper()
    cur=chama_cursos[file]

    if dado == 0:
        html1=f"""
    <h1> Informações sobre o {file}</h1>
    Nome do Centro: {centro_extenso[file]}<br><br>  
    Ano de criação: {chama_ano_criacao[file]}<br><br>  
    Número de departamentos: {chama_departamentos[file]}<br><br> 
    Cursos: {', '.join(str(x) for x in cur)}<br><br>
    Diretor: {chama_diretor[file]}<br><br>
    Vice-Diretor: {chama_vice[file]}<br><br>
    Assessor(es): {chama_assessor[file]}<br><br>
    """  
    else:
        html1=f"""
    <h1> Informações sobre o {file}</h1>
    Nome do Centro: {centro_extenso[file]}<br><br>  
    Ano de criação: {chama_ano_criacao[file]}<br><br>
    Número de departamentos: {chama_departamentos[file]}<br><br>
    Cursos: {', '.join(str(x) for x in cur)}<br><br>
    Diretor: {chama_diretor[file]}<br><br>
    Vice-Diretor: {chama_vice[file]}<br><br>
    Assessor(es): {chama_assessor[file]}<br><br>
    {dado}: {chama_projetos(file,dado)}<br><br>
    Quantidade de professores Envolvidos: {professores_envolvidos[file + dict_ajeita_ano[dado]]}<br><br>
    """
    #picture1 = base64.b64encode(open('Apoio/logos/' + logo ,'rb').read()).decode()
    arquivo_json=limpa_nome_arquivo_json(arquivo_json)
    #iframe1 = IFrame(html1(picture1), width=200+20, height=200+20)   
    icon1 = folium.features.CustomIcon('Apoio/logos/' + logo, icon_size=(20,20))
      

    ifr = IFrame(html=html1, width=500, height=300)
    popup1 = folium.Popup(ifr, max_width=2650)
    #popup1 = folium.Popup(dict_centros[arquivo_json],max_width=600)       
    folium.Marker(location=dict_coordenadas[files],popup= popup1,tooltip='Clique para um maior conhecimento sobre centro',icon=icon1).add_to(mapa_)
    
def mapa_da_ufpb(tooltip, files_logos,dict_coordenadas,files_json,geo_data,state_data, files_dados,mapa_,flag,grupos,dado):
    files_json = []   
    files_logos = []   
    if 'CTDR' in grupos:
        files_json.extend(['CTDR.json'])
        files_logos.extend([ 'ctdr.png'])
    if 'CI' in grupos:
        files_json.extend(['CI.json'])
        files_logos.extend([ 'ci.png'])
    if 'CCA' in grupos:
        files_json.extend(['CCA.json'])
        files_logos.extend([ 'cca.png'])
    if 'CCAE' in grupos:
        files_json.extend(['CCAE.json'])
        files_logos.extend([ 'ccae.png'])
    if 'CCHSA' in grupos:
        files_json.extend(['CCHSA.json'])
        files_logos.extend([ 'cchsa.png'])
    if 'CCJ' in grupos:
        files_json.extend(['CCJ.json'])
        files_logos.extend([ 'ccj.png'])
    if 'CT' in grupos:
        files_json.extend(['CT.json'])
        files_logos.extend([ 'ct.png'])
    if 'CBIOTEC' in grupos:
        files_json.extend(['CBIOTEC.json'])
        files_logos.extend(['cbiotec.png'])
    if 'CCHLA' in grupos:
        files_json.extend(['CCHLA.json'])
        files_logos.extend([ 'cchla.png'])
    if 'CEAR' in grupos:
        files_json.extend(['CEAR.json'])
        files_logos.extend([ 'cear.png'])
    if 'CCSA' in grupos:
        files_json.extend(['CCSA.json'])
        files_logos.extend([ 'ccsa.png'])
    if 'CE' in grupos:
        files_json.extend(['CE.json'])
        files_logos.extend(['ce.png'])
    if 'CCTA' in grupos:
        files_json.extend(['CCTA.json'])
        files_logos.extend(['ccta.png'])
    if 'CCEN' in grupos:
        files_json.extend(['CCEN.json'])
        files_logos.extend(['ccen.png'])
    if 'CCHLA' in grupos:
        files_json.extend(['CCHLA.json'])
        files_logos.extend([ 'cchla.png'])
    if 'CCS' in grupos:
        files_json.extend(['CCS.json'])
        files_logos.extend([ 'ccs.png'])
    if 'CCM' in grupos:
        files_json.extend(['CCM.json'])
        files_logos.extend(['ccm.png'])
  
    if flag == 'nao' or dado == 0: 
        for arquivo_json,logo in zip(files_json,files_logos):
            gera_camadas_ufpb(arquivo_json,mapa_,logo)  
    for arquivo_json,logo in zip(files_json,files_logos):    
        gera_icones_da_ufpb(logo,logo,dict_coordenadas,html1,tooltip,mapa_,arquivo_json,dado)
    if flag == 'sim' and grupos != [] and dado != 0:
        print('cheguei',flush=True)  
        gera_cloropleth(geo_data,state_data,files_dados,mapa_,dado,grupos)    
    #mapa_.save("C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\mapa_ufpb_centros.html") 
    mapa_.save("Apoio/mapa_ufpb_centros.html") 
tab_selected_style = {
    'font-size': '70%',
    'padding': '6px'
}

tab_style = { #Estilos das Tabs
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-size': '75%',
    'fontSize' : '12'
    }
#####
tabs = html.Div([
    dcc.Tabs(id='tabs', value='tab-3', children=[
        dcc.Tab(label='Areia', value='tab-1', style=tab_style, selected_style=tab_selected_style),
         dcc.Tab(label='Bananeiras', value='tab-2', style=tab_style, selected_style=tab_selected_style),
          dcc.Tab(label='João Pessoa', value='tab-3', style=tab_style, selected_style=tab_selected_style),
           dcc.Tab(label='Mangabeira', value='tab-5', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Mamanguape', value='tab-4', style=tab_style, selected_style=tab_selected_style),
])
    ,html.Br()])


card_content = [
    dbc.CardHeader("Filtros do Mapa",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        tabs,
        html.H4("Escolha o grupo desejado:", style={'font-size':19,'margin-top':'14px'}),
        dcc.Dropdown(
        id = 'grupos',  
        options=[
            {'label': j, 'value': j} for j in grupos  
        ],
        value=['Todos os centros'],   
        multi=True,
    searchable=False
    ),
    

    html.Div(html.Br()),
    html.H4("Deseja analisar o mapa pelo quantitativo de projetos por ano?", style={'font-size':19}),

    dbc.RadioItems(
                    options=[  
                        {'label': 'Sim', 'value': 'sim'},
                        {'label': 'Não', 'value': 'nao'},      

                    ],
                    id='flag',
                    value='1',
                    inline = True,
                    labelStyle={'display': 'inline-block','margin-bottom':'10px'}   
                ),
    html.Div([
    html.H4("Escolha o ano para visualizar o mapa:", style={'font-size':19}),

    dcc.Dropdown(
        id = 'dados',  
        options=[
            {'label': j, 'value': j} for j in dados  
        ],
        value=0,   
         multi=False,
    searchable=False,
         style={'margin-bottom':'10px'}

    ),],
    id='choropleth',
    style = {'display': 'none'}),
        ]
    ),
]

jumbotron = dbc.Card(card_content,  outline=True)

card_content_3 = [
    dbc.CardHeader("Mapa da UFPB",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.Iframe(id='mapa', srcDoc=open('Apoio/mapa_ufpb_centros.html', 'r').read(),width='100%',height='580px'), 
        ]
    ),
]

jumbotron_2 = dbc.Card(card_content_3,  outline=True)

body_1 =html.Div([  


        dbc.Row(
           [
               dbc.Col(
                  [

                jumbotron,



                   ], md=4

               ),
              dbc.Col([
     	      jumbotron_2 

                    ], md=8 ),

                ],no_gutters=True
            ),
              
])



def mapa():
    layout = html.Div([
    nav,

	body_1,
    html.Div([], id='value-container', style={'display': 'none'})

     #html.Iframe(id='mapa', srcDoc=open('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\Pasta de backup\\ODE\\mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  

     #html.Iframe(id='mapa', srcDoc=open('Apoio/mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  
    ])
    return layout



