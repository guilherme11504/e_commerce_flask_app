import requests
import json

url = "https://api.mercadopago.com/instore/orders/qr/seller/collectors/2075683624/pos/12345678/qrs"

payload = {
    "external_reference": "reference_12345",
    "title": "Product order",
    "description": "Purchase description.",
    "notification_url": "https://348f-2804-14c-e8-337d-9591-d582-d791-2437.ngrok-free.app/notifications",
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
    "sponsor": {
        "id": 662208785
    },
    "cash_out": {
        "amount": 0
    }
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer APP_USR-5145734205278909-110721-eac6b44452def99e0f15b41f850b0a4b-2075683624"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.status_code)
print(response.json())
