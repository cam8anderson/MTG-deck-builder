from mtgsdk import Card

card_name = 'Yuma'
cards = Card.where(name=card_name).all()

if cards:
    card = cards[0]
    print(f"Name: {card.name}")
    print(f"Mana Cost: {card.mana_cost}")
    print(f"Type: {card.type}")
    print(f"Set: {card.set_name}")
    print(f"Text: {card.text}")
    print(f"Image URL: {card.image_url}")
else:
    print(f"No cards found with name '{card_name}'")