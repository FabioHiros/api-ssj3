from sqlalchemy import create_engine, text
from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy



app=Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:147258369@127.0.0.1:3306/dbapi'
db = SQLAlchemy(app)


#variavel contendo o caminho para o banco de dados
db_connection_string = 'mysql+mysqlconnector://root:147258369@127.0.0.1:3306/dbapi'

#conecta no banco de dados
engine = create_engine(
  db_connection_string)

#seleciona todas as pessoas
def pessoadb():
  with engine.connect() as conn:
    result = conn.execute(text("select * from pessoas"))
    pessoas = []
    for row in result.all():
      pessoas.append(row._asdict())
    return pessoas
  
#seleciona uma pessoa
def select_user(id):
  a=pessoadb()
  usuario= next((x for x in a if x['nome']==id),None) #função pra filtrar por id
  return usuario

