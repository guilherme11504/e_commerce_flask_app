from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Carregando dotenv para variáveis de ambiente
load_dotenv()


# Variáveis de ambiente para conexão com o banco de dados
hostname = os.getenv('SQL_HOSTNAME')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('password')
password_encoded = quote_plus(password)
domain = "http://127.0.0.1:4000"
SECRET_KEY = os.getenv('SECRET_KEY')

class Config:
    SECRET_KEY = SECRET_KEY
    # URI do banco de dados com MySQL e PyMySQL
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password_encoded}@{hostname}/{database}'
    
    # Desativar modificações de rastreamento para melhorar desempenho
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_AUTO_FLUSH = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Pasta onde as imagens dos usuários serão armazenadas
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'user_images')

    # Configurações de extensão permitida para upload de imagens
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Configurações para o pool de conexões
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 20,           # Número máximo de conexões no pool
        "max_overflow": 10,        # Excesso de conexões além do pool_size
        "pool_timeout": 30,       # Tempo máximo para esperar por uma conexão disponível
        "pool_recycle": 3600,     # Tempo para reciclar (renovar) conexões
        "pool_pre_ping": True      
    }

    # Configurações do APScheduler
    SCHEDULER_API_ENABLED = True

    #Tentar fazer aceitar emojis
    JSON_AS_ASCII = False
