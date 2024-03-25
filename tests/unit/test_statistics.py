import pytest

from crapssim import Table, Player
from crapssim.simulator.statistics import SimulatorStatistics
from crapssim.strategy import Strategy


@pytest.fixture
def base_strategy():
    class TestStrategy(Strategy):
        def update_bets(self, player: 'Player') -> None:
            pass
        def completed(self, player: 'Player') -> bool:
            return False

    return TestStrategy()


@pytest.fixture
def players():
    table = Table()
    table.add_player()
    table.add_player()
    return table.players


def test_statistics(base_strategy, players):
    starting_bankroll = 100
    target_bankroll = starting_bankroll*1.5
    base_unit = 1.5
    strategies = {player.name: base_strategy for player in players}
    simulator_statistics = SimulatorStatistics(strategies, starting_bankroll=starting_bankroll,base_unit=base_unit)
    players[0].bankroll = 0
    simulator_statistics.update_after_roll(players[0].table)
    stat_player = simulator_statistics.players[0]
    assert stat_player.name == players[0].name
    assert stat_player.roll_statistics.bankrupt_reached is True
    assert stat_player.roll_statistics.target_reached is False

    players[1].bankroll = target_bankroll
    simulator_statistics.update_after_roll(players[1].table)
    stat_player = simulator_statistics.players[1]
    assert stat_player.name == players[1].name
    assert stat_player.roll_statistics.bankrupt_reached is False
    assert stat_player.roll_statistics.target_reached is True
