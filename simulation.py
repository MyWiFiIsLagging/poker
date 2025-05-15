import random
from functions import find_best_hand

# importing csv
import csv



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
        self.data["cards"] = [] # Cards on the table
        self.data["money"] = 500 # Money given to players at the start of every round
        self.data["bet"] = 10 # Starting bet
        self.data["pool"] = 0 # Sum of all bets, the winning pot 
        self.data["folded"] = 0 # Number of players, who have folded
        self.data["players"] = len(self.players) # Number of players
        
        self.dealer = 0 

        self.table = {}
        self.table["money"] = []
        self.table["pools"] = []
        self.table["folds"] = []

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
            
            while passed < len(self.players) and self.data["folded"] < len(self.players) - 1:
                
                
                # Skip turn if player has folded
                if self.players[bettingPlayer].folded:
                    passed += 1
                    continue
                
                # Skip turn if player has already gone all in
                if self.data["money"] == self.players[bettingPlayer].bet:
                    passed += 1
                    continue
                
                bet = self.players[bettingPlayer].play(self.data)

                
                if bet == self.data["bet"]:
                    # Call
                    passed += 1
                elif bet > self.data["bet"]:
                    # Raise
                    passed = 1
                else:
                    # Fold
                    self.players[bettingPlayer].folded = True
                    self.data["folded"] += 1
                    passed += 1

                    # Move to next player 
                    bettingPlayer = (bettingPlayer+1) % len(self.players)
                    continue

                # Change betting pool, minimum bet, player bet
                self.data["pool"] += max(bet - self.players[bettingPlayer].bet, 0)
                self.data["bet"] = bet
                self.players[bettingPlayer].bet = bet

                # Move to next player
                bettingPlayer = (bettingPlayer+1) % len(self.players)

        self.find_winner()

        self.reset()

        self.create_table()

    # Restart the simulation after every round
    def reset(self):
        self.table["money"].append(self.data["money"])
        self.table["pools"].append(self.data["pool"])
        self.table["folds"].append(self.data["folded"])

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
            hand = find_best_hand(player.hand + self.data["cards"])
            player.table["hands"].append(hand[0])
            player.hand_score = hand[1]
        
        best_hand = 0
        for player in self.players:
            if not player.folded and player.hand_score > best_hand:
                best_hand = player.hand_score
        winners = 0
        for player in self.players:
            if not player.folded and player.hand_score == best_hand:
                winners += 1
        for player in self.players:
            if not player.folded and player.hand_score == best_hand:
                player.total += self.data["pool"] / winners
                player.on_win(self.data)
            else:
                player.total -= player.bet
                player.on_loss(self.data)
            player.reset()

    def create_table(self):
        # File path for the CSV file
        csv_file_path = 'tabulka.csv'

        # Open the file in write mode
        with open(csv_file_path, mode='w', newline='') as file:
            # Create a csv.writer object
            writer = csv.writer(file)
            # Write data to the CSV file
            for player in self.players:
                writer.writerow([player.name, "Bets:"] + player.table["bets"])
                writer.writerow([player.name, "Score:"] + player.table["scores"])
                writer.writerow([player.name, "Hands:"] + player.table["hands"])
                writer.writerow([player.name, "Balance:"] + player.table["balance"])
            
            writer.writerow(["Data", "Money:"] + self.table["money"])
            writer.writerow(["Data", "Pool:"] + self.table["pools"])
            writer.writerow(["Data", "Folds:"] + self.table["folds"])

        # Print a confirmation message
        print(f"CSV file '{csv_file_path}' created successfully.")
    