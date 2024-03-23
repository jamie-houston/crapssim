from dataclasses import dataclass

from prettytable import PrettyTable


@dataclass
class PlayerStatistics:
    name: str
    min_bankroll: float
    min_bankroll_rolls = 0
    max_bankroll: float
    max_bankroll_rolls = 0
    target_reached_count = 0
    bankrupt_count = 0
    total_bankroll = 0
    base_unit: int


class SimulatorStatistics:
    total_rolls = 0
    total_simulations = 0

    def __init__(self, strategies, starting_bankroll, base_unit=25):
        self.players = [PlayerStatistics(name=player, min_bankroll=starting_bankroll, max_bankroll=starting_bankroll,
                                         base_unit=base_unit) for player in strategies.keys()]

    def update_statistics(self, table):
        self.total_rolls += table.dice.n_rolls
        for p in table.players:
            stat = next(player for player in self.players if player.name == p.name)
            if stat.min_bankroll > p.bankroll:
                stat.min_bankroll = p.bankroll
                stat.min_bankroll_rolls = table.dice.n_rolls
            if stat.max_bankroll < p.bankroll:
                stat.max_bankroll = p.bankroll
                stat.max_bankroll_rolls = table.dice.n_rolls
            if p.bankroll < stat.base_unit:
                stat.bankrupt_count += 1

    def update_after_all_rolls(self, player):
        stat = next(p1 for p1 in self.players if p1.name == player.name)
        stat.total_bankroll += player.bankroll
        self.total_simulations += 1

    def generate_table(self):
        result_table = PrettyTable(
            ["strategy", "hit target", "$<Unit", "Avg $", "biggest win", "biggest loss",
             "biggest bet", "highest $, rolls", "lowest $, rolls"])

        for player in self.players:
            result_table.add_row([
                player.name,
                self.get_count_percent(player.target_reached_count),
                self.get_count_percent(player.bankrupt_count),
                round(player.total_bankroll / self.total_simulations, 2), "BIG WIN", "BIG LOGG",
                "BIG BET", f'{player.max_bankroll} ({player.max_bankroll_rolls})',
                f'{player.min_bankroll} ({player.min_bankroll_rolls})'])

        return result_table
    def get_count_percent(self, count):
        return f"{count} ( {(count / self.total_simulations) * 100:.0f}%)"
