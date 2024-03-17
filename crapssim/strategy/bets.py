from crapssim.bet import PassLine, Odds, Place4, Place5, Place6, Place8, Place9, Place10, Field


def passline_odds(player, table, unit=5, strat_info=None, mult=1):
    # Pass line odds
    if mult == "345":
        if table.point.is_on():
            if table.point.number in [4, 10]:
                mult = 3
            elif table.point.number in [5, 9]:
                mult = 4
            elif table.point.number in [6, 8]:
                mult = 5
    else:
        mult = float(mult)

    if (
            table.point.is_on()
            and player.has_bet_type(PassLine)
            and not player.has_bet_type(Odds)
    ):
        player.bet(Odds(mult * unit, player.get_bet_type(PassLine)))


# def place(player, table, unit, strat_info=None):
#     if strat_info is not None:
#         for point in strat_info["numbers"]:
#             match point:
#                 case 4:
#                     player.bet(Place4(unit))
#                 case 5:
#                     player.bet(Place5(unit))
#                 case 6:
#                     player.bet(Place6(unit))
#                 case 8:
#                     player.bet(Place8(unit))
#                 case 9:
#                     player.bet(Place9(unit))
#                 case 10:
#                     player.bet(Place10(unit))
#
def place(player, table, unit=5, strat_info={"numbers": {6, 8}}, skip_point=True):
    strat_info["numbers"] = set(strat_info["numbers"]).intersection({4, 5, 6, 8, 9, 10})
    if skip_point:
        strat_info["numbers"] -= {table.point.number}

    # Place the provided numbers when point is ON
    if table.point.is_on():
        if not player.has_bet("Place4") and 4 in strat_info["numbers"]:
            player.bet(Place4(unit))
        if not player.has_bet("Place5") and 5 in strat_info["numbers"]:
            player.bet(Place5(unit))
        if not player.has_bet("Place6") and 6 in strat_info["numbers"]:
            player.bet(Place6(6 / 5 * unit))
        if not player.has_bet("Place8") and 8 in strat_info["numbers"]:
            player.bet(Place8(6 / 5 * unit))
        if not player.has_bet("Place9") and 9 in strat_info["numbers"]:
            player.bet(Place9(unit))
        if not player.has_bet("Place10") and 10 in strat_info["numbers"]:
            player.bet(Place10(unit))

    # Move the bets off the point number if it shows up later
    if skip_point and table.point.is_on():
        if player.has_bet("Place4") and table.point.number == 4:
            player.remove(player.get_bet("Place4"))
        if player.has_bet("Place5") and table.point.number == 5:
            player.remove(player.get_bet("Place5"))
        if player.has_bet("Place6") and table.point.number == 6:
            player.remove(player.get_bet("Place6"))
        if player.has_bet("Place8") and table.point.number == 8:
            player.remove(player.get_bet("Place8"))
        if player.has_bet("Place9") and table.point.number == 9:
            player.remove(player.get_bet("Place9"))
        if player.has_bet("Place10") and table.point.number == 10:
            player.remove(player.get_bet("Place10"))



def field_bet(player, table, unit):
    player.bet(
        Field(
            unit,
            double=table.payouts["fielddouble"],
            triple=table.payouts["fieldtriple"],
        )
    )
