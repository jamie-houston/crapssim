from crapssim.bet import PassLine, Odds, Come
from crapssim.bet import DontPass, LayOdds
from crapssim.bet import Place, Place4, Place5, Place6, Place8, Place9, Place10
from crapssim.bet import Field, Horn, Hard

"""
Various betting strategies that are based on conditions of the CrapsTable.
Each strategy must take a table and a player_object, and implicitly 
uses the methods from the player object.
"""

"""
Custom Strategies
"""

def corey(player, table, unit=5, strat_info=None):
    # When off, pass line
    passline(player, table, unit)
    
    # When on, 2 come, play odds on 6 or 8, play field when not on 4 or 10
    if table.point.is_on():
        if table.point.number in [6, 8] and not player.has_bet("Odds") and player.has_bet("PassLine"):
            player.bet(Odds(3 * unit, player.get_bet("PassLine")))
        if player.num_bet("Come") < 2:
            player.bet(Come(unit))
        if not player.has_bet("Come4") and not player.has_bet("Come10") and player.num_bet("Come") > 0 and not player.has_bet("Field"):
            player.bet(
                Field(
                    unit,
                    double=table.payouts["fielddouble"],
                    triple=table.payouts["fieldtriple"],
                )
            )

def all_in(player, table, unit=5, strat_info=None):
    # bet horn and all hards
    player.bet(Horn(unit))
    player.bet(Hard(unit, 4))
    player.bet(Hard(unit, 6))
    player.bet(Hard(unit, 8))
    player.bet(Hard(unit, 10))

def dark_and_light(player, table, unit=5, strat_info=None):
    # When off, pass line
    # when on, come bet
    # 2 odds on each
    # 2,12 - bet * .1
    # 3 - bet * .2
    # come/pass bet = total bet * .75
    # point on hard number, bet hard

    all_bets = player.bets_on_table
    dontpass(player, table, unit*2, odds=2)

    if table.point.is_on():
        current_total = unit
        for bet in all_bets:
            if bet.name == "Come" and 7 not in bet.winning_numbers:
                current_total += bet.bet_amount
                player.bet(Odds(bet.bet_amount * 2, bet))
        # if player.num_bet("Come") < 3:
        player.bet(Come(current_total))
        player.bet(Horn(current_total*.2))
        # if table.point.number in [4,6,8,10]:
        #     player.bet(Hard(unit, table.point.number))

    # else:
    #     if player.num_bet("Come") < 3:
    #     if player.num_bet("Come") < 3:
    #         player.bet(Come(unit))

def keep_coming_back(player, table, unit=5, strat_info=None):
    # Get total of existing bets - half of winnings
    # Bet that amount on the field or 1/30 on 2 and 12
    # Bet twice that on come
    all_bets = player.bets_on_table
    current_total = unit

    for bet in all_bets:
        current_total += bet.bet_amount

    # player.bet(Field(current_total))
    player.bet(Hard(current_total/30, 2))
    player.bet(Hard(current_total/30, 12))
    # current_total *= 2
    if table.point.is_off():
        passline(player, table, current_total)
    else:
        player.bet(Come(current_total))


def coming_everywhere(player, table, unit=5, strat_info=None):
    # Bet unit on the pass line
    # Place bet unit on all numbers
    # Bet 10% of all bets on the table on the horn
    # Bet sum of all bets (including horn) on come
    passline(player, table, unit)
    all_bets = player.bets_on_table
    current_total = unit

    for bet in all_bets:
        current_total += bet.bet_amount

    player.bet(Horn(current_total*.1))
    current_total += current_total * .1

    if table.point.is_on():
        if len(all_bets) == 1:
            player.bet(Place10(unit))
            player.bet(Place9(unit))
            player.bet(Place8(unit))
            player.bet(Place6(unit))
            player.bet(Place5(unit))
            player.bet(Place4(unit))
        current_total += unit * 6
        player.bet(Come(current_total+unit))


def nofield(player, table, unit=5, strat_info=None):
    # When off, pass line
    passline(player, table, unit)
    
    # When on, 2 come, play odds on 6 or 8
    if table.point.is_on():
        if table.point.number in [6, 8] and not player.has_bet("Odds") and player.has_bet("PassLine"):
            player.bet(Odds(3 * unit, player.get_bet("PassLine")))
        if player.num_bet("Come") < 2:
            player.bet(Come(unit))

def hedged2come (player, table, unit=5, strat_info=None):
    # When off, don't pass line
    dontpass(player, table, unit)
    passline(player, table, unit)

    if table.point.is_on():
        if table.point.number in [6,8] and not player.has_bet("Odds") and player.has_bet("PassLine"):
            player.bet(Odds(3 * unit, player.get_bet("PassLine")))
        if player.num_bet("Come") < 2:
            player.bet(Come(unit))

"""
Fundamental Strategies
"""

def passline(player, table, unit=5, strat_info=None):
    # Pass line bet
    if table.point.is_off() and not player.has_bet("PassLine"):
        player.bet(PassLine(unit))

def dontpass(player, table, unit=5, odds=0):
    # Don't pass bet
    if table.point.is_off() and not player.has_bet("DontPass"):
        player.bet(DontPass(unit))
    
    if table.point.is_on():
        player.bet(Odds(odds * unit, player.get_bet("DontPass")))
