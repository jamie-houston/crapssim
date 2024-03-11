from crapssim.strategy.strategy import Strategy, dontcome, passline, dontpass
from crapssim.bet import *
from icecream import ic

class NoFieldStrategy(Strategy):
    def __init__(self, unit=5, verbose=False):
        super().__init__(unit, verbose)

    def on_coming_out(self, player, table):
    # When off, pass line
        if self.verbose:
            print(f"NOFIELD:Coming Out")
        passline(player, table, self.unit)
    
    def on_active_point(self, player, table):
        if table.point.number in [6, 8] and not player.has_bet_type(Odds) and player.has_bet_type(PassLine):
            player.bet(Odds(3 * self.unit, player.get_bet_type(PassLine)))
        if player.num_bet("Come") < 2:
            player.bet(Come(self.unit))


class DarkAndLightStrategy(Strategy):
    # When off, pass line
    # when on, come bet
    # 2 odds on each
    # 2,12 - bet * .1
    # 3 - bet * .2
    # come/pass bet = total bet * .75
    # point on hard number, bet hard
    def on_coming_out(self, player, table):
        player.bet(DontPass(self.unit*2))

    def on_active_point(self, player, table):
        player.bet(Come(self.unit))

    def on_any_bet_result(self, player, table, bet_info):
        # if it's a come or pass bet, bet odds
        if bet_info.is_bet_type(DontPass) or bet_info.is_bet_type(Come):
            player.bet(Odds(bet_info.bet_amount * 2, bet_info))

    def on_any_status(self, player, table):
        player.bet(Come(self.unit))
        player.bet(Horn(self.unit*.2))
        player.bet(SingleRoll(self.unit * .1, 2))
        player.bet(SingleRoll(self.unit * .1, 12))
        player.bet(SingleRoll(self.unit * .1, 3))
        if table.point.number in [4,6,8,10]:
            player.bet(Hard(self.unit * .25, table.point.number))


class KeepComingBackStrategy(Strategy):
    def _current_total(self, player):
        # TODO: Make bet total based on winning and current bets... bet less when you're up
        # player.bet(Field(current_total))
        current_total = 0
        all_bets = player.bets_on_table

        for bet in all_bets:
            current_total += bet.bet_amount

        return current_total

    def on_coming_out(self, player, table):
        current_total = self.unit + self._current_total(player)

        passline(player, table, current_total)

    def on_active_point(self, player, table):
        current_total = self.unit + self._current_total(player)

        player.bet(Come(current_total))

    def on_any_status(self, player, table):
        current_total = self._current_total(player)
        horn_bet = round(current_total/30,2)
        player.bet(SingleRoll(horn_bet, 2))
        player.bet(SingleRoll(horn_bet, 12))

class ComingEverywhereStrategy(Strategy):
    def _current_total(self, player):
        all_bets = player.bets_on_table
        profit = player.bankroll_finance.current - player.bankroll_finance.starting
        current_total = 0

        for bet in all_bets:
            current_total += bet.bet_amount
        # ic(current_total, profit, player.bankroll, player.starting_bankroll)
        if profit > 0:
            current_total = int(max(current_total / 2, current_total - (profit / 2)))
        # ic(current_total, profit, player.bankroll)

        current_total -= max(self.unit, player.bankroll_finance.current - 1000)
        current_total = max(self.unit, current_total)
        return current_total
    
    def on_coming_out(self, player, table):
        passline(player, table, self._current_total(player) + self.unit)

    def on_active_point(self, player, table):
        if len(player.bets_on_table) == 1:
            player.bet(Place10(self.unit))
            player.bet(Place9(self.unit))
            player.bet(Place8(self.unit))
            player.bet(Place6(self.unit))
            player.bet(Place5(self.unit))
            player.bet(Place4(self.unit))
        player.bet(Come(self._current_total(player)+self.unit))

class DoNotPassGo(Strategy):
    def __init__(self, unit=25, verbose=False):
        self.bet_placed = False
        self.last_bet_amount = unit
        super().__init__(unit, verbose)

    def on_loss(self, player, table, losing_bet_info):
        next_bet_amount = losing_bet_info.bet_amount + self.unit
        ic(f"Lost {losing_bet_info}. Raising bet to {next_bet_amount}")
        if table.point.is_on():
            self._add_bet(player, DontCome(next_bet_amount))
        else:
            self._add_bet(player, DontPass(next_bet_amount))

    def on_coming_out(self, player, table):
        self._add_bet(player, DontPass(self.unit*3))
        self.bet_placed = False
    
    def on_active_point(self, player, table):
        self._add_bet(player, DontCome(max(self.last_bet_amount - self.unit, self.unit)))
        self.bet_placed = False
    
    def _add_bet(self, player, bet):
        if self.bet_placed == False:
            player.bet(bet)
            self.last_bet_amount = bet.bet_amount
            self.bet_placed = True


class AllInStrat(Strategy):
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
    
    def on_point_set(self,player, table, last_roll):
        if last_roll in [6,8]:
            player.bet(Odds(3 * self.unit, player.get_bet_type(PassLine)))
    
    def on_active_point(self, player, table):
        if player.num_bet(Come) < 2:
            player.bet(Come(self.unit))