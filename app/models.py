from app import db
from datetime import datetime
from datetime import timedelta, timezone
from sqlalchemy.dialects.mysql import LONGTEXT, JSON



class Comprador(db.Model):
    __tablename__ = 'comprador'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.String(100), default='buyer')
    nome_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    profile_image_path = db.Column(db.String(255))
    senha_hash = db.Column(db.String(300), nullable=False)
    status = db.Column(db.Boolean, default=True)
    random_hash = db.Column(db.String(400), nullable=False, unique=True)
    data_criado = db.Column(db.Date,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    pedidos = db.relationship('Pedido', backref='comprador', lazy=True)



class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    nome_usuario = db.Column(db.String(100), nullable=False, unique=True)
    profile_image_path = db.Column(db.String(255))
    senha_hash = db.Column(db.String(300), nullable=False)
    nome_food_truck = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True)
    random_hash = db.Column(db.String(400), nullable=False, unique=True)
    data_criado = db.Column(db.Date, default=datetime.utcnow)

    categoria = db.relationship('Categoria', backref='vendedor', lazy=True)
    produtos = db.relationship('Produto', backref='vendedor', lazy=True)
    totem = db.relationship('Totem', backref=db.backref('vendedor', lazy=True))  # Renomeado para totem



class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendedor_id = db.Column(db.String(300), db.ForeignKey('vendedor.random_hash'),nullable=False)
    nome_categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))  # Descrição da categoria

    # Relação com a tabela Produto
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendedor_id = db.Column(db.String(300), db.ForeignKey('vendedor.random_hash'),nullable=False)
    nome_produto = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(LONGTEXT)  # Descrição detalhada do produto
    editable_items = db.Column(JSON)  # Itens editáveis do produto
    cupons = db.Column(JSON)  # Cupons de desconto
    estoque = db.Column(db.Integer, default=0)  # Quantidade em estoque
    data_criado = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    status = db.Column(db.Boolean, default=True)  # Ativo ou inativo
    random_hash = db.Column(db.String(400), nullable=False, unique=True)  # Adicionando índice único aqui
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)  # Relacionamento com Categoria

    # Outras informações que podem ser úteis
    imagem_path = db.Column(db.String(255))  # URL da imagem do produto
    tempo_preparo = db.Column(db.Integer)  # Tempo de preparo em minutos


class Totem(db.Model):
    __tablename__ = 'totem'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(100), default='totem')
    name = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.String(400), db.ForeignKey('vendedor.random_hash'), nullable=False)
    random_hash = db.Column(db.String(400), nullable=False, unique=True)


class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.String(400), nullable=False, unique=True)  # ID do pedido no MercadoPago
    vendedor_id = db.Column(db.String(400), db.ForeignKey('vendedor.random_hash'), nullable=False)
    comprador_id = db.Column(db.String(400), db.ForeignKey('comprador.random_hash'), nullable=True)  # Chave estrangeira para Comprador
    nome_cliente = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.String(255))  # Observações do cliente
    status = db.Column(db.String(50))  # Ex: "pendente", "em preparação", "concluído"
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())



class ItemPedido(db.Model):
    __tablename__ = 'item_pedido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pedido_id = db.Column(db.String(400), db.ForeignKey('pedido.order_id'), nullable=False)
    produto_id = db.Column(db.String(400), db.ForeignKey('produto.random_hash'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)  # Quantidade do produto no pedido
    preco_unitario = db.Column(db.Float, nullable=False)  # Preço do produto no momento do pedido

    # Relação com Produto
    produto = db.relationship('Produto', backref='itens_pedido', lazy=True)










