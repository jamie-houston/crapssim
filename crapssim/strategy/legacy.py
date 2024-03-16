def passline_odds2(player, table, unit=5, strat_info=None):
    passline_odds(player, table, unit, strat_info=None, mult=2)


def passline_odds345(player, table, unit=5, strat_info=None):
    passline_odds(player, table, unit, strat_info=None, mult="345")



def place68(player, table, unit=5, strat_info=None):
    passline(player, table, unit, strat_info=None)
    # Place 6 and 8 when point is ON
    p_has_place_bets = player.has_bet(
        "Place4", "Place5", "Place6", "Place8", "Place9", "Place10"
    )
    if table.point.is_on() and not p_has_place_bets:
        if table.point.number == 6:
            player.bet(Place8(6 / 5 * unit))
        elif table.point.number == 8:
            player.bet(Place6(6 / 5 * unit))
        else:
            player.bet(Place8(6 / 5 * unit))
            player.bet(Place6(6 / 5 * unit))


def dontpass(player, table, unit=5, strat_info=None):
    # Don't pass bet
    if table.point.is_off() and not player.has_bet_type(DontPass):
        player.bet(DontPass(unit))

def dontcome(player, table, unit=5, strat_info=None):
    # Don't come bet
    if table.point.is_on():
        player.bet(DontCome(unit))

def layodds(player, table, unit=5, strat_info=None, win_mult=1):
    # Assume that someone tries to win the `win_mult` times the unit on each bet, which corresponds
    # well to the max_odds on a table.
    # For `win_mult` = "345", this assumes max of 3-4-5x odds
    dontpass(player, table, unit)

    # Lay odds for don't pass
    if win_mult == "345":
        mult = 6.0
    else:
        win_mult = float(win_mult)
        if table.point.is_on():
            if table.point.number in [4, 10]:
                mult = 2 * win_mult
            elif table.point.number in [5, 9]:
                mult = 3 / 2 * win_mult
            elif table.point.number in [6, 8]:
                mult = 6 / 5 * win_mult

    if (
        table.point.is_on()
        and player.has_bet("DontPass")
        and not player.has_bet("LayOdds")
    ):
        player.bet(LayOdds(mult * unit, player.get_bet("DontPass")))


"""
Detailed Strategies
"""




def knockout(player, table, unit=5, strat_info=None):
    """
    1 unit pass line
    1 unit don’t pass
    3-4-5x odds behind the pass line bet
    """
    passline_odds345(player, table, unit)
    dontpass(player, table, unit)



def place68_cpr(player, table, unit=5, strat_info=None):
    """ place 6 & 8 after point is establish.  Then collect, press, and regress (in that order) on each win """
    ## NOTE: NOT WORKING
    if strat_info is None:
        strat_info = {"mode6": "collect", "mode8": "collect"}

    if table.point.is_on():
        # always place 6 and 8 when they aren't place bets already
        if not player.has_bet("Place6"):
            player.bet(Place6(6 / 5 * unit))
        if not player.has_bet("Place8"):
            player.bet(Place8(6 / 5 * unit))

    if table.bet_update_info is not None:
        # place6
        if player.has_bet("Place6"):
            bet = player.get_bet("Place6")
            if (
                table.bet_update_info[player].get(bet.name) is not None
            ):  # bet has not yet been updated; skip
                # ic("level3")
                # ic(table.bet_update_info[player][bet.name])
                if table.bet_update_info[player][bet.name]["status"] == "win":
                    # ic("place6 mode: {}".format(strat_info["mode6"]))
                    if strat_info["mode6"] == "press":
                        player.remove(bet)
                        player.bet(Place6(2 * bet.bet_amount))
                        strat_info["mode6"] = "regress"
                    elif strat_info["mode6"] == "regress":
                        player.remove(bet)
                        player.bet(Place6(6 / 5 * unit))
                        strat_info["mode6"] = "collect"
                    elif strat_info["mode6"] == "collect":
                        strat_info["mode6"] = "press"
                    # ic("updated place6 mode: {}".format(strat_info["mode6"]))
        # place8
        if player.has_bet("Place8"):
            bet = player.get_bet("Place8")
            if (
                table.bet_update_info[player].get(bet.name) is not None
            ):  # bet has not yet been updated; skip
                # ic("level3")
                # ic(table.bet_update_info[player][bet.name])
                if table.bet_update_info[player][bet.name]["status"] == "win":
                    # ic("place8 mode: {}".format(strat_info["mode8"]))
                    if strat_info["mode8"] == "press":
                        player.remove(bet)
                        player.bet(Place8(2 * bet.bet_amount))
                        strat_info["mode8"] = "regress"
                    elif strat_info["mode8"] == "regress":
                        player.remove(bet)
                        player.bet(Place8(6 / 5 * unit))
                        strat_info["mode8"] = "collect"
                    elif strat_info["mode8"] == "collect":
                        strat_info["mode8"] = "press"

    ic(strat_info)
    return strat_info


if __name__ == "__main__":
    # Test a betting strategy

    from player import Player
    from dice import Dice
    from table import Table

    # table = CrapsTable()
    # table._add_player(Player(500, place68_2come))

    d = Dice()
    p = Player(500, place68_2come)
    p.bet(PassLine(5))
    p.bet(Place6(6))
    ic(p.bets_on_table)
    ic(p.bankroll)
    ic(p.total_bet_amount)
