from crapssim.strategy.strategy import Strategy, passline, dontpass
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
    def on_new_shooter(self, player, table):
        print("DARK::New Shooter")

    def on_coming_out(self, player, table):
        dontpass(player, table, self.unit*2)

    def on_active_point(self, player, table):
        if self.verbose:
            print("DARK::On Active Point")
        all_bets = player.bets_on_table

        current_total = self.unit
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
        profit = player.bankroll - player.starting_bankroll
        current_total = 0

        for bet in all_bets:
            current_total += bet.bet_amount
        # ic(current_total, profit, player.bankroll, player.starting_bankroll)
        if profit > 0:
            current_total = int(max(current_total / 2, current_total - (profit / 2)))
        # ic(current_total, profit, player.bankroll)

        current_total -= max(self.unit, player.bankroll - 1000)
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
    def on_coming_out(self, player, table):
        # passline(player, table, self.unit)
        dontpass(player, table, self.unit)
    
    def on_active_point(self, player, table):
        # TODO: Check loss and double
        dontpass(player, table, self.unit)