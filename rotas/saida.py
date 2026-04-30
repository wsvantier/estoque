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
              'quantidade': p.quantidade,
              'medida':p.produto.medida,
              'validade': p.data_ptbr()
            } for p in produtos]
    return jsonify(dados)
    
