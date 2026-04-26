from flask import Blueprint, render_template
from models import Entrada

estoque = Blueprint('estoque', __name__, url_prefix='/estoque')

@estoque.route('/')
def estoque_home():
    escritorio = Entrada.query.filter(Entrada.produto.has(categoria='ESCRITORIO')).all()
    almoxarifado = Entrada.query.filter(Entrada.produto.has(categoria='ALMOXARIFADO')).all()
    despensa = Entrada.query.filter(Entrada.produto.has(categoria='DESPENSA')).all()
    
    return render_template('estoque.html', escritorio=escritorio, almoxarifado=almoxarifado, despensa=despensa)