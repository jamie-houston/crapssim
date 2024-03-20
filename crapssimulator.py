import csv
from collections import Counter

from prettytable import PrettyTable

import crapssim as craps
from crapssim.strategy.classic import *
from crapssim.strategy.custom import *
from crapssim.table import Table

verbose = False
# n_sim = 10000
n_sim = 10
bankroll = 1000
starting_unit = 25
target_bankroll = 1500
max_shooters = 10

strategies = (
    # "knockout": craps.strategy.knockout,
    # DoNotPassGo,
    # DarkAndLight,
    # KeepComingBack,
    # ComingEverywhere,
    # AllIn,
    # NoField,
    # Hedged2Come,
    # PassLine2Come,
    # Risk12,
    # SafestWay,
    # DiceDoctor,
    # Place68_2Come,
    # Corey,
    # Frankenstein,
    IronCross,
    IronCrossLadder,
)

hybrids = {
    "IronCrossNoFieldOnComeOut": (IronCrossLadder, NoFieldOnComeOut),
    "IronCrossNoField": (IronCrossLadder, NoField)
}


def get_count_percent(count, total):
    return f"{count} ( {(count / total) * 100:.0f}%)"


with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    header = ["Sim Number", "Strategy", "End Bankroll", "Start Bankroll", "Dice Rolls", "Difference", "Dollar/Roll"]
    writer.writerow(header)

    result_summary = {}
    total_rolls = 0
    min_bankroll = {}
    max_bankroll = {}
    target_reached_count = {}
    bankrupt_count = {}
    roll_history = []
    for i in range(n_sim):
        table = Table(verbose=verbose)
        for s in strategies:
            table.add_player(
                craps.Player(bankroll, s(verbose=verbose, unit=starting_unit).update_bets, s.__name__, target_bankroll=target_bankroll,
                             verbose=verbose))

        # for name, variations in hybrids:
        #     s = Strategy(verbose=verbose, unit=starting_unit)
        #     [s(variation) for variation in variations]
        #
        #     craps.Player(bankroll, s.update_bets, name.__name__, target_bankroll=target_bankroll,verbose=verbose)

        table.run(max_rolls=float("inf"), max_shooter=max_shooters)
        total_rolls += table.dice.n_rolls
        roll_history += table.dice_results.dice_total_history
        if verbose:
            print(f"Rolls: {table.dice.n_rolls}")
        for s in strategies: #+ hybrids:
            strategy_player = table.get_player(s.__name__)
            strategy_player_bankroll = strategy_player.bankroll_finance
            current_result = result_summary.get(s, 0)
            if strategy_player_bankroll.smallest < (min_bankroll.get(s) or [bankroll])[0]:
                min_bankroll[s] = strategy_player_bankroll.smallest, table.dice.n_rolls
            if strategy_player_bankroll.largest > (max_bankroll.get(s) or [bankroll])[0]:
                max_bankroll[s] = strategy_player_bankroll.largest, table.dice.n_rolls
            if strategy_player.target_reached:
                target_reached_count[s] = (target_reached_count.get(s) or 0) + 1
            elif strategy_player_bankroll.current < starting_unit:
                bankrupt_count[s] = bankrupt_count.get(s, 0) + 1

            row = [i, s, strategy_player_bankroll.current, bankroll, table.dice.n_rolls,
                   strategy_player_bankroll.current - bankroll,
                   (strategy_player_bankroll.current - bankroll) / table.dice.n_rolls]
            result_summary[s] = current_result + strategy_player_bankroll.current

            writer.writerow(row)

    result_table = PrettyTable(
        ["strategy", "hit target", "$<Unit", "Avg $", "biggest win", "biggest loss",
         "biggest bet", "highest $, rolls", "lowest $, rolls"])

    for strategy, result in sorted(result_summary.items(), key=lambda item: item[1]):
        player = table.get_player(strategy.__name__)
        result_table.add_row([
            player.name,
            get_count_percent((target_reached_count.get(strategy) or 0), n_sim),
            get_count_percent((bankrupt_count.get(strategy) or 0), n_sim),
            round(result / n_sim, 2), player.bet_stats.biggest_win, player.bet_stats.biggest_loss,
            player.bet_stats.biggest_loss, max_bankroll.get(strategy) or 0, min_bankroll.get(strategy, 0)])

    print(f"\n{n_sim} runs. {total_rolls} rolls (avg {(total_rolls / n_sim)}) {max_shooters} max shooters")
    # result_table.set_style(PLAIN_COLUMNS)
    result_table.padding_width = 0

    print(result_table)
    number_counts = Counter(roll_history)
    print(f"Dice Stats: {number_counts}")
