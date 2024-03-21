import crapssim
from crapssim import Table

verbose = True
max_shooters = 1
n_sim = 1
bankroll = 1000
base_unit = 5
strategies = {
    "place68": crapssim.strategy.examples.PassLinePlace68(base_unit),
    "ironcross": crapssim.strategy.examples.IronCross(base_unit),
    "betdontpass": crapssim.strategy.examples.BetDontPass(base_unit),
}

for i in range(n_sim):
    table = Table()
    for s in strategies:
        table.add_player(bankroll=bankroll,strategy=strategies[s], name=s)

    table.run(max_rolls=float("inf"), max_shooter=max_shooters, verbose=verbose)
    for p in table.players:
        print(f"{i}, {p.strategy}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")

print(f"\n{n_sim} runs.  {max_shooters} max shooters")
