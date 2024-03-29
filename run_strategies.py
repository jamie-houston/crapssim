import argparse

from crapssim import Table, logging
from crapssim.statistics.statistics import SimulatorStatistics
from crapssim.strategy.examples import *
import configparser

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-defaults', action='store_true', help='Update default params')
    args = parser.parse_args()


    config_file = "config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)

    current_settings = config["LATEST"] or config["DEFAULT"]

    change_defaults = not (args.use_defaults or input("Keep defaults? (default no)? ").lower()[:1] == 'y')

    def query_bool(question):
        value = current_settings.getboolean(question)
        try:
            if change_defaults:
                reply = input(f"{question} (default {'yes' if value else 'no'})? ").lower()[:1]
                value = value if len(reply) == 0 else reply == 'y'
        except Exception:
            pass
        current_settings[question] = str(value)
        return value

    def query_int(question):
        value = current_settings.getint(question)
        try:
            if change_defaults:
                value = int(input(f"{question} (default {value})? ") or value)
        except Exception:
            pass
        current_settings[question] = str(value)
        return value

    verbose = query_bool("verbose")

    max_shooters = query_int("max_shooters")
    n_sim = query_int("n_sim")
    bankroll = query_int("bankroll")
    base_unit = query_int("base_unit")

    config['LATEST'] = current_settings

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    all_strategies = {
        BetDontPass,
        BetPassLine,
        DiceDoctor,
        HammerLock,
        IronCross,
        Knockout,
        Pass2Come,
        PassLinePlace68,
        PassLinePlace68Move59,
        Place68CPR,
        Place68DontCome2Odds,
        Place68Move59,
        PlaceInside,
        Risk12,
        TwoCome,
        # BetPlace,
        # FieldWinProgression,
        # IronCrossLadder,
        # Place682Come,
    }

    strategies = {strat.__name__: strat(base_unit) for strat in all_strategies}

    simulator = SimulatorStatistics(strategies, bankroll, total_simulations=n_sim)

    for i in range(n_sim):
        table = Table()
        for strategy in strategies:
            table.add_player(bankroll=bankroll, strategy=strategies[strategy], name=strategy)

        table.run(max_rolls=float("inf"), max_shooter=max_shooters, verbose=verbose,
                  update_after_roll=simulator.update_after_roll)
        for p in table.players:
            simulator.update_after_all_rolls(p)
    logging.log(f"\n{n_sim} runs.  {max_shooters} max shooters")

    result_table = simulator.generate_table()
    print(result_table)
