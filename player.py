class Player():
    # Create necessary variables
    def __init__(self, name):
        self.name = name

        self.hand = []

        self.bet = 0

        self.total = 0

        self.folded = False

        self.hand_score = 0
    
    # Reset variables after end of round
    def reset(self):
        self.folded = False
        self.bet = 0
        self.hand = []
        self.hand_score = 0