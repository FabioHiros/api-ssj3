from flask import Flask,render_template, request ,session,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,create_engine
from crud import pessoadb,select_user,moda
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask("__name__")
app.secret_key = '_5#y2L"F4dasQ8dasdasc]/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:147258369@127.0.0.1:3306/dbapi'
#variavel contendo o caminho para o banco de dados
db_connection_string = 'mysql+mysqlconnector://root:147258369@127.0.0.1:3306/dbapi'

#conecta no banco de dados
engine = create_engine(
  db_connection_string)

db=SQLAlchemy(app)

class pessoas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True,nullable=False)
    funcao = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(300),nullable=False)
    nota1 = db.Column(db.String(100))
    nota2 = db.Column(db.String(100))
    nota3 = db.Column(db.String(100))
    nota4 = db.Column(db.String(100))
    nota5 = db.Column(db.String(100))
  


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/estrutura')
def estrutura():
    return render_template('estrutura.html')


@app.route('/planningpoker')
def planningp():
    return render_template('planning_poker.html')

@app.route('/processbacklog')
def processb():
    return render_template('process_backlog.html')

@app.route('/productbacklog')
def productb():
    return render_template('product_backlog.html')


@app.route('/sprintplanning')
def sprintp():
    return render_template('sprint_planning.html')

@app.route('/sprintretrospective')
def sprintr():
    return render_template('sprint_retrospective.html')


@app.route('/dailyscrum')
def dailys():
    return render_template('daily_scrum.html')

@app.route('/burndownchart')
def burndown():
    return render_template('burndown.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/notas/',methods=['POST','GET'])
def notas():
    # time=pessoadb()
    nomes = pessoas.query.all()
    # 
    # 
    # print(data)
    # print(data['nota1'])
    if request.method == "POST":
            nome=request.form['nome']
            
           # data = pessoas.query.get(request.form.get('nome'))
            data=pessoas.query.filter_by(nome=nome).first()     
            # data=select(request.form.get('nome'))
            print(data)
            print(data.nota1)
            data.nota1 = f'{data.nota1}{request.form['nota1']}'
            print(data.nota1)
            data.nota2 =  request.form['nota2']
            data.nota3 =  request.form['nota3']
            data.nota4 =  request.form['nota4']
            data.nota5 =  request.form['nota5']
            db.session.add(data)
            db.session.commit()
            return render_template('index.html')
    return render_template('notas.html',nomes=nomes)

# @app.route('/avaliar/',methods=['POST','GET'])
# def update():
    
#     return render_template('notas.html')
#seleciona usuário pelo id
@app.route('/user/<id>')
def select(id):
    user=select_user(id)
    return user


#Login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = pessoas.query.filter_by(email=email).first()
        newuser = moda(email)
        if check_password_hash(user.password,password):
            session['email'] = user.email
            return render_template('/usuario.html',data=newuser)
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/usuario',methods=['POST','GET'])
def user():
   
    data= request.form
    
    if  cadastro(data) == False:
        flash('EMAIL ALREADY EXISTS',category='error')
        return render_template('registro.html')
    else:
        flash('Sucessfuly registered!',category='success')
        return render_template('usuario.html', data=data)


def cadastro(data):
  with engine.connect() as conn:
    user= pessoas.query.filter_by(email=data['email']).first()
    if user:
      return False
    else:
      conn.execute(text(f"INSERT INTO pessoas( nome, email, funcao, password, nota1, nota2, nota3, nota4, nota5) VALUES ( '{data['nome']}', '{data['email']}', '{data['funcao']}', '{generate_password_hash(data['password'],method='pbkdf2',salt_length=16)}','{'0'}','{'0'}','{'0'}','{'0'}','{'0'}')"))
    
      conn.commit()