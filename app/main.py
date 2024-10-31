from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True

    def hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(self, start: tuple[int, int], end: tuple[int, int], is_drowned=False) -> None:
        self.decks = self._create_decks(start, end)
        self.is_drowned = is_drowned

    def _create_decks(self, start: tuple[int, int], end: tuple[int, int]) -> list[Deck]:
        decks = []
        if start[0] == end[0]:
            for column in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], column))
        else:
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, start[1]))

        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.hit()
            self.is_drowned = all(not d.is_alive for d in self.decks)
            return "Sunk!" if self.is_drowned else "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list[tuple[tuple[int, int], tuple[int, int]]]):
        self.field = {}
        self.ships = []

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            result = ship.fire(*location)
            return result
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)
                    if deck and deck.is_alive:
                        print(u"\u25A1", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print()
        print()
