#!/usr/bin/env python3
"""Display unicode playing card characters."""

import argparse


def print_verbose():
    """Print detailed information about each card."""
    suits = {
        'Spades': range(0x1F0A1, 0x1F0AF),
        'Hearts': range(0x1F0B1, 0x1F0BF),
        'Diamonds': range(0x1F0C1, 0x1F0CF),
        'Clubs': range(0x1F0D1, 0x1F0DF),
    }

    rank_names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Knight', 'Queen', 'King']

    print("Playing Card Unicode Characters\n")

    for suit_name, card_range in suits.items():
        print(f"\n{suit_name}:")
        print("─" * 40)
        for i, code in enumerate(card_range):
            if i < len(rank_names):
                card = chr(code)
                print(f"{rank_names[i]:8} {card}  (U+{code:04X})")

    # Card back
    print(f"\n\nCard Back:")
    print("─" * 40)
    card_back = chr(0x1F0A0)
    print(f"Back     {card_back}  (U+1F0A0)")

    # Jokers
    print(f"\n\nJokers:")
    print("─" * 40)
    jokers = [0x1F0BF, 0x1F0CF, 0x1F0DF]
    joker_names = ['Red Joker', 'Black Joker', 'White Joker']
    for name, code in zip(joker_names, jokers):
        joker = chr(code)
        print(f"{name:12} {joker}  (U+{code:04X})")


def print_simple():
    """Print all cards in a single line."""
    cards = []

    # Card back
    cards.append(chr(0x1F0A0))

    # All suits
    suit_ranges = [
        range(0x1F0A1, 0x1F0AF),  # Spades
        range(0x1F0B1, 0x1F0BF),  # Hearts
        range(0x1F0C1, 0x1F0CF),  # Diamonds
        range(0x1F0D1, 0x1F0DF),  # Clubs
    ]

    for card_range in suit_ranges:
        for code in card_range:
            cards.append(chr(code))

    # Jokers
    cards.append(chr(0x1F0BF))  # Red Joker
    cards.append(chr(0x1F0CF))  # Black Joker
    cards.append(chr(0x1F0DF))  # White Joker

    print(' '.join(cards))


def main():
    parser = argparse.ArgumentParser(description='Display unicode playing card characters.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show detailed information about each card')

    args = parser.parse_args()

    if args.verbose:
        print_verbose()
    else:
        print_simple()


if __name__ == "__main__":
    main()
