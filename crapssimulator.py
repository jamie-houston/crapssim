import crapssim as craps
import customstrat
import csv
from crapssim.strategy.custom import AllInStrat, DarkAndLightStrategy, NoFieldStrategy, KeepComingBackStrategy, ComingEverywhereStrategy, DoNotPassGo, Hedged2Come, PassLine2ComeStrategy, Risk12Strategy, SafestWayStrategy
from icecream import ic
from prettytable import PrettyTable 
from fractions import Fraction


verbose = True
ic.disable()
# n_sim = 10000
n_sim = 1
bankroll = 1000
target_bankroll = 1200
max_shooters = 10
strategies = {
    # "do not pass go strat": DoNotPassGo(verbose=verbose).update_bets,
    # "darkandlight strat": DarkAndLightStrategy().update_bets,
    # "keep coming strat": KeepComingBackStrategy().update_bets,
    # "coming everywhere strat": ComingEverywhereStrategy(verbose=verbose).update_bets,
    # "all in strat": AllInStrat(verbose=verbose).update_bets,
    # "nofield strat": NoFieldStrategy(verbose=verbose).update_bets,
    # "hedged2come strat": Hedged2Come(verbose=verbose).update_bets,
    # "knockout": craps.strategy.knockout,
    # "pass2come": PassLine2ComeStrategy(verbose=verbose).update_bets,
    "risk12": Risk12Strategy(verbose=verbose).update_bets,
    # "corey": customstrat.corey,
    # "safest way": SafestWayStrategy(verbose=verbose).update_bets,
}

def get_count_percent(count, total):
    return f"{count} ( {(count/total) * 100:.0f}%)"

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
    for s in strategies:
        result_summary[s] = 0
        min_bankroll[s] = bankroll, 0
        max_bankroll[s] = bankroll, 0
        target_reached_count[s] = 0
        bankrupt_count[s] = 0
    for i in range(n_sim):
        if verbose:
            print("\nNew Shooter!")
        table = craps.Table(verbose=verbose)
        for s in strategies:
            table.add_player(craps.Player(bankroll, strategies[s], s, target_bankroll=target_bankroll, verbose=verbose))

        table.run(max_rolls=float("inf"), max_shooter=max_shooters)
        total_rolls += table.dice.n_rolls
        if verbose:
            print(f"Rolls: {table.dice.n_rolls}")
        for s in strategies:
            strategy_player = table._get_player(s)
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



            row = [i, s, strategy_player_bankroll.current, bankroll, table.dice.n_rolls, strategy_player_bankroll.current-bankroll, (strategy_player_bankroll.current-bankroll)/table.dice.n_rolls]
            result_summary[s] = current_result + strategy_player_bankroll.current
            if verbose:
                print(f"{s}: {strategy_player_bankroll}")

            writer.writerow(row)
    print("\nSummary")
    print(f"Number of rolls: {total_rolls}")

    result_table = PrettyTable(["strategy", "target reached", "bankroll gone", "average bankroll", "biggest win", "biggest loss", "biggest bet", "biggest bankroll, rolls", "smallest bankroll, rolls"]) 

    for strategy, result in sorted(result_summary.items(), key=lambda item: item[1]):
        player = table._get_player(strategy)
        result_table.add_row([
            player.name,
            get_count_percent(target_reached_count[strategy], n_sim),
            get_count_percent(bankrupt_count[strategy], n_sim),
            round(result/n_sim, 2), player.bet_stats.biggest_win, player.bet_stats.biggest_loss, player.bet_stats.biggest_loss, max_bankroll[strategy], min_bankroll[strategy]])
    
    print(f"{n_sim} runs. {total_rolls} rolls (avg {(total_rolls/n_sim)}. {max_shooters} max shooters)")
    print(result_table)

