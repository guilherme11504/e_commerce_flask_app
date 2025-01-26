from flask import Blueprint, request, jsonify
from app.routes.api.payments.controler import Controler
from flask import render_template, redirect, url_for, session
import requests
import json
import qrcode
import io
import base64
import random
import mercadopago

controler = Controler()

payments_bp = Blueprint('payments_bp', __name__)

sdk = mercadopago.SDK("APP_USR-8041984352821246-121422-a3147d932ebe09a272a87fa8094877bd-204338743")


@payments_bp.route('/notification', methods=['POST'])
def notification():
    notification = request.json
    controler.receive_notification(notification)
    return 'OK', 200

@payments_bp.route('/generate_qr', methods=['POST'])
def generate_qr():
    url = "https://api.mercadopago.com/instore/orders/qr/seller/collectors/2075683624/pos/12345678/qrs"

    payload = json.dumps({
        "external_reference": "reference_12345",
        "title": "Product order",
        "description": "Purchase description.",
        "notification_url": "https://bf8b-2804-14c-e8-337d-2859-8fe6-ceba-7eb6.ngrok-free.app/notifications",
        "total_amount": 100,
        "items": [
            {
                "sku_number": "A123K9191938",
                "category": "marketplace",
                "title": "Point Mini",
                "description": "This is the Point Mini",
                "unit_price": 100,
                "quantity": 1,
                "unit_measure": "unit",
                "total_amount": 100
            }
        ],
        "cash_out": {
            "amount": 0
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer APP_USR-5145734205278909-110721-eac6b44452def99e0f15b41f850b0a4b-2075683624'
    }

    # Faz a requisição para o MercadoPago para obter o URL do QR Code
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        response_data = response.json()
        qr_code_url = response_data.get("qr_code")  # Ajuste este campo conforme a resposta da API

        if qr_code_url:
            # Gera o QR Code como imagem
            qr = qrcode.make(qr_code_url)
            buffered = io.BytesIO()
            qr.save(buffered, format="PNG")
            qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # Retorna o QR Code em base64 para o frontend
            return jsonify({"qr_code": qr_code_base64})

        else:
            return jsonify({"error": "URL do QR Code não encontrada na resposta."}), 400
    else:
        return jsonify({"error": "Erro na requisição para o MercadoPago.", "details": response.text}), response.status_code
    
@payments_bp.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    data = request.json
    print(data)
    return jsonify(data), 200


@payments_bp.route('/pagamento', methods=['GET'])
def pagamento():
    return render_template('payment_screen.html')

@payments_bp.route('/process_payment', methods=['POST'])
def make_payment():

    data = request.json
    print(data)
    payment_data = {
        "transaction_amount": float(data.get("transaction_amount")),
        "token": data.get("token"),
        "description": data.get("description"),
        "installments": int(data.get("installments")),
        "payment_method_id": data.get("payment_method_id"),
        "payer": {
            "email": data.get("cardholderEmail"),
            "identification": {
                "type": data.get("identificationType"),
                "number": data.get("identificationNumber")
            },
            "first_name": data.get("cardholderName")
        },
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    print(payment)



