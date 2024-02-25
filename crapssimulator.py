import crapssim as craps
import customstrat
import csv

# n_sim = 10000
n_sim = 1
bankroll = 200
strategies = {
    # "nofield": customstrat.nofield,
    # "hedged2come": customstrat.hedged2come,
    # "knockout": craps.strategy.knockout,
    # "pass2come": craps.strategy.pass2come,
    # "risk12": craps.strategy.risk12,
    "darkandlight": customstrat.dark_and_light
    # "corey": customstrat.corey
}

with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    header = ["Sim Number", "Strategy", "End Bankroll", "Start Bankroll", "Dice Rolls", "Difference", "Dollar/Roll"]
    writer.writerow(header)

    result_summary = {}
    for s in strategies:
        result_summary[s] = 0
    for i in range(n_sim):
        table = craps.Table()
        for s in strategies:
            table.add_player(craps.Player(bankroll, strategies[s], s))

        table.run(max_rolls=float("inf"), max_shooter=1, verbose=True)
        for s in strategies:
            current_result = result_summary[s]
            row = [i, s, table._get_player(s).bankroll, bankroll, table.dice.n_rolls, table._get_player(s).bankroll-bankroll, (table._get_player(s).bankroll-bankroll)/table.dice.n_rolls]
            result_summary[s] = current_result + table._get_player(s).bankroll
            # print(row)

            writer.writerow(row)
    print("Summary")
    sorted_summary = []

    for strategy, result in sorted(result_summary.items(), key=lambda item: item[1]):
    # for strat,result in result_summary.items():
        sorted_summary.append(f"{result}: {strategy}")
        print(f"{strategy} = {result}")