from flask import Blueprint, request
from app.routes.api.orders.controler import Controler
from flask import render_template, redirect, url_for, session,flash,jsonify

controler = Controler()

orders_bp = Blueprint('orders_bp', __name__)


@orders_bp.route('/api/order', methods=['POST'])
def create_order():
    data = request.get_json()
    print(f"Received data: {data}")
    
    total = data.get('total')
    client_name = data.get('client_name')
    order_type = data.get('order_type')
    observacoes = data.get('observacoes')
    products_list = data.get('products')
    vendedor_id = data.get('vendedor_id')
    
    print(f"Total: {total}")
    print(f"Client Name: {client_name}")
    print(f"Order Type: {order_type}")
    print(f"Observacoes: {observacoes}")
    print(f"Products List: {products_list}")
    
    result = controler.make_order(total, client_name, order_type, observacoes, products_list,vendedor_id)
    print(f"Order creation result: {result}")
    
    if result:
        return jsonify({'message': 'Order created'}), 201
    else:
        return jsonify({'message': 'Error'}), 400
    

#criando rotas para marcar o pedido como pronto, preparando, cancelado ou pendente

@orders_bp.route('/api/order/status', methods=['GET'])
def change_order_status():
    
    order_id = request.args.get('order_id')
    status = request.args.get('status')
    
    print(f"Order ID: {order_id}")
    print(f"Status: {status}")
    
    result = controler.change_order_status(order_id, status)
    print(f"Order status change result: {result}")
    
    if result:
        return redirect(url_for('main_bp.pedidos'))
    else:
        return jsonify({'message': 'Error'}), 400