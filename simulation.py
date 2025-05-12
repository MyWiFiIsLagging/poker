import random
from template import Algorithm as p 

class Simulation:
    def __init__(self, players):
        
        self.data = {}
        self.data["cards"] = []
        self.data["money"] = 500
        self.data["bet"] = 10
        self.data["folded"] = 0
        
        # DO NOT READ IN ALGORITHM
        self.players = players
        self.deck = [
            "♠2", "♠3", "♠4", "♠5", "♠6", "♠7", "♠8", "♠9", "♠10", "♠11", "♠12", "♠13", "♠14",
            "♥2", "♥3", "♥4", "♥5", "♥6", "♥7", "♥8", "♥9", "♥10", "♥11", "♥12", "♥13", "♥14",
            "♣2", "♣3", "♣4", "♣5", "♣6", "♣7", "♣8", "♣9", "♣10", "♣11", "♣12", "♣13", "♣14", 
            "♦2", "♦3", "♦4", "♦5", "♦6", "♦7", "♦8", "♦9", "♦10", "♦11", "♦12", "♦13", "♦14"
        ]

        self.dealer = 0 

    def play_round(self):
        # Deal 2 cards to every player
        for player in self.players:
            player.hand.append(self.deck.pop(random.randint(0, len(self.deck)-1)))
            player.hand.append(self.deck.pop(random.randint(0, len(self.deck)-1)))

        for round in range(0, 4):
            if round == 1:
                for i in range(0, 3):
                    self.data["cards"].append(self.deck.pop(random.randint(0, len(self.deck)-1)))
            if round > 1:
                self.data["cards"].append(self.deck.pop(random.randint(0, len(self.deck)-1)))

            bettingPlayer = self.dealer
            passed = 0

            while passed < len(self.players):
                bettingPlayer = (bettingPlayer+1) % (len(self.players) - self.data["folded"])

                if self.players[bettingPlayer].folded:
                    continue

                bet = min(self.players[bettingPlayer].play(self.data), self.data["money"])

                if bet == self.data["bet"]:
                    self.players[bettingPlayer].bet = bet
                    passed += 1
                elif self.data["money"] >= bet > self.data["bet"]:
                    self.players[bettingPlayer].bet = bet
                    self.data["bet"] = bet
                    passed = 1
                else:
                    self.data["folded"] += 1
                    self.players[bettingPlayer].folded = True
        self.find_winner()

        self.reset()

    def reset(self):
        self.deck = [
            "♠1", "♠2", "♠3", "♠4", "♠5", "♠6", "♠7", "♠8", "♠9", "♠10", "♠11", "♠12", "♠13",
            "♥1", "♥2", "♥3", "♥4", "♥5", "♥6", "♥7", "♥8", "♥9", "♥10", "♥11", "♥12", "♥13",
            "♣1", "♣2", "♣3", "♣4", "♣5", "♣6", "♣7", "♣8", "♣9", "♣10", "♣11", "♣12", "♣13", 
            "♦1", "♦2", "♦3", "♦4", "♦5", "♦6", "♦7", "♦8", "♦9", "♦10", "♦11", "♦12", "♦13"
        ]
        self.dealer = (self.dealer+1) % len(self.players)


        self.data = {}
        self.data["cards"] = []
        self.data["money"] = 500
        self.data["bet"] = 0
    
    def find_winner():
        pass


"""s = Simulation([p(), p()])
s.play_round()
   """     

from collections import Counter

def parse_card(card):
    suit = card[0]  # Extract the suit symbol
    rank = int(card[1:])  # Extract the rank as an integer
    return suit, rank

def is_straight(ranks):
    unique_ranks = sorted(set(ranks), reverse=True)

    for i in range(len(unique_ranks) - 4):
        if unique_ranks[i] - unique_ranks[i + 4] == 4:
            return unique_ranks[i:i+5]

    if {14, 2, 3, 4, 5}.issubset(set(ranks)):
        return 5

    return None

def is_flush(cards):
    suit_counts = Counter([card[0] for card in cards])
    for suit, count in suit_counts.items():
        if count >= 5:
            return sorted([card for card in cards if card[0] == suit], key=lambda x: x[1], reverse=True)[:5]
    return None

def find_best_hand(cards):
    parsed_cards = [parse_card(card) for card in cards]
    ranks = sorted([rank for suit, rank in parsed_cards], reverse=True)

    rank_counts = Counter(ranks)

    # Check for straight flush
    flush_cards = is_flush(parsed_cards)
    if flush_cards:
        flush_ranks = [card[1] for card in flush_cards]
        straight_flush = is_straight(flush_ranks)
        if straight_flush:
            return "Straight Flush", max(straight_flush)

    # Check for four of a kind
    four_kind = [rank for rank, freq in rank_counts.items() if freq == 4]
    if four_kind:
        return "Four of a Kind", four_kind

    # Check for full house
    three_kind = [rank for rank, freq in rank_counts.items() if freq == 3]
    pair = [rank for rank, freq in rank_counts.items() if freq == 2]
    if three_kind and pair:
        return "Full House", [max(three_kind), max(pair)]

    # Check for flush
    if flush_cards:
        return "Flush", [card[1] for card in flush_cards]

    # Check for straight
    straight = is_straight(ranks)
    if straight:
        return "Straight", straight

    # Check for three of a kind
    if three_kind:
        return "Three of a Kind", [max(three_kind)]

    # Check for two pair
    if len(pair) >= 2:
        return "Two Pair", sorted(pair, reverse=True)[:2]

    # Check for one pair
    if pair:
        return "Pair", [max(pair)]

    # Default for High card
    return "High Card", ranks[:5]


# Example usage
cards = ["♥5", "♣3", "♥4", "♥2", "♥3", "♥6", "♦9"]
best_hand = find_best_hand(cards)
print("Best hand:", best_hand)