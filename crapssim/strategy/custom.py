from crapssim.strategy.bets import place
from crapssim.strategy.classic import IronCrossLadder, DiceDoctor
from crapssim.strategy.strategy import Strategy
from crapssim.bet import *
from icecream import ic


class NoField(Strategy):
    def __init__(self, unit=5, verbose=False):
        super().__init__(unit, verbose)

    def on_coming_out(self, player, table):
        # When off, pass line
        if self.verbose:
            print(f"NOFIELD:Coming Out")
        player.bet(PassLine(self.unit))

    def on_active_point(self, player, table):
        if table.point.number in [6, 8] and not player.has_bet_type(Odds) and player.has_bet_type(PassLine):
            player.bet(Odds(3 * self.unit, player.get_bet_type(PassLine)))
        if player.number_of_bets_by_type(Come) < 2:
            player.bet(Come(self.unit))


class DarkAndLight(Strategy):
    # When off, pass line
    # when on, come bet
    # 2 odds on each
    # 2,12 - bet * .1
    # 3 - bet * .2
    # come/pass bet = total bet * .75
    # point on hard number, bet hard
    def on_coming_out(self, player, table):
        player.bet(DontPass(self.unit * 2))

    def on_active_point(self, player, table):
        player.bet(Come(self.unit))

    def after_bet_result(self, player, table, bet_info):
        # if it's a come or pass bet, bet odds
        if bet_info.is_bet_type(DontPass) or bet_info.is_bet_type(Come):
            player.bet(Odds(bet_info.bet_amount * 2, bet_info))

    def on_any_status(self, player, table):
        player.bet(Come(self.unit))
        player.bet(Horn(self.unit * .2))
        player.bet(SingleRoll(self.unit * .1, 2))
        player.bet(SingleRoll(self.unit * .1, 12))
        player.bet(SingleRoll(self.unit * .1, 3))
        if table.point.number in [4, 6, 8, 10]:
            player.bet(Hard(self.unit * .25, table.point.number))


class KeepComingBack(Strategy):
    def on_coming_out(self, player, table):
        current_total = self.unit + get_current_total_without_profit(player, self.unit)

        player.bet(PassLine(current_total))

    def on_active_point(self, player, table):
        current_total = self.unit + get_current_total_without_profit(player, self.unit)

        player.bet(Come(current_total))

    def on_any_status(self, player, table):
        current_total = get_current_total_without_profit(player, self.unit)
        horn_bet = round(current_total / 30, 2)
        player.bet(SingleRoll(horn_bet, 2))
        player.bet(SingleRoll(horn_bet, 12))


class ComingEverywhere(Strategy):
    # Bet total of all existing bets on Pass/Come
    # Bet 1 unit on all places

    def on_coming_out(self, player, table):
        player.bet(PassLine(get_current_total_without_profit(player, self.unit)))

    def on_active_point(self, player, table):
        if len(player.bets_on_table) == 1:
            player.bet(Place10(self.unit))
            player.bet(Place9(self.unit))
            player.bet(Place8(self.unit))
            player.bet(Place6(self.unit))
            player.bet(Place5(self.unit))
            player.bet(Place4(self.unit))
        player.bet(Come(get_current_total_without_profit(player, self.unit) + self.unit))


class DoNotPassGo(Strategy):
    def __init__(self, unit=25, starting_multiplier=3, verbose=False):
        self.bet_placed = False
        self.last_bet_amount = unit
        self.starting_multiplier = starting_multiplier
        super().__init__(unit, verbose)

    def on_loss(self, player, table, losing_bet_info):
        next_bet_amount = losing_bet_info.bet_amount + self.unit
        ic(f"Lost {losing_bet_info}. Raising bet to {next_bet_amount}")
        if table.point.is_on():
            self._add_bet(player, DontCome(next_bet_amount))
        else:
            self._add_bet(player, DontPass(self.unit * self.starting_multiplier))

    def on_coming_out(self, player, table):
        self._add_bet(player, DontPass(self.unit * self.starting_multiplier))
        self.bet_placed = False

    def on_active_point(self, player, table):
        self._add_bet(player, DontCome(max(self.last_bet_amount - self.unit, self.unit)))
        self.bet_placed = False

    def _add_bet(self, player, bet):
        if not self.bet_placed:
            player.bet(bet)
            self.last_bet_amount = bet.bet_amount
            self.bet_placed = True


class AllIn(Strategy):
    def on_any_status(self, player, table):
        player.bet(Horn(self.unit))
        player.bet(Hard(self.unit, 4))
        player.bet(Hard(self.unit, 6))
        player.bet(Hard(self.unit, 8))
        player.bet(Hard(self.unit, 10))


class Hedged2Come(Strategy):
    # When off, don't pass line
    # When point is 6 or 8, put 3 times odds on pass line
    # Add up to 2 come bets

    def on_coming_out(self, player, table):
        player.bet(PassLine(self.unit))

    def on_point_set(self, player, table, last_roll):
        if last_roll in [6, 8]:
            player.bet(Odds(3 * self.unit, player.get_bet_type(PassLine)))

    def on_active_point(self, player, table):
        if player.number_of_bets_by_type(Come) < 2:
            player.bet(Come(self.unit))


class PassLine2Come(Strategy):
    def on_coming_out(self, player, table):
        player.bet(PassLine(self.unit))

    def on_active_point(self, player, table):
        if player.number_of_bets_by_type(Come) < 2:
            player.bet(Come(self.unit))


class Risk12(Strategy):
    """
    Before a point is established:
    1 unit pass line
    1 unit field bet
    After a point is established:
    1 unit (plus cap) place bet on 6 and 8, if you have winnings from the pre-point phase:
    Generally, if the point is 4/9/10, you can take your field winnings plus cap for the place bets
    If the point is 5/6/8, you lost in the field, but if you had won on some combinations of
    earlier rolls (2, 12, 11) you might have enough to add one or both of the place bets.
    """
    def __init__(self, unit=5, verbose=False):
        super().__init__(unit, verbose)
        self.strat_info = {"winnings": 0}

    def on_coming_out(self, player, table):
        player.bet(PassLine(self.unit))

        if table.last_roll in table.payouts["fielddouble"]:
            # win double from the field, lose pass line, for a net of 1 unit win
            self.strat_info["winnings"] += self.unit
        elif table.last_roll in table.payouts["fieldtriple"]:
            # win triple from the field, lose pass line, for a net of 2 unit win
            self.strat_info["winnings"] += 2 * self.unit
        elif table.last_roll == 11:
            # win the field and pass line, for a net of 2 units win
            self.strat_info["winnings"] += 2 * self.unit
        player.bet(
            Field(
                self.unit,
                double=table.payouts["fielddouble"],
                triple=table.payouts["fieldtriple"],
            )
        )

    def on_new_shooter(self, player, table):
        self.strat_info = {"winnings": 0}

    def on_active_point(self, player, table):
        if table.point.number in [4, 9, 10]:
            place(player, table, self.unit, strat_info={"numbers": {6, 8}})
        elif table.point.number in [5, 6, 8]:
            # lost field bet, so can't automatically cover the 6/8 bets.  Need to rely on potential early winnings
            if self.strat_info["winnings"] >= 2 * self.unit:
                place(player, table, self.unit, strat_info={"numbers": {6, 8}})
            elif self.strat_info["winnings"] >= 1 * self.unit:
                if table.point.number != 6:
                    place(player, table, self.unit, strat_info={"numbers": {6}})
                else:
                    place(player, table, self.unit, strat_info={"numbers": {8}})


def get_current_total_without_profit(player, unit):
    all_bets = player.bets_on_table
    profit = player.bankroll_finance.current - player.bankroll_finance.starting
    current_total = 0

    for bet in all_bets:
        current_total += bet.bet_amount
    if profit > 0:
        current_total = int(max(current_total / 2, current_total - (profit / 2)))

    current_total -= max(unit, player.bankroll_finance.current - player.bankroll_finance.starting)
    current_total = max(unit, current_total)
    return current_total


class SafestWay(Strategy):
    def on_coming_out(self, player, table):
        player.bet(PassLine(self.unit))

    def on_active_point(self, player, table):
        if player.number_of_bets_by_type(Come) < player.number_of_bets_by_type(DontCome):
            player.bet(DontCome, self.unit)
        else:
            player.bet(Come(self.unit))


class Corey(Strategy):
    def on_coming_out(self, player, table):
        # When off, pass line
        player.bet(PassLine(self.unit))

    # When on, 2 come, play odds on 6 or 8, play field when not on 4 or 10
    def on_point_set(self, player, table, last_roll):
        if last_roll in [6,8]:
            player.add_odds(PassLine, 3 * self.unit, last_roll)

    def on_active_point(self, player, table):
        if player.number_of_bets_by_type(Come) < 2:
            player.bet(Come(self.unit))
        if not player.has_bet("Come4") and not player.has_bet("Come10") and player.number_of_bets_by_type(
                Come) > 0 and not player.has_bet_type(Field):
            player.bet(
                Field(
                    self.unit,
                    double=table.payouts["fielddouble"],
                    triple=table.payouts["fieldtriple"],
                )
            )

class Frankenstein(Strategy):

    def __init__(self, unit=5, verbose=False):
        super().__init__(unit, verbose)
        self.strategies = (IronCrossLadder(unit, verbose), DiceDoctor(unit, verbose))
