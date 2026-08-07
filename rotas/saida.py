from flask import Blueprint, render_template, jsonify, session, redirect, request
from models import Entrada, Saida, db, ItemSaida

saida = Blueprint('saida', __name__, url_prefix='/saida')

## Rota index
@saida.route('/')
def saida_home():
    carrinho = session.get('carrinho', [])
    itens = []
    
    for item in carrinho:
        produto = Entrada.query.get(item['entrada_id'])
        
        itens.append({
            'id': produto.id,
            'nome': produto.produto.nome,
            'quantidade': item['quantidade'],
            'medida': produto.produto.medida
        })
        
    saidas = Saida.query.all()
    
    return render_template('saida.html', produtos=itens, saidas=saidas)

'''## API para o select categoria
@saida.route('/api/categoria/<cat>')
def saida_api_categoria(cat):
    produtos = Entrada.query.filter(
    Entrada.produto.has(categoria=cat),  # Filtra pelo produto relacionado
    Entrada.quantidade > 0
).order_by().all()
    
    dados = [{'id': p.id,
              'nome': p.produto.nome,
              'produto_id': p.produto_id,
              'quantidade': p.quantidade,
              'medida':p.produto.medida,
              'validade': p.data_ptbr()
            } for p in produtos]
    return jsonify(dados)'''

from models import Entrada, Produto  # Certifique-se de importar o modelo Produto
from flask import jsonify

## API para o select categoria
@saida.route('/api/categoria/<cat>')
def saida_api_categoria(cat):
    # Faz o join com Produto para conseguir ordenar pelo nome dele
    produtos = (Entrada.query
                .join(Entrada.produto)
                .filter(Produto.categoria == cat, Entrada.quantidade > 0)
                .order_by(Produto.nome.asc())
                .all())

    dados = [{'id': p.id,
              'nome': p.produto.nome,
              'produto_id': p.produto_id,
              'quantidade': p.quantidade,
              'medida': p.produto.medida,
              'validade': p.data_ptbr()
            } for p in produtos]

    return jsonify(dados)

    
### Carrinho ###

# Adicionar ao carrinho
@saida.post('/carrinho/add')
def saida_carrinho_add():
    
    carrinho = session.get('carrinho', [])
    
    entrada_id = int(request.form['select_produto'])
    quantidade = int(request.form['quantidade'])
    produto = Entrada.query.get(entrada_id)
    
    if produto.quantidade < quantidade:
        return "Estoque insuficiente"
    
    for item in carrinho:
        if item['entrada_id'] == entrada_id:
            item['quantidade'] += quantidade
            break
    else:
        carrinho.append({
            'entrada_id': entrada_id,
            'quantidade': quantidade
        })
    
    session['carrinho'] = carrinho
    
    return redirect('/saida')

# Remover do carrinho
@saida.route('/carrinho/del/<int:index>')
def saida_carrinho_del(index):
    
    carrinho = session.get('carrinho', [])

    if index < len(carrinho):
        carrinho.pop(index)

    session['carrinho'] = carrinho
    session.modified = True
    
    return redirect('/saida')

## Finalizar e debitar do estoque
@saida.post('/carrinho/finalizar')
def saida_carrinho_finalizar():
    resposavel = request.form['resp']
    carrinho = session.get('carrinho', [])
    
    if not carrinho:
        return 'Carrinho vazio'
    
    saida = Saida(responsavel=resposavel)
    db.session.add(saida)
    db.session.flush()
    
    for item in carrinho:
        produto = Entrada.query.get(item['entrada_id'])
        
        if produto.quantidade < item['quantidade']:
            return f"Estoque insuficiente para {produto.produto.nome}"
        
        produto.quantidade -= item['quantidade']
        
        item_saida = ItemSaida(
            saida_id = saida.id,
            entrada_id = produto.id,
            quantidade = item['quantidade']
        )
        db.session.add(item_saida)
    
    db.session.commit()

    session.pop('carrinho', None)
    
    
    return redirect(f'/saida/listar/{saida.id}')

# Listar itens que saíram
@saida.route('/listar/<int:id>')
def saida_listar(id):
    saida = Saida.query.get(id)
    itens = ItemSaida.query.filter_by(saida_id = id).all()
    return render_template('listar_saida.html', resp = saida.responsavel, itens=itens)
