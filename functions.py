from collections import Counter

# Parses a card to a more workable-with format (suit, rank)
def parse_card(card):
    suit = card[0]
    rank = int(card[1:])
    return suit, rank

# Determines whether a list of card ranks contains a straight 🏳️‍🌈
def is_straight(ranks):
    unique_ranks = sorted(set(ranks), reverse=True)

    for i in range(len(unique_ranks) - 4):
        if unique_ranks[i] - unique_ranks[i + 4] == 4:
            return unique_ranks[i]

    if {14, 2, 3, 4, 5}.issubset(set(ranks)):
        return 5

    return None

# Determines whether a list of parsed cards contains a flush, returns a sorted array of their ranks
def is_flush(cards):
    suit_counts = Counter([card[0] for card in cards])
    for suit, count in suit_counts.items():
        if count >= 5:
            return sorted([card[1] for card in cards if card[0] == suit], reverse=True)[:5]
    return None

# Finds best hand from a list of cards, returns name of hand and a value for comparing
def find_best_hand(cards):
    # Parse cards to a more workable-with format
    parsed_cards = [parse_card(card) for card in cards]
    ranks = sorted([rank for suit, rank in parsed_cards], reverse=True)

    rank_counts = Counter(ranks)

    # Check for straight flush
    flush_ranks = is_flush(parsed_cards)
    if flush_ranks:
        straight_flush = is_straight(flush_ranks)
        if straight_flush:
            return "Straight Flush", (8 + straight_flush/100) 

    # Check for four of a kind
    four_kind = [rank for rank, freq in rank_counts.items() if freq == 4]
    if four_kind:
        return "Four of a Kind", (7 + four_kind/100)

    # Check for full house
    three_kind = [rank for rank, freq in rank_counts.items() if freq == 3]
    pair = [rank for rank, freq in rank_counts.items() if freq == 2]
    if three_kind and pair:
        return "Full House", (6 + three_kind/100)

    # Check for flush
    if flush_ranks:
        value = "5."
        for card in flush_ranks:
            value += str(card).zfill(2)
        return "Flush", float(value)

    # Check for straight
    straight = is_straight(ranks)
    if straight:
        return "Straight", (4 + straight/100)

    # Check for three of a kind
    if three_kind:
        return "Three of a Kind", (3 + three_kind[0]/100)

    # Check for two pair
    if len(pair) >= 2:
        sorted_pair = sorted(pair, reverse=True)[:2]
        return "Two Pair", (2 + sorted_pair[0]/100 + sorted_pair[1]/10000)

    # Check for one pair
    if pair:
        return "Pair", (1 + pair[0]/100)

    # Default for High card
    return "High Card", sum(ranks[:5])/100
