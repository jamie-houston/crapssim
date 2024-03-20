from crapssim.bet import Come, Odds, PassLine, Place, Place10, Place4, Place5, Place6, Place8, Place9, Field
from crapssim.strategy.bets import field_bet, passline_odds, place
from crapssim.strategy.strategy import Strategy


class IronCross(Strategy):
    """
    1 unit line bet with 2x odds
    1 unit field bet (while the point is ON)
    2 unit place bet on 5
    2 unit (plus cap) place bet on 6 and 8
    If the point is a 5, 6, or 8, skip the place bet on that number
    """

    @property
    def unit(self):
        return self.base_unit

    def __init__(self, unit=5, verbose=False):
        super().__init__(unit, verbose)
        self.strat_info = {"multiplier": 1}

    def on_coming_out(self, player, table):
        player.bet(PassLine(self.unit))

    def on_seven_out(self, player, table):
        multiplier = self.strat_info["multiplier"]
        if player.bankroll_finance.current < player.bankroll_finance.starting:
            multiplier += 1
        else:
            multiplier = max(multiplier - 1, 1)
        self.strat_info["multiplier"] = multiplier

    def on_any_status(self, player, table):
        field_bet(player, table, self.unit)

    def on_point_set(self, player, table, last_roll):
        passline_odds(player, table, self.unit, strat_info=None, mult=2)
        place(player, table, 2 * self.unit, strat_info={"numbers": {5, 6, 8}})


class IronCrossLadder(IronCross):
    @property
    def unit(self):
        multiplier = self.strat_info["multiplier"]
        return self.base_unit * multiplier


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

        field_bet(player, table, amount)


class NoFieldOnComeOut(Strategy):
    def after_roll_callback(self, player, table):
        if table.point.is_off():
            player.remove_if_present("Field")


class NoField(Strategy):
    def after_roll_callback(self, player, table):
        player.remove_if_present("Field")
