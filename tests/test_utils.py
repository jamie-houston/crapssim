from crapssim.bet import BetStatus
from crapssim.dice import Dice


def set_point(table, roll):
    # roll once to establish point

    dice = Dice()
    dice.fixed_roll(roll)
    table._update_table(dice)

def verify_bet_not_on_table(player, bet):
    assert player.has_bet(bet) == False

def verify_bet_on_table(player, bet):
    assert player.has_matching_bet(bet)

def verify_roll_wins(table, player, bet, roll):
    dice = Dice()
    current_bankroll = player.bankroll_finance.current
    player.bet(bet)

    dice.fixed_roll(roll)
    info = player._update_bet(table, dice)[bet]
    assert info.status == BetStatus.WIN
    # validate win and payout
    assert player.bankroll_finance.current == current_bankroll + (bet.bet_amount * bet.payoutratio)

def verify_roll_loses(table, player, bet, roll):
    dice = Dice()
    player.bet(bet)
    dice.fixed_roll(roll)
    info = player._update_bet(table, dice)[bet]

    # validate loss
    assert info.status == BetStatus.LOSE
    
def verify_no_outcome(table, player, bet, roll):
    dice = Dice()
    player.bet(bet)
    dice.fixed_roll(roll)
    info = player._update_bet(table, dice)[bet]

    # validate loss
    assert info.status == BetStatus.PUSH
    