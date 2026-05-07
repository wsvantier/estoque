from flask import Flask, redirect
from models import db
from rotas.entrada import entrada
from rotas.estoque import estoque
from rotas.saida import saida

# Criando o app
app = Flask(__name__)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'chave-secreta'

# Iniciando extensões
db.init_app(app)

# Criando tabelas
with app.app_context():
    db.create_all()

# Cadastrando blueprints
app.register_blueprint(entrada)
app.register_blueprint(saida)
app.register_blueprint(estoque)

@app.route('/')
def index():
    return redirect('/estoque')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')