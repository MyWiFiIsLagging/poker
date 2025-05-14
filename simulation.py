import random
from functions import find_best_hand

class Simulation:
    def __init__(self, players):
        self.players = players
        self.deck = [
            "♠2", "♠3", "♠4", "♠5", "♠6", "♠7", "♠8", "♠9", "♠10", "♠11", "♠12", "♠13", "♠14",
            "♥2", "♥3", "♥4", "♥5", "♥6", "♥7", "♥8", "♥9", "♥10", "♥11", "♥12", "♥13", "♥14",
            "♣2", "♣3", "♣4", "♣5", "♣6", "♣7", "♣8", "♣9", "♣10", "♣11", "♣12", "♣13", "♣14", 
            "♦2", "♦3", "♦4", "♦5", "♦6", "♦7", "♦8", "♦9", "♦10", "♦11", "♦12", "♦13", "♦14"
        ]

        
        self.data = {}
        self.data["cards"] = []
        self.data["money"] = 500
        self.data["bet"] = 10
        self.data["pool"] = 0
        self.data["folded"] = 0
        self.data["players"] = len(self.players)
        
        

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

            while passed < len(self.players) and self.data["folded"] >= len(self.players) - 1:
                bettingPlayer = (bettingPlayer+1) % (len(self.players) - self.data["folded"])

                if self.players[bettingPlayer].folded:
                    continue

                bet = 0
                if self.players[bettingPlayer].bet == self.data["money"] == self.data["bet"]:
                    bet = self.data["bet"]
                else:
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
        self.data["folded"] = 0
        self.data["players"] = len(self.players)
    
    def find_winner(self):
        for player in self.players:
            player.hand_score = find_best_hand(player.hand + self.data["cards"])
        
        best_hand = max(player.hand_score for player in self.players)
        winners = 0
        for player in self.players:
            if player.hand_score == best_hand:
                winners += 1
        for player in self.players:
            if player.hand_score == best_hand:
                player.total += self.data["pool"] / winners
                player.on_win()
            else:
                player.total -= player.bet
                player.on_loss()
            player.reset()
            
        