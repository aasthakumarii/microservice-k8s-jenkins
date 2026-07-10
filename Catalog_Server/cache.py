import os
import requests

FRONTEND_SERVER = os.getenv("FRONTEND_SERVER", "frontend-service")
FRONTEND_PORT = 5002


def invalidate_item(book_id):

    response = requests.delete(
        f"http://{FRONTEND_SERVER}:{FRONTEND_PORT}/invalidate-item/{book_id}"
    )

    if response.status_code == 204:
        msg = "Book Invalidated (item/id)"
    else:
        msg = "Error! Cannot invalidate proxy (cache)"

    return (
        msg + "\n" + response.text,
        response.status_code,
        response.headers.items(),
    )


def invalidate_topic(book_topic):

    response = requests.delete(
        f"http://{FRONTEND_SERVER}:{FRONTEND_PORT}/invalidate-topic/{book_topic}"
    )

    if response.status_code == 204:
        msg = "Book Invalidated (topic)"
    else:
        msg = "Error! Cannot invalidate proxy (cache)"

    return (
        msg + "\n" + response.text,
        response.status_code,
        response.headers.items(),
    )