from template import Algorithm as Player
from simulation import Simulation

sim = Simulation([Player("Hráč 1"), Player("Hráč 2"), Player("Hráč 3")])

sim.play_round()