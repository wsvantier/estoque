from flask import Blueprint, render_template

saida = Blueprint('saida', __name__, url_prefix='/saida')

@saida.route('/')
def saida_home():
    return render_template('saida.html')