import crapssim as craps
import customstrat
import csv
from crapssim.strategy.custom import DarkAndLightStrategy, NoFieldStrategy, KeepComingBackStrategy, ComingEverywhereStrategy, DoNotPassGo


verbose = False
n_sim = 100
# n_sim = 1
bankroll = 1000
target_bankroll = 1500
max_shooters = 2
strategies = {
    "do not pass go strat": DoNotPassGo(verbose=verbose).update_bets,
    "darkandlight strat": DarkAndLightStrategy().update_bets,
    "keep coming strat": KeepComingBackStrategy().update_bets,
    "coming everywhere strat": ComingEverywhereStrategy(verbose=verbose).update_bets,
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
    min_bankroll = {}
    max_bankroll = {}
    for s in strategies:
        result_summary[s] = 0
        min_bankroll[s] = bankroll
        max_bankroll[s] = bankroll
    for i in range(n_sim):
        print("\nNew Shooter!")
        table = craps.Table(verbose=verbose)
        for s in strategies:
            table.add_player(craps.Player(bankroll, strategies[s], s, target_bankroll=target_bankroll, verbose=verbose))

        table.run(max_rolls=float("inf"), max_shooter=max_shooters)
        total_rolls += table.dice.n_rolls
        print(f"Rolls: {table.dice.n_rolls}")
        for s in strategies:
            strategy_player = table._get_player(s)
            strategy_player_bankroll = strategy_player.bankroll
            current_result = result_summary[s]
            min_bankroll[s] = min(strategy_player_bankroll, min_bankroll[s])
            max_bankroll[s] = max(strategy_player_bankroll, max_bankroll[s])

            row = [i, s, strategy_player_bankroll, bankroll, table.dice.n_rolls, strategy_player_bankroll-bankroll, (strategy_player_bankroll-bankroll)/table.dice.n_rolls]
            result_summary[s] = current_result + strategy_player_bankroll
            print(f"{s}: {strategy_player_bankroll}")

            writer.writerow(row)
    print("\nSummary")
    print(f"Number of rolls: {total_rolls}")

    for strategy, result in sorted(result_summary.items(), key=lambda item: item[1]):
        player = table._get_player(strategy)
        print(f"\n{strategy} = {result}")
        if player.reached_target:
            print(f"***{player.name} reached target of {player.target_bankroll}***")
        print(f"biggest win: {player.biggest_win} biggest loss: {player.biggest_loss} biggest best: {player.biggest_bet} biggest bankroll: {max_bankroll[strategy]} smallest: {min_bankroll[strategy]}")