from flask import Blueprint, render_template

entrada = Blueprint('entrada', __name__, url_prefix='/entrada')

@entrada.route('/')
def estoque_home():
    return render_template('entrada.html')