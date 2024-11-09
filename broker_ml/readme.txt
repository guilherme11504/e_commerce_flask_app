API Mensageiro
Visão Geral
O seleniumBroker é um módulo Python que roda em Flask, projetado para transformar diferentes tipos de mensagens em objetos padronizados. Este módulo é dividido em filas (queues) para gerenciar a mensagem recebida e possui um executor para facilitar a conexão com a própria API.
O intuito foi facilitar a comunicação dos mensageiros baseados em webdrivers, facilitando o escalamento e linkando diretamente com as requisições.

Funcionalidades
Recepção de Mensagens: Recebe mensagens de diferentes tipos e formatos.
Transformação de Mensagens: Converte as mensagens recebidas em objetos padronizados.
Filas (Queues): Gerencia a ordem e o processamento das mensagens recebidas.
Executor: Facilita a conexão e comunicação com o broker.


Instale as dependências:

pip install -r requirements.txt


Iniciando o Servidor
Para iniciar o servidor Flask, execute:

python app.py

Para facilitar a execução do próprio executor, somente 2 endpoints existem e a ação depende do payload enviado.

Todos os payloads podem ser enviados com mais facilidade pelo executor.py

A porta padrão é 1446.

É altamente recomendável o uso de gunicorn ou algum servidor de WSGI.


seleniumBroker/
│
├── app.py            # Ponto de entrada principal do Flask
├── executor.py       # Módulo executor para facilitar a conexão com o broker
├── message.py  # Módulo de gerenciador de filas e mensagens
├── gun.py # Módulo de integração com o gunicorn
├── answertest.py # Módulo de teste e debugging
├── requirements.txt  # Dependências do projeto
└── readme.txt         # Este arquivo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests no repositório.
