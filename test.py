from template import Algorithm as Player
from simulation import Simulation

sim = Simulation([Player("Hrac 1"), Player("Hrac 2"), Player("Hrac 3")])

for i in range(10):
    sim.play_round()
sim.create_table()