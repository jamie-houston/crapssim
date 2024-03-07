import pytest
import crapssim as craps 
from crapssim.bet import BetStatus, Hard, Place6, Horn, SingleRoll
from crapssim.dice import Dice

def test_hard_way():
    unit = 10
    bankroll = 100
    bet = Hard(unit, 4)
    player = craps.Player(bankroll=bankroll)
    table = craps.Table()
    verify_roll_wins(table, player, bet, (2,2))
    verify_bet_on_table(player, bet)
    verify_roll_loses(table, player, bet, (1,3))
    verify_bet_not_on_table(player, bet)

def test_place_bet():
    unit = 12
    bankroll = 100
    # create place bet
    bet = Place6(unit)
    player = craps.Player(bankroll=bankroll)
    table = craps.Table()

    set_point(table, (3,6))

    verify_roll_wins(table, player, bet, (3,3))
    verify_bet_on_table(player, bet)
    verify_no_outcome(table, player, bet, (2,3))
    verify_bet_on_table(player, bet)
    verify_roll_loses(table, player, bet, (1,6))
    verify_bet_not_on_table(player, bet)

def test_single_roll():
    unit = 10
    bankroll = 100
    player = craps.Player(bankroll=bankroll)
    table = craps.Table()
    bet = SingleRoll(unit, 2)

    verify_roll_wins(table, player, bet, (1,1))
    verify_bet_not_on_table(player, bet)
    verify_roll_loses(table, player, bet, (1,3))
    verify_bet_not_on_table(player, bet)

def test_payout_correct():
    table = craps.Table()
    unit = 5
    dice = Dice()
    bet = SingleRoll(unit, 12)
    dice.fixed_roll((6,6))
    result = bet._update_bet(table, dice)
    assert result.win_amount == unit * 30
    assert result.status == BetStatus.WIN

    bet = Horn(unit)
    dice.fixed_roll((1,1))
    result = bet._update_bet(table, dice)
    assert result.win_amount == unit * 30/4
    assert result.status == BetStatus.WIN

def set_point(table, roll):
    dice = Dice()

    dice.fixed_roll(roll)

    # roll once to establish point
    table._update_table(dice)

def verify_bet_not_on_table(player, bet):
    assert player.has_bet(bet) == False

def verify_bet_on_table(player, bet):
    assert player.has_matching_bet(bet)

def verify_roll_wins(table, player, bet, roll):
    dice = Dice()
    # create hardway bet
    current_bankroll = player.bankroll
    player.bet(bet)

    # roll hard way
    dice.fixed_roll(roll)
    info = player._update_bet(table, dice)[bet.name]
    assert info.status == BetStatus.WIN
    # validate win and payout
    assert player.bankroll == current_bankroll + (bet.bet_amount * bet.payoutratio)

def verify_roll_loses(table, player, bet, roll):
    dice = Dice()
    # roll non-hardway
    player.bet(bet)
    dice.fixed_roll(roll)
    info = player._update_bet(table, dice)

    # validate loss
    assert info.status == BetStatus.LOSE
    
def verify_no_outcome(table, player, bet, roll):
    dice = Dice()
    # roll non-hardway
    player.bet(bet)
    dice.fixed_roll(roll)
    info = player._update_bet(table, dice)

    # validate loss
    assert info.status == BetStatus.PUSH
    