import pytest
import crapssim as craps 
from crapssim.bet import Hard, Place6, Horn, SingleRoll
from crapssim.dice import Dice
from crapssim.strategy.strategy import Strategy

class TestStrategy(Strategy):
    def __init__(self):
        super().__init__("Test Strategy")

    def 

def test_win():
    strategy = TestStrategy()
    unit = 10
    bankroll = 100
    bet = Hard(unit, 4)
    player = craps.Player(bankroll=bankroll)
    table = craps.Table()
    dice = Dice()
    dice.roll()
    player.bet(bet)

    player._update_bet(table, dice)
    Strategy.on_roll(player, table, unit)