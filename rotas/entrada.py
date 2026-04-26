from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from unidecode import unidecode
from models import db, Entrada, Produto
from datetime import datetime

entrada = Blueprint('entrada', __name__, url_prefix='/entrada')

# Home
@entrada.route('/')
def entrada_home():
    produtos = Produto.query.order_by(Produto.categoria,Produto.nome).all()
    return render_template('entrada.html', produtos=produtos)

# Cadastro de Tipo de Produto
@entrada.route('/add_produto', methods = ['POST'])
def entrada_add_produto():
    nome = unidecode(str(request.form['nome']).upper()) # Tudo em maiúsculo e sem acentuação
    categoria = request.form['categoria']
    produto = Produto.query.filter_by(nome=nome).first() # Procura se já tem no db
    
    if produto:
       flash('Já cadastrado','warning')
    else:
        novo_produto = Produto(nome=nome, categoria=categoria)
        db.session.add(novo_produto)
        db.session.commit()
        
    return redirect(url_for('entrada.entrada_home'))

# API que filtra por categoria

@entrada.route('/api/produtos/<cat>')
def entrada_api_produtos(cat):
    produtos = Produto.query.filter_by(categoria=cat).all()
    
    dados = [{'id': p.id,
              'nome': p.nome 
            } for p in produtos]
    return jsonify(dados)


### Entrada de Mercadorias

from datetime import datetime

@entrada.route('/add_entrada', methods=['POST'])
def entrada_add_entrada():
    produto = int(request.form['produto'])
    quantidade = int(request.form['quantidade'])
    validade_str = request.form.get('validade')  

    validade = None

    # Teste para ver se a validade é indeterminada e se o produto já existe com a mesma
    # data de validade para somar a quantidade                                                                                  
    if validade_str:
        validade = datetime.strptime(validade_str, '%Y-%m-%d').date()
        existe = Entrada.query.filter_by(produto_id=produto,validade=validade).first()
    else:
        existe = Entrada.query.filter_by(produto_id=produto,validade=None).first()

    # Se já existe → soma quantidade
    if existe:
        existe.quantidade += quantidade

    # Se não existe → cria novo
    else:
        nova_entrada = Entrada(
            produto_id=produto,
            quantidade=quantidade,
            validade=validade
        )
        db.session.add(nova_entrada)

    db.session.commit()

    return redirect(url_for('entrada.entrada_home'))