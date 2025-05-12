class Player():
    def __init__(self):
        self.hand = []

        self.bet = 0

        self.total = 0

        self.folded = False
    
    def reset(self):
        self.folded = False
        self.bet = 0
        self.hand = []