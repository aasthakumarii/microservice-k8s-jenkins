from flask_application import (
    app,
    abort,
    request,
    CATALOG_SERVER,
    ORDER_SERVER,
    CATALOG_PORT,
    ORDER_PORT
)

import requests
import json
from flask import jsonify

from cache import lookup_cache, search_cache, SearchEntry


# -----------------------------
# Search Books by Topic
# -----------------------------
@app.route('/search/<topic>', methods=['GET'])
def search_according_to_topic(topic):

    # Check cache first
    if topic in search_cache:
        print("\nResult fetched from search cache\n")
        return jsonify(search_cache.get(topic).search_result)

    response = requests.get(
        f"http://{CATALOG_SERVER}:{CATALOG_PORT}/query-by-subject/{topic}"
    )

    if response.status_code == 200:
        search_cache.insert(topic, SearchEntry(response.json()))
        print("\nSearch Cache Updated\n")

    return response.text, response.status_code, response.headers.items()


# -----------------------------
# Book Information
# -----------------------------
@app.route('/info/<id>', methods=['GET'])
def info_according_to_id(id):

    if not id.isnumeric():
        abort(422)

    cached_book = lookup_cache.get(int(id))

    if cached_book is not None:
        print("\nResult fetched from lookup cache\n")
        return cached_book

    response = requests.get(
        f"http://{CATALOG_SERVER}:{CATALOG_PORT}/query-by-item/{id}"
    )

    if response.status_code == 200:
        lookup_cache.insert(int(id), response.json())
        print("\nLookup Cache Updated\n")

    return response.text, response.status_code, response.headers.items()


# -----------------------------
# Purchase Book
# -----------------------------
@app.route('/purchase/<id>', methods=['PUT'])
def purchase(id):

    if not id.isnumeric():
        abort(422)

    response = requests.get(
        f"http://{ORDER_SERVER}:{ORDER_PORT}/purchase/{id}"
    )

    return response.text, response.status_code, response.headers.items()


# -----------------------------
# Update Book
# -----------------------------
@app.route('/edit/<id>', methods=['PUT'])
def edit(id):

    if not id.isnumeric():
        abort(422)

    data = request.json or {}

    if "quantity" not in data or "price" not in data:
        abort(400)

    response = requests.put(
        f"http://{CATALOG_SERVER}:{CATALOG_PORT}/updateInfo/{id}",
        data=json.dumps(data)
    )

    return response.text, response.status_code, response.headers.items()


# ---------------------------------------------------
# Cache Invalidation APIs
# ---------------------------------------------------

@app.route('/invalidate-item/<book_id>', methods=['DELETE'])
def invalidate_item(book_id):

    lookup_cache.remove(int(book_id))
    return "Cache invalidated (id)", 204


@app.route('/invalidate-topic/<book_topic>', methods=['DELETE'])
def invalidate_topic(book_topic):

    containing_entries = [
        key
        for key, value in search_cache.cache.items()
        if book_topic in value.topics
    ]

    for entry in containing_entries:
        search_cache.remove(entry)

    return "Cache invalidated (topic)", 204


# ---------------------------------------------------
# Debug Endpoint
# ---------------------------------------------------

@app.route('/show-all-caches/', methods=['GET'])
def dump():

    response = {
        "lookup": [
            {"Tag": id, **lookup_cache.cache[id]}
            for id in lookup_cache.lru_Q
        ],
        "search": [
            {
                "Tag": topic,
                "topics": list(search_cache.cache[topic].topics),
                "search_result": search_cache.cache[topic].search_result
            }
            for topic in search_cache.lru_Q
        ]
    }

    return response, 200