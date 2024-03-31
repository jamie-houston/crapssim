from crapssim import Player
from crapssim.bet import Field
from crapssim.strategy import AggregateStrategy, Strategy, PassLineOddsMultiplier, BetPointOn
from crapssim.strategy.examples import IronCross, DiceDoctor, BetPassLine, BetPlace


class RedCross(AggregateStrategy):
    """Strategy that bets the PassLine, bets the PassLine Odds, and bets Place on the 5, 6, and 8.
    If the point is on and there is no bet on the field, place a bet on the field. Equivalent to:
    BetPassLine(...) + PassLineOddsMultiplier(2), + BetPlace({...}) + BetPointOn(Field(...))"""

    def __init__(self, base_amount: float):
        """Creates the IronCross strategy based on the base_amount, using that number to determine
        the amounts for all the other numbers.

        Parameters
        ----------
        base_amount
            The base amount of the bets. This amount is used for the PassLine and Field.
            base_amount * (6/5) * 2 is used for placing the six and eight, and base amount * 2
            is used for placing the five.
        """
        self.base_amount = base_amount
        self.field_amount = 0

        super().__init__(IronCross(base_amount=base_amount))

    def after_roll(self, player: 'Player') -> None:
        """If it's a seven out, set field amount (for place 4,9,10) back to 0
        """
        if player.table.last_roll == 7:
            self.field_amount = 0

    def update_bets(self, player: 'Player') -> None:
        """
        If the last roll was in the field, increase 4,9,10 by 1/3 of the winnings
        :param player:
        :return:
        """
        for strategy in self.strategies:
            if not strategy.completed(player):
                strategy.update_bets(player)

        for bet in player.bets:
            if isinstance(bet, Field):
                bet_result = bet.get_result(player.table)
                if bet_result.won:
                    bet_amount = self.field_amount + self.base_amount
                    # TODO: Increment (update?) with each win
                    BetPlace({4: bet_amount, 9: bet_amount, 10: bet_amount}, skip_point=True).update_bets(player)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(base_amount={self.base_amount})'
