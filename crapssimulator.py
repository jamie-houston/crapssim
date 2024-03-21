import csv
from collections import Counter

from prettytable import PrettyTable

import crapssim as craps

from crapssim.strategy import BetDontPass, BetPassLine
from crapssim.table import Table

verbose = True
# n_sim = 10000
n_sim = 1
bankroll = 1000
target_bankroll = 1500
max_shooters = 10

strategies = {
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
    # IronCross,
    # IronCrossLadder,
    # IronCrossNoField,
    # IronCrossNoFieldOnComeOut,
    BetDontPass,
    BetPassLine
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
    for s in strategies:
        result_summary[s] = 0
        min_bankroll[s] = bankroll, 0
        max_bankroll[s] = bankroll, 0
        target_reached_count[s] = 0
        bankrupt_count[s] = 0
    for i in range(n_sim):
        table = Table()
        for s in strategies:
            table.add_player(bankroll=bankroll,strategy=s(bet_amount=25),name=s.__name__)
                # craps.Player(bankroll, s(verbose=verbose).update_bets, s.__name__, target_bankroll=target_bankroll,
                #              verbose=verbose))

        table.run(max_rolls=float("inf"), max_shooter=max_shooters)
        total_rolls += table.dice.n_rolls
        # roll_history += table.dice_results.dice_total_history
        if verbose:
            print(f"Rolls: {table.dice.n_rolls}")
        for s in strategies:
            strategy_player = table.get_player(s.__name__)
            strategy_player_bankroll = strategy_player.bankroll_finance
            current_result = result_summary[s]
            if strategy_player_bankroll.smallest < min_bankroll[s][0]:
                min_bankroll[s] = strategy_player_bankroll.smallest, table.dice.n_rolls
            if strategy_player_bankroll.largest > max_bankroll[s][0]:
                max_bankroll[s] = strategy_player_bankroll.largest, table.dice.n_rolls
            if not strategy_player.continue_rolling:
                target_reached_count[s] += 1
            elif strategy_player_bankroll.current < 10:
                bankrupt_count[s] += 1

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
            get_count_percent(target_reached_count[strategy], n_sim),
            get_count_percent(bankrupt_count[strategy], n_sim),
            round(result / n_sim, 2), player.bet_stats.biggest_win, player.bet_stats.biggest_loss,
            player.bet_stats.biggest_loss, max_bankroll[strategy], min_bankroll[strategy]])

    print(f"\n{n_sim} runs. {total_rolls} rolls (avg {(total_rolls / n_sim)}) {max_shooters} max shooters")
    # result_table.set_style(PLAIN_COLUMNS)
    result_table.padding_width = 0

    print(result_table)
    number_counts = Counter(roll_history)
    print(f"Dice Stats: {number_counts}")
