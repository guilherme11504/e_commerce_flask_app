from flask import Blueprint, render_template, redirect, url_for, request, session,current_app, flash, jsonify
from app.routes.api.products.controler import Controler
import os
from werkzeug.utils import secure_filename
from pathlib import Path

controler = Controler()

products_bp =Blueprint('products_bp', __name__)

def get_first_image_path(produto):
    # Caminho absoluto para a pasta de imagens do produto
    base_dir = Path(current_app.config['BASE_DIR']) / 'app' / 'static' / produto.imagem_path
    
    # Listar arquivos e filtrar para obter imagens (jpg, png, etc.)
    image_files = [f for f in base_dir.iterdir() if f.is_file() and f.suffix in ['.jpg', '.jpeg', '.png', '.gif', '.webp']]
    
    if image_files:
        # Retorna o caminho relativo da primeira imagem encontrada
        first_image_path = f"{produto.imagem_path}/{image_files[0].name}"
        return first_image_path
    else:
        # Opcional: caminho para uma imagem padrão caso não haja nenhuma imagem
        return "user_products/default.jpg"
    
def get_all_images_path(produto):
    # Caminho absoluto para a pasta de imagens do produto
    base_dir = Path(current_app.config['BASE_DIR']) / 'app' / 'static' / produto.imagem_path

    # Listar arquivos e filtrar para obter imagens (jpg, png, etc.)
    image_files = [f for f in base_dir.iterdir() if f.is_file() and f.suffix in ['.jpg', '.jpeg', '.png', '.gif', '.webp']]

    # Retorna os caminhos relativos de todas as imagens encontradas
    return [f"{produto.imagem_path}/{image_file.name}" for image_file in image_files]

# Registra como filtro no blueprint
products_bp.add_app_template_filter(get_all_images_path)

# Registra como filtro no blueprint
products_bp.add_app_template_filter(get_first_image_path)

@products_bp.route('/register_categoria', methods=['POST'])
def register_categoria():
    nome_categoria = request.form.get('nome_categoria')
    descricao = request.form.get('descricao')
    result = controler.register_categoria(nome_categoria, descricao)
    if not result:
        error_message = 'Erro ao cadastrar categoria'
        return redirect(url_for('main_bp.cadastrar_categorias_page'))
    
@products_bp.route('/register_product', methods=['POST'])
def register_product():
    nome_produto = request.form['nome_produto']
    preco = request.form['preco']
    descricao = request.form.get('descricao')
    estoque = request.form['estoque']
    categoria_id = request.form['categoria_id']
    cupons = request.form.getlist('cupons[]')
    itens_editaveis = request.form.getlist('itens_editaveis[]')
    tempo_preparo = request.form.get('tempo_preparo')
    imagens = request.files.getlist('imagens')  # Obtém a lista de arquivos

    print(f'formulario recebido: {request.form.to_dict()}')

    if len(imagens) > 5:
        error_message = "Você pode fazer upload de no máximo 5 imagens."
        return redirect(url_for('products_bp.register_product'))

    result = controler.register_product(nome_produto,preco,descricao,estoque,categoria_id,tempo_preparo,imagens,cupons,itens_editaveis)
    if not result:
        error_message = 'erro ao cadastrar produto'
        return redirect('cadastrar_produto_page',error_message=error_message)

    flash("Produto cadastrado com sucesso!")
    return redirect(url_for('main_bp.produtos'))


@products_bp.route('/edit_product', methods=['POST'])
def edit_product():
    nome_produto = request.form['nome_produto']
    preco = request.form['preco']
    descricao = request.form.get('descricao')
    estoque = request.form['estoque']
    categoria_id = request.form['categoria_id']
    cupons = request.form.getlist('cupons[]')
    itens_editaveis = request.form.getlist('itens_editaveis[]')
    tempo_preparo = request.form.get('tempo_preparo')
    product_id = request.form.get('product_id')
    imagens = request.files.getlist('imagens')  # Obtém a lista de arquivos

    if len(imagens) > 5:
        error_message = "Você pode fazer upload de no máximo 5 imagens."
        return redirect(url_for('products_bp.register_product'))
    
    result = controler.edit_product(nome_produto,preco,descricao,estoque,categoria_id,tempo_preparo,imagens,cupons,itens_editaveis,product_id)
    if not result:
        error_message = 'erro ao cadastrar produto'
        return redirect('cadastrar_produto_page',error_message=error_message)

    flash("Produto editado com sucesso!")
    return redirect(url_for('main_bp.produtos'))

@products_bp.route('/excluir_imagem', methods=['POST'])
def excluir_imagem():
    data = request.get_json()
    imagem = data.get('image')

    if imagem:
        try:
            # Caminho absoluto da imagem
            image_path = Path(current_app.config['BASE_DIR']) / 'app' / 'static' / imagem
            if image_path.exists():
                os.remove(image_path)
                return jsonify({"message": "Imagem excluída com sucesso."}), 200
            else:
                return jsonify({"message": "Imagem não encontrada."}), 404
        except Exception as e:
            return jsonify({"message": f"Erro ao excluir a imagem: {str(e)}"}), 500
    return jsonify({"message": "Dados inválidos."}), 400

