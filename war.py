import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, value) for suit in suits for value in values]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def play_card(self):
        return self.hand.pop(0) if self.hand else None

class Game:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player("Player 1"), Player("Player 2")]
        self.deck.shuffle()

    def print_status(self):
        size_player1 = len(self.players[0].hand)
        size_player2 = len(self.players[1].hand)

        if size_player1 > size_player2:
            print(f"Player 1 is leading with {size_player1} cards against {size_player2} cards of Player 2")
        elif size_player2 > size_player1:
            print(f"Player 2 is leading with {size_player2} cards against {size_player1} cards of Player 1")
        else:
            print(f"Both players have the same number of cards: {size_player1}")

    def start_game(self):
        # Divide the deck between two players
        while self.deck.cards:
            self.players[0].add_card(self.deck.deal())
            self.players[1].add_card(self.deck.deal())

        # Begin rounds
        while self.players[0].hand and self.players[1].hand:
            print("---")
            self.print_status()  # Printing the current status
            print("---")
            input("Press Enter to play the next round...")
            print("---")
            self.play_round()

    def play_round(self):
        card1 = self.players[0].play_card()
        card2 = self.players[1].play_card()

        print(f"Player 1 plays: {card1}")
        print(f"Player 2 plays: {card2}")

        if self.card_value(card1) > self.card_value(card2):
            print("Player 1 wins this round!")
            self.players[0].add_card(card1)
            self.players[0].add_card(card2)
        elif self.card_value(card2) > self.card_value(card1):
            print("Player 2 wins this round!")
            self.players[1].add_card(card1)
            self.players[1].add_card(card2)
        else:
            print("War! Each player draws two extra cards.")
            self.handle_war()

    def handle_war(self):
        input("Press Enter to continue...")
        print("---")

        # Check if players have enough cards to continue the war
        if len(self.players[0].hand) < 3 or len(self.players[1].hand) < 3:
            print("One of the players does not have enough cards for war.")
            return

        # Draw two extra cards, keeping the initial war card
        war_cards_p1 = [self.players[0].play_card()]  # Initial war card
        war_cards_p2 = [self.players[1].play_card()]  # Initial war card

        for _ in range(2):
            if self.players[0].hand:
                war_cards_p1.append(self.players[0].play_card())
            if self.players[1].hand:
                war_cards_p2.append(self.players[1].play_card())

        # Compare the last drawn card
        card1 = war_cards_p1[-1] if war_cards_p1 else None
        card2 = war_cards_p2[-1] if war_cards_p2 else None
        print(f"Player 1's war card: {card1}")
        print(f"Player 2's war card: {card2}")

        # Determine the winner of the war
        if card1 and card2 and self.card_value(card1) > self.card_value(card2):
            print("Player 1 wins the war!")
            self.players[0].hand.extend(war_cards_p1 + war_cards_p2)
        elif card1 and card2 and self.card_value(card2) > self.card_value(card1):
            print("Player 2 wins the war!")
            self.players[1].hand.extend(war_cards_p1 + war_cards_p2)
        else:
            print("War again!")
            self.players[0].hand.extend(war_cards_p1)
            self.players[1].hand.extend(war_cards_p2)
            self.handle_war()

    def card_value(self, card):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                  'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return values[card.value]

if __name__ == "__main__":
    game = Game()
    game.start_game()

