import pytest
import crapssim as craps 
from crapssim.bet import Hard, Place6
from crapssim.dice import Dice

def test_hard_way():
    unit = 10
    bankroll = 100
    bet = Hard(unit, 4)
    player = craps.Player(bankroll=bankroll)
    table = craps.Table()
    verify_roll_wins(table, player, bet, (2,2))
    verify_roll_loses(table, player, bet, (1,3))

def test_place_bet():
    unit = 12
    bankroll = 100
    # create place bet
    bet = Place6(unit)
    player = craps.Player(bankroll=bankroll)
    table = craps.Table()

    set_point(table, (3,6))

    verify_roll_wins(table, player, bet, (3,3))
    verify_roll_loses(table, player, bet, (1,3))

def set_point(table, roll):
    dice = Dice()

    dice.fixed_roll(roll)

    # roll once to establish point
    table._update_table(dice)

def verify_roll_wins(table, player, bet, roll):
    dice = Dice()
    # create hardway bet
    current_bankroll = player.bankroll
    player.bet(bet)

    # roll hard way
    dice.fixed_roll(roll)
    player._update_bet(table, dice)
    
    # validate win and payout
    assert player.bankroll == current_bankroll + (bet.bet_amount * bet.payoutratio)

    # validate bet no longer valid (1 time bet)
    assert player.bets_on_table == []

def verify_roll_loses(table, player, bet, roll):
    dice = Dice()
    # roll non-hardway
    current_bankroll = player.bankroll
    player.bet(bet)
    dice.fixed_roll(roll)
    player._update_bet(table, dice)

    # validate loss
    assert player.bankroll == current_bankroll - bet.bet_amount
    