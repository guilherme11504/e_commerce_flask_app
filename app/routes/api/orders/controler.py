from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import random
import string
from flask import session, current_app
import os
from datetime import datetime


class Controler:

    def make_order(self, total, client_name, order_type, observacoes, products_list,vendedor_id):
        try:
            from app.models import Pedido, ItemPedido,Pedido_status, Comprador
            if not vendedor_id:
                return False
            buyer_id = session.get('totem_hash')
            print(f"buyer_id: {buyer_id}")
            user_type = session.get('user_type')
            print(f"user_type: {user_type}")
            order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            print(f"order_id: {order_id}")
            if user_type != 'totem':
                buyer_id = session.get('user_hash')
                comprador = Comprador.query.filter_by(random_hash=buyer_id).first()
                if not comprador:
                    return False
                buyer_name = comprador.nome_completo
                print(f"buyer_id (user_hash): {buyer_id}")
                order = Pedido(
                    order_id=order_id,
                    vendedor_id=vendedor_id,
                    comprador_id=buyer_id,
                    comprador_nome=buyer_name,
                    tipo_pedido=order_type, 
                    total_pedido=total,
                    observacoes=observacoes,
                    data_criacao=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )
            else:
                order = Pedido(
                    order_id=order_id,
                    vendedor_id=vendedor_id,
                    totem_id=buyer_id,
                    comprador_nome=client_name,
                    tipo_pedido=order_type, 
                    total_pedido=total,
                    observacoes=observacoes,
                    data_criacao=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )
            
            db.session.add(order)
            db.session.commit()
            print(f"Order added: {order}")
            pedido_status = Pedido_status(pedido_id=order_id, status='Pendente')
            db.session.add(pedido_status)
            for product in products_list:
                item = ItemPedido(pedido_id=order_id, produto_id=product.get('id'), quantidade=product.get('quantity'), preco_unitario=product.get('price'), editable_items=product.get('editableItems'))
                db.session.add(item)
                print(f"Item added: {item}")
            db.session.commit()
            print("Order committed successfully")
            return True
        except Exception as e:
            print(f"Exception: {e}")
            return False
        
    def change_order_status(self, order_id, status):
        try:
            from app.models import Pedido_status, Vendedor, Pedido
            user = session.get('user_hash')
            if not user:
                return False
            user_data = Vendedor.query.filter_by(random_hash=user).first()
            if not user_data:
                return False
            order = Pedido.query.filter_by(order_id=order_id).first()
            if not order:
                return False
            if order.vendedor_id != user_data.random_hash:
                return False       
            new_status = Pedido_status(pedido_id=order_id, status=status)
            db.session.add(new_status)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Exception: {e}")
            return False