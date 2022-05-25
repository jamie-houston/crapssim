import pytest

from crapssim.strategy.defaults import HammerLock
from crapssim.table import Table
from crapssim.bet import PassLine, DontPass, LayOdds4, LayOdds5, LayOdds6, LayOdds8, LayOdds9, LayOdds10,\
    Place6, Place8, Place5, Place9


@pytest.mark.parametrize("point, last_roll, strat_info, bets_before, dice_result, bets_after", [
    (
        None, None, None, 
        [],
        None, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 4, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 2, {'mode': 'place68'}, 
        [],
        (1, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 3, {'mode': 'place68'}, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place_inside'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        5, 3, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        5, 9, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0)]
    ),
    (
        5, 10, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0)]
    ),
    (
        5, 6, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0)]
    ),
    (
        None, 7, {'mode': 'takedown'}, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        9, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        9, 3, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 9, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 2, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        None, 4, {'mode': 'place_inside'}, 
        [Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 12, {'mode': 'place68'}, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 12, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 2, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 3, {'mode': 'place68'}, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 9, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 12, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        6, 3, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        6, 5, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)]
    ),
    (
        None, 7, {'mode': 'takedown'}, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place_inside'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 5, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 6, {'mode': 'place68'}, 
        [Place8(bet_amount=12.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 8, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 8, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, {'mode': 'place68'}, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, {'mode': 'place68'}, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 6, {'mode': 'place68'}, 
        [Place8(bet_amount=12.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 8, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 3, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 3, {'mode': 'place68'}, 
        [],
        (2, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 5, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 3, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 3, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 8, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 12, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 6, {'mode': 'place68'}, 
        [Place8(bet_amount=12.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place8(bet_amount=12.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        8, 2, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place_inside'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place8(bet_amount=12.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        4, 9, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 8, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 5, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 11, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 10, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 3, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 8, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 10, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 6, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 3, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (1, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 12, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 2, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        4, 5, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        None, 7, {'mode': 'takedown'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 6, {'mode': 'place68'}, 
        [Place8(bet_amount=12.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 5, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 12, {'mode': 'place68'}, 
        [],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        9, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        9, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place8(bet_amount=12.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        9, 8, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place9(bet_amount=5.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0)]
    ),
    (
        None, 7, {'mode': 'takedown'}, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, {'mode': 'place68'}, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 10, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 5, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 12, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0)],
        (4, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        5, 12, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        5, 9, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0)]
    ),
    (
        None, 5, {'mode': 'takedown'}, 
        [],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        9, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place8(bet_amount=12.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        9, 2, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        9, 6, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place5(bet_amount=5.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0)]
    ),
    (
        9, 5, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0)]
    ),
    (
        9, 5, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0)]
    ),
    (
        9, 12, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0)]
    ),
    (
        None, 7, {'mode': 'takedown'}, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 5, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        6, 5, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)]
    ),
    (
        None, 6, {'mode': 'takedown'}, 
        [],
        (5, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (5, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 8, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        4, 6, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place5(bet_amount=5.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0)]
    ),
    (
        None, 7, {'mode': 'takedown'}, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 2, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 12, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 6, {'mode': 'place68'}, 
        [Place8(bet_amount=12.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0)],
        (5, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place_inside'}, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (4, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 3, {'mode': 'place68'}, 
        [],
        (1, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        9, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        9, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (1, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        9, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0)],
        (2, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place_inside'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 4, {'mode': 'place68'}, 
        [Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 3, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 6, {'mode': 'place68'}, 
        [Place8(bet_amount=12.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        8, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (4, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        8, 12, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds8(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 6, {'mode': 'place68'}, 
        [Place8(bet_amount=12.0)],
        (5, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        6, 2, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (1, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        6, 9, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0)],
        (5, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)]
    ),
    (
        6, 5, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)]
    ),
    (
        6, 4, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)]
    ),
    (
        6, 8, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)]
    ),
    (
        6, 4, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0)]
    ),
    (
        None, 7, {'mode': 'takedown'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 2, {'mode': 'place68'}, 
        [],
        (1, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 11, {'mode': 'place68'}, 
        [],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0)],
        (3, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place_inside'}, 
        [],
        (3, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 3, {'mode': 'place68'}, 
        [],
        (2, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        4, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 3, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 11, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        4, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place8(bet_amount=12.0)],
        (1, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds4(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        None, 4, {'mode': 'place_inside'}, 
        [Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)],
        (1, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        6, 6, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 3), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 12, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        6, 4, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (2, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds6(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        10, 8, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0)],
        (6, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0), Place9(bet_amount=5.0)]
    ),
    (
        10, 9, {'mode': 'place_inside'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place5(bet_amount=5.0), Place6(bet_amount=6.0), Place8(bet_amount=6.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0)]
    ),
    (
        10, 12, {'mode': 'takedown'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0)],
        (6, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0)]
    ),
    (
        None, 7, {'mode': 'takedown'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (1, 6), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (6, 1), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        5, 5, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (3, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        5, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)],
        (6, 4), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds5(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (5, 2), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        9, 9, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (4, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds9(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    ),
    (
        None, 7, {'mode': 'place68'}, 
        [],
        (2, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)]
    ),
    (
        10, 10, {'mode': 'place68'}, 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0)],
        (5, 5), 
        [PassLine(bet_amount=5.0), DontPass(bet_amount=5.0), LayOdds10(bet_amount=30.0), Place6(bet_amount=12.0), Place8(bet_amount=12.0)]
    )
])
def test_hammerlock_integration(point, last_roll, strat_info, bets_before, dice_result, bets_after):
    table = Table()
    table.point.number = point
    table.last_roll = last_roll
    strategy = HammerLock(5)
    if strat_info is None:
        strat_info = {'mode': 'place68'}
    if table.point.status == 'On' and strat_info['mode'] == 'place68' \
        and (Place6(12) not in bets_before and Place8(12) in bets_before
             or Place8(12) not in bets_before and Place6(12) in bets_before):
        strategy.place_win_count = 1
    elif table.point.status == 'On' and strat_info['mode'] == 'place_inside' \
        and (Place5(5) not in bets_before or Place6(6) not in bets_before or
             Place8(6) not in bets_before or Place9(5) not in bets_before):
        strategy.place_win_count = 2
    elif strat_info['mode'] == 'takedown':
        strategy.place_win_count = 2
    elif table.point.status == 'On' and strat_info['mode'] == 'place_inside':
        strategy.place_win_count = 1
    table.add_player(bankroll=float("inf"), strategy=strategy) # ADD STRATEGY HERE
    table.players[0].bets_on_table = bets_before
    table.dice.result = dice_result
    strategy.after_roll(table.players[0])
    table.add_player_bets()
    assert set(table.players[0].bets_on_table) == set(bets_after)
