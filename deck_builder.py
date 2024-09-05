from mtgsdk import Card

import requests
import random


def fetch_commander(name):
    results = Card.where(name=name).all()
    if not results:
        print(f"No results found for '{name}'")
        return None
    
    for card in results:
        print(f"Found card: {card.name} - Types: {card.type}")
        # Ensure the card is a legendary creature or planeswalker suitable for commander
        if 'Legendary' in card.type and ('Creature' in card.type or 'Planeswalker' in card.type):
            return card
    
    print(f"No valid commander found for '{name}'")
    return None

def fetch_lands(color_identity, count):
    lands = []
    
    # Basic land mapping based on color identity
    color_to_basic_land = {
        'W': 'Plains',
        'U': 'Island',
        'B': 'Swamp',
        'R': 'Mountain',
        'G': 'Forest'
    }
    
    # Add basic lands to the deck
    basics_per_color = count // len(color_identity)
    for color in color_identity:
        basic_land_name = color_to_basic_land.get(color)
        for _ in range(basics_per_color):
            lands.append(basic_land_name)

    # Fetch non-basic lands using the MTG API
    needed = count - len(lands)
    if needed > 0:
        url = "https://api.magicthegathering.io/v1/cards"
        params = {
            'type': 'Land',
            'pageSize': 100
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            non_basic_lands = response.json().get('cards', [])
            random.shuffle(non_basic_lands)
            for card in non_basic_lands:
                if len(lands) < count:
                    lands.append(card['name'])
    return lands

def fetch_ramp_cards(color_identity, count):
    ramp_cards = []
    query = Card.where(color_identity=''.join(color_identity)).where(types='Artifact,Creature').where(game_format='Commander')
    
    # Common ramp keywords
    ramp_keywords = ['add mana', 'search your library for a land', 'search your library for a basic', ]
    
    query = Card.where(color_identity=''.join(color_identity)).where(types='Artifact,Creature').where(game_format='Commander')
    print(query)
    results = query.all()
    random.shuffle(results)
    added = set()
    for card in results:
        if len(ramp_cards) >= count:
            break
        text = card.text or ''
        if any(keyword in text.lower() for keyword in ramp_keywords):
            if card.name not in added:
                ramp_cards.append(card.name)
                added.add(card.name)
    
    return ramp_cards

def fetch_card_draw_cards(color_identity, count):
    card_draw = []
    query = Card.where(color_identity=''.join(color_identity)).where(game_format='Commander')
    
    draw_keywords = ['draw a card', 'draw cards', 'equal to', 'discard and draw']
    
    results = query.all()
    random.shuffle(results)
    added = set()
    for card in results:
        if len(card_draw) >= count:
            break
        text = card.text or ''
        if any(keyword in text.lower() for keyword in draw_keywords):
            if card.name not in added:
                card_draw.append(card.name)
                added.add(card.name)
    
    return card_draw

def fetch_removal_cards(color_identity, count):
    removal_cards = []
    query = Card.where(color_identity=''.join(color_identity)).where(game_format='Commander')
    
    removal_keywords = ['destroy target', 'exile target', 'remove target', 'counter target']
    
    results = query.all()
    random.shuffle(results)
    added = set()
    for card in results:
        if len(removal_cards) >= count:
            break
        text = card.text or ''
        if any(keyword in text.lower() for keyword in removal_keywords):
            if card.name not in added:
                removal_cards.append(card.name)
                added.add(card.name)
    
    return removal_cards

def fetch_board_wipes(color_identity, count):
    board_wipes = []
    query = Card.where(color_identity=''.join(color_identity)).where(game_format='Commander')
    
    wipe_keywords = ['destroy all', 'exile all', 'each creature', 'all creatures']
    
    results = query.all()
    random.shuffle(results)
    added = set()
    for card in results:
        if len(board_wipes) >= count:
            break
        text = card.text or ''
        if any(keyword in text.lower() for keyword in wipe_keywords):
            if card.name not in added:
                board_wipes.append(card.name)
                added.add(card.name)
    
    return board_wipes

def fetch_synergistic_cards(commander, color_identity, count):
    synergistic_cards = []
    query = Card.where(color_identity=''.join(color_identity)).where(game_format='Commander')
    
    # Identify keywords from commander
    commander_text = commander.text or ''
    commander_types = commander.types or []
    keywords = commander_text.lower().split()
    types = commander_types
    
    results = query.all()
    random.shuffle(results)
    added = set()
    for card in results:
        if len(synergistic_cards) >= count:
            break
        text = card.text or ''
        card_types = card.types or []
        # Simple synergy check: shared keywords or types
        if any(word in text.lower() for word in keywords) or any(t in card_types for t in types):
            if card.name not in added:
                synergistic_cards.append(card.name)
                added.add(card.name)
    
    return synergistic_cards

def compile_deck(deck_parts):
    deck = []
    deck.append(deck_parts['Commander'].name)
    deck.extend(deck_parts['Lands'])
    #deck.extend(deck_parts['Ramp'])
    #deck.extend(deck_parts['Card_Draw'])
    #deck.extend(deck_parts['Removal'])
    #deck.extend(deck_parts['Board_Wipes'])
    #deck.extend(deck_parts['Synergistic'])



    print(f"Compiled deck: {deck}")
    return deck

def validate_deck(deck):
    if len(deck) != 100:
        print(f"Deck size is {len(deck)} cards, adjusting...")
        # Logic to add or remove cards to make the deck 100 cards