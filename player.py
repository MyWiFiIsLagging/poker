class Player():
    # Create necessary variables
    def __init__(self, name):
        self.name = name

        self.hand = []

        self.bet = 0

        self.total = 0

        self.folded = False

        self.hand_score = 0

        self.table = {}
        self.table["bets"] = []
        self.table["scores"] = []
        self.table["hands"] = []
        self.table["balance"] = []
    # Reset variables after end of round
    def reset(self):
        self.table["bets"].append(self.bet)
        self.table["scores"].append(self.hand_score)
        self.table["balance"].append(self.total)

        self.folded = False
        self.bet = 0
        self.hand = []
        self.hand_score = 0