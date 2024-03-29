import operator
from dataclasses import dataclass, field, InitVar

from prettytable import PrettyTable


@dataclass(order=True)
class PlayerStatistics:
    name: str
    base_unit: int
    min_bankroll_rolls = 0
    max_bankroll_rolls = 0
    biggest_win = 0
    biggest_loss = 0
    biggest_bet = 0
    target_reached_sim: set = field(default_factory=set)
    bankrupt_reached_sim: set = field(default_factory=set)
    total_bankroll: float = field(init=False)
    bankroll_target: float = None
    min_bankroll: float = field(init=False)
    max_bankroll: float = field(init=False)
    starting_bankroll: InitVar[float | None] = None

    def __post_init__(self, starting_bankroll):
        self.total_bankroll = self.min_bankroll = self.max_bankroll = starting_bankroll
        if self.bankroll_target is None:
            self.bankroll_target = starting_bankroll * 1.5


class SimulatorStatistics:
    total_rolls = 0
    total_sims = 0

    def __init__(self, strategies, starting_bankroll, base_unit=25, total_simulations=0):
        self.players = [PlayerStatistics(
            name=player, starting_bankroll=starting_bankroll, base_unit=base_unit) for player in
            strategies.keys()]
        self.total_simulations = total_simulations

    def update_after_roll(self, table):
        for p in table.players:
            player_stats = next(player for player in self.players if player.name == p.name)
            self.__update_bankroll_stats(player_stats, p.total_cash, table.dice.n_rolls)
            self.__update_bet_stats(p, player_stats)

    def __update_bankroll_stats(self, player_stats, player_cash, number_of_rolls):
        if player_stats.min_bankroll > player_cash:
            player_stats.min_bankroll = player_cash
            player_stats.min_bankroll_rolls = number_of_rolls
        if player_stats.max_bankroll < player_cash:
            player_stats.max_bankroll = player_cash
            player_stats.max_bankroll_rolls = number_of_rolls
        if player_cash < player_stats.base_unit:
            player_stats.target_reached_sim.add(self.total_sims)
        if player_cash >= player_stats.bankroll_target:
            player_stats.bankrupt_reached_sim.add(self.total_sims)

    def __update_bet_stats(self, p, player_stats):
        for bet in p.bets:
            player_stats.biggest_bet = max(bet.amount, player_stats.biggest_bet)
            bet_result = bet.get_result(p.table)
            if bet_result.won:
                player_stats.biggest_win = max(bet_result.amount, player_stats.biggest_win)
            elif bet_result.lost:
                player_stats.biggest_loss = min(bet_result.amount, player_stats.biggest_loss)

    def update_after_all_rolls(self, player):
        self.total_rolls += player.table.dice.n_rolls
        self.total_sims += 1
        stat = next(p1 for p1 in self.players if p1.name == player.name)
        stat.total_bankroll += player.total_cash

    def generate_table(self):
        result_table = PrettyTable(
            ["strategy", "hit target", "$<Unit", "Avg $", "biggest win", "biggest loss",
             "biggest bet", "highest $, rolls", "lowest $, rolls"])

        result_table.padding_width = 0
        # for player in sorted(self.players, key=lambda item: item.bankroll):
        for player in sorted(self.players, key=operator.attrgetter("total_bankroll")):
            result_table.add_row([
                player.name,
                self.get_count_percent(player.target_reached_sim),
                self.get_count_percent(player.bankrupt_reached_sim),
                f'${player.total_bankroll / self.total_simulations:.2f}', player.biggest_win, player.biggest_loss,
                player.biggest_bet, f'${player.max_bankroll:.2f} ({player.max_bankroll_rolls})',
                f'${player.min_bankroll:.2f} ({player.min_bankroll_rolls})'])

        return result_table

    def get_count_percent(self, list):
        return f"{len(list)} ( {(len(list) / self.total_simulations) * 100:.0f}%)"
