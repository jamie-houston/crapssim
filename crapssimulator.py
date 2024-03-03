import crapssim as craps
import customstrat
import csv
from crapssim.strategy.strategy import *


# n_sim = 10000
n_sim = 1
bankroll = 1000
strategies = {
    "dark strat": DarkAndLightStrategy().update_bets,
    # "dark pattern": DarkAndLightStrategy.update_bets,
    # "nofield": customstrat.nofield,
    # "hedged2come": customstrat.hedged2come,
    # "knockout": craps.strategy.knockout,
    # "pass2come": craps.strategy.pass2come,
    # "risk12": craps.strategy.risk12,
    "darkandlight": customstrat.dark_and_light,
    # "coming everywhere": customstrat.coming_everywhere,
    # "keep coming back": customstrat.keep_coming_back,
    # "corey": customstrat.corey,
    # "allin": customstrat.all_in,
}

with open('data.csv', 'w', newline='') as f:
    verbose = True
    writer = csv.writer(f)
    header = ["Sim Number", "Strategy", "End Bankroll", "Start Bankroll", "Dice Rolls", "Difference", "Dollar/Roll"]
    writer.writerow(header)

    result_summary = {}
    total_rolls = 0
    for s in strategies:
        result_summary[s] = 0
    for i in range(n_sim):
        print("\nNew Shooter!")
        table = craps.Table(verbose=verbose)
        for s in strategies:
            table.add_player(craps.Player(bankroll, strategies[s], s, verbose=verbose))

        darkStrat = DarkAndLightStrategy()
        noFieldStrat = NoFieldStrategy()
        # table.add_player(craps.Player(bankroll, darkStrat.update_bets, "Dark Strat", verbose=verbose))
        # table.add_player(craps.Player(bankroll, noFieldStrat.update_bets, "No Field Strat", verbose=verbose))
        table.run(max_rolls=float("inf"), max_shooter=5)
        total_rolls += table.dice.n_rolls
        print(f"Rolls: {table.dice.n_rolls}")
        for s in strategies:
            current_result = result_summary[s]
            row = [i, s, table._get_player(s).bankroll, bankroll, table.dice.n_rolls, table._get_player(s).bankroll-bankroll, (table._get_player(s).bankroll-bankroll)/table.dice.n_rolls]
            result_summary[s] = current_result + table._get_player(s).bankroll
            print(f"{s}: {table._get_player(s).bankroll}")

            writer.writerow(row)
    print("\nSummary")
    print(f"Number of rolls: {total_rolls}")
    sorted_summary = []

    for player in table.players:
        print(f"{player.name} - biggest win: {player.biggest_win} biggest loss: {player.biggest_loss} biggest best: {player.biggest_bet}")

    for strategy, result in sorted(result_summary.items(), key=lambda item: item[1]):
    # for strat,result in result_summary.items():
        sorted_summary.append(f"{result}: {strategy}")
        print(f"{strategy} = {result}")