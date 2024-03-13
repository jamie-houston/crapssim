import crapssim as craps 
from crapssim.bet import BetStatus, Hard, Odds, PassLine, Place6, Horn, SingleRoll
from crapssim.dice import Dice
from crapssim.player import Player
from crapssim.table import Table
from tests.test_utils import set_point, verify_bet_not_on_table, verify_bet_on_table, verify_no_outcome, verify_roll_loses, verify_roll_wins

def test_hard_way():
    unit = 10
    bankroll = 100
    bet = Hard(unit, 4)
    player = Player(bankroll=bankroll)
    table = Table()
    verify_roll_wins(table, player, bet, (2,2))
    verify_bet_not_on_table(player, bet)
    verify_roll_loses(table, player, bet, (1,3))
    verify_bet_not_on_table(player, bet)

def test_place_bet():
    unit = 12
    bankroll = 100
    # create place bet
    bet = Place6(unit)
    player = Player(bankroll=bankroll)
    table = Table()
    set_point(table, (3,6))

    verify_roll_wins(table, player, bet, (3,3))
    verify_bet_on_table(player, bet)
    verify_no_outcome(table, player, bet, (2,3))
    verify_bet_on_table(player, bet)
    verify_roll_loses(table, player, bet, (1,6))
    verify_bet_not_on_table(player, bet)

def test_single_roll_bet():
    unit = 10
    bankroll = 100
    player = Player(bankroll=bankroll)
    table = Table()
    bet = SingleRoll(unit, 2)

    verify_roll_wins(table, player, bet, (1,1))
    verify_bet_not_on_table(player, bet)
    verify_roll_loses(table, player, bet, (1,3))
    verify_bet_not_on_table(player, bet)

def test_payout_correct():
    table = Table()
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

def test_odds():
    table = Table()
    unit = 5
    bankroll = 100
    passline_bet = PassLine(unit)
    player = Player(bankroll = bankroll)
    verify_no_outcome(table, player, passline_bet, (3,6))
    verify_bet_on_table(player, passline_bet)
    odds_bet = Odds(unit, passline_bet)
    verify_no_outcome(table, player, odds_bet, (1,4))
    verify_no_outcome(table, player, passline_bet, (2,3))
    verify_bet_on_table(player, passline_bet)
    verify_bet_on_table(player, odds_bet)

    # TODO: Verify odds and passline bets
    # verify_roll_wins(table, player, odds_bet, (4,5))