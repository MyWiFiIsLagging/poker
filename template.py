from player import Player

class Algorithm(Player):
    # Feel free to add any custom variables
    def __init__(self):
        super().__init__()



    # Function triggered when player's turn comes
    #
    # Should return integers:
    # data["bet"] = call/check
    # data["bet"] < x = raise to x (clamped to data["money"])
    # x < data["bet"] or any non-integer value = fold
    #
    # data (dictionary) contents:
    # "cards" - the cards layed on the table
    # "bet" - current bet
    # "money" - the budget for every player, resets each round
    #
    # self.hand - 

    def play(self, data):
        print(self.hand)
        print(data)
        return int(input("input"))

    # Function triggered when player wins a round
    def on_win(self):
        pass
    
    # Function triggered when player loses a round
    def on_loss(self):
        pass