import pytest
import crapssim as craps 
from crapssim.bet import Hard, Place6
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

def test_place_bet():
    unit = 12
    bankroll = 100
    player = craps.Player(bankroll=bankroll)
    table = craps.Table()

    current_bankroll = player.bankroll

    dice = Dice()
    dice.fixed_roll((3,6))

    # roll once to establish point
    table._update_table(dice)

    # create place bet
    bet = Place6(unit)
    player.bet(bet)

    # roll 6
    dice.fixed_roll((3,3))
    player._update_bet(table, dice)
    
    # validate win and payout
    assert player.bankroll == current_bankroll + (unit * bet.payoutratio)

    # validate bet still valid
    # TODO: Currently all bets are pulled off after each roll... this should be only 1 time rolls
    # assert player.bets_on_table == [bet]
    # roll non-6
    current_bankroll = player.bankroll
    player.bet(bet)
    dice.fixed_roll((1,3))
    player._update_bet(table, dice)

    # validate loss
    assert player.bankroll == current_bankroll - bet.bet_amount
