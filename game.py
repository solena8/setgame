from dataclasses import dataclass, field
import random

from card import Card


@dataclass
class Game:
    pile: list[Card] = field(default_factory=list)
    selection: list[Card] = field(default_factory=list)
    set: list[Card] = field(default_factory=list)

    def __post_init__(self):
        for number in ["1", "2", "3"]:
            for shape in ["L", "O", "V"]:
                for color in ["V", "M", "R"]:
                    for filling in ["H", "P", "V"]:
                        self.pile.append(Card(number=number, shape=shape, color=color, filling=filling))

        # création de la pile de 81 cartes différentes
        # Return the new Game

    def len_pile(self) -> int:
        return len(self.pile)

    def len_selection(self) -> int:
        return len(self.selection)

    def move_cards_from_pile_to_selection(self, nb_cards: int) -> None:
        # extraction d'un nb de cartes définit de la pile, de manière aléatoire
        # et ajout à la sélection
        random_selection = random.sample(self.pile, nb_cards)
        for card in random_selection:
            self.selection.append(card)
            self.pile.remove(card)

    def init_selection(self):
        # création de la sélection initiale de 12 cartes à partir de la pile
        self.move_cards_from_pile_to_selection(12)

    def add_3_cards(self):
        # ajout de 3 cartes de la pile vers la selection si 1)il reste des cartes dans la pile
        # et 2) si la selection comporte 9 cartes, ou 12 mais sans avoir trouvé de match avant
        # (comme ça lorsqu'on a atteint 15 cartes et trouvé ensuite un match, on redescend à 12 après)
        if (self.len_pile() >= 3) and ((self.len_selection() == 12 and not self.set) or (self.len_selection() == 9)):
            self.move_cards_from_pile_to_selection(3)

    # définition des règles de matching pour les 4 méthodes ci dessous :
    # chacun des 4 types de paramètre (nombre, couleur, forme et remplissage)
    # doit avoir 3 occurences complètement identiques (1, 1, 1 par ex.)
    # ou 3 occurences complètements différentes (1, 2, 3 par ex.)

    @staticmethod
    def card_param_number(card1: Card, card2: Card, card3: Card) -> bool:
        return (card1.number == card2.number == card3.number) or (
                    card1.number != card2.number != card3.number != card1.number)

    @staticmethod
    def card_param_color(card1: Card, card2: Card, card3: Card) -> bool:
        return (card1.color == card2.color == card3.color) or (card1.color != card2.color != card3.color != card1.color)

    @staticmethod
    def card_param_shape(card1: Card, card2: Card, card3: Card) -> bool:
        return (card1.shape == card2.shape == card3.shape) or (card1.shape != card2.shape != card3.shape != card1.shape)

    @staticmethod
    def card_param_filling(card1: Card, card2: Card, card3: Card) -> bool:
        return (card1.filling == card2.filling == card3.filling) or (
                card1.filling != card2.filling != card3.filling != card1.filling)

    @staticmethod
    def check_if_set_is_valid(card1: Card, card2: Card, card3: Card) -> bool:
        # vérification des 4 types de paramètres pour 3 cartes
        return (Game.card_param_number(card1, card2, card3) and
                Game.card_param_color(card1, card2, card3) and
                Game.card_param_shape(card1, card2, card3) and
                Game.card_param_filling(card1, card2, card3))

    def find_set(self) -> list[Card]:
        # Trouver un set de 3 cartes dans la sélection
        self.set = []
        for card_1 in self.selection:
            for card_2 in self.selection:
                for card_3 in self.selection:
                    if card_1 != card_2 and card_2 != card_3 and card_1 != card_3:
                        if Game.check_if_set_is_valid(card_1, card_2, card_3):
                            self.set = [card_1, card_2, card_3]
                            return self.set

    def print_and_remove_from_selection(self):
        # enlever les cartes du set trouvé précédemment de la sélection
        print(self.set)
        for card in self.set:
            self.selection.remove(card)

    def game_over(self):
        # définition du game over : si on a pas trouvé de set à la dernière recherche et que
        # soit la pile est vide
        # soit la sélection comportait déja 15 cartes (on ne veut pas avoir une sélection de 18 cartes)
        return not self.find_set() and (
                    self.len_selection() >= 15 or self.len_pile() < 3)

    def game_play(self):
        self.init_selection()
        while not self.game_over():
            self.find_set()
            if self.set:
                self.print_and_remove_from_selection()
            self.add_3_cards()
        print("No more matches found.")
        print("Remaining cards are:", self.selection, self.pile)
        print(len(self.selection), "+", len(self.pile), "cards left")