from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,redirect,flash
)
import psycopg2 as psy

import time
from homepage import Homepage
from logging import FileHandler, WARNING    
import pandas as pd

  
  
mydb=psy.connect (
host='ec2-50-16-221-180.compute-1.amazonaws.com',
user = 'wixkuwpoquopsg',
password='1aa6dba2540b43f31fda04e681fd7011385fdea3d25c809360972f799d7ca122',
database='db1tovgvvjoa7p')

mycursor=mydb.cursor()



mycursor.execute('''select * from  public."cadastro" ''')

myresult= mycursor.fetchall()
colnames = [desc[0] for desc in mycursor.description]
df = pd.DataFrame(data=myresult, columns=colnames )

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []

for index,row in df.iterrows():
    users.append(User(id=1, username=row['usuario'], password=row['senha']))

server = Flask(__name__)


app = Flask(__name__)

app.secret_key = 'somesecretkeythatonlyishouldknow'

if not app.debug:
    file_handler = FileHandler('errorlog.txt')
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)



@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        if session['user_id']==None and request.endpoint != 'login' and request.endpoint != 'registro':
                return redirect(url_for('login'))
        user = [x for x in users if x.id == session['user_id']]
        if user != []:
            g.user = user[0]
    else:
        if request.endpoint == '/app1/_dash-update-component':
            return '404'

@app.route('/registro', methods=['GET', 'POST'])
def registro(): 
    if request.method == 'POST':
        if (request.form['username_registro'] and request.form['email_registro'] and request.form['password_registro']):

            mycursor.execute('''
                            INSERT INTO public."cadastro" (usuario, email, senha)
                            VALUES
                            (%s,%s,%s)
                            ''',(request.form['username_registro'],request.form['email_registro'], request.form['password_registro']))
            mydb.commit()
            return redirect(url_for('login'))

    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    mycursor.execute('''select * from  public."usuarios_cadastrados" ''')

    myresult= mycursor.fetchall()
    colnames = [desc[0] for desc in mycursor.description]
    df = pd.DataFrame(data=myresult, columns=colnames )

    users = []

    for index,row in df.iterrows():
        users.append(User(id=1, username=row['usuario'], password=row['senha']))

    session['user_id']=None
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        print(username,flush=True)
        password = request.form['password']
        user = [x for x in users if x.username == username]
        if user != []:
            user = user[0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('/app1/'))
        else:
            flash('Erro: \"Campo Usuario ou Senha: Inválido.\"')

        return redirect(url_for('login'))

    return render_template('index.html')



@app.route('/app1/')
def app1():
    if not g.user:
        return redirect(url_for('login'))
    #time.sleep(3)
    print('vamo ver2')
    return redirect(url_for('/app1/_dash-update-component'))



@app.route('/')
def inicio():
    print('vamover3',flush=True)
    return redirect(url_for('login'))


if __name__ == '__main__':
    server.run(port=1020)




