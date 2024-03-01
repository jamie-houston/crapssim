import pytest
import crapssim as craps 
from crapssim.bet import Field, Horn, Hard
from crapssim.dice import Dice


def hardway_bet(player, table, unit=5, strat_info=None):
    # bet horn and all hards
    player.bet(Hard(unit, 4))

def test_hard_way():
    unit = 10
    bankroll = 100
    bet = Hard(unit, 4)
    player = craps.Player(bankroll=bankroll, bet_strategy=hardway_bet)
    table = craps.Table()

    # create hardway bet
    current_bankroll = player.bankroll
    player.bet(bet)

    # roll hard way
    dice = Dice()
    dice.fixed_roll((2,2))
    player._update_bet(table, dice)
    
    # validate win and payout
    assert player.bankroll == current_bankroll + (unit * bet.payoutratio)

    # validate bet no longer valid (1 time bet)
    assert player.bets_on_table == []
    # roll non-hardway
    current_bankroll = player.bankroll
    player.bet(bet)
    dice.fixed_roll((1,3))
    player._update_bet(table, dice)

    # validate loss
    assert player.bankroll == current_bankroll - bet.bet_amount