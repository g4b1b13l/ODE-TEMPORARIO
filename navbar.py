import dash_bootstrap_components as dbc

import dash_html_components as html 

import base64

ode = base64.b64encode(open('Apoio/ode.png', 'rb').read())
# try running the app with one of the Bootswatch themes e.g.
# app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])

# make a reuseable navitem for the different examples

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
                dbc.DropdownMenuItem("Mapa Geral", href="/mapa-ufpb"),       
                dbc.DropdownMenuItem("Análise Vocabular", href="/estudo-vocabular"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Dados discentes", href="/discente"),
                dbc.DropdownMenuItem("Dados docentes", href="/docente"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Quem somos?", href="/quemsomos"),
                #html.A(dbc.DropdownMenuItem('Sair'),href='/'), 
                #dbc.DropdownMenuItem(divider=True),
                #dbc.DropdownMenuItem("Rafael", href="/rafael"),
                #dbc.DropdownMenuItem("Rafael2", href="/rafael2"),
                #dbc.DropdownMenuItem("Rafael3", href="/rafael3"),
                #dbc.DropdownMenuItem("Emmanuela", href="/emmanuela"),
                #dbc.DropdownMenuItem("João", href="/joao"),
                #dbc.DropdownMenuItem("Relatório", href="/relatorio"),              
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
    toggle_style={"color": "white", "background-color":'#04383f'},
    color="primary",
    style={'background-color':'#04383f'}
)
# this is the default navbar style created by the NavbarSimple component

# here's how you can recreate the same thing using Navbar


# this example that adds a logo to the navbar brand




def Navbar():
  navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(ode.decode()), height="50px")),
                        dbc.Col(dbc.NavbarBrand('Home', className="ml-2",href='/home',style={'color':'white'})),
                    ],
                    align="center",
                    no_gutters=True,
                    style={'background-color':'#04383f','fontColor':'white'}
                ),
                #href="/app1/_dash-update-component",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
                style={'background-color':'#04383f', 'fontColor':'white'}
            ),
        ]
    ),
    color = '#04383f',sticky='top'

    #dark=True,
    #className="mb-5",
)



  return navbar




