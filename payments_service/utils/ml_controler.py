import requests
from datetime import datetime, timedelta  
import os
import json


class ML:
        urls = {
            "query_message":"https://api.mercadolibre.com/messages/{}?tag=post_sale&mark_as_read = false",
            'send_message': 'https://api.mercadolibre.com/messages/packs/{}/sellers/{}?tag=post_sale',
            'send_attachment': 'https://api.mercadolibre.com/messages/attachments?tag=post_sale&site_id=MLB',
            "user_id": "https://api.mercadolibre.com/users/me",
            "query_claim":"https://api.mercadolibre.com/post-purchase{}",
            "send_claim_message":"https://api.mercadolibre.com/post-purchase/v1/claims/{}/actions/send-message",
            "reasons":"https://api.mercadolibre.com/post-purchase/v1/claims/reasons/{}"
        }

        def __init__(self, access_token):
            self.app_path = os.path.abspath(os.path.dirname("app"))
            self.access_token = access_token
            self.headers = {
                  'Authorization': 'Bearer {}'.format(self.access_token),
                    'Content-Type': 'application/json'
            }
            print(self.headers)
            print(f"App path: {self.app_path}")

        def getUserID(self):
            response = requests.get(self.urls['user_id'], headers=self.headers)
            print(response)
            return response.json()['id']
        
        def create_user_directory(self, path):
             path = str(path)
             if not os.path.exists(path):
                 os.makedirs(path)
        
        def save_message(self, venda_id, message, user_id):
            # Define o caminho do arquivo JSON consolidado
            path = os.path.join(self.app_path, str(user_id))
            if not os.path.exists(path):
                self.create_user_directory(user_id)

            arquivo_json = os.path.join(path, f"{venda_id}.json")
            
            # Inicializa a estrutura padrão apenas se o arquivo não existir
            if not os.path.exists(arquivo_json):
                dados_venda = {"claims": {}, "internal_comments": [], "messages": []}
            else:
                # Carrega o conteúdo existente do JSON
                with open(arquivo_json, "r", encoding="utf-8-sig") as file:
                    dados_venda = json.load(file)
                    
                    # Garante que todas as chaves existam, caso estejam faltando
                    if "claims" not in dados_venda:
                        dados_venda["claims"] = {}
                    if "internal_comments" not in dados_venda:
                        dados_venda["internal_comments"] = []
                    if "messages" not in dados_venda:
                        dados_venda["messages"] = []

            # Verifica se a mensagem já está presente na lista "messages" pelo ID
            message_ids = {msg["id"] for msg in dados_venda["messages"]}
            if message["id"] not in message_ids:
                # Adiciona a nova mensagem à lista de mensagens se ainda não existir
                dados_venda["messages"].append(message)
            else:
                # Se a mensagem já existe, retorna uma mensagem indicando que foi ignorada
                return "Mensagem já existente, ignorada"

            # Identifica o último remetente e conta mensagens pendentes, se aplicável
            vendedor_id = user_id  # ID do vendedor, conhecido
            ultima_mensagem_vendedor_idx = -1
            mensagens_pendentes = 0
            
            # Itera sobre as mensagens em ordem reversa para encontrar a última mensagem do vendedor
            for i in range(len(dados_venda["messages"]) - 1, -1, -1):
                msg = dados_venda["messages"][i]
                remetente_id = msg["from"]["user_id"]

                if remetente_id == vendedor_id:
                    # Encontrou a última mensagem do vendedor
                    ultima_mensagem_vendedor_idx = i
                    break

            # Verifica se há mensagens do comprador desde a última mensagem do vendedor
            if ultima_mensagem_vendedor_idx == -1:
                # Se não houver mensagem do vendedor, conta todas as mensagens do comprador como pendentes
                mensagens_pendentes = sum(1 for msg in dados_venda["messages"] if msg["from"]["user_id"] != vendedor_id)
            else:
                # Conta apenas as mensagens do comprador desde a última mensagem do vendedor
                mensagens_pendentes = sum(1 for i in range(ultima_mensagem_vendedor_idx + 1, len(dados_venda["messages"]))
                                        if dados_venda["messages"][i]["from"]["user_id"] != vendedor_id)

            # Adiciona o número de mensagens pendentes ao primeiro nível do JSON
            if mensagens_pendentes > 0:
                dados_venda["mensagens_pendentes"] = mensagens_pendentes
            else:
                # Remove a chave se não houver mensagens pendentes
                if "mensagens_pendentes" in dados_venda:
                    del dados_venda["mensagens_pendentes"]


            # Salva o JSON atualizado com a nova mensagem e o contador de mensagens pendentes
            with open(arquivo_json, "w", encoding="utf-8-sig") as file:
                json.dump(dados_venda, file, indent=4, ensure_ascii=False)

            # Retorna o status da operação
            return "Mensagem salva com sucesso"



        
        def get_message(self, message_id):
                response = requests.get(self.urls['query_message'].format(message_id), headers=self.headers)
                return response.json()
        
        def send_message(self, order_id, receiver_id, message, attachments):
            # Obtém o user_id do remetente
            user_id = self.getUserID()
            
            # Cria o corpo da requisição
            data = {
                "from": {
                    "user_id": user_id
                },
                "to": {
                    "user_id": receiver_id
                },
                "text": message
            }
            
            # Adiciona os anexos, se houver
            if attachments:
                data["attachments"] = attachments

            # URL da requisição - ajustada conforme a documentação
            url = self.urls['send_message'].format(order_id, user_id)
            
            # Envia a requisição POST usando os headers que já estão no self.headers
            response = requests.post(url, headers=self.headers, json=data)
            

            # Verifica o status da resposta
            responsejson = response.json()
            self.save_message(order_id, responsejson, user_id)
            return responsejson
        
        def send_claim_message(self, claim_id, message, attachments,receiver_role):
            url = self.urls['send_claim_message'].format(claim_id)
            payload = {
                "message": message,
                "receiver_role": receiver_role
            }
            if attachments:
                payload['attachments'] = attachments
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return response.text
            
        
        def get_claim(self, claim_resource):
            url = self.urls['query_claim'].format(claim_resource)
            print(f"URL: {url}")
            response = requests.get(url, headers=self.headers)
            return response.json()
        
        def get_claim_details(self, claim_resource):
            url = self.urls['query_claim'].format(claim_resource) + "/detail"
            print(f"URL: {url}")
            response = requests.get(url, headers=self.headers)
            return response.json()
        
        def get_claim_actions_history(self, claim_resource):
            url = self.urls['query_claim'].format(claim_resource) + "/actions-history"
            print(f"URL: {url}")
            response = requests.get(url, headers=self.headers)
            return response.json()
        
        def get_claim_status_history(self, claim_resource):
            url = self.urls['query_claim'].format(claim_resource) + "/status-history"
            print(f"URL: {url}")
            response = requests.get(url, headers=self.headers)
            return response.json()
        
        def get_claim_reputation_info(self, claim_resource):
            url = self.urls['query_claim'].format(claim_resource) + "/affects-reputation"
            print(f"URL: {url}")
            response = requests.get(url, headers=self.headers)
            return response.json()
        
        def get_claim_messages(self, claim_resource):
            url = self.urls['query_claim'].format(claim_resource) + "/messages"
            print(f"URL: {url}")
            response = requests.get(url, headers=self.headers)
            return response.json()
        
        def get_reason_details(self, reason_id):
            url = self.urls['reasons'].format(reason_id)
            response = requests.get(url, headers=self.headers)
            return response.json()
        
