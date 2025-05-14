from player import Player

class Algorithm(Player):
    # Feel free to add any custom variables
    def __init__(self, name):
        super().__init__(name)



    # Function triggered when player's turn comes
    #
    # Should return integers:
    # data["bet"] = call/check
    # data["bet"] < x = raise to x (clamped to data["money"])
    # x < data["bet"] or any non-integer value = fold
    #
    # data (dictionary) contents:
    # data["cards"] - the cards layed on the table
    # data["bet"] - current bet
    # data["money"] - the budget for every player, resets each round
    # data["players"] - number of players (including those who have folded)
    # data["folded"] - number of players who have folded
    # data["pool"] - money in the betting pool
    #
    # DO NOT EDIT THESE VALUES, you may only read them 
    # self.hand - the 2 cards in hand
    # self.bet - the money you're currently betting
    # self.total - the sum of how much you have won/lost
    #
    # Please don't use any other variables

    def play(self, data):
        print("-------------------")
        print(self.name)
        print(self.hand)
        print(data)
        return int(input("Bet:"))

    # Function triggered when player wins a round (before reset)
    def on_win(self, data):
        print(f"{self.name} won {data["pool"] - self.bet} chips")
    
    # Function triggered when player loses a round (before reset)
    def on_loss(self, data):
        print(f"{self.name} lost {self.bet} chips")