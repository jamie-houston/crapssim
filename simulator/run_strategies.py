from dataclasses import dataclass

from prettytable import PrettyTable

import crapssim
from crapssim import Table
from crapssimulator import get_count_percent


@dataclass
class PlayerStatistics:
    name: str
    min_bankroll: float
    min_bankroll_rols: 0
    max_bankroll: float
    max_bankroll_rols: 0
    target_reached_count = 0
    bankrupt_count = 0
    total_bankroll = 0

class SimulatorStatistics:
    total_rolls = 0
    def __init__(self, strategies, starting_bankroll):
        self.players = [PlayerStatistics(name=player, min_bankroll=starting_bankroll, max_bankroll=starting_bankroll) for player in strategies.keys()]


    def update_statistics(self, table):
        print(f'Updating {table}')
        self.total_rolls += table.dice.n_rolls
        for p in table.players:
            stat = next(player for player in self.players if player.name == p.name)
            if stat.min_bankroll > p.bankroll:
                stat.min_bankroll = p.bankroll
                stat.min_bankroll_rolls = table.dice.n_rolls
            if stat.max_bankroll < p.bankroll:
                stat.max_bankroll = p.bankroll
                stat.max_bankroll_rols = table.dice.n_rolls
            if p.bankroll < base_unit:
                stat.bankrupt_count += 1

    def update_after_all_rolls(self, player):
        stat = next(p1 for p1 in self.players if p1.name == p.name)
        stat.total_bankroll += player.bankroll


    @staticmethod
    def get_count_percent(count, total):
        return f"{count} ( {(count / total) * 100:.0f}%)"


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

simulator = SimulatorStatistics(strategies, bankroll)

for i in range(n_sim):
    table = Table()
    for s in strategies:
        table.add_player(bankroll=bankroll,strategy=strategies[s], name=s)

    table.run(max_rolls=float("inf"), max_shooter=max_shooters, verbose=verbose, external_event=simulator.update_statistics)
    for p in table.players:
        print(f"{i}, {p.strategy}, {p.bankroll}, {bankroll}, {table.dice.n_rolls}")
print(f"\n{n_sim} runs.  {max_shooters} max shooters")

result_table = PrettyTable(
    ["strategy", "hit target", "$<Unit", "Avg $", "biggest win", "biggest loss",
     "biggest bet", "highest $, rolls", "lowest $, rolls"])

for player in simulator.players:
    result_table.add_row([
        player.name,
        get_count_percent(player.target_reached_count, n_sim),
        get_count_percent(player.bankrupt_count, n_sim),
        round(player.total_bankroll / n_sim, 2), "BIG WIN", "BIG LOGG",
        "BIG BET", f'{player.max_bankroll} ({player.max_bankroll_rols})', f'{player.min_bankroll} ({player.min_bankroll_rols})'])
# print(simulator.players)

print (result_table)
