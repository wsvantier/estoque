from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), nullable=False, unique=True)
    categoria = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome}>'
    
    
    # Função para ser usado na parte de exclusão, para não apagar o que já teve entrada    
    def usado(self):
        return len(self.entradas) > 0 

class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    validade = db.Column(db.Date, nullable=True)
    data_entrada = db.Column(db.Date, nullable=True, default=date.today)

    produto = db.relationship('Produto', backref='entradas')

    def __repr__(self):
        return f'<Entrada {self.produto.nome} - {self.quantidade}>'
    
    def iten_validade (self):
        return f"{self.produto.nome} - {self.validade}"

    def esta_vencido(self):
        return self.validade < date.today()
    
    def data_ptbr(self):
        if self.validade:
            return datetime.strftime(self.validade,'%d/%m/%Y')
        else:
            return "Indeterminado"

class Saida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, default=date.today)
    responsavel = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Saida {self.data} - {self.responsavel}>'

class ItemSaida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saida_id = db.Column(db.Integer, db.ForeignKey("saida.id"), nullable=False)
    entrada_id = db.Column(db.Integer, db.ForeignKey("entrada.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    saida = db.relationship('Saida', backref='itens')
    entrada = db.relationship('Entrada', backref='itens')

    def __repr__(self):
        return f'<ItemSaida {self.quantidade} de Entrada {self.entrada.id} para Saida {self.saida.id}>'