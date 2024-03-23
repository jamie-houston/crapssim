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
    bankroll_target: float
    bankrupt_count = 0
    total_bankroll = 0
    biggest_win = 0
    biggest_loss = 0
    base_unit: int
    biggest_bet = 0


class SimulatorStatistics:
    total_rolls = 0
    total_simulations = 0

    def __init__(self, strategies, starting_bankroll, base_unit=25):
        self.players = [PlayerStatistics(name=player, min_bankroll=starting_bankroll, max_bankroll=starting_bankroll,
                                         base_unit=base_unit, bankroll_target=starting_bankroll * 1.5) for player in
                        strategies.keys()]

    def update_after_roll(self, table):
        self.total_rolls += table.dice.n_rolls
        for p in table.players:
            player_stats = next(player for player in self.players if player.name == p.name)
            self.__update_bankroll_stats(p, player_stats)
            self.__update_bet_stats(p, player_stats)

    def __update_bankroll_stats(self, p, player_stats):
        if player_stats.min_bankroll > p.bankroll:
            player_stats.min_bankroll = p.bankroll
            player_stats.min_bankroll_rolls = p.table.dice.n_rolls
        if player_stats.max_bankroll < p.bankroll:
            player_stats.max_bankroll = p.bankroll
            player_stats.max_bankroll_rolls = p.table.dice.n_rolls
        if p.bankroll < player_stats.base_unit:
            player_stats.bankrupt_count += 1
        if p.bankroll > player_stats.bankroll_target:
            player_stats.target_reached_count += 1

    def __update_bet_stats(self, p, player_stats):
        for bet in p.bets:
            player_stats.biggest_bet = max(bet.amount, player_stats.biggest_bet)
            bet_result = bet.get_result(p.table)
            if bet_result.won:
                player_stats.biggest_win = max(bet_result.amount, player_stats.biggest_win)
            elif bet_result.lost:
                player_stats.biggest_loss = min(bet_result.amount, player_stats.biggest_loss)

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
                round(player.total_bankroll / self.total_simulations, 2), player.biggest_win, player.biggest_loss,
                player.biggest_bet, f'{player.max_bankroll} ({player.max_bankroll_rolls})',
                f'{player.min_bankroll} ({player.min_bankroll_rolls})'])

        return result_table


    def get_count_percent(self, count):
        return f"{count} ( {(count / self.total_simulations) * 100:.0f}%)"
