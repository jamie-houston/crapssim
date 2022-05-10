from crapssim import Table
from crapssim.bet import PassLine
from crapssim.strategy import BetPassLine


def test_default_strategy():
    table = Table()
    table.add_player()
    assert table.players[0].bet_strategy == BetPassLine(5)


def test_irremovable_bet():
    bet = PassLine(50)
    table = Table()
    table.add_player(500)
    table.fixed_roll_and_update([2, 2])
    bet.update(table)
    print(table.point.status)
    assert bet.is_removable(table.players[0]) is False


def test_existing_bet():
    table = Table()
    table.add_player()
    bet_one = PassLine(50)
    table.players[0].add_bet(bet_one)
    bet_two = PassLine(50)
    table.players[0].add_bet(bet_two)

    bet_count = len(table.players[0].bets_on_table)
    bet_amount = table.players[0].bets_on_table[0].bet_amount
    bankroll = table.players[0].bankroll
    total_bet_amount = table.players[0].total_bet_amount

    assert (bet_count, bet_amount, bankroll, total_bet_amount) == (1, 100, 0, 100)
