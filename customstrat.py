from crapssim.bet import PassLine, Odds, Come
from crapssim.bet import DontPass, LayOdds
from crapssim.bet import Place, Place4, Place5, Place6, Place8, Place9, Place10, SingleRoll
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

def hedged2come (player, table, unit=5, strat_info=None):
    # When off, don't pass line
    dontpass(player, table, unit)

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
    