from flask_application import app
from flask import abort
import requests
import json
import os

CATALOG_SERVER = os.getenv("CATALOG_SERVER", "catalog-service")
CATALOG_PORT = 5000


@app.route('/purchase/<int:id>', methods=['GET'])
def purchase(id):

    response = requests.get(
        f'http://{CATALOG_SERVER}:{CATALOG_PORT}/query-by-item/{id}'
    )

    if response.status_code != 200:
        return "This book is not found!", response.status_code, response.headers.items()

    response_json = response.json()

    quantity = response_json.get("quantity")
    price = response_json.get("price")

    if quantity == 0:
        return (
            "There is no any more book to buy",
            response.status_code,
            response.headers.items()
        )

    data = {
        "quantity": quantity - 1,
        "price": price
    }

    response = requests.put(
        f'http://{CATALOG_SERVER}:{CATALOG_PORT}/update/{id}',
        data=json.dumps(data)
    )

    return response.text, response.status_code, response.headers.items()