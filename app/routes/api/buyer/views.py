from flask import Blueprint, request
from app.routes.api.buyer.controler import Controler
from flask import render_template, redirect, url_for, session,flash
from app.models import *

controler = Controler()

buyer_bp = Blueprint('buyer_bp', __name__)


@buyer_bp.route('/buyer_home', methods=['GET'])
def buyer_home():
    sellers = controler.get_sellers()
    categorias = controler.get_categorias()
    print(f'categorias: {categorias}')
    return render_template('buyer_home.html', sellers=sellers, categorias=categorias)


@buyer_bp.route('/seller_store', methods=['GET'])
def seller_store():
    seller_hash = request.args.get('seller_hash')
    seller = controler.get_seller(seller_hash)
    products = controler.get_products(seller_hash)

    return render_template('client_menu.html',vendedor=seller, produtos=products)

@buyer_bp.route('/api/get_user_info', methods=['GET'])
def get_user_info():
    user_hash = session['user_hash']
    user_info = controler.get_user_info(user_hash)
    return user_info