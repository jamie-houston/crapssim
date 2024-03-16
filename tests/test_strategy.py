import crapssim as craps
from crapssim.dice import Dice
from crapssim.strategy.strategy import Strategy


class TestStrategy(Strategy):
    def __init__(self):
        super().__init__("Test Strategy")
        self.is_set = False

    def on_new_shooter(self, player, table):
        self.is_set = True


def test_new_shooter():
    strategy = TestStrategy()
    unit = 10
    bankroll = 100
    player = craps.Player(bankroll=bankroll, bet_strategy=strategy.update_bets)
    table = craps.Table()
    table.add_player(player)
    dice = Dice()
    dice.roll()

    assert strategy.is_set == False
    player._add_strategy_bets(table, unit)

    assert strategy.is_set == True
