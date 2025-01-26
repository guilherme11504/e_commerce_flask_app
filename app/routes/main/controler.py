import os
from flask import url_for, session
from app import db
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

class Controler:

    def getProdutos(self):
        from app.models import Produto, Vendedor, Categoria
        user_hash = session['user_hash']
        produtos = db.session.query(Produto, Categoria).join(Categoria, Produto.categoria_id == Categoria.id).filter(Produto.vendedor_id == user_hash).all()
        return produtos
    
    def getCategories(self):
        from app.models import Produto, Vendedor, Categoria
        user_hash = session['user_hash']
        categorias = Categoria.query.filter_by(vendedor_id=user_hash).all()
        return categorias
    
    def getallprodutos(self, vendedor_hash):
        from app.models import Produto
        produtos = Produto.query.filter_by(vendedor_id=vendedor_hash).all()
        return produtos
    
    def get_product(self,  product_hash):
        from app.models import Produto
        produto = Produto.query.filter_by(random_hash=product_hash).first()
        return produto

    def getPedidos(self, user_id, user_type):
        from app.models import Pedido, ItemPedido, Vendedor, Produto, Pedido_status
        try:
            
            if user_type == 'seller':
                # Verifica se o vendedor existe
                seller = Vendedor.query.filter_by(random_hash=user_id).first()
                if not seller:
                    print("Seller not found")
                    return []

                # Subquery para obter o último status de cada pedido
                subquery = db.session.query(
                    Pedido_status.pedido_id,
                    func.max(Pedido_status.data_criado).label('last_update')
                ).group_by(
                    Pedido_status.pedido_id
                ).subquery()

                # Alias para o join com Pedido_status
                last_status = aliased(Pedido_status)

                # Faz o join entre as tabelas e retorna todos os campos
                pedidos = db.session.query(
                    Pedido,
                    ItemPedido,
                    Produto,
                    last_status
                ).join(
                    ItemPedido, Pedido.order_id == ItemPedido.pedido_id
                ).join(
                    Produto, ItemPedido.produto_id == Produto.random_hash
                ).outerjoin(
                    subquery, Pedido.order_id == subquery.c.pedido_id
                ).outerjoin(
                    last_status,
                    (last_status.pedido_id == subquery.c.pedido_id) &
                    (last_status.data_criado == subquery.c.last_update)
                ).filter(
                    Pedido.vendedor_id == user_id
                ).order_by(
                    Pedido.data_criacao.desc()
                ).all()

                parsed_pedidos = {}
                
                for pedido, item_pedido, produto, pedido_status in pedidos:
                    if pedido.order_id not in parsed_pedidos:
                        parsed_pedidos[pedido.order_id] = {
                            'order_id': pedido.order_id,
                            'comprador_nome': pedido.comprador_nome,
                            'tipo_pedido': pedido.tipo_pedido,
                            'total_pedido': pedido.total_pedido,
                            'observacoes': pedido.observacoes,
                            'status': pedido_status.status if pedido_status else None,
                            'data_criacao': pedido.data_criacao.strftime('%d-%m-%Y %H:%M:%S'),
                            'produtos': []
                        }
                    
                    # Caminho base real até a pasta static
                    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static'))
                    base_image_path = os.path.join(base_path, produto.imagem_path)

                    print(f"Base path: {base_path}")
                    print(f"Base image path from DB: {produto.imagem_path}")
                    print(f"Image folder path: {base_image_path}")

                    # Verifica se a pasta de imagens do produto existe
                    if os.path.isdir(base_image_path):
                        fotos = os.listdir(base_image_path)
                        if fotos:
                            first_image = fotos[0]
                            product_image_url = f"/static/{produto.imagem_path}/{first_image}"
                        else:
                            product_image_url = None
                    else:
                        product_image_url = None

                    print(f"Base image URL: {product_image_url}")

                    # Prevenir duplicação de itens
                    produto_id_set = set(parsed_pedidos[pedido.order_id].get('produto_ids', []))
                    if produto.random_hash not in produto_id_set:
                        produto_id_set.add(produto.random_hash)
                        parsed_pedidos[pedido.order_id]['produtos'].append({
                            'produto_id': produto.random_hash,
                            'nome_produto': produto.nome_produto,
                            'product_image': f"/static/{produto.imagem_path}/{os.listdir(base_image_path)[0]}" if os.path.isdir(base_image_path) else None,
                            'quantidade': item_pedido.quantidade,
                            'preco_unitario': item_pedido.preco_unitario,
                            'editable_items': item_pedido.editable_items,
                            'tempo_preparo': produto.tempo_preparo,
                            'pedido_id': pedido.order_id
                        })

                # Ordena os pedidos por data de criação
                sorted_pedidos = sorted(parsed_pedidos.values(), key=lambda x: x['data_criacao'], reverse=False)
                return sorted_pedidos

            else:
                print("User type not supported")
                return []
        except Exception as e:
            print(f"Exception occurred in getPedidos: {e}")
            return []
        
    def get_sellers_by_internal_category(self, categoria_id):
        from app.models import Vendedor, Categoria_loja
        sellers = Vendedor.query.filter_by(categoria_id=categoria_id).all()
        categoria = Categoria_loja.query.filter_by(id=categoria_id).first()
        if not sellers:
            return None, None
        return sellers, categoria