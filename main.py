from __future__ import annotations
from typing import Any, Union, Dict, Tuple
from enum import Enum
import random

BLUE = "blue"
YELLOW = "yellow"
RED = "red"
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings
#


START_DECK = {
    RED: 11,
    BLUE: 6,
    YELLOW: 6
}

DISCARD = {
    RED: 0,
    BLUE: 0,
    YELLOW: 0
}

SIX_PLAYERS_CONFIG: Dict[str, int] = {
    RED: 2,
    BLUE: 3,
    YELLOW: 1
}

# always play blue > yellow > red (except for when yellow and red have the same destination?)
def blue_strategy_0(location: Tuple,  card_0: str, card_1: str):
    if BLUE in [card_0, card_1]:
        return BLUE
    elif YELLOW in [card_0, card_1] and location not in tiles_yellow_goes_red:
        return YELLOW
    elif RED in [card_0, card_1]:
        return RED
    elif YELLOW in [card_0, card_1]:
        return YELLOW
    else:
        raise ValueError(card_0, card_1, location)

def blue_strategy_1(location: Tuple, card_0: str, card_1: str):
    # If at origin or layer 4, play red > blue > yellow
    # comparator = location[0] >= 3
    comparator = (location == (4, 0)) or (location == (3, 0))
    if comparator:
        if RED in [card_0, card_1]:
            return RED
        elif BLUE in [card_0, card_1]:
            return BLUE
        else:
            return YELLOW
    else:
        return blue_strategy_0(location, card_0, card_1)


# Always play red > yellow > blue (except for when yellow and blue have the same destination)
def red_strategy_0(location: Tuple, card_0: str, card_1: str):
    if RED in [card_0, card_1]:
        return RED
    elif YELLOW in [card_0, card_1] and location not in tiles_yellow_goes_blue:
        return YELLOW
    elif BLUE in [card_0, card_1]:
        return BLUE
    elif YELLOW in [card_0, card_1]:
        return YELLOW
    else:
        raise ValueError(card_0, card_1, location)


def yellow_strategy_0(location: Tuple, card_0: str, card_1: str):
    if card_0 == card_1:
        return card_0

    # Spot where yellow causes a loss
    if location == (0, 2) and BLUE in [card_0, card_1]:
        return BLUE
    elif location == (0, 2) and YELLOW in [card_0, card_1]:
        return YELLOW
    elif location == (0, 2) and RED in [card_0, card_1]:
        return RED
    elif location == (0, 2):
        raise Exception("Yikes")

    elif location == (0, 4) and RED in [card_0, card_1]:
        return RED
    elif location == (0, 4) and YELLOW in [card_0, card_1]:
        return YELLOW
    elif location == (0, 4) and BLUE in [card_0, card_1]:
        return BLUE
    elif location == (0, 4):
        raise Exception("Yikes")

    elif YELLOW in [card_0, card_1]:
        return YELLOW

    else:
        # TODO: do better logic for this. For now just throw in a blue.
        # layer = location[0]

        if RED in [card_0, card_1]:
            return BLUE
        elif BLUE in [card_0, card_1]:
            return BLUE
        else:
            raise ValueError("Yikers")


class Tile:

    def __init__(self, blue: Union[Tile, str], yellow: Union[Tile, str], red: Union[Tile, str]):
        self.blue = blue
        self.yellow = yellow
        self.red = red
        self.location = None

        self.next_tiles = {
            BLUE: self.blue,
            YELLOW: self.yellow,
            RED: self.red
        }

red_victory = RED
blue_victory = BLUE
yellow_victory = YELLOW

# Layer 0

# Key is (layer, index left to right)
tiles = {}

# Final tile
tiles[0, 3] = Tile(blue_victory, yellow_victory, red_victory)

# Red victory-adjacent, right to left
tiles[0, 2] = Tile(tiles[0, 3], red_victory, red_victory)
tiles[0, 1] = Tile(tiles[0, 2], tiles[0, 2], red_victory)
tiles[0, 0] = Tile(tiles[0, 1], tiles[0, 1], red_victory)

# Blue victory adjacent, left to right
tiles[0, 4] = Tile(blue_victory, blue_victory, tiles[0, 3])
tiles[0, 5] = Tile(blue_victory, tiles[0, 4], tiles[0, 4])
tiles[0, 6] = Tile(blue_victory, tiles[0, 5], tiles[0, 5])

# Layer 1 - up to down, left to right
tiles[1, 2] = Tile(blue=tiles[0, 2], yellow=tiles[0, 3], red=tiles[0, 4])
tiles[1, 1] = Tile(blue=tiles[1, 2], yellow=tiles[0, 2], red=tiles[0, 1])
tiles[1, 0] = Tile(blue=tiles[1, 1], yellow=tiles[0, 1], red=tiles[0, 0])
tiles[1, 3] = Tile(blue=tiles[0, 5], yellow=tiles[0, 4], red=tiles[1, 2])
tiles[1, 4] = Tile(blue=tiles[0, 6], yellow=tiles[0, 5], red=tiles[1, 3])

tiles[2, 2] = Tile(blue=tiles[1, 3], yellow=tiles[1, 2], red=tiles[1, 1])
tiles[2, 1] = Tile(blue=tiles[2, 2], yellow=tiles[1, 1], red=tiles[1, 0])
tiles[2, 0] = Tile(blue=tiles[2, 1], yellow=tiles[1, 0], red=tiles[1, 0])
tiles[2, 3] = Tile(blue=tiles[1, 4], yellow=tiles[1, 3], red=tiles[2, 2])
tiles[2, 4] = Tile(blue=tiles[1, 4], yellow=tiles[1, 4], red=tiles[2, 3])

tiles[3, 1] = Tile(blue=tiles[2, 3], yellow=tiles[2, 1], red=tiles[2, 1])
tiles[3, 0] = Tile(blue=tiles[3, 1], yellow=tiles[2, 1], red=tiles[2, 0])
tiles[3, 2] = Tile(blue=tiles[2, 4], yellow=tiles[2, 3], red=tiles[3, 1])

tiles[4, 1] = Tile(blue=tiles[3, 2], yellow=tiles[3, 1], red=tiles[3, 0])
tiles[4, 0] = Tile(blue=tiles[4, 1], yellow=tiles[3, 0], red=tiles[3, 0])
tiles[4, 2] = Tile(blue=tiles[3, 2], yellow=tiles[3, 2], red=tiles[4, 1])

tiles[5, 0] = Tile(blue=tiles[4, 2], yellow=tiles[4, 1], red=tiles[4, 0])

for key, val in tiles.items():
    val.location = key

tiles_yellow_goes_red = [tiles[0, 2], tiles[0, 5], tiles[0, 6], tiles[2, 0], tiles[3, 1], tiles[4, 0]]
tiles_yellow_goes_blue = [tiles[0, 0], tiles[0, 1], tiles[0, 4], tiles[2, 4], tiles[4, 2]]

origin = tiles[5, 0]

yellow_wins = 0
red_wins = 0
blue_wins = 0


def play_game():

    blue_strat_to_use = blue_strategy_1
    yellow_strat_to_use = yellow_strategy_0
    red_strat_to_use = red_strategy_0

    strats = {
        BLUE: blue_strat_to_use,
        YELLOW: yellow_strat_to_use,
        RED: red_strat_to_use
    }

    yellow_events = {"convert": 3, "none": 2}

    n_players = 6
    players: Dict[str, int] = SIX_PLAYERS_CONFIG.copy()
    in_deck: Dict[str, int] = START_DECK.copy()
    discard = DISCARD.copy()

    current_tile = origin

    while True:
        current_location = current_tile.location
        players_pool = players.copy()

        captain = random.choices(list(players_pool.keys()), weights=players_pool.values(), k=1)[0] # noqa
        players_pool[captain] -= 1

        lieutenant = random.choices(list(players_pool.keys()), weights=players_pool.values(), k=1)[0] # noqa
        players_pool[lieutenant] -= 1

        if sum(players_pool.values()) > 0:

            navigator = random.choices(list(players_pool.keys()), weights=players_pool.values(), k=1)[0] # noqa
            players_pool[navigator] -= 1
        else:
            # No navigator, we randomly flip.
            navigator = None

        if sum(in_deck.values()) <= 4:

            for k, v in discard.items():
                in_deck[k] += v
                discard[k] = 0

        assert sum(in_deck.values()) >= 4

        captain_card_0 = random.choices(list(in_deck.keys()), weights=in_deck.values(), k=1)[0] # noqa
        in_deck[captain_card_0] -= 1
        captain_card_1 = random.choices(list(in_deck.keys()), weights=in_deck.values(), k=1)[0] # noqa
        in_deck[captain_card_1] -= 1

        captain_choice = strats[captain](location=current_location, card_0=captain_card_0, card_1=captain_card_1)

        if captain_choice == captain_card_0:
            discard[captain_card_1] += 1
        else:
            discard[captain_card_0] += 1

        lieutenant_card_0 = random.choices(list(in_deck.keys()), weights=in_deck.values(), k=1)[0] # noqa
        in_deck[lieutenant_card_0] -= 1
        lieutenant_card_1 = random.choices(list(in_deck.keys()), weights=in_deck.values(), k=1)[0] # noqa
        in_deck[lieutenant_card_1] -= 1

        lieutenant_choice = strats[lieutenant](location=current_location, card_0=lieutenant_card_0, card_1=lieutenant_card_1)

        if lieutenant_choice == lieutenant_card_0:
            discard[lieutenant_card_1] += 1
        else:
            discard[lieutenant_card_0] += 1

        if navigator:
            navigator_choice = strats[navigator](location=current_location, card_0=lieutenant_choice, card_1=captain_choice)
        else:
            navigator_choice = random.choices([lieutenant_choice, captain_choice], k=1)[0]
        if navigator_choice == lieutenant_choice:
            discard[captain_choice] += 1
        else:
            discard[lieutenant_choice] += 1
        next_tile = current_tile.next_tiles[navigator_choice]

        if next_tile in [blue_victory, yellow_victory, red_victory] and (next_tile == navigator or navigator is None):
            return next_tile

        # Navigator goes overboard.
        elif next_tile in [blue_victory, yellow_victory, red_victory] and navigator is not None:
            players[navigator] -= 1
            discard[navigator_choice] += 1
            continue

        if navigator_choice == YELLOW:
            yellow_event = random.choices(list(yellow_events.keys()), weights=yellow_events.values(), k=1)[0] # noqa
            yellow_events[yellow_event] -= 1

            if yellow_event == "convert":
                convert_choices = {
                    BLUE: players[BLUE],
                    RED: players[RED]
                }

                converted = random.choices(list(convert_choices.keys()), weights=convert_choices.values(), k=1)[0] # noqa

                players[YELLOW] += 1
                players[converted] -= 1

        current_tile = next_tile


if __name__ == '__main__':
    n_games = 100000
    WINS = {BLUE: 0,
            RED: 0,
            YELLOW: 0}

    for i in range(0, n_games):
        win = play_game()

        WINS[win] += 1

    print(WINS)


