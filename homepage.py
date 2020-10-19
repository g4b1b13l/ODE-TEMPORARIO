import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from navbar import Navbar
import base64
from dash.dependencies import Output, Input, State
nav = Navbar()



background = base64.b64encode(open('Apoio/background.png', 'rb').read())
cear = base64.b64encode(open('Apoio/cear.png', 'rb').read())
ufpb = base64.b64encode(open('Apoio/ufpb.png', 'rb').read())
proex = base64.b64encode(open('Apoio/proex.png', 'rb').read())
prac = base64.b64encode(open('Apoio/prac.png', 'rb').read())
sti = base64.b64encode(open('Apoio/sti.png', 'rb').read()) 
back='data:image/png;base64,{}'.format(cear.decode())
ode = base64.b64encode(open('Apoio/ode.png', 'rb').read())


jumbotron =dbc.Jumbotron(
    [
              dbc.Row(
           [    
          dbc.Col([],md=2),
           dbc.Col([

        #html.Hr(className="my-2"),
        dbc.Fade(
            html.H3("Bem vindo(a) ao",style={'font-size':'55px'}),
            id="fade_bem_vindo_1",
            is_in=True,
            appear=True,
            style={"transition": "opacity 2000ms ease", 'textAlign':'center','color':'#04383f'}
        ),

        dbc.Fade(
            html.H3("Observatório de Dados",style={'font-size':'55px'}),
            id="fade_bem_vindo_1_",
            is_in=True,
            appear=True,
            style={"transition": "opacity 2500ms ease", 'textAlign':'center','color':'#04383f'}
        ),
        #dbc.Fade(
        #    html.H1("ao", className="display-3"),
        #    id="fade2",
        #    is_in=True,
        #    appear=True,
        #    style={"transition": "opacity 2500ms ease", 'textAlign':'center'}
        #),   
        dbc.Fade(         
            html.H3("da Extensão",style={'font-size':'55px'}),
            id="fade_bem_vindo_2",
            is_in=True,
            appear=True,
            style={"transition": "opacity 3000ms ease", 'textAlign':'center','color':'#04383f'}
        ),


        ]),
        dbc.Col([
          dbc.Fade(
        html.Img(id='img_logo_ode',height='300'
        ,srcSet='data:image/png;base64,{}'.format(ode.decode())
       
         ),

        is_in=True,
        appear=True,
            style={"transition": "opacity 3000ms ease"}
        ),
         ],md=2),

        dbc.Col([],md=2),


       ],align='center'),


     #   dbc.FormGroup(
    #[
        #dbc.RadioItems(
        #    options=[
       #         {"label": "", "value": 1},
      #          {"label": "", "value": 2},
     #       ],
    #        value=1,
   #         id="radioitems-inline-input",
  #          inline=True,
 #           style={'text-align': 'center'},

##        ),
#    ]
#)

       # html.P(
#"""\
#     A extensão universitária é uma ferramenta de promoção do desenvolvimento social e difusão do conhecimento tanto interno como também fora da universidade. Muitas são as ações desenvolvidas na UFPB com este objetivo, onde, por enquanto, existem poucas ferramentas sendo implementadas para avaliar dados gerados e permitir um acompanhamento de tais atividades de forma quantitativa. \n     A proposta submetida, é uma opção para permitir uma visão mais quantitativa dos dados criados por meio dessas ações, usando ferramentas de análise de dados e propondo métricas que auxiliam sua gestão dentro da UFPB, por meio da PRAC ou até mesmo das Assessorias de Extensão. \n     Esta iniciativa, agora em seu segundo ano, é batizada de Observatório de Dados da Extensão e fornece informações estratégicas para um melhor conhecimento das ações de extensão desenvolvidas na UFPB."""
#        ),


    ],className='back',id='homepage_back',style={'width':'100%'}
)

jumbotron_2 =html.Div([dbc.Jumbotron(
    [
        dbc.Fade(
            html.H1("O que é o ODE?",style={'font-size':'55px'}),
            id="fade_oque_1",
            is_in=True,
            appear=False,
            style={"transition": "opacity 2000ms ease", 'textAlign':'left','color':'#04383f','display': 'block'}
        ),
        html.Hr(className="my-2",style={'color':'#f7f7f7'}),
        html.Div(html.Br()),
        html.Div(html.Br()), 
        dbc.Fade(         
        html.P(['A extensão universitária tem como objetivo promover o desenvolvimento social e a difusão de conhecimentos para a universidade. Muitas são as ações desenvolvidas na UFPB com este objetivo, onde, por enquanto, existem poucas ferramentas sendo implementadas para avaliar dados gerados e permitir um acompanhamento de tais atividades.',html.Br(),  'Esse projeto visa apresentar os dados da extensão de forma quantitativa, usando ferramentas de análise de dados e propondo métricas que auxiliam sua gestão dentro da UFPB, por meio da PRAC ou até mesmo das Assessorias de Extensão.',html.Br(), 'Esta iniciativa é batizada de Observatório de Dados da Extensão e fornece informações estratégicas para um melhor conhecimento das ações de extensão desenvolvidas na UFPB.'],style={'textAlign':'justify','whiteSpace': 'pre-wrap'}
        ),            id="fade_oque_2",
            is_in=True,
            appear=False,
            style={"transition": "opacity 3000ms ease", 'textAlign':'center','display': 'block'},
            
        ),
       
       

   #     dbc.FormGroup(
   # [
   #     dbc.RadioItems(
   #         options=[
   #             {"label": "", "value": 1},
   #             {"label": "", "value": 2},
   #         ],
   #         value=1,
   #         id="radioitems-inline-input",
   ##         inline=True,
    #        style={'text-align': 'center'},

        #),
    #]
#)

       # html.P(
#"""\
#     A extensão universitária é uma ferramenta de promoção do desenvolvimento social e difusão do conhecimento tanto interno como também fora da universidade. Muitas são as ações desenvolvidas na UFPB com este objetivo, onde, por enquanto, existem poucas ferramentas sendo implementadas para avaliar dados gerados e permitir um acompanhamento de tais atividades de forma quantitativa. \n     A proposta submetida, é uma opção para permitir uma visão mais quantitativa dos dados criados por meio dessas ações, usando ferramentas de análise de dados e propondo métricas que auxiliam sua gestão dentro da UFPB, por meio da PRAC ou até mesmo das Assessorias de Extensão. \n     Esta iniciativa, agora em seu segundo ano, é batizada de Observatório de Dados da Extensão e fornece informações estratégicas para um melhor conhecimento das ações de extensão desenvolvidas na UFPB."""
#        ),


    ],className='back_2',id='homepage_back_2',style={'display': 'inline-block', 'textAlign':'center'}
)])

jumbotron_3 =html.Div([dbc.Jumbotron(
    [
              html.H1("Parceiros", className="display-3",style={ 'textAlign':'left','color':'#04383f'}),
              html.Div(html.Br()), 
              html.Div(html.Br()),

              dbc.Row(
           [    


     dbc.Col([
      html.A([
                html.Img(id='img_logo_prac',height='250px', 
                  style={'display':'block', 'max-width': '100%','margin-left':'10px'} 
                        ,srcSet='data:image/png;base64,{}'.format(ufpb.decode())
                        ),],href="https://www.ufpb.br/"),],width=3),


           dbc.Col([
           html.A([
                html.Img(id='img_logo_cear',height='250px',
                  style={'display':'block', 'max-width': '100%','object-fit': 'cover','margin-left':'-100px'}
                        ,srcSet='data:image/png;base64,{}'.format(cear.decode())
                        ),],href="http://www.cear.ufpb.br/"),],width=3),


    dbc.Col([
    html.A([
                html.Img(id='img_logo_proex',height='250px',
                  style={'display':'block', 'max-width': '100%','margin-left':'-70px'}
                        ,srcSet='data:image/png;base64,{}'.format(proex.decode())
                        ),],href="http://www.prac.ufpb.br/"),],width=3),
    


    dbc.Col([
    html.A([
                html.Img(id='img_logo_sti',height='250px',
                  style={'display':'block', 'max-width': '100%','margin-left':'-70px'}
                        ,srcSet='data:image/png;base64,{}'.format(sti.decode())
                        ),],href="https://www.sti.ufpb.br/"),],width=3),

           ],no_gutters=True)

    ],style={'background-color':'#f7f7f7'}
)])







body = dbc.Row([ dbc.Col([
              jumbotron, 
              jumbotron_2,
              jumbotron_3
				])

],style={'background-color':'#f7f7f7'})


def Homepage():
    layout = html.Div([
    nav,
    body
    ])
    return layout



