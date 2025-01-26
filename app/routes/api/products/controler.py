from app import db
import random
import string
from flask import session, current_app
import os
from werkzeug.utils import secure_filename
import random
import string
from pathlib import Path


class Controler:

    def gerar_hash(self, tamanho=16):
        caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e dígitos
        hash_aleatorio = ''.join(random.choice(caracteres) for _ in range(tamanho))
        return hash_aleatorio
    

    def register_categoria(self, nome_categoria, descricao):
        from app.models import Categoria
        try:
            user_hash = session['user_hash']
            if not nome_categoria or not descricao:
                return False
            categoria = Categoria(
                vendedor_id=user_hash,
                nome_categoria=nome_categoria,
                descricao=descricao
            )
            db.session.add(categoria)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False
        
    def register_product(self, nome_produto, preco, descricao, estoque, categoria, tempo_prep, imagens,cupons,itens_editaveis):
        from app.models import Produto
        user_hash = session['user_hash']
        product_hash = self.gerar_hash()  # Gere ou obtenha um ID único para o produto
        
        # Diretório relativo a partir de 'static'
        relative_path = f'user_products/{user_hash}/{product_hash}'
        # Caminho absoluto para o diretório do produto
        base_dir = Path(current_app.config['BASE_DIR']) / 'app' / 'static' / relative_path
        print(f"Tentando criar o diretório: {base_dir}")

        # Tenta criar o diretório
        try:
            base_dir.mkdir(parents=True, exist_ok=True)
            print(f"Diretório criado com sucesso: {base_dir}")
        except Exception as e:
            print(f"Erro ao criar o diretório {base_dir}: {e}")
            return False

        # Salvando as imagens no diretório criado
        for imagem in imagens:
            if imagem and imagem.filename != '':
                filename = secure_filename(imagem.filename)
                try:
                    imagem.save(base_dir / filename)
                    print(f"Imagem salva com sucesso: {base_dir / filename}")
                except Exception as e:
                    print(f"Erro ao salvar a imagem {filename}: {e}")

        # Salvando apenas o caminho da pasta no banco de dados
        try:
            produto = Produto(
                vendedor_id=user_hash,
                nome_produto=nome_produto,
                preco=preco,
                descricao=descricao,
                estoque=estoque,
                cupons=cupons,
                editable_items=itens_editaveis,
                categoria_id=categoria,
                imagem_path=relative_path,  # Apenas o caminho da pasta
                random_hash=product_hash,
                tempo_preparo=tempo_prep
            )
            db.session.add(produto)
            db.session.commit()
            print(f"Produto '{nome_produto}' registrado com sucesso!")
            return True
        except Exception as e:
            print(f'Erro ao inserir produto: {e}')
            db.session.rollback()

    def edit_product(self, nome_produto, preco, descricao, estoque, categoria, tempo_prep, imagens, cupons, itens_editaveis, product_id):
        from app.models import Produto
        user_hash = session['user_hash']

        # Diretório relativo a partir de 'static'
        relative_path = f'user_products/{user_hash}/{product_id}'
        # Caminho absoluto para o diretório do produto
        base_dir = Path(current_app.config['BASE_DIR']) / 'app' / 'static' / relative_path
        
        # Criar o diretório se ele não existir
        if not os.path.exists(base_dir):
            try:
                os.makedirs(base_dir)
                print(f"Diretório criado com sucesso: {base_dir}")
            except Exception as e:
                print(f"Erro ao criar o diretório: {e}")
                return False

        # Salvando as imagens no diretório criado
        for imagem in imagens:
            if imagem and imagem.filename != '':
                filename = secure_filename(imagem.filename)
                try:
                    imagem.save(base_dir / filename)
                    print(f"Imagem salva com sucesso: {base_dir / filename}")
                except Exception as e:
                    print(f"Erro ao salvar a imagem {filename}: {e}")
                    return False

        try:
            produto = Produto.query.filter_by(random_hash=product_id).first()
            produto.nome_produto = nome_produto
            produto.preco = preco
            produto.descricao = descricao
            produto.estoque = estoque
            produto.cupons = cupons
            produto.editable_items = itens_editaveis
            produto.categoria_id = categoria
            produto.tempo_preparo = tempo_prep
            db.session.commit()
            return True
        except Exception as e:
            print(f'Erro ao editar produto: {e}')
            db.session.rollback()
            return False





        

