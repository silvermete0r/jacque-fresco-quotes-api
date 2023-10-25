from flask import Flask, request, jsonify, render_template
import json
import random

app = Flask(__name__)

API_KEYS = ('Sr1AQyAjphVgCYf829Pl', '8LGR56axDF6xI0JiQ4gt', '0SqVzqG1DfQz1cxham51', '6rZInaN22e0juVmr2iTE', 'oOn2dnNCYt1ulN1W1Xaw')

with open('data/quotes_base.json', 'r') as f:
    quotes_data = json.load(f)

with open('data/about_info.json', 'r') as f:
    bio_data = json.load(f)

@app.route('/')
@app.route('/docs')
def docs():
    return render_template('index.html')

@app.route('/bio')
@app.route('/info')
def info():
    return jsonify(bio_data)

@app.route('/quotes', methods=['GET'])
@app.route('/quotes/random', methods=['GET'])
def get_random_quote():
    api_key = request.args.get('api_key')
    if api_key not in API_KEYS:
        return jsonify({"error": "Unauthorized!"}), 401
    random_quote = random.choice(quotes_data)
    return jsonify(random_quote)

@app.route('/quotes/<int:quote_id>', methods=['GET'])
def get_quote_by_id(quote_id):
    api_key = request.args.get('api_key')
    if api_key not in API_KEYS:
        return jsonify({"error": "Unauthorized!"}), 401
    if 0 < quote_id <= len(quotes_data):
        return jsonify(quotes_data[quote_id-1])
    else:
        return jsonify({"error": "Quote not found!"}), 404

@app.route('/quotes/search', methods=['GET'])
def search_quotes():
    api_key = request.args.get('api_key')
    if api_key not in API_KEYS:
        return jsonify({"error": "Unauthorized!"}), 401
    query = request.args.get('query')
    if query:
        matching_quotes = [quote for quote in quotes_data if query.lower() in quote['tags']]
        return jsonify(matching_quotes)
    else:
        return jsonify({"error": "Please provide a query parameter!"}), 400

if __name__ == '__main__':
    app.run(debug=True)