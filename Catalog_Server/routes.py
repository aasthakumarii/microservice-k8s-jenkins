from book import info, search, update, updateInfo
from flask_application import app, request, abort
import json
import requests

from cache import invalidate_item, invalidate_topic

# Get info about a book
def get_info(book_id):
	return info(book_id)


# Get all books about specific subject/topic
def get_books_related_to_topic(book_topic):
	return search(book_topic)


# The queries is only two categories, query-by-item & query-by-subject
queries = {
	'query-by-item': {
		'function': get_info
	},
	'query-by-subject': {
		'function': get_books_related_to_topic
	}
}


# Get query and filter it
@app.route('/<string:query>/<parameter>', methods=['GET'])
def queryFromDB(query, parameter):
	# If query is not in two categories
	if query not in queries:
		return 'Invalid query method has been called called', 404
	
	# Get the procedure from dictionary then call it
	return queries[query]['function'](parameter)


# Update an book (Decrease quantity) according to specific ID
@app.route('/update/<book_id>', methods=['PUT'])
def update_book(book_id):

	if request is None:
		abort(400)

	data_json = json.loads(request.data)

	# If there is no quantity key in PUT method => Bad request
	if data_json.get('quantity') is None:
		abort(400)

	quantity = data_json.get('quantity')

	try:
		# invalidate data in the caches in front-end
		book = info(book_id)
		invalidate_item(book_id)
		invalidate_topic(json.loads(book).get('topic'))
		print('\nCache (proxy) invalidated!\n')
	except: 
		return 'can not invalidate book!'
	
	book = update(book_id, quantity)
		
	return book


# Update an book (Quantity and Cost) according to specific ID
@app.route('/updateInfo/<book_id>', methods=['PUT'])
def updateInfo_book(book_id):

	if request is None:
		abort(400)

	data = json.loads(request.data)
	
	if data is None:
		data = {}

	if data.get('quantity') is None or data.get('price') is None:
		abort(400)

	try:
		# invalidate data in the caches in front-end
		book = info(book_id)
		invalidate_item(book_id)
		invalidate_topic(json.loads(book).get('topic'))
		print('\nCache (proxy) invalidated!\n')
	except: 
		return 'Cannot invalidate book !'

	book = updateInfo(book_id, data.get('quantity'), data.get('price'))
		
	return book



