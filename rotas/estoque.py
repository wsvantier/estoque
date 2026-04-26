from flask import Blueprint, render_template

estoque = Blueprint('estoque', __name__, url_prefix='/estoque')

@estoque.route('/')
def estoque_home():
    return render_template('estoque.html')