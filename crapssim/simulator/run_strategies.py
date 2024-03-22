import crapssim
from crapssim import Table
from crapssim.simulator.statistics import SimulatorStatistics

verbose = False
max_shooters = 10
n_sim = 1000
bankroll = 1000
base_unit = 25
strategies = {
    "place68": crapssim.strategy.examples.PassLinePlace68(base_unit),
    "ironcross": crapssim.strategy.examples.IronCross(base_unit),
    "betdontpass": crapssim.strategy.examples.BetDontPass(base_unit),
}

simulator = SimulatorStatistics(strategies, bankroll)

for i in range(n_sim):
    table = Table()
    for s in strategies:
        table.add_player(bankroll=bankroll,strategy=strategies[s], name=s)

    table.run(max_rolls=float("inf"), max_shooter=max_shooters, verbose=verbose, external_event=simulator.update_statistics)
    for p in table.players:
        simulator.update_after_all_rolls(p)
    #     print(f"{i}, {p.strategy}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")
print(f"\n{n_sim} runs.  {max_shooters} max shooters")

# print(simulator.players)

result_table = simulator.generate_table()
print (result_table)
