from flask import Blueprint, render_template, jsonify
from models import Entrada, Saida

saida = Blueprint('saida', __name__, url_prefix='/saida')

## Rota index
@saida.route('/')
def saida_home():
    return render_template('saida.html')

## API para o select categoria
@saida.route('/api/categoria/<cat>')
def saida_api_categoria(cat):
    produtos = Entrada.query.filter(
    Entrada.produto.has(categoria=cat),  # Filtra pelo produto relacionado
    Entrada.quantidade > 0
).all()
    
    dados = [{'id': p.id,
              'nome': p.produto.nome,
              'produto_id': p.produto_id,
              'validade': p.validade
            } for p in produtos]
    return jsonify(dados)
    
## API para o select lote
@saida.route('/api/lote/<int:produto_id>')
def saida_api_lote(produto_id):
    lotes = Entrada.query.filter(Entrada.produto_id==produto_id,  Entrada.quantidade > 0).all()

    dados = [ {'id':l.id,
              'produto_id': l.produto_id,
               'nome':l.produto.nome,
               'validade': l.validade,
               'quantidade': l.quantidade}
                for l in lotes ]

    return jsonify(dados)