from flask import Flask, request, abort
import os

app = Flask(__name__)

# Kubernetes/Docker service names
CATALOG_SERVER = os.getenv("CATALOG_SERVER", "catalog-service")
ORDER_SERVER = os.getenv("ORDER_SERVER", "order-service")

CATALOG_PORT = 5000
ORDER_PORT = 5001