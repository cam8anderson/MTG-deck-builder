from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from mtgsdk import Card
from deck_builder import (fetch_commander, fetch_lands, fetch_ramp_cards, fetch_synergistic_cards, 
                          fetch_card_draw_cards, fetch_board_wipes, fetch_removal_cards, compile_deck)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    card_name = request.form.get('card_name')
    cards = Card.where(name=card_name).all()

    card_list = []
    for card in cards:
        card_data = {
            'name': card.name,
            'mana_cost': card.mana_cost,
            'type': card.type,
            'set_name': card.set_name,
            'text': card.text,
            'image_url': card.image_url
        }
        card_list.append(card_data)

    return render_template('home.html', cards=card_list)

@app.route('/select_commander', methods=['GET'])
def select_commander():
    commander_name = request.args.get('name')
    commander = fetch_commander(commander_name)
    if commander:
        session['commander'] = commander_name
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/deck')
def deck():
    commander_name = session.get('commander')
    if not commander_name:
        return redirect(url_for('home'))
    
    commander = fetch_commander(commander_name)
    color_identity = commander.color_identity if commander else []
    deck = {'Commander': commander}

    deck['Lands'] = fetch_lands(color_identity, 37)
    deck['Ramp'] = fetch_ramp_cards(color_identity, 10)
    deck['Card_Draw'] = fetch_card_draw_cards(color_identity, 10)
    #deck['Removal'] = fetch_removal_cards(color_identity, 5)
    #deck['Board_Wipes'] = fetch_board_wipes(color_identity, 5)
    #deck['Synergistic'] = fetch_synergistic_cards(commander, color_identity, 32)
#
    full_deck = compile_deck(deck)

    

    return render_template('deck.html', deck=deck, full_deck=full_deck)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
