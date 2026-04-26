from flask import Flask, render_template
from models import db, Produto, Saida, ItemSaida, Entrada

# Criando o app
app = Flask(__name__)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Iniciando exteções
db.init_app(app)

@app.route('/')
def index():
    return render_template('estoque.html')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html')

@app.route('/saida')
def saida():
    return render_template('saida.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Criando banco de dados
    app.run(debug = True, host = '0.0.0.0')