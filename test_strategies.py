import crapssim as craps
import customstrat

strategy = customstrat.dark_and_light

verbose = True
bankroll = 2000
player_name = "Test"
table = craps.Table(verbose=verbose)
table.add_player(craps.Player(bankroll, strategy, player_name, verbose=verbose))
table.run(max_rolls=float("inf"), max_shooter=1)
# dice = craps.Dice().fixed_roll((1,1))
# table._update_player_bets(dice=dice)
player = table.get_player(player_name)
print(player.bankroll, bankroll, table.dice.n_rolls, player.bankroll-bankroll, (player.bankroll-bankroll)/table.dice.n_rolls)
