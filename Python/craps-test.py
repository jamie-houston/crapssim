import os, sys
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
if rootDir not in sys.path: # add parent dir to paths
    sys.path.append(rootDir)
# import sys
# import os

# # Get the parent directory
# parent_dir = os.path.dirname(os.path.realpath(__file__))

# # Add the parent directory to sys.path
# sys.path.append(parent_dir)

# Import the module from the parent directory
import crapssim as craps

if __name__ == "__main__":

    # # Testing the rolling of dice
    # d1 = Dice()

    # d1.roll()
    # d1.roll()
    # d1.roll()

    # print("Number of rolls: {}".format(d1.n_rolls_))
    # print("Last Roll: {}".format(d1.result_))
    # print("Last Roll Total: {}".format(d1.total_))

    # Test making a player
    # Sean = Player(500)
    # print("Sean's bankroll: {}".format(Sean.bankroll))

    # Test making a bet
    # Sean.bet(passline(5))
    # print("Sean's bankroll: {}".format(Sean.bankroll))
    # print("Sean's current bets: {}".format(
    #   {b.name: b.bet_amount for b in Sean.bets_on_table}
    # ))
    # print("Sean's total bet amount: {}".format(sum(
    #  [b.bet_amount for b in Sean.bets_on_table]
    # )))

    table = craps.Table()

    # place8 bet
    Sean = craps.player.Player(100, "Sean")
    d = craps.dice.Dice()
    # Sean.bet(come(5))
    # # d.fixed_roll([4,4])
    # Sean.bet(come(6))
    Sean.bet(craps.bet.Come(5))

    d.fixed_roll([4, 4])
    Sean._update_bet(None, d)
    Sean.bet(craps.bet.Come(10))
    print("Sean's current bets: {}".format(
        {b.name: b.bet_amount for b in Sean.bets_on_table}
    ))  # NTS: this will not show duplicate bets, but they still exist
    print(Sean.bets_on_table)

    print(Sean.get_bet("Come", "8"))
