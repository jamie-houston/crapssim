from crapssim.strategy import AggregateStrategy
from crapssim.strategy.examples import IronCross, DiceDoctor


class IronCrossLadder(AggregateStrategy):
    def __init__(self, base_amount: float):
        super().__init__(IronCross(base_amount), DiceDoctor(base_amount))
