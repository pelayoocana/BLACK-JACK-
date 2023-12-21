import tkinter as tk
from tkinter import PhotoImage, messagebox
import random

class Card:
    def __init__(self, suit: str, value: int):
        self.suit = suit
        self.value = value
        pass


    def get_numeric_value(self) -> int:
        if self.value in ['K', 'Q', 'J']:
            return 10 
        elif self.value == 'A':
            return 11
        else:
            return int(self.value)
        pass

    def get_image(self):
        # TODO: Return the path to the card's image
        return f"img/{self.value}_of_{self.suit}.png"

        pass

class Deck:
    def __init__(self, suits = [], values = []):
        self.cards = []
        for value in values:
            for suit in suits:
                self.cards.append(Card(suit.value))

        pass

    def shuffle(self):
        random.shuffle(self.cards)
        # TODO: Shuffle the cards
        pass

    def deal(self)-> Card:
        if not self.cards:
            raise ValueError("Empty Deck")
        return self.cards.pop()
        # TODO: Deal one card from the deck
        pass

class EnglishDeck(Deck):
    def __init__(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        super().__init__(suits, values)
        # lo que hemos hecho aqui ha sido crear dos listas que incluyan los valores que van a tomar las cartas,
        # el constructor hereda de la clase anterior los atributos señalados entre paréntesis
        pass

class Hand:
    def __init__(self):
        self.cards = []
        # abrimos un espacio para almacenar las cartas en esta lista 
        pass

    def add_card(self, card: Card):
        self.cards.append(card)
        # Incluimos cada carta que nos toque  en nuestra lista
        pass

    def value(self)->int:
        total_value = sum(card.get_numeric_value() for card in self.cards)
        num_As = sum(1 for card in self.cards if card.value == 'A')

        while total_value > 21 and num_As:
            total_value -= 10
            num_As -= 1
        # En este fragmento, lo que  hemos hecho ha sido buscar cual es el valor que tene nuestra carta para saber si llegamos al numero necesario para ganar y hacer blackjack 
        pass

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        # inicializamos estos atributos como name y como la ejecución de la clase Hand()
        pass

class BlackjackGame:
    def __init__(self):
        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.deck = EnglishDeck
        self.deck.shuffle()
        # inicializamos nuestros atributos de jugadores como la clase Player, pero para un jugador y un crupier
        # Hacemos shuffle para barajar cartas a ser repartidas entre los juugadores 
        pass

    def start_game(self):
        self.player.hand = Hand()
        self.dealer.hand = Hand()
        # empieza el juego con un espacio para cada jugador o crupier con la clase Hand 

        for i in range (2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())
            # Hacemos un bucle for con rango 2, debido que tendremos que otorgar dos cartas a cada jugador y estos las incluirán en su self.deck para jugar 
        pass

    def hit(self)-> bool:
        self.player.hand.add_card(self.deck.deal())
        return self.player.hand.value() > 21
        # Hemos añadidos las cartas a la baraja personal del jugador, y ha de sumar al menos 21 entre las dos 
        pass

    def dealer_hit(self) -> bool:
        if self.dealer.hand.value() >=17:
            return False 
        self.dealer.hand.add_card(self.deck.deal())
        return self.dealer.hand.value() <=21
        # No se reparten mas cartas si el crupier tiene el valor de 17 entre la suma de las suyas 
        # Hna de mantener su valor por debajo de 21, ya que sino perderán
        pass

    def determine_winner(self):
        player_value = self.player.hand.value()
        dealer_value = self.dealer.hand.value()

        if player_value > 21:
            return "Too high man, the house always wins"
        if dealer_value > 21:
            return "Oh you tricked the house, you win"
        elif dealer_value>player_value:
            return "Busted, house wins"
        elif player_value> dealer_value:
            return "You  win"
        else:
            return "Its a tie"
        # TODO: Determine and return the winner of the game
        pass

# The GUI code is provided, so students don't need to modify it
class BlackjackGUI:
    def __init__(self, game):
        self.game = game

        self.root = tk.Tk()
        self.root.title("Blackjack")

        # Frames for the player and the dealer
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(side=tk.LEFT, padx=10)

        self.deck_frame = tk.Frame(self.root)
        self.deck_frame.pack(side=tk.LEFT, padx=10)

        self.dealer_frame = tk.Frame(self.root)
        self.dealer_frame.pack(side=tk.RIGHT, padx=10)

        # "Stand" button
        self.btn_stand = tk.Button(self.deck_frame, text="Stand", command=self.handle_stand, state=tk.NORMAL)
        self.btn_stand.pack(side=tk.BOTTOM)

        self.start_game()

    def start_game(self):
        self.game.start_game()
        self.update_interface()

    def handle_hit(self, event):
        if self.game.hit():
            self.update_interface()
            self.end_game("You've busted! The house wins.")
            return
        self.update_interface()

    def handle_stand(self):
        self.btn_stand.config(state=tk.DISABLED)
        while self.game.dealer_hit():
            self.update_interface()
        self.end_game(self.game.determine_winner())

    def update_interface(self):
        # Remove all widgets from player, deck, and dealer frames
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        
        for widget in self.deck_frame.winfo_children():
            widget.destroy()

        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

        # Player's cards
        player_previous_frame = tk.Frame(self.player_frame)
        player_previous_frame.pack(side=tk.LEFT, pady=10)

        for card in self.game.player.hand.cards[:-1]:  # All cards except the last one
            img = PhotoImage(file=card.get_image())
            img = img.subsample(3, 3)  # Resize the image (adjust according to your preference)
            lbl = tk.Label(player_previous_frame, image=img)
            lbl.image = img
            lbl.pack(side=tk.TOP, pady=5)  # Add vertical space between cards

        # The last card of the player in the center
        last_card = self.game.player.hand.cards[-1]
        img = PhotoImage(file=last_card.get_image())
        lbl = tk.Label(self.player_frame, image=img)
        lbl.image = img
        lbl.pack(side=tk.LEFT, padx=10)  # Center the last card horizontally a bit more
        
        # Deck in the middle
        img = PhotoImage(file="img/card_back_01.png")
        lbl = tk.Label(self.deck_frame, image=img, cursor="hand2")
        lbl.image = img
        lbl.pack(side=tk.TOP, padx=10)
        lbl.bind("<Button-1>", self.handle_hit)
        
        # "Stand" button below the deck
        self.btn_stand = tk.Button(self.deck_frame, text="Stand", command=self.handle_stand, state=tk.NORMAL)
        self.btn_stand.pack(side=tk.BOTTOM)

        # Dealer's cards
        dealer_previous_frame = tk.Frame(self.dealer_frame)
        dealer_previous_frame.pack(side=tk.RIGHT, pady=10)

        for card in self.game.dealer.hand.cards[:-1]:  # All cards except the last one
            img = PhotoImage(file=card.get_image())
            img = img.subsample(3, 3)  # Resize the image (adjust according to your preference)
            lbl = tk.Label(dealer_previous_frame, image=img)
            lbl.image = img
            lbl.pack(side=tk.TOP, pady=5)  # Add vertical space between cards

        # The last card of the dealer in the center
        last_card = self.game.dealer.hand.cards[-1]
        img = PhotoImage(file=last_card.get_image())
        lbl = tk.Label(self.dealer_frame, image=img)
        lbl.image = img
        lbl.pack(side=tk.RIGHT, padx=10)  # Center the last card horizontally a bit more

    def end_game(self, message):
        messagebox.showinfo("Result", message)
        self.root.quit()

    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    game_logic = BlackjackGame()
    app = BlackjackGUI(game_logic)
    app.run()
