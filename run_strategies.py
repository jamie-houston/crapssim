import crapssim
from crapssim import Table
from crapssim.statistics.statistics import SimulatorStatistics
from crapssim.strategy.examples import *

verbose = False
max_shooters = 10
n_sim = 10
bankroll = 1000
base_unit = 25

all_strategies = {
    BetDontPass,
    BetPassLine,
    # BetPlace,
    # DiceDoctor,
    # FieldWinProgression,
    # HammerLock,
    IronCross,
    Knockout,
    Pass2Come,
    PassLinePlace68,
    PassLinePlace68Move59,
    Place682Come,
    Risk12,
                  }
strategies = {strat.__name__: strat(base_unit) for strat in all_strategies}

simulator = SimulatorStatistics(strategies, bankroll, total_simulations=n_sim)

for i in range(n_sim):
    table = Table()
    for strategy in strategies:
        table.add_player(bankroll=bankroll, strategy=strategies[strategy], name=strategy)

    table.run(max_rolls=float("inf"), max_shooter=max_shooters, verbose=verbose,
              update_after_roll=simulator.update_after_roll)
    for p in table.players:
        print(f"Updating {p.name}")
        simulator.update_after_all_rolls(p)
print(f"\n{n_sim} runs.  {max_shooters} max shooters")

result_table = simulator.generate_table()
print(result_table)
