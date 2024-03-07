import crapssim as craps
import customstrat
import csv
from crapssim.strategy.custom import DarkAndLightStrategy, NoFieldStrategy, KeepComingBackStrategy, ComingEverywhereStrategy, DoNotPassGo


verbose = False
n_sim = 1000
# n_sim = 1
bankroll = 1000
target_bankroll = 1500
max_shooters = 10
strategies = {
    "darkandlight strat": DarkAndLightStrategy().update_bets,
    "keep coming strat": KeepComingBackStrategy().update_bets,
    "coming everywhere strat": ComingEverywhereStrategy(verbose=verbose).update_bets,
    "do not pass go strat": DoNotPassGo(verbose=verbose).update_bets,
    "nofield strat": NoFieldStrategy().update_bets,
    "hedged2come": customstrat.hedged2come,
    "knockout": craps.strategy.knockout,
    "pass2come": craps.strategy.pass2come,
    "risk12": craps.strategy.risk12,
    "allin": customstrat.all_in,
    "corey": customstrat.corey,
    "allin": customstrat.all_in,
}

with open('data.csv', 'w', newline='') as f:
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
            table.add_player(craps.Player(bankroll, strategies[s], s, target_bankroll=target_bankroll, verbose=verbose))

        table.run(max_rolls=float("inf"), max_shooter=max_shooters)
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
        if player.reached_target:
            print(f"***{player.name} reached target of {player.target_bankroll}***")

    for strategy, result in sorted(result_summary.items(), key=lambda item: item[1]):
        sorted_summary.append(f"{result}: {strategy}")
        print(f"{strategy} = {result}")