import requests
import json
import qrcode
import sys

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

response = requests.post(url, headers=headers, data=payload)

if response.status_code == 200:
    response_data = response.json()
    qr_code_url = response_data.get("qr_code")  # Ajuste conforme o campo do JSON que contém o link do QR Code

    if qr_code_url:
        # Gerar o QR Code no terminal
        qr = qrcode.QRCode()
        qr.add_data(qr_code_url)
        qr.make()
        qr.print_ascii()  # Exibe o QR Code em ASCII no terminal
    else:
        print("URL do QR Code não encontrada na resposta.")
else:
    print(f"Erro na requisição: {response.status_code}")
    print(response.text)
