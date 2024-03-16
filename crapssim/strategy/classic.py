from crapssim.bet import Come, Odds, PassLine, Place, Place10, Place4, Place5, Place6, Place8, Place9, Field
from crapssim.strategy.strategy import Strategy


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


def place(player, table, unit, strat_info=None):
    if strat_info is not None:
        for point in strat_info["numbers"]:
            match point:
                case 4:
                    player.bet(Place4(unit))
                case 5:
                    player.bet(Place5(unit))
                case 6:
                    player.bet(Place6(unit))
                case 8:
                    player.bet(Place8(unit))
                case 9:
                    player.bet(Place9(unit))
                case 10:
                    player.bet(Place10(unit))


class IronCross(Strategy):
    """
    1 unit line bet with 2x odds
    1 unit field bet (while the point is ON)
    2 unit place bet on 5
    2 unit (plus cap) place bet on 6 and 8
    If the point is a 5, 6, or 8, skip the place bet on that number
    """
    def __amount_to_bet(self):
        multiplier = self.strat_info["multiplier"]
        return self.unit * multiplier

    def __init__(self, unit=5, verbose=False, alternatives = None):
        super().__init__(unit, verbose, alternatives)
        self.strat_info = {"multiplier": 1}

    def on_coming_out(self, player, table):
        player.bet(PassLine(self.__amount_to_bet()))

    def on_seven_out(self, player, table):
        multiplier = self.strat_info["multiplier"]
        if player.bankroll_finance.current < player.bankroll_finance.starting:
            multiplier += 1
        else:
            multiplier = max(multiplier - 1, 1)
        self.strat_info["multiplier"] = multiplier

    def on_any_status(self, player, table):
        if not player.has_bet_type(Field):
            player.bet(
                Field(
                    self.__amount_to_bet(),
                    double=table.payouts["fielddouble"],
                    triple=table.payouts["fieldtriple"],
                )
            )

    def on_point_set(self, player, table, last_roll):
        passline_odds(player, table, self.__amount_to_bet(), strat_info=None, mult=2)
        place(player, table, 2 * self.__amount_to_bet(), strat_info={"numbers": {5, 6, 8}})


class IronCrossOriginal(IronCross):
    def __amount_to_bet(self):
        return self.unit

    def __init__(self, unit=5, verbose=False):
        super().__init__(unit, verbose)
        self.strat_info = {"multiplier": 1}

    def on_coming_out(self, player, table):
        player.bet(PassLine(self.__amount_to_bet()))

    def on_seven_out(self, player, table):
        multiplier = self.strat_info["multiplier"]
        if player.bankroll_finance.current < player.bankroll_finance.starting:
            multiplier += 1
        else:
            multiplier = max(multiplier - 1, 1)
        self.strat_info["multiplier"] = multiplier

    def on_any_status(self, player, table):
        if not player.has_bet_type(Field):
            player.bet(
                Field(
                    self.__amount_to_bet(),
                    double=table.payouts["fielddouble"],
                    triple=table.payouts["fieldtriple"],
                )
            )

    def on_point_set(self, player, table, last_roll):
        passline_odds(player, table, self.__amount_to_bet(), strat_info=None, mult=2)
        place(player, table, 2 * self.__amount_to_bet(), strat_info={"numbers": {5, 6, 8}})


class Place68_2Come(Strategy):
    """
    Once point is established, place 6 and 8, with 2 additional come bets.
    The goal is to be on four distinct numbers, moving place bets if necessary
    """

    def on_active_point(self, player, table):
        current_numbers = []
        for bet in player.bets_on_table:
            current_numbers += bet.winning_numbers
        current_numbers = list(set(current_numbers))

        if len(player.bets_on_table) < 4:
            # always place 6 and 8 when they aren't come bets or place bets already
            if 6 not in current_numbers:
                player.bet(Place6(6 / 5 * self.unit))
            if 8 not in current_numbers:
                player.bet(Place8(6 / 5 * self.unit))

    def on_any_status(self, player, table):
        current_numbers = []
        for bet in player.bets_on_table:
            current_numbers += bet.winning_numbers
        current_numbers = list(set(current_numbers))

        # add come of passline bets to get on 4 numbers
        if player.number_of_bets_by_type(Come) == 0 and len(player.bets_on_table) < 4:
            if table.point.is_on():
                player.bet(Come(self.unit))
            if table.point.is_off() and (
                    player.has_bet_type(Place6) or player.has_bet_type(Place8)
            ):
                player.bet(PassLine(self.unit))

        # if come bet or passline goes to 6 or 8, move place bets to 5 or 9
        pass_come_winning_numbers = []
        if player.has_bet_type(PassLine):
            pass_come_winning_numbers += player.get_bet_type(PassLine).winning_numbers
        if player.has_bet_type(Come):
            pass_come_winning_numbers += player.get_bet("Come", "Any").winning_numbers

        if 6 in pass_come_winning_numbers:
            if player.has_bet_type(Place6):
                player.remove(player.get_bet_type(Place6))
            if 5 not in current_numbers:
                player.bet(Place5(self.unit))
            elif 9 not in current_numbers:
                player.bet(Place9(self.unit))
        elif 8 in pass_come_winning_numbers:
            if player.has_bet_type(Place8):
                player.remove(player.get_bet_type(Place8))
            if 5 not in current_numbers:
                player.bet(Place5(self.unit))
            elif 9 not in current_numbers:
                player.bet(Place9(self.unit))


class DiceDoctor(Strategy):
    """
    2 unit field bet, with a bet progression if you win.
    """
    def __init__(self, unit=5, verbose=False):
        super().__init__(unit, verbose)
        self.strat_info = None

    def on_any_status(self, player, table):

        if self.strat_info is None or table.last_roll in Field(0).losing_numbers:
            self.strat_info = {"progression": 0}
        else:
            self.strat_info["progression"] += 1

        bet_progression = [10, 20, 15, 30, 25, 50, 35, 70, 50, 100, 75, 150]
        prog = self.strat_info["progression"]
        if prog < len(bet_progression):
            amount = bet_progression[prog] * self.unit / 5
        elif prog % 2 == 0:
            # alternate between second to last and last
            amount = bet_progression[len(bet_progression) - 2] * self.unit / 5
        else:
            amount = bet_progression[len(bet_progression) - 1] * self.unit / 5

        player.bet(
            Field(
                amount,
                double=table.payouts["fielddouble"],
                triple=table.payouts["fieldtriple"],
            )
        )


# class HammerLock(Strategy):
    """
    1 unit pass line bet
    1 unit don’t pass bet, with a lay of 6 units in odds
    A phased place bet approach (no matter what the point is):
    Start with 2 unit (with cap) place bet each on 6 and 8
    If one of these bets wins, shift to 1 unit each inside (place the 5, 6, 8, and 9)
    If one of the inside bets wins, take all place bets down
    """
    # def on_coming_out(self, player, table):
    #     player.bet(PassLine(self.unit))
    #
    # def on_point_set(self, player, table, last_roll):
    #     passline_odds(player, table, self.unit(), strat_info=None, mult=345)
    #
    #     place_nums = set()
    #     for bet in player.bets_on_table:
    #         if isinstance(bet, Place):
    #             place_nums.add(bet.winning_numbers[0])
    #     place_point_nums = place_nums.copy()
    #     place_point_nums.add(table.point.number)
    #
    #     has_place68 = (6 in place_nums) or (8 in place_nums)
    #     has_place5689 = (
    #             (5 in place_nums) or (6 in place_nums) or (8 in place_nums) or (9 in place_nums)
    #     )
    #
    #     # 3 phases, place68, place_inside, takedown
    #     if self.strat_info is None or table.point.is_off():
    #         self.strat_info = {"mode": "place68"}
    #         for bet_nm in ["Place5", "Place6", "Place8", "Place9"]:
    #             player.remove_if_present(bet_nm)
    #
    #     if self.strat_info["mode"] == "place68":
    #         if table.point.is_on() and has_place68 and place_nums != {6, 8}:
    #             # assume that a place 6/8 has won
    #             if player.has_bet("Place6"):
    #                 player.remove(player.get_bet("Place6"))
    #             if player.has_bet("Place8"):
    #                 player.remove(player.get_bet("Place8"))
    #             self.strat_info["mode"] = "place_inside"
    #             place(
    #                 player,
    #                 table,
    #                 self.unit,
    #                 self.strat_info={"numbers": {5, 6, 8, 9}},
    #                 self.skip_point=False,
    #             )
    #         else:
    #             place(
    #                 player,
    #                 table,
    #                 2 * unit,
    #                 strat_info={"numbers": {6, 8}},
    #                 skip_point=False,
    #             )
    #     elif strat_info["mode"] == "place_inside":
    #         if table.point.is_on() and has_place5689 and place_nums != {5, 6, 8, 9}:
    #             # assume that a place 5/6/8/9 has won
    #             for bet_nm in ["Place5", "Place6", "Place8", "Place9"]:
    #                 player.remove_if_present(bet_nm)
    #             strat_info["mode"] = "takedown"
    #         else:
    #             place(
    #                 player,
    #                 table,
    #                 unit,
    #                 strat_info={"numbers": {5, 6, 8, 9}},
    #                 skip_point=False,
    #             )
    #     elif strat_info["mode"] == "takedown" and table.point.is_off():
    #         strat_info = None
