import crapssim
from crapssim import Table
from crapssim.simulator.statistics import SimulatorStatistics

verbose = False
max_shooters = 10
n_sim = 10
bankroll = 1000
base_unit = 25
strategies = {
    "place68": crapssim.strategy.examples.PassLinePlace68(base_unit),
    "ironcross": crapssim.strategy.examples.IronCross(base_unit),
    "betdontpass": crapssim.strategy.examples.BetDontPass(base_unit),
    "risk12": crapssim.strategy.examples.Risk12(),
    "betpassline": crapssim.strategy.examples.BetPassLine(base_unit),
}

simulator = SimulatorStatistics(strategies, bankroll, total_simulations = n_sim)

for i in range(n_sim):
    table = Table()
    for s in strategies:
        table.add_player(bankroll=bankroll,strategy=strategies[s], name=s)

    table.run(max_rolls=float("inf"), max_shooter=max_shooters, verbose=verbose, update_after_roll=simulator.update_after_roll)
    for p in table.players:
        simulator.update_after_all_rolls(p)
    #     print(f"{i}, {p.strategy}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")
print(f"\n{n_sim} runs.  {max_shooters} max shooters")

# print(simulator.players)

result_table = simulator.generate_table()
print (result_table)
