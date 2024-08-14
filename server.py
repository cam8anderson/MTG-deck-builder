from flask import (Flask, render_template, request, jsonify)
from mtgsdk import Card

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    card_name = request.form.get('card_name')
    cards = Card.where(name=card_name).all()


    card_list = []
    unique_cards = set()

    for card in cards:
         if card.name not in unique_cards:
            card_data = {
                'name': card.name,
                'mana_cost': card.mana_cost,
                'type': card.type,
                'set_name': card.set_name,
                'text': card.text,
                'image_url': card.image_url
            }
            card_list.append(card_data)
            unique_cards.add(card.name)

    return render_template('home.html', cards=card_list)

@app.route('/get_cards', methods=['GET'])
def get_cards():
    query = request.args.get('query')
    
    if query:
        cards = Card.where(name=query).all()
        cards_list = []
        for card in cards:
            cards_list.append({
                'name': card.name,
                'mana_cost': card.mana_cost,
                'type': card.type,
                'set_name': card.set_name,
                'text': card.text,
                'image_url': card.image_url
            })
        return jsonify(cards_list)
    else:
        return jsonify({'error': 'No query parameter provided'}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)