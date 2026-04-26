from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from unidecode import unidecode
from models import db, Entrada, Produto

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
        print('Já cadastrado')
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

@entrada.route('/add_entrada', methods = ['POST'])
def entrada_add_entrada():
    produto = request.form['produto']
    quantidade = request.form['quantidade']
    validade = request.form['validade']
    
    print(produto)
    print(quantidade)
    print(validade)
    
    return redirect(url_for('entrada.entrada_home'))
    